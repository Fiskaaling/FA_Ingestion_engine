from . import streymmatingar

def init(ingestion_listbox):
    mainsidir = ingestion_listbox.insert("", 0, text='Sidir')
    ingestion_listbox.insert(mainsidir, 0, text="Streymmátingar")

def check_click(item, RightFrame, root):
    toReturn = 1
    if item == 'Streymmátingar':
        streymmatingar.streym(RightFrame, root)
    else:
        toReturn = 0
    return toReturn
