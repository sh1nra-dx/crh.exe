from mysql import create_db_connection

def get_all():
    dbc = create_db_connection()
    try:
        cursor = dbc.cursor()
        query = "SELECT * FROM shop ORDER BY id ASC"
        cursor.execute(query)
        raw_data = cursor.fetchall()
        queue_list = []
        for d in raw_data:
            queue_list.append({
                'name': d[1],
                'command': d[2],
                'cabinetCount': d[3],
                'maxCapacity': d[4],
                'playerCount': d[5],
                'updateTime': d[6].strftime('%Y-%m-%d %H:%M:%S'),
            })
        cursor.close()
        dbc.close()
        return {
            'error': False,
            'list': queue_list,
        }
    except:
        dbc.close()
        return {
            'error': True,
            'msg': '数据查询失败，请稍后再试',
        }

def get_one(command):
    dbc = create_db_connection()
    try:
        cursor = dbc.cursor()
        query = "SELECT * FROM shop WHERE command = %s LIMIT 1"
        cursor.execute(query, (command))
        raw_data = cursor.fetchone()
        queue_info = {
            'name': raw_data[1],
            'command': raw_data[2],
            'cabinetCount': raw_data[3],
            'maxCapacity': raw_data[4],
            'playerCount': raw_data[5],
            'updateTime': raw_data[6].strftime('%Y-%m-%d %H:%M:%S'),
        }
        cursor.close()
        dbc.close()
        return {
            'error': False,
            'info': queue_info,
        }
    except:
        dbc.close()
        return {
            'error': True,
            'msg': '数据更新失败，请稍后再试',
        }

def add_player(command, number):
    dbc = create_db_connection()
    try:
        cursor = dbc.cursor()
        select_query = "SELECT * FROM shop WHERE command = %s LIMIT 1"
        cursor.execute(select_query, (command))
        raw_data = cursor.fetchone()
        shop_id = raw_data[0]
        player_count = raw_data[5]
        player_count += int(number)
        update_query = "UPDATE shop SET player_count = %s, update_time = NOW() WHERE id = %s LIMIT 1"
        cursor.execute(update_query, (player_count, shop_id))
        dbc.commit()
        select_query = "SELECT * FROM shop WHERE id = %s LIMIT 1"
        cursor.execute(select_query, (shop_id))
        raw_data = cursor.fetchone()
        queue_info = {
            'name': raw_data[1],
            'command': raw_data[2],
            'cabinetCount': raw_data[3],
            'maxCapacity': raw_data[4],
            'playerCount': raw_data[5],
            'updateTime': raw_data[6].strftime('%Y-%m-%d %H:%M:%S'),
        }
        cursor.close()
        dbc.close()
        return {
            'error': False,
            'info': queue_info,
        }
    except:
        dbc.rollback()
        dbc.close()
        return {
            'error': True,
            'msg': '数据更新失败，请稍后再试',
        }

def del_player(command, number):
    dbc = create_db_connection()
    try:
        cursor = dbc.cursor()
        select_query = "SELECT * FROM shop WHERE command = %s LIMIT 1"
        cursor.execute(select_query, (command))
        raw_data = cursor.fetchone()
        shop_id = raw_data[0]
        player_count = raw_data[5]
        if (player_count - int(number)) <= 0:
            player_count = 0
        else:
            player_count -= int(number)
        update_query = "UPDATE shop SET player_count = %s, update_time = NOW() WHERE id = %s LIMIT 1"
        cursor.execute(update_query, (player_count, shop_id))
        dbc.commit()
        select_query = "SELECT * FROM shop WHERE id = %s LIMIT 1"
        cursor.execute(select_query, (shop_id))
        raw_data = cursor.fetchone()
        queue_info = {
            'name': raw_data[1],
            'command': raw_data[2],
            'cabinetCount': raw_data[3],
            'maxCapacity': raw_data[4],
            'playerCount': raw_data[5],
            'updateTime': raw_data[6].strftime('%Y-%m-%d %H:%M:%S'),
        }
        cursor.close()
        dbc.close()
        return {
            'error': False,
            'info': queue_info,
        }
    except:
        dbc.rollback()
        dbc.close()
        return {
            'error': True,
            'msg': '数据更新失败，请稍后再试',
        }
