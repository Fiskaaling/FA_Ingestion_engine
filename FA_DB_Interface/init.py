import FA_DB_Interface.stovna_geo_okid
import FA_DB_Interface.inset_matingar

db_host = '192.168.43.94'
db_user = 'JK'
db_password = 'koda'
db_info = {'user' : db_user, 'password' : db_password, 'host': db_host, 'database': 'fa_db'}

def init(ingestion_listbox):
    databasi = ingestion_listbox.insert("", 0, text='Dátugrunnur')
    okid = ingestion_listbox.insert(databasi, 0, text="Stovna Geo Økið")
    ingestion_listbox.insert(databasi, 0, text="Inset Mátingar")

def check_click(item, RightFrame, root):
    if item == 'Stovna Geo Økið':
        FA_DB_Interface.stovna_geo_okid.stovna_geo_okid(RightFrame, root, db_info)
    elif item == 'Inset Mátingar':
        FA_DB_Interface.inset_matingar.inset_matingar(RightFrame, db_host, db_user, db_password)
