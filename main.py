from generate import *
from rating_graphic import *

N = 5
cnt_players = N
cnt_tournaments = 20
average_tours = 400
cnt_users = 400
cnt_tasks = 400

with psycopg2.connect(dbname='chessnet', user='max', password='max', host='localhost') as conn:
    clean_db(conn)
    data = generate(conn, cnt_players, cnt_tournaments, average_tours, cnt_users, cnt_tasks)
    show_all_rating_graphics('standard', data, conn)
