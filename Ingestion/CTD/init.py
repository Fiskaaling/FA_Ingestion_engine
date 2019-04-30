import Ingestion.CTD.plotAscii
import Ingestion.CTD.Process_data

def init(ingestion_listbox):
    ctd = ingestion_listbox.insert("", 0, text='Seabird SBE 25 CTD')
    ingestion_listbox.insert(ctd, 0, text="Tekna Ascii fíl")
    ingestion_listbox.insert(ctd, 0, text="Processera rádata")


def check_click(item, RightFrame, root):
    toReturn = 1
    if item == 'Tekna Ascii fíl':
        Ingestion.CTD.plotAscii.asciiPlt(RightFrame, root)
    elif item == 'Processera rádata':
        Ingestion.CTD.Process_data.process_CTD_Data(RightFrame, root)
    else:
        toReturn = 0
    return toReturn
