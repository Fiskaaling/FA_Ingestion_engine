from sidir.LaTeX import HelloWorld as hello

def init(ingestion_listbox):
    mainsidir = ingestion_listbox.insert("", 0, text='Sidir')
    ingestion_listbox.insert(mainsidir, 0, text="Streymmátingar")

def check_click(item, RightFrame, root):
    toReturn = 1
    if item == 'Streymmátingar':
        hello.streym(RightFrame, root)
    elif item == 'Stovna Økið':
        stovna_okid.stovna_okid(RightFrame, root, db_info)
    elif item == 'Wordlist Editor':
        wordlist_editor.wl_edtitor(RightFrame, root, db_info)
    elif item == 'Leita í mátingum':
        Leitamatingar.Leita(RightFrame, db_host, db_user, db_password)
    else:
        toReturn = 0
    return toReturn
