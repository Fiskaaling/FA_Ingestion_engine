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

    teknaPltBtn = Button(menuFrame, text='Tekna Plot', command=lambda: tekna(fig, canvas, markeraTidvar.get(),
                                                                             fraEntry.get(), tilEntry.get()))
    teknaPltBtn.pack(side=LEFT)
    markeraTidvar = IntVar()
    markeraTid = Checkbutton(menuFrame, text='Markera tíðarinterval', variable=markeraTidvar)
    markeraTid.pack(side=LEFT)

    Label(menuFrame, text='Frá:').pack(side=LEFT)

    fraEntry = Entry(menuFrame, width =3)
    fraEntry.pack(side=LEFT)
    Label(menuFrame, text='Til:').pack(side=LEFT)
    tilEntry = Entry(menuFrame, width=3)
    tilEntry.pack(side=LEFT)

    goymmynd_btn = Button(menuFrame, text='Goym Mynd', command=lambda: goymmynd(fig, canvas)).pack(side=LEFT)

    fig = Figure(figsize=(12, 8), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)


def velFil():
    global filnavn
    filnavn = filedialog.askopenfile(title='Vel fíl', filetypes = (("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    print(filnavn)

def tekna(fig, canvas, tekna, fra, til):
    fig.clf()
    ax = fig.add_subplot(111)
    data = pd.read_csv(filnavn)
    for i in range(len(data.columns)):
        ax.plot(data[data.columns[i]])
    ax.set_ylim(0, 5)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    print('done')

def goymmynd(fig, canvas):
    filnavn = filedialog.asksaveasfilename(parent=root, title="Goym mynd",  filetypes=(("png Fílur", "*.png"), ("jpg Fílur", "*.jpg")))
    print('Goymir mynd')
    fig.savefig(filnavn, dpi=1200, bbox_inches='tight')
    print('Liðugt')