import Ingestion.CTD.plotAsci

def init(ingestion_listbox):
    ctd = ingestion_listbox.insert("", 0, text='Seabird SBE 25 CTD')
    ingestion_listbox.insert(ctd, 0, text="Tekna Ascii fíl")


def check_click(item, RightFrame, root):
    if item == 'Tekna Ascii fíl':
        Ingestion.CTD.plotAsci.asciiPlt(RightFrame, root)
