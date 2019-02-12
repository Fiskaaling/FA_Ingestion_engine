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

def load(frame, root2):
    global root
    global filnavn
    global loada
    loada = ''
    filnavn = '../data/depth.txt'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Vatnstoduanalysa', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='títtir').pack(side=TOP, anchor=W)

    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    velMappuBtn = Button(menuFrame, text='Vel Fíl', command=lambda: velFil())
    velMappuBtn.pack(side=LEFT)

    teknatiddirPltBtn = Button(menuFrame, text='Tekna tiddir', command=lambda: teknatiddir(fig, canvas, latEntry.get()))
    teknatiddirPltBtn.pack(side=LEFT)

    Label(menuFrame, text='lat:').pack(side=LEFT)

    latEntry = Entry(menuFrame, width=3)
    latEntry.pack(side=LEFT)
    latEntry.delete(0, END)
    latEntry.insert(0, 62)

    Button(menuFrame, text='Tekna Feilin', command=lambda: teknafeil(fig, canvas)).pack(side=LEFT)
    Button(menuFrame, text='goym', command=lambda: goymcsv('')).pack(side=LEFT)

    fig = Figure(figsize=(12, 8), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)


def inles(file):
    Dep = pd.read_csv(file, skiprows=16, sep='\t', index_col=0, decimal=",",
                  names=['Y', 'm', 'd', 'H', 'M', 'S', '0', '1', 'Dep'])
    Dep = Dep[Dep['Dep'] > 10]
    Dep.reset_index(inplace=True, drop=True)
    time = []
    for i in range(len(Dep)):
        time.append(mdate.date2num(dt.datetime(Dep['Y'][i] + 2000, Dep['m'][i], Dep['d'][i], Dep['H'][i], Dep['M'][i], Dep['S'][i])))
    Dep['dato'] = time

    return Dep[Dep['dato'] > Dep['dato'][0]+1/24][['dato', 'Dep']]

def velFil():
    global filnavn
    filnavn = filedialog.askopenfile(title='Vel fíl', filetypes = (("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    print(filnavn)

def teknatiddir(fig, canvas, lat):
    global filnavn
    global loada
    global coef
    global data
    fig.clf()
    ax = fig.add_subplot(111)
    if loada != filnavn:
        loada = filnavn
        data = inles(filnavn)
        coef = utide.solve(data['dato'], data['Dep'], lat=float(lat), conf_int='MC', method='ols')
    ax.bar(coef.name, coef.A)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)

def teknafeil(fig, canvas):
    fig.clf()
    ax = fig.add_subplot(111)
    tide = utide.reconstruct(data['dato'], coef)
    ax.plot(data['dato'], data['Dep'] - tide.h)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)


def goymcsv(filnavn2):
    if filnavn2 == '':
        filnavn2 = filedialog.asksaveasfilename(parent=root, title="Goym mynd",  filetypes=(("csv Fílur", "*.csv"), ("all files", "*.*")))
    pd.DataFrame({'Navn': coef.name, 'frq [CPH]': coef.aux.frq, 'A': coef.A}).to_csv(filnavn2, index=False)
