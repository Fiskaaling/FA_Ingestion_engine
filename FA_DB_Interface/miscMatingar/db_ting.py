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

def listfelagar(setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT Id_felagar, Felag, Kontaktpersónur, Vanligt_embargo_dagar FROM wl_felagar")
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

def insetmating(setup_dict, id, destdir, embargo):
    db_connection, cursor = fadblogin(setup_dict)

    cursor.execute(
        "INSERT into Mátingar (id, Mátari, Start_tid, Stop_tid, Path_to_data, Umbiði_av, Embargo_til)"
        " VALUE (%s, %s, %s, %s, %s, %s, %s);",
        (id, setup_dict['Instroment'], setup_dict['Utfiltdato']['Startdato'],
         setup_dict['Utfiltdato']['Enddato'], destdir, setup_dict['info']['id'], embargo))
    for x in setup_dict['uppsetan'].keys():
        if setup_dict['uppsetan'][x] != '':
            print((id, x, setup_dict['uppsetan'][x]))
            cursor.execute("INSERT into Uppsetingar (uppseting_id, uppseting, virði) VALUE (%s, %s, %s)",
                           (id, x, setup_dict['uppsetan'][x]))
    #TODO inset økir
    db_connection.commit()

    db_connection.disconnect()

def stopnull(setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT id, Mátari, Start_tid FROM mátingar WHERE Stop_tid is NULL ORDER BY Start_tid")
    out = cursor.fetchall()
    db_connection.disconnect()
    return out

def getdatepath(id, setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT Start_tid, Path_to_data FROM mátingar WHERE id=%s", (id,))
    out = cursor.fetchone()
    db_connection.disconnect()
    return out

def Dagførupp(id, setup_dict):
    db_connection, cursor = fadblogin(setup_dict)

    cursor.execute("SELECT Mátari FROM mátingar where id=%s", (id,))
    Mátari = cursor.fetchone()[0]
    cursor.execute("SELECT møgulig_uppseting_ID, Uppseting_Navn, std_uppseting FROM møguligar_uppsetingar"
                   " WHERE Instrument_Navn=%s", (Mátari,))
    Møguligarupp = cursor.fetchall()
    cursor.execute("SELECT uppseting, virði FROM uppsetingar WHERE uppseting_id=%s", (id,))
    upp = cursor.fetchall()
    db_connection.disconnect()
    return Møguligarupp, upp

def uppdatedb(setup_dict):
    db_connection, cursor = fadblogin(setup_dict)

    if setup_dict['Utfiltdato']['Enddato'] != None:
        cursor.execute("UPDATE mátingar SET Stop_tid = %s WHERE id=%s",
                       (setup_dict['Utfiltdato']['Enddato'], setup_dict['id']))
    #TODO hettar kemur ikki at rigga um man setur níggjar møguligar uppsetaninr inn
    for x in setup_dict['uppsetan'].keys():
        cursor.execute("UPDATE uppsetingar SET virði = %s WHERE uppseting_id = %s AND uppseting = %s",
                       (setup_dict['uppsetan'][x], setup_dict['id'], x))
    db_connection.commit()
    db_connection.disconnect()

def getPTD(setup_dict, destdir):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT Path_to_data FROM mátingar WHERE Path_to_data LIKE %s", (destdir + '%',))
    out = [x[0] for x in cursor.fetchall()]
    db_connection.disconnect()
    return out