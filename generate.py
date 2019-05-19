import random
from lib import *
import requests as rq
from bs4 import BeautifulSoup
from inserts import *
import psycopg2
from CaseData import CaseData


def get_name(s):
    s = s.replace("'", "")
    s = s.replace(",", "")
    if not ' ' in s:
        return (s, '')
    else:
        return (s.split()[0], s.split()[1])


def rating2int(r):
    print(r)
    if r == 'unrat.':
        return 1000
    if len(r.split()) > 1:
        r = r.split()[0]
    return int(r)


def generate(conn, cnt_players, cnt_tournaments, average_tours, cnt_users, cnt_tasks, cnt_players_from=300):
    if cnt_players > cnt_players_from:
        print('cnt_players > cnt_players_from, exiting')
        exit(0)

    pld = {'birth_from': '1901', 'birth_to': '2015', 'activity': '1', 'count': str(cnt_players_from), 'type': 'classic'}
    print('data downloaded')
    soup = BeautifulSoup(rq.post('http://shahmaty.info/ajax.php', pld).text, features="html.parser")
    print('data parsed')

    arr = []
    for tag in soup.findAll('span'):
        arr.append(tag.text.strip())
    arr = arr[8:]
    new_arr = []
    for i in range(len(arr)):
        if i % 8 in [2, 4, 5, 6]:
            new_arr.append(arr[i])
    arr = new_arr

    real_ratings = []
    names = []
    surnames = []
    countries = []
    player_ids = []
    i = 0
    while i < len(arr):
        name, surname = get_name(arr[i])
        names.append(name)
        surnames.append(surname)
        real_ratings.append((rating2int(arr[i + 1]), rating2int(arr[i + 2]), rating2int(arr[i + 3])))
        i += 4

    for tag in soup.findAll('img'):
        if tag['alt'] != '':
            countries.append(tag['alt'])

    print(len(names))
    print(len(surnames))
    print(len(real_ratings))
    print(len(countries))

    step = cnt_players_from // cnt_players
    for i in range(cnt_players):
        names[i] = names[i * step]
        surnames[i] = surnames[i * step]
        real_ratings[i] = real_ratings[i * step]
        countries[i] = countries[i * step]
    names = names[:cnt_players]
    surnames = surnames[:cnt_players]
    real_ratings = real_ratings[:cnt_players]
    countries = countries[:cnt_players]

    for i in range(cnt_players):
        player_ids.append(add_real_player(names[i], surnames[i], countries[i], conn))

    tournament_names = [random_tournament_name() for _ in range(cnt_tournaments)]
    tournament_dates = [random_tournament_date() for _ in range(cnt_tournaments)]
    tournament_rules = [random.choice(['Swiss', 'Random', 'Round', 'Double-elimination', 'Single-elimination']) for _ in range(cnt_tournaments)]
    tmp = list(set(countries))
    tournament_countries = [random.choice(tmp) for _ in range(cnt_tournaments)]
    infos = [random_tournament_name() for _ in range(cnt_tournaments)]
    tournament_ids = []
    for i in range(cnt_tournaments):
        tournament_ids.append(add_tournament(tournament_names[i], tournament_dates[i][0], tournament_dates[i][1], tournament_rules[i], tournament_countries[i], infos[i], conn))

    print(player_ids)

    game_ids = []
    for i in range(cnt_tournaments):
        print('Tournament {} added'.format(str(i)))
        k = random.randint(5, 15)
        cur_players = []
        cur_real_ratings = []
        used_randids = set()
        for j in range(k):
            randid = random.randrange(0, cnt_players)
            if not randid in used_randids:
                cur_players.append(player_ids[randid])
                cur_real_ratings.append(real_ratings[randid])
                used_randids.add(randid)
        for pid in cur_players:
            add_player_to_tournament(pid, tournament_ids[i], conn)
        for j in range(average_tours):
            control_type = random.choice(['standard', 'blitz', 'rapid'])
            control_type_id = 0
            if control_type == 'rapid':
                control_type_id = 1
            if control_type == 'blitz':
                control_type_id = 2

            randid = random.randrange(0, len(cur_players))
            p1 = cur_players[randid]
            real_rating1 = cur_real_ratings[randid][control_type_id]

            randid = random.randrange(0, len(cur_players))
            p2 = cur_players[randid]
            real_rating2 = cur_real_ratings[randid][control_type_id]

            if p1 != p2:
                result = get_result_by_real_rating(real_rating1, real_rating2)
                time_left_1 = rand_time_left()
                time_left_2 = rand_time_left()
                date = shift(tournament_dates[i][0], random.randint(1, 5))
                ret = add_real_game(p1, p2, result, time_left_1, time_left_2, date, control_type + random.choice(['fisher', 'boyomi']), control_type, tournament_ids[i], conn)
                game_ids.append(ret)

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

    tasks = []
    for i in range(cnt_tasks):
        author_username = random.choice(usernames)
        online_game_from_id = None
        real_game_from_id = None
        if random.choice([1, 2]) == 1:
            real_game_from_id = random.choice(game_ids)
        body = 'Task1.0:' + random_password(50)
        difficulty = random.randint(1, 10)
        goal = random.choice(['stale mate', 'mate', 'endless check'])
        task_type = random.choice(['sacrifice', 'bound', 'fork'])
        ret = add_task(author_username, online_game_from_id, real_game_from_id, body, difficulty, goal, task_type, conn)
        tasks.append(ret)

    ret_data = CaseData()
    ret_data.countries = countries
    ret_data.real_ratings = real_ratings
    ret_data.player_ids = player_ids
    ret_data.names = names
    ret_data.surnames = surnames

    return ret_data
