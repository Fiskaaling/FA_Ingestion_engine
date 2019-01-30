import mysql.connector as db


def fadblogin(setup_dict):
    db_connection = db.connect(**setup_dict['login'])
    return db_connection, db_connection.cursor()

def status(setup_dict):
    db_connection, cursor = fadblogin(setup_dict)
    cursor.execute("SELECT * FROM wl_status")
    return [x[0] for x in cursor.fetchall()]