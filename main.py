from inserts import *
from generate import *


cnt_players = 20
cnt_tournaments = 20
average_tours = 9
cnt_users = 20
cnt_tasks = 20

with psycopg2.connect(dbname='chessnet', user='max', password='max', host='localhost') as conn:
    clean_db(conn)
    generate(conn, cnt_players, cnt_tournaments, average_tours, cnt_users, cnt_tasks)
