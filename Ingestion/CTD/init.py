import Ingestion.CTD.plotAscii
import Ingestion.CTD.Process_data
import Ingestion.CTD.bin_average
import Ingestion.CTD.tidarseria_linja
import Ingestion.CTD.skraset_stodir
import Ingestion.CTD.align_ctd
from Ingestion.CTD import cruise_overview
#import Ingestion.CTD.MultipleAxisProfile

def init(ingestion_listbox):
    ctd = ingestion_listbox.insert("", 0, text='Seabird SBE 25 CTD')
    ingestion_listbox.insert(ctd, 0, text="Tekna Ascii fíl")
    ingestion_listbox.insert(ctd, 0, text="Linju Tíðarseria")
    ingestion_listbox.insert(ctd, 0, text="Skráset støðir")
    ingestion_listbox.insert(ctd, 0, text="Bin Average")
    ingestion_listbox.insert(ctd, 0, text="Processera rádata")
    ingestion_listbox.insert(ctd, 0, text="Plot Multiple Axis Profile")
    ingestion_listbox.insert(ctd, 0, text="Align CTD")


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
    elif item == 'Align CTD':
        Ingestion.CTD.align_ctd.align_ctd_frame(RightFrame, root)
    elif item == 'Túr yvirlit':
        cruise_overview.cruise_overview_frame(RightFrame, root)
    elif item == 'Plot Multiple Axis Profile':
        pass
        #Ingestion.CTD.MultipleAxisProfile.plot_axis_root(RightFrame, root)
    else:
        toReturn = 0
    return toReturn

