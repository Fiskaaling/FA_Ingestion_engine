import fileinput
import getpass  # Til at fáa brúkaranavn
import os
import subprocess
from tkinter import *
from tkinter import filedialog

import matplotlib
import numpy as np
import pandas as pd

from misc.faLog import gerlog, log_e, log_b, log_print, log_w, log_clear

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
from shutil import copyfile

def cruise_overview_frame(frame, root2):
    mappunavn = './Ingestion/CTD/Lokalt_Data/'
    frames_dict = {'mappunavn': mappunavn}
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)

    controlsFrame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    controlsFrame.pack(side=TOP)

    Button(controlsFrame, text='Stovna Túr', command=lambda: velFilir('.txt')).pack(side=LEFT)


    frames_dict['cruiseFrame'] = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    frames_dict['cruiseFrame'].pack(side=LEFT, anchor=W, expand=True, fill=BOTH)

    frames_dict['castFrame'] = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    frames_dict['castFrame'].pack(side=LEFT, anchor=W, expand=True, fill=BOTH)

    frames_dict['statusFrame'] = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    frames_dict['statusFrame'].pack(side=LEFT, anchor=W, expand=True, fill=BOTH)

    frames_dict['selectedFrame'] = 0
    frames_dict['selectedCruse'] = 0
    frames_dict['selectedCast'] = 0

    updateCruseFrame(frames_dict)

    def key(event):
        print(len(frames_dict['cruises']))
        print(frames_dict['selectedCruse'])
        if frames_dict['selectedFrame'] == 0:
            if event.keysym == 'Up':
                if (frames_dict['selectedCruse'] - 1) >= 0:
                    frames_dict['selectedCruse'] -= 1
                    updateCruseFrame(frames_dict)
            if event.keysym == 'Down':
                if frames_dict['selectedCruse'] + 1 < len(frames_dict['cruises']):
                    frames_dict['selectedCruse'] += 1
                    updateCruseFrame(frames_dict)
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
    for widget in frames_dict['castFrame'].winfo_children(): # Tømur quality frame
        widget.destroy()
    Label(frames_dict['castFrame'], text='Cast', font=("Courier", 14)).pack(side=TOP)
    print(frames_dict['mappunavn'] + frames_dict['cruises'][frames_dict['selectedCruse']])
    print(frames_dict['mappunavn'])

    frames_dict['casts'] = os.listdir(frames_dict['mappunavn'] + '/' + frames_dict['cruises'][frames_dict['selectedCruse']] + '/RAW/')
    frames_dict['casts'].sort()
    castsDict = {}
    for i, cast in enumerate(frames_dict['casts']):
        if i == frames_dict['selectedCast']:
            castsDict[str(cast)] = Label(frames_dict['castFrame'], text=cast, font=("Courier", 12, 'underline'))
        else:
            castsDict[str(cast)] = Label(frames_dict['castFrame'], text=cast, font=("Courier", 12))
        castsDict[str(cast)].pack(side=TOP)
    print('Eg eri her!')


def updateCruseFrame(frames_dict):
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
