from FA_DB_Interface import stovna_geo_okid, stovna_okid, Matingar, wordlist_editor

db_host = '192.168.43.62'
db_user = 'JK'
db_password = 'koda'
db_info = {'user': db_user, 'password': db_password, 'host': db_host, 'database': 'fa_db'}


def init(ingestion_listbox):
    databasi = ingestion_listbox.insert("", 0, text='Dátugrunnur')
    ingestion_listbox.insert(databasi, 0, text="Stovna Geo Økið")
    ingestion_listbox.insert(databasi, 0, text="Stovna Økið")
    ingestion_listbox.insert(databasi, 0, text='Mátingar')
    ingestion_listbox.insert(databasi, 0, text='Wordlist Editor')


def check_click(item, RightFrame, root):
    toReturn = 0
    if item == 'Stovna Geo Økið':
        stovna_geo_okid.stovna_geo_okid(RightFrame, root, db_info)
    elif item == 'Mátingar':
        Matingar.inset_matingar(RightFrame, db_host, db_user, db_password)
    elif item == 'Stovna Økið':
        stovna_okid.stovna_okid(RightFrame, root, db_info)
    elif item == 'Wordlist Editor':
        wordlist_editor.wl_edtitor(RightFrame, root, db_info)
    else:
        toReturn = 1
    return toReturn
