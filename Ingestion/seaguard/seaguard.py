from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdate
import datetime as dt
import utide
import misc.sker_endar as sker


'''
minst til at fáa hettar uppa plass og bruka misc.sker_endar
'''



def load(frame, root2):
    global root
    global filnavn
    global loada
    global options
    global dropdown
    options = ['Battery Voltage', 'Memory Used',
       'Last Interval', 'Time Correction', 'Turbidity', 'Abs Speed',
       'Direction', 'North', 'East', 'Heading', 'Tilt X', 'Tilt Y', 'SP Std',
       'Strength', 'Ping Count', 'Abs Tilt', 'Max Tilt', 'Std Tilt',
       'Conductivity', 'Temperature', 'Pressure', 'Temperature.1',
       'Tide Pressure', 'Tide Level', 'O2Concentration', 'AirSaturation',
       'Temperature.2', 'Depth', 'Salinity', 'Speed of Sound', 'Density',
       'Pressure.1', 'Temperature.3', 'Conductivity.1', 'Latitude',
       'Air Pressure']
    loada = ''
    filnavn = '../data/SUNE1801.txt'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seaguard', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='seaguard').pack(side=TOP, anchor=W)

    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    Button(menuFrame, text='Vel Fíl', command=lambda: velFil()).pack(side=LEFT)

    Button(menuFrame, text='Tekna',
                               command=lambda: teknatiddir(fig, canvas, dropdown.get())).pack(side=LEFT)


    dropdown = StringVar()
    dropdown.set(options[0])
    OptionMenu(menuFrame, dropdown, *options).pack(side=LEFT)


    fig = Figure(figsize=(12, 8), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)


def inles(file):
    global Data
    global options
    global dropdown
    Data = pd.read_csv(file, skiprows=1, sep='\t', index_col=0)
    m, M = sker.Seaguardcut(Data)
    Data = Data[m:M].reset_index(drop=True)
    Data['Time tag (Gmt)'] = \
        [mdate.date2num(dt.datetime.strptime(x, '%d.%m.%y %H:%M:%S')) for x in Data['Time tag (Gmt)'].values]
    temp = Data['Time tag (Gmt)'][0]
    for m in range(len(Data)):
        if temp + 1/12 < Data['Time tag (Gmt)'][m]:
            break
    temp = Data['Time tag (Gmt)'].values[-1]
    for M in range(len(Data)-1, -1, -1):
        if temp + 1/12 > Data['Time tag (Gmt)'][M]:
            break
    Data = Data[m:M]

def velFil():
    global loada
    global filnavn
    filnavn = filedialog.askopenfile(title='Vel fíl', filetypes = (("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    if filnavn != loada:
        inles(filnavn)
        loada = filnavn

def teknatiddir(fig, canvas, y):
    global Data
    fig.clf()
    ax = fig.add_subplot(111)

    ax.plot(Data['Time tag (Gmt)'], Data[y])
    fig.autofmt_xdate()

    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
