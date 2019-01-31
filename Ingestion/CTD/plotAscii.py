from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.dates as md
import datetime as dt


def asciiPlt(frame, root2):
    global root
    global filnavn
    filnavn = ''
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Plot Ascii').pack(side=TOP, anchor=W)

    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    velMappuBtn = Button(menuFrame, text='Vel Fíl', command=lambda: velFil())
    velMappuBtn.pack(side=LEFT)

    teknaPltBtn = Button(menuFrame, text='Tekna Plot', command=lambda: tekna(fig, canvas, indexEntry.get()))
    teknaPltBtn.pack(side=LEFT)
    markeraTidvar = IntVar()
    markeraTid = Checkbutton(menuFrame, text='Markera tíðarinterval', variable=markeraTidvar)
    markeraTid.pack(side=LEFT)

    Label(menuFrame, text='Index:').pack(side=LEFT)

    indexEntry = Entry(menuFrame, width =3)
    indexEntry.pack(side=LEFT)

    goymmynd_btn = Button(menuFrame, text='Goym Mynd', command=lambda: goymmynd(fig, canvas)).pack(side=LEFT)

    fig = Figure(figsize=(12, 8), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)


def velFil():
    global filnavn
    filnavn = filedialog.askopenfile(title='Vel fíl', filetypes = (("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    print(filnavn)

def tekna(fig, canvas, index):
    fig.clf()
    ax = fig.subplots()
    a = int(index)
    #ax = fig.add_subplot(111)
    plt.subplot()
    data = pd.read_csv(filnavn, encoding='latin-1')
    ax.plot(-data[data.columns[0]], 'k')
    ax.set_xlabel('Tíð [?]')
    ax.set_ylabel('Dýpið', color='k')
    ax2 = ax.twinx()
    ax2.plot(data[data.columns[a]], 'b')
    ax2.tick_params('y', colors='b')
    ax2.set_ylabel(data.columns[a], color='b')
    #for i in range(len(data.columns)):
    #ax.set_ylim(0, 5)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    print('done')

def goymmynd(fig, canvas):
    filnavn = filedialog.asksaveasfilename(parent=root, title="Goym mynd",  filetypes=(("pdf Fílur", "*.pdf"), ("png Fílur", "*.png")))
    print('Goymir mynd')
    fig.savefig(filnavn, dpi=600, bbox_inches='tight')
    print('Liðugt')