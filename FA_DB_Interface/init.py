import FA_DB_Interface.stovna_geo_okid
import FA_DB_Interface.stovna_okid

db_host = '192.168.43.94'
db_user = 'JK'
db_password = 'koda'

def init(ingestion_listbox):
    databasi = ingestion_listbox.insert("", 0, text='Dátugrunnur')
    ingestion_listbox.insert(databasi, 0, text="Stovna Geo Økið")
    ingestion_listbox.insert(databasi, 0, text="Stovna Økið")


def check_click(item, RightFrame, root):
    if item == 'Stovna Geo Økið':
        FA_DB_Interface.stovna_geo_okid.stovna_geo_okid(RightFrame, root, db_host, db_user, db_password)
    elif item == 'Stovna Økið':
        FA_DB_Interface.stovna_okid.stovna_okid(RightFrame, root, db_host, db_user, db_password)
