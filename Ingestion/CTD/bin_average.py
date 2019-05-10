from tkinter import *
from tkinter import filedialog
from misc.faLog import *
import pandas as pd
import numpy as np
import platform
import os
from shutil import copyfile
import subprocess
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def bin_average_frame(frame, root2):
    global root
    global mappunavn
    filnavn = ''
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Bin Average').pack(side=TOP, anchor=W)
    controlsFrame = Frame(frame)
    controlsFrame.pack(side=TOP, anchor=W)
    velMappuBtn = Button(controlsFrame, text='Vel Fílir', command=lambda: velFil())
    velMappuBtn.pack(side=LEFT, anchor=W)

    processBtn = Button(controlsFrame, text='Processera', command=lambda: processera(mappunavn, fig, canvas))
    processBtn.pack(side=LEFT, anchor=W)

    fig = Figure(figsize=(12, 8), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)

def velFil():
    global mappunavn
    mappunavn = filedialog.askdirectory(title='Vel túramappu', initialdir='./Ingestion/CTD/Lokalt_Data')

def processera(mappunavn, fig, canvas):
    fig.clf()
    ax = fig.subplots()
    filnavn = os.listdir(mappunavn)
    data = pd.read_csv(mappunavn + '/' + filnavn[1], encoding='latin-1')
    ax.plot(-data[data.columns[0]])
    ax.set_xlabel('Tíð [?]')
    ax.set_ylabel('Dýpið', color='k')
    ax2 = ax.twinx()
    ax2.plot(np.diff(data[data.columns[0]]), 'b')
    ax2.set_ylim([-0.2, 0.2])
    ax2.tick_params('y', colors='b')
    #ax2.set_ylabel(data.columns[1], color='b')
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)