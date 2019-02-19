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


def getmatinger2(kolonnir, tabellir, wherecall, where, setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    if len(kolonnir) == 0:
        raise Exception('kolonnir er tómt')
    elif len(tabellir) == 0:
        raise Exception('tabellir er tómt')

    sel = "SELECT " + kolonnir[0]
    for x in kolonnir[1::]:
        sel += ', ' + x

    sel += ' FROM ' + tabellir[0]
    for x in tabellir[1::]:
        sel += ', ' + x

    if len(wherecall) > 0:
        sel += ' WHERE ' + wherecall[0]
        for x in wherecall[1::]:
            sel += ' AND ' + x

    cursor.execute(sel, tuple(where))

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


def get_felagar(setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT Id_felagar, Felag, Kontaktpersónur FROM wl_felagar")
    out = cursor.fetchall()
    db_connection.disconnect()
    return out
