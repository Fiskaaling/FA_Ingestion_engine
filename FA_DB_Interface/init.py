import FA_DB_Interface.stovna_geo_okid
import FA_DB_Interface.inset_matingar
import FA_DB_Interface.Dagfør_matingar

db_host = '192.168.43.94'
db_user = 'JK'
db_password = 'koda'

def init(ingestion_listbox):
    databasi = ingestion_listbox.insert("", 0, text='Dátugrunnur')
    okid = ingestion_listbox.insert(databasi, 0, text="Stovna Geo Økið")
    ingestion_listbox.insert(databasi, 0, text="Inset Mátingar")
    ingestion_listbox.insert(databasi, 0, text="Dagfør Mátingar")

def check_click(item, RightFrame, root):
    if item == 'Stovna Geo Økið':
        FA_DB_Interface.stovna_geo_okid.stovna_geo_okid(RightFrame, root, db_host, db_user, db_password)
    elif item == 'Inset Mátingar':
        FA_DB_Interface.inset_matingar.inset_matingar(RightFrame, db_host, db_user, db_password)
    elif item == 'Dagfør Mátingar':
        FA_DB_Interface.Dagfør_matingar.Dagfør_matingar(RightFrame, db_host, db_user, db_password)
