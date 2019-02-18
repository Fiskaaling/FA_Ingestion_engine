import mysql.connector as db

def fadblogin(setup_dict):
    db_connection = db.connect(**setup_dict['login'])
    return db_connection, db_connection.cursor()

def getcol(setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("DESCRIBE mátingar")
    out = [x[0] for x in cursor.fetchall()]
    db_connection.disconnect()
    return out

def getmatinger(setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT * FROM mátingar")
    out = cursor.fetchall()
    db_connection.disconnect()
    return out

def get_slag(setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT * FROM wl_instument_slag")
    out = cursor.fetchall()
    db_connection.disconnect()
    return out

def get_instrumentir(setup_dict, slag):
    db_connection, cursor = fadblogin(setup_dict)

    if slag == 'Øll':
        cursor.execute("SELECT navn FROM instrumentir")
    else:
        cursor.execute("SELECT navn FROM instrumentir WHERE slag=%s", (slag,))

    out = cursor.fetchall()
    db_connection.disconnect()
    return out
