import pandas as pd
import os
import glob
from tkinter import *
from tkinter import messagebox
import matplotlib
import Ingestion.CTD.align_ctd
import Ingestion.CTD.bin_average
import getpass
import fileinput
import subprocess
from tkinter import filedialog
from shutil import copyfile
matplotlib.use('TkAgg')
import xml.etree.ElementTree as ET

def cruise_overview_frame(frame, root2, selectedCruse=''):
    if not os.path.exists('./Ingestion/CTD/Lokalt_Data/'):
        print('Ger lokala mappu')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/')
    else:
        print('Lokala mappan er til')

    # TODO: Sleppa uttanum fasta mappustrukturin. Byrja við at velja datamapp og arbeiða haðan.

    mappunavn = './Ingestion/CTD/Lokalt_Data/'
    frames_dict = {'mappunavn': mappunavn}
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)

    # Turnummar - Stovna tur
    controlsFrame = Frame(frame)
    controlsFrame.pack(side=TOP)
    Label(controlsFrame, text='Túrnummar:').pack(side=LEFT)

    turnummar = Entry(controlsFrame, width=10)
    turnummar.pack(side=LEFT)
    # stovna_tur
    Button(controlsFrame, text='Stovna Túr', command=lambda: stovna_tur(turnummar.get(), frames_dict)).pack(side=LEFT)

####################################################################################################################
# Upper panel Data Conversion, Filter, Align, CTM, Derive, Window Filter, Bin Average, Ascii Out, Ger figurar
####################################################################################################################

# Túr ramma
    frames_dict['cruiseFrame'] = Frame(frame)
    frames_dict['cruiseFrame'].pack(side=LEFT, anchor=W, expand=True, fill=BOTH)
# Status ramma
    frames_dict['statusFrame'] = Frame(frame)
    frames_dict['statusFrame'].pack(side=LEFT, anchor=W, expand=True, fill=BOTH)
    Label(frames_dict['statusFrame'], text='Status á viðgerð', font=("Courier", 14)).pack(side=TOP)

    frames_dict['selectedFrame'] = 0
    frames_dict['selectedCruse'] = 0
    frames_dict['selectedCast'] = 0

    frames_dict['frame'] = frame
    frames_dict['root2'] = root2

    updatecruseframe(frames_dict)
    #print('SelectedCruise: {}'.format(selectedCruse))
    cruises = os.listdir(mappunavn)
    cruises.sort()
    #print(cruises)
    for i, file in enumerate(cruises):
        #print(file)
        if file == selectedCruse:
            frames_dict['selectedCruse'] = i
            updateCastsFrame(frames_dict)
    updatecruseframe(frames_dict)

    def key(event):
        #print(len(frames_dict['cruises']))
        #print(frames_dict['selectedCruse'])
        if frames_dict['selectedFrame'] == 0:
            if event.keysym == 'Up':
                if (frames_dict['selectedCruse'] - 1) >= 0:
                    frames_dict['selectedCruse'] -= 1
                    updatecruseframe(frames_dict)
            if event.keysym == 'Down':
                if frames_dict['selectedCruse'] + 1 < len(frames_dict['cruises']):
                    frames_dict['selectedCruse'] += 1
                    updatecruseframe(frames_dict)
        if frames_dict['selectedFrame'] == 1:
            if event.keysym == 'Up':
                if (frames_dict['selectedCast'] - 1) >= 0:
                    frames_dict['selectedCast'] -= 1
                    updateCastsFrame(frames_dict)
            if event.keysym == 'Down':
                if frames_dict['selectedCast'] + 1 < len(frames_dict['casts']):
                    frames_dict['selectedCast'] += 1
                    updateCastsFrame(frames_dict)
        if event.keysym == 'Right':
            if frames_dict['selectedFrame'] < 2:
                frames_dict['selectedFrame'] += 1
            if frames_dict['selectedFrame'] == 1:
                updateCastsFrame(frames_dict)
        if event.keysym == 'Left':
            if frames_dict['selectedFrame'] > 0:
                frames_dict['selectedFrame'] -= 1
            if frames_dict['selectedFrame'] == 1:
                updateCastsFrame(frames_dict)
        print(event.keysym)

    root.bind('<Key>', key)

def updateCastsFrame(frames_dict):
    if 'castFrameDict' in frames_dict:
        for frame in frames_dict['castFrameDict']:
            for widget in frames_dict['castFrameDict'][frame].winfo_children(): # Tømur quality frame
                widget.destroy()
            frames_dict['castFrameDict'][frame].pack_forget()
            frames_dict['castFrameDict'][frame].destroy()
        frames_dict['statusFrameBelow'].destroy()

    frames_dict['casts'] = os.listdir(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/RAW/')
    frames_dict['casts'].sort()
    castsDict = {}
    buttonsDict = {}
    castFrameDict = {}
    if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/turMetadata.csv'):
        metadata = pd.read_csv(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/turMetadata.csv', index_col=False)
    else:
        metadata = pd.DataFrame(columns=['key', 'value'])

    meanAlignCTDSum = 0
    meanAlignCTDDivideby = 0

    for i, cast in enumerate(frames_dict['casts']):
        castFrameDict[cast] = Frame(frames_dict['statusFrame'])
        castFrameDict[cast].pack(side=TOP)
        castsDict[str(cast)] = Label(castFrameDict[cast], text=cast[:-4], font=("Courier", 12))
        castsDict[str(cast)].pack(side=LEFT)

        # Create buttons for Data Conversion and Filter.
        # IF statement controlls color of button
        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/1_Data_Conversion/' + cast[:-4]+'.cnv'):
            col = 'lightgreen'
        else:
            col = '#D9D9D9'
        buttonsDict['DataConv' + cast] = Button(castFrameDict[cast], text='Data Conversion', bg=col)
        buttonsDict['DataConv' + cast].pack(side=LEFT)
        buttonsDict['Filter' + cast] = Button(castFrameDict[cast], text='Filter', bg=col)
        buttonsDict['Filter' + cast].pack(side=LEFT)

        # Align buttons
        AlignCTD_ok = 0
        for metadataRowIndex, metadataRow in enumerate(metadata.iloc[:,0]):
            if metadataRow.split('CTD')[1][:-4] == cast[:-4]:
                print('Align row found')
                AlignCTD_ok = metadata.iloc[metadataRowIndex, 1]
                meanAlignCTDSum += metadata.iloc[metadataRowIndex, 1]
                meanAlignCTDDivideby += 1
            else:
                print('Align row not found')

        if AlignCTD_ok:
            var, col = AlignCTD_ok, 'Green'
        elif os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/3_Align_CTD/' + cast[:-4]+'.cnv'):
            if AlignCTD_ok:
                var, col = AlignCTD_ok, 'lightgreen'
            else:
                var, col = 0, 'lightgreen'
        else:
            var, col = 0, '#D9D9D9'

        buttonsDict['AlignCTD' + cast] = Button(castFrameDict[cast], text='Align CTD ' + "{:.2f}".format(var), bg=col,
                                                command=lambda: Ingestion.CTD.align_ctd.align_ctd_frame(frames_dict['frame'],
                                                frames_dict['root2'],selectNewFolder=False,mappunavn=frames_dict['mappunavn'] + '/' +frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/2_Filter/',filIndex=0))
        buttonsDict['AlignCTD' + cast].pack(side=LEFT)

        # CTM buttons
        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/4_CTM/' + cast[:-4]+'.cnv'):
            col = 'lightgreen'
        else: col = '#D9D9D9'
        buttonsDict['CTM' + cast] = Button(castFrameDict[cast], text='CTM', bg=col)
        buttonsDict['CTM' + cast].pack(side=LEFT)

        # Derive buttons
        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/5_Derive/' + cast[:-4]+'.cnv'):
            col = 'lightgreen'
        else: col = '#D9D9D9'
        buttonsDict['Derive' + cast] = Button(castFrameDict[cast], text='Derived Variables', bg=col)
        buttonsDict['Derive' + cast].pack(side=LEFT)

        # Window Filter buttons
        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/6_Window_Filter/' + cast[:-4]+'.cnv'):
            col = 'lightgreen'
        else: col = '#D9D9D9'
        buttonsDict['Window_Filter' + cast] = Button(castFrameDict[cast], text='Window Filter', bg=col)
        buttonsDict['Window_Filter' + cast].pack(side=LEFT)

        # Bin Average buttons
        binAverageInputFolder = frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/ASCII_ALL/'
        binAverageInputFolder = binAverageInputFolder.replace('//', '/')
        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/7_Bin_Average/' + cast[:-4]+'.cnv'):
            col = 'lightgreen'
        else: col = '#D9D9D9'
        buttonsDict['BA' + cast] = Button(castFrameDict[cast], text='Bin Average', command=lambda: Ingestion.CTD.bin_average.bin_average_frame(frames_dict['frame'], frames_dict['root2'], mappunavn=binAverageInputFolder), bg=col)
        buttonsDict['BA' + cast].pack(side=LEFT)

        # Ascii out buttons
        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/ASCII/ASCII_Downcast/' + cast[:-4]+'.asc'): col = 'lightgreen'
        else: col = '#D9D9D9'
        buttonsDict['ASCII_out' + cast] = Button(castFrameDict[cast], text='Ascii out', bg=col)
        buttonsDict['ASCII_out' + cast].pack(side=LEFT)

        # Ger figurar buttons
        buttonsDict['MakeFigures' + cast] = Button(castFrameDict[cast], text='Ger figurar')
        buttonsDict['MakeFigures' + cast].pack(side=LEFT)

        # Góðska
        castsDict['GodskaLabel' + str(cast)] = Label(castFrameDict[cast], text='Góðska:', font=("Courier", 12))
        castsDict['GodskaLabel' + str(cast)].pack(side=LEFT)

        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/ASCII/ASCII_Downcast/metadata/' + cast[:-4] + '_metadata.csv'):
            metadataCast = pd.read_csv(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/ASCII/ASCII_Downcast/metadata/' + cast[:-4] + '_metadata.csv', index_col=False)
            print('her: ',metadataCast.iloc[:, 0])
            for metadataRowIndex, metadataRow in enumerate(metadataCast.iloc[:, 0]):
                print(metadataCast)
                print(metadataRow)
                if metadataRow.split('CTD')[1][:-4] == cast[:-4]:
                    AlignCTD_ok = metadata.iloc[metadataRowIndex, 1]
                    meanAlignCTDSum += metadata.iloc[metadataRowIndex, 1]
                    meanAlignCTDDivideby += 1
                print('ok')
            print(metadataCast)
            castsDict['GodskaLabelvar' + str(cast)] = Label(castFrameDict[cast], text='farts', font=("Courier", 12))
            castsDict['GodskaLabelvar' + str(cast)].pack(side=LEFT)
        else:
            metadata = pd.DataFrame(columns=['key', 'value'])

    ####################################################################################################################
    # Lower panel KOYR VIÐGERÐ
    ####################################################################################################################

    # Read processing choises from file
    xmlcon_align = pd.read_csv('Ingestion/CTD/Settings/xmlcon_align_choice.txt')
    TripNo = int(frames_dict['cruises'][frames_dict['selectedCruse']])
    choises = xmlcon_align[xmlcon_align.trip < TripNo].iloc[-1]

    frames_dict['castFrameDict'] = castFrameDict
    frames_dict['statusFrameBelow'] = Frame(frames_dict['statusFrame'])
    frames_dict['statusFrameBelow'].pack(side=TOP, anchor=W)
    Label(frames_dict['statusFrameBelow'], text='Koyr viðgerð', font=("Courier", 14)).pack(side=TOP)

    # Conversion og Filter
    frames_dict['ConvFilter_area'] = Frame(frames_dict['statusFrameBelow'])
    frames_dict['ConvFilter_area'].pack(side=TOP, anchor=W)
    frames_dict['ConvFilter_btn'] = Button(frames_dict['ConvFilter_area'],
                                           text='Koyr Data Conversion og Filter',
                                           command=lambda: conv_og_filter(frames_dict, choises.xmlcon), width=35)
    frames_dict['ConvFilter_btn'].pack(side=LEFT)
    Label(frames_dict['ConvFilter_area'],
          text=f' Xmlcon file used:\t {choises.xmlcon}.xmlcon\t\t Calibrated: {choises.calibrated}').pack(side=LEFT)

    # TODO: Gera 2 knøttar úteftir til Align. 1 ið brúkar virði, ið eru roknaði frammanundan, 2 id koyrir Rokna Align modulið.

    # Align Standard
    frames_dict['AlignStandard_area'] = Frame(frames_dict['statusFrameBelow'])
    frames_dict['AlignStandard_area'].pack(side=TOP, anchor=W)
    frames_dict['AlignStandard_btn'] = Button(frames_dict['AlignStandard_area'],
                                              text='Koyr Align við Standard virðum',
                                              command=lambda: align_ctd_standard(frames_dict, choises.c, choises.ox,), width=35)
    frames_dict['AlignStandard_btn'].pack(side=LEFT)
    Label(frames_dict['AlignStandard_area'],
          text=f' Align values used:\t Cond = {choises.c}, Ox = {choises.ox}\t Calculated: {choises.calculated} by {choises.by}').pack(side=LEFT)

    frames_dict['statusFrameBelowAlign'] = Frame(frames_dict['statusFrameBelow'])
    frames_dict['statusFrameBelowAlign'].pack(side=TOP, anchor=W)

    # Align Calculate
    meanAlignCTD = 0
    if meanAlignCTDDivideby:
        meanAlignCTD = meanAlignCTDSum/meanAlignCTDDivideby
        frames_dict['AlignCTDLabel'] = Label(frames_dict['statusFrameBelowAlign'], text="{:.2f}".format(meanAlignCTD))
    else:
        frames_dict['AlignCTDLabel'] = Label(frames_dict['statusFrameBelowAlign'], text=str(-1))

    if len(os.listdir(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/RAW/')) == len(os.listdir(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/3_Align_CTD/')):
        frames_dict['AlignCTDButton'] = Button(frames_dict['statusFrameBelowAlign'],
                                               text='Rokna Align CTD',
                                               command=lambda: align_ctd(frames_dict, meanAlignCTD), width=35)
    else:
        frames_dict['AlignCTDButton'] = Button(frames_dict['statusFrameBelowAlign'],
                                               text='Rokna Align CTD',
                                               command=lambda: align_ctd(frames_dict, meanAlignCTD), width=35)
    frames_dict['AlignCTDButton'].pack(side=LEFT)

    Label(frames_dict['statusFrameBelowAlign'], text=' Mean Align value:').pack(side=LEFT)
    frames_dict['AlignCTDLabel'].pack(side=LEFT)

    # CTM, Derive and Window Filter
    frames_dict['window_filter_btn'] = Button(frames_dict['statusFrameBelow'], 
                                              text='Koyr CTM, Derived og Window filter',
                                              command=lambda: CTM_derived_window(frames_dict, choises.xmlcon), width=35)
    frames_dict['window_filter_btn'].pack(side=TOP, anchor=W)

def stovna_tur(turnummar, frames_dict):
    mappunavn = filedialog.askdirectory(title='Vel rádatamappu')
    casts = os.listdir(mappunavn)

    if not os.path.exists('./Ingestion/CTD/Lokalt_Data/' + turnummar + '/'):
        print('Ger lokala mappu')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turnummar)
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turnummar + '/Processed')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turnummar + '/RAW')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turnummar + '/Processed/1_Data_Conversion')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turnummar + '/Processed/2_Filter')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turnummar + '/Processed/3_Align_CTD')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turnummar + '/Processed/4_CTM')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turnummar + '/Processed/5_Derive')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turnummar + '/Processed/6_Window_Filter')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turnummar + '/Processed/ASCII_ALL')
    else:
        print('Lokala mappan er til')

    casts.sort()
    for i, cast in enumerate(casts):
        filnavn = str(turnummar) + '{:03d}'.format(i + 1)
        if os.path.isfile('{}/{}.xml'.format(mappunavn, filnavn)):
            print('file is')
            copyfile('{}/{}.xml'.format(mappunavn, filnavn),
                     './Ingestion/CTD/Lokalt_Data/' + turnummar + '/RAW/' + filnavn + '.xml')
        else:
            filnavnorginal = os.listdir(mappunavn + '/' + cast)
            filnavnorginal = filnavnorginal[0]
            # TODO: Flyt ístaðin fyri at kopiera
            copyfile(mappunavn + '/' + cast + '/' + filnavnorginal,
                     './Ingestion/CTD/Lokalt_Data/' + turnummar + '/RAW/' + filnavn + '.xml')
    # TODO: krasjar tá stovna túr er gjørt, tí onnur cast koma við í okkurt index. Riggar at pressesera víðari um man genstartar.
    updatecruseframe(frames_dict)
    updateCastsFrame(frames_dict)

# funkur, ið koyra røttu prossesering tá túr trýstir á knøttarnar

# Rokna Conversion og Filter
def conv_og_filter(frames_dict,xmlcon):
    for cast in frames_dict['casts']:
        TripNo = frames_dict['cruises'][frames_dict['selectedCruse']]
        if os.name == 'nt':
            commands = ['C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe']
        else:
            commands = ['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe']
        subprocess.call(commands +
                        [f"{os.getcwd()}/ingestion/CTD/Settings/1_DatCnv.txt",
                         # 1: command, 2: program, 3: in, 4: out
                         f"{os.getcwd()}/ingestion/CTD/Settings/{xmlcon}.xmlcon",
                         f"{os.getcwd()}/ingestion/CTD/Settings/DatCnv.psa",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/RAW/{cast}",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/1_Data_Conversion",
                         '#m'])

        subprocess.call(commands +
                        [f"{os.getcwd()}/ingestion/CTD/Settings/2_Filter.txt",
                        # 1: program, 2: in, 3: out
                        f"{os.getcwd()}/ingestion/CTD/Settings/Filter.psa",
                        f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/1_Data_Conversion/{cast[:-4]}",
                        f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/2_Filter",
                        '#m'])

        updateCastsFrame(frames_dict)

def align_ctd_standard(frames_dict,CondAdv,OxAdv):

    # Corrections to AlignCTD .psa file
    tree = ET.parse(f"{os.getcwd()}/Ingestion/CTD/Settings/AlignCTD.psa")
    # set filter A for variables C, T and B for P
    tree.find('./ValArray/*[@variable_name="Conductivity"]').attrib['value'] = str(CondAdv)
    tree.find('./ValArray/*[@variable_name="Oxygen raw, SBE 43"]').attrib['value'] = str(OxAdv)
    tree.write(f"{os.getcwd()}/Ingestion/CTD/Settings/AlignCTD.psa", encoding="UTF-8", xml_declaration=True)

    for cast in frames_dict['casts']:
        TripNo = frames_dict['cruises'][frames_dict['selectedCruse']]
        print('Align: ', cast, TripNo)

        if os.name == 'nt':
            commands = ['C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe']
        else:
            commands = ['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe']

        subprocess.call(commands + [f"{os.getcwd()}/ingestion/CTD/Settings/3_Align_CTD.txt",
                         # 1: program, 2: in, 3: out
                         f"{os.getcwd()}/ingestion/CTD/Settings/AlignCTD.psa",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/2_Filter/{cast[:-4]}",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/3_Align_CTD",
                         '#m'])

        updateCastsFrame(frames_dict)
        updatecruseframe(frames_dict)

# Rokna Align CTD
# TODO: Gera Align Modul til at finna bestu align fyri C og Ox (og Par og FLu). C er konstant um CTD'in ikki broytist, men Ox kann broytast við árstíðunum
def align_ctd(frames_dict, ox_offset):
    if os.name == 'nt':
        winedir = 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/'
    else:
        winedir = f'/home/{getpass.getuser()}/.wine/drive_c/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/'
    copyfile(f'{winedir}AlignCTD_(custom)_original.psa', f'{winedir}AlignCTD_(custom).psa')
    ikki_funni_linju = True

    with fileinput.FileInput(winedir + 'AlignCTD_(custom).psa', inplace=True) as file:
        for line in file:
            ikki_funni_linju = False
            print(line.replace('-77', str(ox_offset)), end='')

    if ikki_funni_linju:
        messagebox.showerror('Feilur við export', 'Customstart fílur ikki funnin!')
        raise FileNotFoundError('Customstart fílur ikki funnin')

    for cast in frames_dict['casts']:
        TripNo = frames_dict['cruises'][frames_dict['selectedCruse']]
        if os.name == 'nt':
            print('Input: ' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/2_Filter/' + cast[:-4])
            subprocess.call(['C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             f"{os.getcwd()}/ingestion/CTD/Settings/3_Align_CTD_(custom).txt",
                             # 1: program, 2: in, 3: out
                             f"{os.getcwd()}/ingestion/CTD/Settings/AlignCTD_(custom).psa",
                             f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/2_Filter/{cast[:-4]}",
                             f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/3_Align_CTD",
                             '#m'])
        else:
            print('Input: ' + 'Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/2_Filter/' + cast[:-4])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             f"{os.getcwd()}/ingestion/CTD/Settings/3_Align_CTD_(custom).txt",
                             # 1: program, 2: in, 3: out
                             f"{os.getcwd()}/ingestion/CTD/Settings/AlignCTD_(custom).psa",
                             f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/2_Filter/{cast[:-4]}",
                             f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/3_Align_CTD",
                             '#m'])
        updateCastsFrame(frames_dict)
        updatecruseframe(frames_dict)

def CTM_derived_window(frames_dict,xmlcon):
    for cast in frames_dict['casts']:
        TripNo = frames_dict['cruises'][frames_dict['selectedCruse']]
        if os.name == 'nt':
            commands = ['C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe']
        else:
            commands = ['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe']
        subprocess.call(commands + [f"{os.getcwd()}/ingestion/CTD/Settings/4_CTM.txt",
                         # 1: program, 2: in, 3: out
                         f"{os.getcwd()}/ingestion/CTD/Settings/CellTM.psa",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/3_Align_CTD/{cast[:-4]}",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/4_CTM",
                         '#m'])
        subprocess.call(commands + [f"{os.getcwd()}/ingestion/CTD/Settings/6_Derive.txt",
                         # 1: command, 2: in, 3: out
                         f"{os.getcwd()}/ingestion/CTD/Settings/{xmlcon}.xmlcon",
                         f"{os.getcwd()}/ingestion/CTD/Settings/Derive.psa",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/4_CTM/{cast[:-4]}",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/5_Derive", '#m'])
        subprocess.call(commands + [f"{os.getcwd()}/ingestion/CTD/Settings/7_Window_Filter.txt",
                         # 1: program, 2: in, 3: out
                         f"{os.getcwd()}/ingestion/CTD/Settings/W_Filter.psa",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/5_Derive/{cast[:-4]}",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/6_Window_Filter", '#m'])
        subprocess.call(commands + [f"{os.getcwd()}/ingestion/CTD/Settings/9_All_ASCII_Out.txt",
                         # 1: program, 2: in, 3: out
                         f"{os.getcwd()}/ingestion/CTD/Settings/All_ASCII_Out.psa",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/6_Window_Filter/{cast[:-4]}",
                         f"{os.getcwd()}/Ingestion/CTD/Lokalt_Data/{TripNo}/Processed/ASCII_ALL", '#m'])

        updateCastsFrame(frames_dict)
        updatecruseframe(frames_dict)

def updatecruseframe(frames_dict):
    for widget in frames_dict['cruiseFrame'].winfo_children(): # Tømur quality frame
        widget.destroy()
    Label(frames_dict['cruiseFrame'], text='Túrur', font=("Courier", 14)).pack(side=TOP)
    frames_dict['cruises'] = os.listdir(frames_dict['mappunavn'])
    frames_dict['cruises'].sort()
    cruisesDict = {}
    for i, cruise in enumerate(frames_dict['cruises']):
        if i == frames_dict['selectedCruse']:
            cruisesDict[str(cruise)] = Label(frames_dict['cruiseFrame'], text=cruise, font=("Courier", 12, 'underline'))
        else:
            cruisesDict[str(cruise)] = Label(frames_dict['cruiseFrame'], text=cruise, font=("Courier", 12))
        cruisesDict[str(cruise)].pack(side=TOP)
    frames_dict['cruisesDict'] = cruisesDict