

def max_rating_real_player_id(conn, rating_type='standard'):
    with conn.cursor() as cursor:
        query = 'select id from realplayer where world_chess_{}_rating = (select max(world_chess_{}_rating) from realplayer)'\
            .format(rating_type, rating_type)
        cursor.execute(query)
        return cursor.fetchone()[0]
