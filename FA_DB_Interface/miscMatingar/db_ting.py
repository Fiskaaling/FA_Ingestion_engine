import mysql.connector as db


def fadblogin(setup_dict):
    db_connection = db.connect(**setup_dict['login'])
    return db_connection, db_connection.cursor()

def status(setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT Status FROM wl_status")
    out = [x[0] for x in cursor.fetchall()]
    db_connection.disconnect()
    return out

def listinstrumentir(status, setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    if status == 'alt':
        cursor.execute("SELECT navn, status, Slag FROM instrumentir")
    else:
        cursor.execute("SELECT navn, status, Slag FROM instrumentir WHERE status=%s", (status,))
    out = cursor.fetchall()
    db_connection.disconnect()
    return out

def getuppsetanir(Navn, setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT møgulig_uppseting_ID, Uppseting_Navn, std_uppseting "
                   "FROM Møguligar_uppsetingar WHERE Instrument_Navn=%s", (Navn,))
    out = cursor.fetchall()
    db_connection.disconnect()
    return out

def getlastid(setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT id FROM Mátingar ORDER BY id DESC LIMIT 1")
    out = cursor.fetchone()
    db_connection.disconnect()
    return out[0]

def insetmating(setup_dict, id, destdir):
    db_connection, cursor = fadblogin(setup_dict)

    if setup_dict['Utfiltdato']['Enddato'] == None:
        cursor.execute("INSERT into Mátingar (id, Mátari, Start_tid, Path_to_data) VALUE (%s, %s, %s, %s);",
                       (id, setup_dict['Instroment'], setup_dict['Utfiltdato']['Startdato'], destdir))
    else:
        cursor.execute(
            "INSERT into Mátingar (id, Mátari, Start_tid, Stop_tid, Path_to_data) VALUE (%s, %s, %s, %s, %s);",
            (id, setup_dict['Instroment'], setup_dict['Utfiltdato']['Startdato'],
             setup_dict['Utfiltdato']['Enddato'], destdir))
    for x in setup_dict['uppsetan'].keys():
        if setup_dict['uppsetan'][x] != '':
            print((id, x, setup_dict['uppsetan'][x]))
            cursor.execute("INSERT into Uppsetingar (uppseting_id, uppseting, virði) VALUE (%s, %s, %s)",
                           (id, x, setup_dict['uppsetan'][x]))
    #TODO inset økir
    db_connection.commit()

    db_connection.disconnect()