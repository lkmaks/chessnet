from inserts import *
from generate import *
from rating_graphic import *
from selects import *

N = 10
cnt_players = N
cnt_tournaments = 400
average_tours = 50
cnt_users = N
cnt_tasks = N * 2

with psycopg2.connect(dbname='chessnet', user='max', password='max', host='localhost') as conn:
    clean_db(conn)
    data = generate(conn, cnt_players, cnt_tournaments, average_tours, cnt_users, cnt_tasks)
    show_all_rating_graphics('standard', data, conn)
