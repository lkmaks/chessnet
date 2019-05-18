from inserts import *

with psycopg2.connect(dbname='chessnet', user='max', password='max', host='localhost') as conn:
    clean_db(conn)
    p1 = add_real_player('maksim', 'lavrik', 'Russia', conn)
    p2 = add_real_player('lektor', 'vektor', 'Russia', conn)
    t1 = add_tournament('match of the century', '11.05.2019', '11.05.2019', 'match bo5', 'Russia', 'im just playing russia you know i love you', conn)
    add_real_game(p1, p2, 1, '0:01', '0:01', '11.05.2019', '2h +30s fisher', 'standard', t1, conn)
    add_player_to_tournament(p1, t1, conn)
    add_player_to_tournament(p2, t1, conn)
