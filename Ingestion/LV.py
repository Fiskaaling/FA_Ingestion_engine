from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


def vedurstodirPlt(frame, root2):
    global root
    global filnavn
    filnavn = '/home/johannus/Documents/FA_Ingestion_engine/Kort_Data/Syðradalur.txt'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Landsverk', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Veðurstøðir').pack(side=TOP, anchor=W)
    velMappuBtn = Button(frame, text='Vel Fíl', command=lambda: velFil())
    velMappuBtn.pack(side=TOP, anchor=W)

    teknaPltBtn = Button(frame, text='Tekna Plot', command=lambda: tekna(fig, canvas))
    teknaPltBtn.pack(side=TOP, anchor=W)

    fig = Figure(figsize=(8, 12), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)


def velFil():
    global filnavn
    filnavn = filedialog.askopenfile(title='Vel fíl', filetypes = (("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    print(filnavn)

def tekna(fig, canvas):
    fig.clf()
    #ax = fig.add_subplot(111)
    ax = plt.gca()
    data = pd.read_csv(filnavn, sep='\t')
    print(data)
    print(data.columns.values)

    farvaHer = np.zeros((len(data), 1))
    farts = []
    for i in range(len(data)):
        if (i > 115) and (i < 175):
            farvaHer[i] = 1
            farts.append(True)
        else:
            farts.append(False)
    #fig, ax = plt.subplots()
    #fig.set_size_inches(9, 6)
    #plt.figure(figsize=(9, 6))
    #ax.figsize((9, 6))
    xax = data['Date and time   ']
    plt.plot(xax, data['wind_mean1'], label='Miðal vindur')
    plt.plot(xax, data['gust2'], label='Hvirla')

    plt.xticks(np.linspace(0, len(data), 10), rotation='vertical')
    #ax.fill_between(xax, -100, 100, where=farts, facecolor='green', alpha=0.5)
    plt.ylim(0, 15)
    plt.legend()
    #plt.savefig('Figures/test.png', bbox_inches='tight')
    #plt.show()

    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    print('done')