import pandas as pd
import os
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


def cruise_overview_frame(frame, root2, selectedCruse=''):
    if not os.path.exists('./Ingestion/CTD/Lokalt_Data/'):
        print('Ger lokala mappu')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/')
    else:
        print('Lokala mappan er til')

    mappunavn = './Ingestion/CTD/Lokalt_Data/'
    frames_dict = {'mappunavn': mappunavn}
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)

    controlsFrame = Frame(frame)
    controlsFrame.pack(side=TOP)


    Label(controlsFrame, text='Túrnummar:').pack(side=LEFT)

    turnummar = Entry(controlsFrame, width=10)
    turnummar.pack(side=LEFT)
    Button(controlsFrame, text='Stovna Túr', command=lambda: stovna_tur(turnummar.get(), frames_dict)).pack(side=LEFT)

    frames_dict['cruiseFrame'] = Frame(frame)
    frames_dict['cruiseFrame'].pack(side=LEFT, anchor=W, expand=True, fill=BOTH)

    frames_dict['statusFrame'] = Frame(frame)
    frames_dict['statusFrame'].pack(side=LEFT, anchor=W, expand=True, fill=BOTH)

    Label(frames_dict['statusFrame'], text='Status á viðgerð', font=("Courier", 14)).pack(side=TOP)

    frames_dict['selectedFrame'] = 0
    frames_dict['selectedCruse'] = 0

    frames_dict['selectedCast'] = 0

    frames_dict['frame'] = frame
    frames_dict['root2'] = root2

    updatecruseframe(frames_dict)
    print('SelectedCruise: {}'.format(selectedCruse))
    cruises = os.listdir(mappunavn)
    cruises.sort()
    print(cruises)
    for i, file in enumerate(cruises):
        print(file)
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
        #print(frames_dict['castFrameDict'])
        for frame in frames_dict['castFrameDict']:
            #print(frames_dict['castFrameDict'][frame])
            for widget in frames_dict['castFrameDict'][frame].winfo_children(): # Tømur quality frame
                #print(widget)
                widget.destroy()
            frames_dict['castFrameDict'][frame].pack_forget()
            frames_dict['castFrameDict'][frame].destroy()
        frames_dict['statusFrameBelow'].destroy()
    #print(frames_dict['mappunavn'] + frames_dict['cruises'][frames_dict['selectedCruse']])
    #print(frames_dict['mappunavn'])

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

    ####################################################################################################################
    # Upper panel Data Conversion, Filter, Align, CTM, Derive, Window Filter, Bin Average, Ascii Out, Ger figurar
    ####################################################################################################################

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
            col = '#40E0D0'
        buttonsDict['DataConv' + cast] = Button(castFrameDict[cast], text='Data Conversion', bg=col)
        buttonsDict['DataConv' + cast].pack(side=LEFT)
        buttonsDict['Filter' + cast] = Button(castFrameDict[cast], text='Filter', bg=col)
        buttonsDict['Filter' + cast].pack(side=LEFT)

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
            var, col = 0, '#40E0D0'
        buttonsDict['AlignCTD' + cast] = Button(castFrameDict[cast], text='Align CTD ' + "{:.2f}".format(var), bg=col,
                                                command=lambda: Ingestion.CTD.align_ctd.align_ctd_frame(frames_dict['frame'],frames_dict['root2'],selectNewFolder=False,mappunavn=frames_dict['mappunavn'] + '/' +frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/2_Filter/',filIndex=0))
        buttonsDict['AlignCTD' + cast].pack(side=LEFT)

        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/4_CTM/' + cast[:-4]+'.cnv'):
            buttonsDict['CTM' + cast] = Button(castFrameDict[cast], text='CTM', bg='lightgreen')
        else:
            buttonsDict['CTM' + cast] = Button(castFrameDict[cast], text='CTM')
        buttonsDict['CTM' + cast].pack(side=LEFT)

        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/5_Derive/' + cast[:-4]+'.cnv'):
            buttonsDict['Derive' + cast] = Button(castFrameDict[cast], text='Derived Variables', bg='lightgreen')
        else:
            buttonsDict['Derive' + cast] = Button(castFrameDict[cast], text='Derived Variables')
        buttonsDict['Derive' + cast].pack(side=LEFT)

        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/5_Derive/' + cast[:-4]+'.cnv'):
            buttonsDict['Window_Filter' + cast] = Button(castFrameDict[cast], text='Window Filter', bg='lightgreen')
        else:
            buttonsDict['Window_Filter' + cast] = Button(castFrameDict[cast], text='Window Filter')
        buttonsDict['Window_Filter' + cast].pack(side=LEFT)

        binAverageInputFolder = frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/ASCII_ALL/'
        binAverageInputFolder = binAverageInputFolder.replace('//', '/')
        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/7_Bin_Average/' + cast[:-4]+'.cnv'):
            buttonsDict['BA' + cast] = Button(castFrameDict[cast], text='Bin Average', bg='lightgreen', command=lambda: Ingestion.CTD.bin_average.bin_average_frame(frames_dict['frame'], frames_dict['root2'], mappunavn=binAverageInputFolder))
        else:
            buttonsDict['BA' + cast] = Button(castFrameDict[cast], text='Bin Average', command=lambda: Ingestion.CTD.bin_average.bin_average_frame(frames_dict['frame'], frames_dict['root2'], mappunavn=binAverageInputFolder))
        buttonsDict['BA' + cast].pack(side=LEFT)

        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/ASCII/ASCII_Downcast/' + cast[:-4]+'.asc'):
            buttonsDict['ASCII_out' + cast] = Button(castFrameDict[cast], text='Ascii out', bg='lightgreen')
        else:
            buttonsDict['ASCII_out' + cast] = Button(castFrameDict[cast], text='Ascii out')
        buttonsDict['ASCII_out' + cast].pack(side=LEFT)

        buttonsDict['MakeFigures' + cast] = Button(castFrameDict[cast], text='Ger figurar')
        buttonsDict['MakeFigures' + cast].pack(side=LEFT)

        castsDict['GodskaLabel' + str(cast)] = Label(castFrameDict[cast], text='Góðska:', font=("Courier", 12))
        castsDict['GodskaLabel' + str(cast)].pack(side=LEFT)

        if os.path.exists(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/ASCII/ASCII_Downcast/metadata/' + cast[:-4] + '_metadata.csv'):
            metadataCast = pd.read_csv(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/ASCII/ASCII_Downcast/metadata/' + cast[:-4] + '_metadata.csv', index_col=False)

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


    frames_dict['castFrameDict'] = castFrameDict
    frames_dict['statusFrameBelow'] = Frame(frames_dict['statusFrame'])
    frames_dict['statusFrameBelow'].pack(side=TOP, anchor=W)
    Label(frames_dict['statusFrameBelow'], text='Koyr rokning').pack(side=TOP, anchor=W)

    frames_dict['conv_and_filter_btn'] = Button(frames_dict['statusFrameBelow'], 
                                                text='Rokna Conversion og Filter', 
                                                command=lambda: conv_og_filter(frames_dict), bg='lightgreen', width=30)
    frames_dict['conv_and_filter_btn'].pack(side=TOP, anchor=W)

    frames_dict['statusFrameBelowAlign'] = Frame(frames_dict['statusFrameBelow'])
    frames_dict['statusFrameBelowAlign'].pack(side=TOP, anchor=W)

    meanAlignCTD = 0
    if meanAlignCTDDivideby:
        meanAlignCTD = meanAlignCTDSum/meanAlignCTDDivideby
        frames_dict['AlignCTDLabel'] = Label(frames_dict['statusFrameBelowAlign'], text="{:.2f}".format(meanAlignCTD))
    else:
        frames_dict['AlignCTDLabel'] = Label(frames_dict['statusFrameBelowAlign'], text=str(-1))

    if len(os.listdir(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/RAW/')) == len(os.listdir(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/3_Align_CTD/')):
        frames_dict['AlignCTDButton'] = Button(frames_dict['statusFrameBelowAlign'],
                                               text='Rokna Align CTD',
                                               command=lambda: align_ctd(frames_dict, meanAlignCTD), bg='lightgreen', width=30)
    else:
        frames_dict['AlignCTDButton'] = Button(frames_dict['statusFrameBelowAlign'],
                                               text='Rokna Align CTD',
                                               command=lambda: align_ctd(frames_dict, meanAlignCTD), width=30)
    frames_dict['AlignCTDButton'].pack(side=LEFT)

    Label(frames_dict['statusFrameBelowAlign'], text='Miðal Align CTD virði:').pack(side=LEFT)
    frames_dict['AlignCTDLabel'].pack(side=LEFT)
    
    frames_dict['AlignCTDButton1'] = Button(frames_dict['statusFrameBelow'],
                                            text='Rokna Align CTD við Standard virðum', anchor=W,
                                            command=lambda: align_ctd(frames_dict, 2.5), bg='lightgreen', width=35, )
    frames_dict['AlignCTDButton1'].pack(side=TOP, anchor=W)

    frames_dict['window_filter_btn'] = Button(frames_dict['statusFrameBelow'], 
                                              text='Rokna CTM, Derived og Window filter', anchor=W,
                                              command=lambda: CTM_derived_window(frames_dict), bg='lightgreen', width=35)
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
        # TODO: Um man velur mappu har castini ikki eru í hvør sínari mappu, processera tað allíkavæl
        filnavnorginal = os.listdir(mappunavn + '/' + cast)
        filnavnorginal = filnavnorginal[0]
        filnavn = str(turnummar) + '{:03d}'.format(i + 1)
        # TODO: Flyt ístaðin fyri at kopiera
        copyfile(mappunavn + '/' + cast + '/' + filnavnorginal, './Ingestion/CTD/Lokalt_Data/' + turnummar + '/RAW/' + filnavn + '.xml')

    updatecruseframe(frames_dict)
    updateCastsFrame(frames_dict)

# funkur, ið koyra røttu prossesering  tá túr trýstir á knøttarnar

# Rokna Conversion og Filter
def conv_og_filter(frames_dict):
    for cast in frames_dict['casts']:
        print(cast)
        subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                         "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/1_DatCnv.txt",
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/RAW/' + cast),
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/1_Data_Conversion'),
                         '#m'])
        subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                         "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/2_Filter.txt",
                         str(
                             'Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/1_Data_Conversion/' + cast[:-4]),
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/2_Filter'), '#m'])
        updateCastsFrame(frames_dict)

# Rokna Align CTD
def align_ctd(frames_dict, ox_offset):
    winedir = '/home/' + getpass.getuser() + '/.wine/drive_c/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/'
    copyfile(winedir + 'AlignCTD_(custom)_original.psa', winedir + 'AlignCTD_(custom).psa')
    ikki_funni_linju = True
    with fileinput.FileInput(winedir + 'AlignCTD_(custom).psa', inplace=True) as file:
        for line in file:
            ikki_funni_linju = False
            print(line.replace('-77', str(ox_offset)), end='')

    if ikki_funni_linju:
        messagebox.showerror('Feilur við export', 'Customstart fílur ikki funnin!')
        raise FileNotFoundError('Customstart fílur ikki funnin')

    for cast in frames_dict['casts']:
        print('Input: ' + 'Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/2_Filter/' + cast[:-4])
        subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                         "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/3_Align_CTD_(custom).txt",
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/2_Filter/' + cast[:-4]),
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/3_Align_CTD'), '#m'])
    updateCastsFrame(frames_dict)
    updatecruseframe(frames_dict)

def CTM_derived_window(frames_dict):
    for cast in frames_dict['casts']:
        print(cast)
        subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                         "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/4_CTM.txt",
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/3_Align_CTD/' + cast[:-4]),
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/4_CTM'), '#m'])
        subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                         "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/6_Derive.txt",
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/4_CTM/' + cast[:-4]),
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/5_Derive'), '#m'])
        subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                         "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/7_Window_Filter.txt",
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/5_Derive/' + cast[:-4]),
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/6_Window_Filter'), '#m'])
        subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',  # Eyka - Til alt data
                         "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/9_All_ASCII_Out.txt",
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/6_Window_Filter/' + cast[:-4]),
                         str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/Processed/ASCII_ALL'), '#m'])

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
