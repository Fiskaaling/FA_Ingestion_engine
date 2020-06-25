import os
import platform
import subprocess
from shutil import copyfile
from tkinter import filedialog

from misc.faLog import *


def process_CTD_Data(frame, root2):
    global root
    global mappunavn
    filnavn = ''
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Processera data').pack(side=TOP, anchor=W)

    velMappuBtn = Button(frame, text='Vel Fílir', command=lambda: velFil())
    velMappuBtn.pack(side=TOP, anchor=W)

    processBtn = Button(frame, text='Processera', command=lambda: processera(mappunavn, int(turnummar.get())))
    processBtn.pack(side=TOP, anchor=W)

    Label(frame, text='Túrnummar:').pack(side=TOP, anchor=W)

    turnummar = Entry(frame, width=10)
    turnummar.pack(side=TOP, anchor=W)

    log_frame = Frame(frame, height=300, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)


def velFil():
    global mappunavn
    mappunavn = filedialog.askdirectory(title='Vel túramappu')
    print('Mappa: ' + mappunavn)


def processera(mappunavn, turnummar):
    log_b()
    turdato = os.path.basename(mappunavn)
    casts = os.listdir(mappunavn)
    print(casts)
    print(turdato)
    print(os.getcwd())
    if not os.path.exists('./Ingestion/CTD/Lokalt_Data/' + turdato + '/'):
        print('Ger lokala mappu')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato)
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/RAW')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/1_Data_Conversion')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/2_Filter')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/3_Align_CTD')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/4_CTM')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/5_Derive')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/6_Window_Filter')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/ASCII_ALL')

    else:
        print('Lokala mappan er til')
    casts.sort()
    for i, cast in enumerate(casts):
        # TODO: Um man velur mappu har castini ikki eru í hvør sínari mappu, processera tað allíkavæl
        filnavnorginal = os.listdir(mappunavn + '/' + cast)
        filnavnorginal = filnavnorginal[0]
        filnavn = str(turnummar) + '{:03d}'.format(i + 1)
        # TODO: Flyt ístaðin fyri at kopiera
        copyfile(mappunavn + '/' + cast + '/' + filnavnorginal, './Ingestion/CTD/Lokalt_Data/' + turdato + '/RAW/' + filnavn + '.xml')
        print(cast)
        print(filnavn)
        if platform.system() == 'Linux':
            # hey hey
            # Hettar riggar bara um wine er og SBE Data processing er installera, og um settings mappan er har hon skal vera
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/1_DatCnv.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/RAW/' + filnavn + '.xml'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/1_Data_Conversion'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/2_Filter.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/1_Data_Conversion/' + filnavn),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/2_Filter'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/3_Align_CTD.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/2_Filter/' + filnavn),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/3_Align_CTD'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/4_CTM.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/3_Align_CTD/' + filnavn),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/4_CTM'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/6_Derive.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/4_CTM/' + filnavn),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/5_Derive'), '#m'])

            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/7_Window_Filter.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/5_Derive/' + filnavn),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/6_Window_Filter'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',  # Eyka - Til alt data
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/9_All_ASCII_Out.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/6_Window_Filter/' + filnavn),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/ASCII_ALL'), '#m'])
        else:
            log_w('Koda ikki skriva til hesa stýriskipan')

    log_e()
