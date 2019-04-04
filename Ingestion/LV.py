from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as md
import datetime as dt


def vedurstodirPlt(frame, root2):
    global root
    global filnavn
    filnavn = '/home/johannus/Documents/FA_Ingestion_engine/Kort_Data/Syðradalur.txt'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Landsverk', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Veðurstøðir').pack(side=TOP, anchor=W)

    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    velMappuBtn = Button(menuFrame, text='Vel Fíl', command=lambda: velFil())
    velMappuBtn.pack(side=LEFT)

    teknaPltBtn = Button(menuFrame, text='Tekna Plot', command=lambda: tekna(fig, canvas, markeraTidvar.get(),
                                                                             fraEntry.get(), tilEntry.get(),
                                                                             ylimEntry.get()))
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
    Label(menuFrame, text='Ylim:').pack(side=LEFT)
    ylimEntry = Entry(menuFrame, width=3)
    ylimEntry.pack(side=LEFT)
    ylimEntry.insert(0, '15')

    Label(menuFrame, text='DPI:').pack(side=LEFT)
    dpiEntry = Entry(menuFrame, width=3)
    dpiEntry.pack(side=LEFT)
    dpiEntry.insert(0, '300')
    goymmynd_btn = Button(menuFrame, text='Goym Mynd', command=lambda: goymmynd(fig, canvas, dpiEntry.get())).pack(side=LEFT)

    fig = Figure(figsize=(12, 8), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)


def velFil():
    global filnavn
    filnavn = filedialog.askopenfile(title='Vel fíl', filetypes = (("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    print(filnavn)

def tekna(fig, canvas, tekna, fra, til, ylim):
    fig.clf()
    ax = fig.add_subplot(111)
    print(tekna)
    #ax = plt.gca()
    data = pd.read_csv(filnavn, sep='\t')
    if tekna:
        print('markeraokid')
        farvaHer = np.zeros((len(data), 1))
        farts = []
        for i in range(len(data)):
            fra = int(fra)
            til = int(til)
            if (i > fra) and (i < til):
                farvaHer[i] = 1
                farts.append(True)
            else:
                farts.append(False)
    #fig, ax = plt.subplots()
    #fig.set_size_inches(9, 6)
    #plt.figure(figsize=(9, 6))
    #ax.figsize((9, 6))

    #xax = data['Date and time   ']
    xax = [md.date2num(dt.datetime.strptime(x,'%Y-%m-%d %H:%M:%S')) for x in data['Date and time   '].values]

    #xaxc = xax
    #for i in range(len(xax)-1, -1, -1):
    #    if i%10 == 0:
    #        print(i)
    #    else:
    #        del xaxc[i]
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_formatter(md.DateFormatter('%d. %b %H:%M'))
    fig.autofmt_xdate()
    ax.plot(xax, data['wind_mean1'], label='Miðal vindur')
    ax.plot(xax, data['gust2'], label='Hvirla')
    #ax.set_xticklabels(xax, rotation=40)
    #plt.xticks(np.linspace(0, len(data), 10), rotation='vertical')
    if tekna:
        ax.fill_between(xax, -100, 100, where=farts, facecolor='green', alpha=0.2)
    ax.set_ylim(0, int(ylim))
    ax.legend()
    fig.savefig('tmp.png',bbox_inches='tight')
    #plt.legend()
    #plt.savefig('Figures/test.png', bbox_inches='tight')
    #plt.show()
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    print('done')

def goymmynd(fig, canvas, dpisetting):
    filnavn = filedialog.asksaveasfilename(parent=root, title="Goym mynd",  filetypes=(("pdf Fílur", "*.pdf"), ("png Fílur", "*.png"), ("jpg Fílur", "*.jpg")))
    print('Goymir mynd')
    fig.savefig(filnavn, dpi=int(dpisetting), bbox_inches='tight')
    print('Liðugt')