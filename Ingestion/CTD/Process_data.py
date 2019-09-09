from tkinter import *
from tkinter import filedialog
from misc.faLog import *
import pandas as pd
import numpy as np
import platform
import os
from shutil import copyfile
import subprocess

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

    processBtn = Button(frame, text='Processera', command=lambda: processera(mappunavn))
    processBtn.pack(side=TOP, anchor=W)

    log_frame = Frame(frame, height=300, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

def velFil():
    global mappunavn
    mappunavn = filedialog.askdirectory(title='Vel túramappu')
    print('Mappa: ' + mappunavn)


def processera(mappunavn):
    log_b()
    turdato = os.path.basename(mappunavn)
    casts = os.listdir(mappunavn)
    print(casts)
    print(turdato)
    print(os.getcwd())
    if not os.path.exists('./Ingestion/CTD/Lokalt_Data/' + turdato + '/'):
        print('Ger lokala mappu')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato)
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/0_RAW_DATA')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/1_Data_Conversion')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/2_Filter')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/3_Align_CTD')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/4_CTM')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/5_Loop_Edit')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/6_Derive')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/7_Window_Filter')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/8_Bin_Average')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/9_ASCII_Out')
        os.mkdir('./Ingestion/CTD/Lokalt_Data/' + turdato + '/75_All_ASCII_Out')

    else:
        print('Lokala mappan er til')

    for cast in casts:
        filnavn = os.listdir(mappunavn + '/' + cast)
        filnavn = filnavn[0]
        copyfile(mappunavn + '/' + cast + '/' + filnavn, './Ingestion/CTD/Lokalt_Data/' + turdato + '/0_RAW_DATA/' + filnavn)
        filnavn = filnavn[:-4]
        print(cast)
        print(filnavn)
        if platform.system() == 'Linux':
            # Hettar riggar bara um wine er og SBE Data processing er installera, og um settings mappan er har hon skal vera
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/1_DatCnv.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/0_RAW_DATA/' + filnavn + '.xml'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/1_Data_Conversion'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/2_Filter.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/1_Data_Conversion/' + filnavn + '.cnv'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/2_Filter'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/3_Align_CTD.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/2_Filter/' + filnavn + '.cnv'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/3_Align_CTD'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/4_CTM.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/3_Align_CTD/' + filnavn + '.cnv'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/4_CTM'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/5_Loop_Edit.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/4_CTM/' + filnavn + '.cnv'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/5_Loop_Edit'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/6_Derive.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/5_Loop_Edit/' + filnavn + '.cnv'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/6_Derive'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/7_Window_Filter.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/6_Derive/' + filnavn + '.cnv'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/7_Window_Filter'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/8_Bin_Average(1m).txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/7_Window_Filter/' + filnavn + '.cnv'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/8_Bin_Average'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/9_ASCII_Out.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/8_Bin_Average/' + filnavn + '.cnv'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/9_ASCII_Out'), '#m'])
            subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe', # Eyka - Til alt data
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/9_ASCII_Out.txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/7_Window_Filter/' + filnavn + '.cnv'),
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/75_All_ASCII_Out'), '#m'])
        else:
            log_w('Koda ikki skriva til hesa stýriskipan')

    log_e()