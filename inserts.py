import psycopg2
from lib import *

tables = ['article', 'comment', 'onlinegame', 'onlineuser', 'playerinrealgame',
          'playerintournament', 'realgame', 'realplayer', 'task', 'tournament',
          'userinonlinegame']


def get_att_list(table, conn):
    with conn.cursor() as cursor:
        query = "select column_name from information_schema.columns where table_name = '{}'".format(table)
        cursor.execute(query)
        return [e[0] for e in cursor.fetchall()]


def clean_db(conn):
    with conn.cursor() as cursor:
        for t in tables:
            cursor.execute('TRUNCATE {} CASCADE;'.format(t))


def get_last_id(table, conn):
    with conn.cursor() as cursor:
        query = "select max(id) from {};".format(table)
        cursor.execute(query)
        return cursor.fetchone()[0]


def get_attr(table, id, attr, conn):
    with conn.cursor() as cursor:
        query = "select {} from {} where id={};".format(attr, table, id)
        cursor.execute(query)
        return cursor.fetchone()[0]


def add_real_player(name, surname, country, conn):
    att_list = get_att_list('realplayer', conn)[1:]
    with conn.cursor() as cursor:
        query = "insert into realplayer ({}) values ('{}', '{}', '{}', {});"\
            .format(','.join(att_list), name, surname, country, '1000,' * 6 + '0,' * 5 + '0')
        cursor.execute(query)
        return get_last_id('realplayer', conn)


def add_online_user(username, email, password, conn, player_id=None):
    with conn.cursor() as cursor:
        att_list = get_att_list('onlineuser', conn)
        query = "insert into onlineuser ({}) values ('{}', {}, '{}', '{}', {})".format(
            ','.join(att_list), username, "NULL" if player_id is None else player_id, email, password, '0,' * 10 + '0'
        )
        cursor.execute(query)
        return username


def add_tournament(name, date_from, date_to, rule, country, tournament_info, conn):
    with conn.cursor() as cursor:
        query = "insert into tournament (name, date_from, date_to, rule, country, tournament_info) values "
        query += "('{}', {}, {}, '{}', '{}', '{}')"\
            .format(name, sql_date(date_from), sql_date(date_to), rule, country, tournament_info)
        cursor.execute(query)
        return get_last_id('tournament', conn)


def add_real_game(white_id, black_id, result, time_left1, time_left2, date, time_control, control_type,
                  tournament_id, conn):
    # result: 0 - white win, 1 - draw, 2 - black win
    with conn.cursor() as cursor:
        query = "insert into realgame (tournament_id, game_date, time_control," \
                " game_result, control_type) values ({}, {}, '{}', {}, '{}')".format(
            tournament_id, sql_date(date), time_control, result, control_type
        )
        cursor.execute(query)
        game_id = get_last_id('realgame', conn)

        typo = 'world'
        r1 = get_attr('realplayer', white_id, '{}_chess_{}_rating'.format(typo, control_type), conn)
        r2 = get_attr('realplayer', black_id, '{}_chess_{}_rating'.format(typo, control_type), conn)
        new_r1, new_r2 = new_ratings(r1, r2, result)
        query = 'update realplayer set {}_chess_{}_rating = {} WHERE id = {}'\
            .format(typo, control_type, str(new_r1), white_id)
        cursor.execute(query)
        query = 'update realplayer set {}_chess_{}_rating = {} WHERE id = {}'\
            .format(typo, control_type, str(new_r2), black_id)
        cursor.execute(query)

        query = "insert into playerinrealgame (real_player_id, real_game_id, color, time_left, rating_delta)" \
                " values ({}, {}, '{}', '{}', {})".format(
            white_id, game_id, 'white', time_left1, str(new_r1 - r1)
        )
        cursor.execute(query)
        query = "insert into playerinrealgame (real_player_id, real_game_id, color, time_left, rating_delta) values" \
                " ({}, {}, '{}', '{}', {})".format(
            black_id, game_id, 'black', time_left2, str(new_r2 - r2)
        )
        cursor.execute(query)

        if result == 0:
            wins_as_white = get_attr('realplayer', white_id, 'wins_as_white', conn)
            losses_as_black = get_attr('realplayer', black_id, 'losses_as_black', conn)
            query = 'update realplayer set wins_as_white = {} where id = {}'\
                .format(str(wins_as_white + 1), str(white_id))
            cursor.execute(query)
            query = 'update realplayer set losses_as_black = {} where id = {}'\
                .format(str(losses_as_black + 1), str(black_id))
            cursor.execute(query)
        elif result == 2:
            losses_as_white = get_attr('realplayer', white_id, 'losses_as_white', conn)
            wins_as_black = get_attr('realplayer', black_id, 'wins_as_black', conn)
            query = 'update realplayer set losses_as_white = {} where id = {}'\
                .format(str(losses_as_white + 1), str(white_id))
            cursor.execute(query)
            query = 'update realplayer set wins_as_black = {} where id = {}'\
                .format(str(wins_as_black + 1), str(black_id))
            cursor.execute(query)
        elif result == 1:
            draws_as_white = get_attr('realplayer', white_id, 'draws_as_white', conn)
            draws_as_black = get_attr('realplayer', black_id, 'draws_as_black', conn)
            query = 'update realplayer set draws_as_white = {} where id = {}'\
                .format(str(draws_as_white + 1), str(white_id))
            cursor.execute(query)
            query = 'update realplayer set draws_as_black = {} where id = {}'\
                .format(str(draws_as_black + 1), str(black_id))
            cursor.execute(query)
        return get_last_id('realgame', conn)


def add_player_to_tournament(player_id, tournament_id, conn):
    with conn.cursor() as cursor:
        query = "insert into playerintournament (tournament_id, real_player_id) values ({}, {})".format(
            str(tournament_id), str(player_id)
        )
        cursor.execute(query)
        return get_last_id('playerintournament', conn)


def add_task(author_username, online_game_from_id, real_game_from_id, task_body, difficulty, goal, task_type, conn):
    with conn.cursor() as cursor:
        real_game_from_id = ("NULL" if real_game_from_id is None else real_game_from_id)
        online_game_from_id = ("NULL" if online_game_from_id is None else online_game_from_id)

        query = 'insert into task (author_username, online_game_from_id,' \
                ' real_game_from_id, task_body, difficulty, goal, task_type) '
        query += "values ('{}', {}, {}, '{}', {}, '{}', '{}')".format(author_username, online_game_from_id,
                                                              real_game_from_id, task_body, str(difficulty), goal,
                                                              task_type)
        cursor.execute(query)


def all_players(conn):
    with conn.cursor() as cursor:
        query = "select name from realplayer;"
        cursor.execute(query)
        ret = cursor.fetchall()
        return ret


# with psycopg2.connect(dbname='chessnet', user='max', password='max', host='localhost') as conn:
#     clean_db(conn)
#     p1 = add_real_player('maksim', 'lavrik', 'Russia', conn)
#     p2 = add_real_player('lektor', 'vektor', 'Russia', conn)
#     t1 = add_tournament('match of the century', '11.05.2019', '11.05.2019', 'match bo5', 'Russia', 'im just playing russia you know i love you')
#     add_real_game(p1, p2, 1, '0:01', '0:01', '11.05.2019', '2h +30s fisher', 'standard', t1, conn)
