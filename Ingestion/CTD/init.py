import Ingestion.CTD.plotAscii
import Ingestion.CTD.Process_data
import Ingestion.CTD.bin_average
import Ingestion.CTD.tidarseria_linja
import Ingestion.CTD.skraset_stodir

def init(ingestion_listbox):
    ctd = ingestion_listbox.insert("", 0, text='Seabird SBE 25 CTD')
    ingestion_listbox.insert(ctd, 0, text="Tekna Ascii fíl")
    ingestion_listbox.insert(ctd, 0, text="Linju Tíðarseria")
    ingestion_listbox.insert(ctd, 0, text="Skráset støðir")
    ingestion_listbox.insert(ctd, 0, text="Bin Average")
    ingestion_listbox.insert(ctd, 0, text="Processera rádata")


def check_click(item, RightFrame, root):
    toReturn = 1
    if item == 'Tekna Ascii fíl':
        Ingestion.CTD.plotAscii.asciiPlt(RightFrame, root)
    elif item == 'Linju Tíðarseria':
        Ingestion.CTD.tidarseria_linja.CTDtidarseria_lin(RightFrame, root)
    elif item == 'Processera rádata':
        Ingestion.CTD.Process_data.process_CTD_Data(RightFrame, root)
    elif item == 'Bin Average':
        Ingestion.CTD.bin_average.bin_average_frame(RightFrame, root)
    elif item == 'Skráset støðir':
        Ingestion.CTD.skraset_stodir.skraset_stodir(RightFrame, root)
    else:
        toReturn = 0
    return toReturn
