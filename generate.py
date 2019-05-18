import random
from lib import *
import requests as rq
from bs4 import BeautifulSoup
from inserts import *
import psycopg2


def get_name(s):
    s = s.replace("'", "")
    s = s.replace(",", "")
    if not ' ' in s:
        return (s, '')
    else:
        return (s.split()[0], s.split()[1])


def generate(conn, cnt_players, cnt_tournaments, average_tours, cnt_users, cnt_tasks):
    pld = {'birth_from': '1901', 'birth_to': '2015', 'activity': '1', 'count': str(cnt_players), 'type': 'classic'}
    soup = BeautifulSoup(rq.post('http://shahmaty.info/ajax.php', pld).text, features="html.parser")

    arr = []
    for tag in soup.findAll('span'):
        arr.append(tag.text.strip())
    arr = arr[8:]
    new_arr = []
    for i in range(len(arr)):
        if i % 8 in [2, 4, 5, 6]:
            new_arr.append(arr[i])
    arr = new_arr

    rating = []
    names = []
    surnames = []
    countries = []
    player_ids = []
    i = 0
    while i < len(arr):
        name, surname = get_name(arr[i])
        names.append(name)
        surnames.append(surname)
        rating.append((arr[i + 1], arr[i + 2], arr[i + 3]))
        i += 4

    for tag in soup.findAll('img'):
        if tag['alt'] != '':
            countries.append(tag['alt'])

    print(len(names))
    print(len(surnames))
    print(len(rating))
    print(len(countries))

    for i in range(cnt_players):
        player_ids.append(add_real_player(names[i], surnames[i], countries[i], conn))

    for c in countries:
        if len(c) >= 20:
            print(c)

    tournament_names = [random_tournament_name() for _ in range(cnt_tournaments)]
    tournament_dates = [random_tournament_date() for _ in range(cnt_tournaments)]
    tournament_rules = [random.choice(['Swiss', 'Random', 'Round', 'Double-elimination', 'Single-elimination']) for _ in range(cnt_tournaments)]
    tmp = list(set(countries))
    tournament_countries = [random.choice(tmp) for _ in range(cnt_tournaments)]
    infos = [random_tournament_name() for _ in range(cnt_tournaments)]
    tournament_ids = []
    print(tournament_names)
    for i in range(cnt_tournaments):
        tournament_ids.append(add_tournament(tournament_names[i], tournament_dates[i][0], tournament_dates[i][1], tournament_rules[i], tournament_countries[i], infos[i], conn))

    for i in range(cnt_tournaments):
        k = random.randint(5, 15)
        players = []
        for j in range(k):
            players.append(player_ids[random.randrange(0, cnt_players)])
        players = list(set(players))
        for pid in players:
            add_player_to_tournament(pid, tournament_ids[i], conn)
        for j in range(average_tours):
            control_type = random.choice(['standard', 'blitz', 'rapid'])
            p1 = random.choice(players)
            p2 = random.choice(players)
            r1 = get_attr('realplayer', str(p1), 'world_chess_{}_rating'.format(control_type), conn)
            r2 = get_attr('realplayer', str(p2), 'world_chess_{}_rating'.format(control_type), conn)
            result = get_result_by_rating(r1, r2)
            time_left_1 = rand_time_left()
            time_left_2 = rand_time_left()
            date = shift(tournament_dates[i][0], random.randint(1, 5))
            add_real_game(p1, p2, result, time_left_1, time_left_2, date, control_type + random.choice(['fisher', 'boyomi']), control_type, tournament_ids[i], conn)

    usernames = []
    for i in range(cnt_users):
        username = random_username()
        email = random_email()
        password = random_password()
        player_id = None
        if random.randint(1, 5) == 1:
            player_id = random.choice(player_ids)
        ret_id = add_online_user(username, email, password, conn, player_id)
        usernames.append(ret_id)

    # for i in range(cnt_tasks):
    #     author_username = random.choice(usernames)

