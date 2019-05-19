import psycopg2
import matplotlib.pyplot as plt
from inserts import *


def show_rating_graphic(player_id, control_type, conn):
    with conn.cursor() as cursor:
        query = """select distinct t2.game_date, sum(t1.rating_delta) over(order by t2.game_date) from
            playerinrealgame t1 inner join realgame t2 on t1.real_game_id = t2.id
            where t1.real_player_id = {} and t2.control_type='{}'
            order by t2.game_date;""".format(str(player_id), control_type)
        cursor.execute(query)
        data = cursor.fetchall()
        x = [e[0] for e in data]
        y = [1000 + e[1] for e in data]
        plt.plot(x, y)
        plt.show()


def show_all_rating_graphics(control_type, case_data, conn):
    with conn.cursor() as cursor:
        real_rating = dict()
        for i in range(len(case_data.player_ids)):
            real_rating[case_data.player_ids[i]] = case_data.real_ratings[i]
        query = 'select id from realplayer;'
        cursor.execute(query)
        ids = [e[0] for e in cursor.fetchall()]
        fig, axes = plt.subplots(nrows=len(ids), ncols=1, figsize=(12, 4 * len(ids)))
        for i in range(len(ids)):
            player_id = ids[i]
            query = """select distinct t2.game_date, sum(t1.rating_delta) over(order by t2.game_date) from
                        playerinrealgame t1 inner join realgame t2 on t1.real_game_id = t2.id
                        where t1.real_player_id = {} and t2.control_type='{}'
                        order by t2.game_date;""".format(str(player_id), control_type)
            cursor.execute(query)
            data = cursor.fetchall()
            x = [e[0] for e in data]
            y = [1000 + e[1] for e in data]
            print(len(x))
            name = get_attr('realplayer', ids[i], 'name', conn)
            surname = get_attr('realplayer', ids[i], 'surname', conn)
            axes[i].set_title(name + ' ' + surname + ', real rating: {}'.format(str(real_rating[player_id])))
            axes[i].plot(x, y, c='#ff0000')
        plt.show()
