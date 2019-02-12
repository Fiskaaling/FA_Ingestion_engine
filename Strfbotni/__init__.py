from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def vedurstodirPlt(frame, root2):
    global root
    global filnavn
    filnavn = '/home/johannus/Documents/FA_Ingestion_engine/Kort_Data/Syðradalur.txt'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Streymmátinar frá botni', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Streymmátinar frá botni').pack(side=TOP, anchor=W)

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

    fig = Figure(figsize=(8, 12), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)