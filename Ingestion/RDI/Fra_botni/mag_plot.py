from tkinter import filedialog
from misc.faLog import *
import pandas as pd
import numpy as np
import matplotlib.dates as md
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def mag_plot(frame, root2):
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='RDI Streymmátari', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Magnitude plot').pack(side=TOP, anchor=W)
    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    Button(menuFrame, text='Vel Fíl', command=vel_fil).pack(side=LEFT)
    Button(menuFrame, text='Tekna', command=lambda: rokna(canvas, ax)).pack(side=LEFT)
    Button(menuFrame, text='CLF', command=lambda: clear_figur(canvas)).pack(side=RIGHT)
    Button(menuFrame, text='Goym mynd', command=lambda: goymmynd(fig)).pack(side=RIGHT)
    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root2)

    plot_frame = Frame(frame)
    plot_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    global fig
    fig = Figure(figsize=(8, 16), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    fig.clf()
    ax = fig.add_subplot(111)
    #ax.axis('equal')
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)

def rokna(canvas, ax):
    print('hello')
    log_b()
    df = pd.read_csv(RDI_filnavn, skiprows=11, sep='\t', index_col=0, decimal=",")
    print(df.columns.values)
    ar = np.array(df['YR'])
    mdr = np.array(df['MO'])
    dag = np.array(df['DA'])
    h = np.array(df['HH'])
    m = np.array(df['MM'])
    print(len(ar))
    date = np.zeros((len(ar)))
    for i in range(len(ar)):
        try:
            date[i] = md.date2num(datetime.strptime(
                str(ar[i]) + '.' + str(mdr[i]) + '.' + str(dag[i]) + '.' + str(h[i]) + '.' + str(m[i]),
                '%y.%m.%d.%H.%M'))
        except Exception as e:
            print('Dugi ikki ' + str(i))
            print(str(ar[i]) + '.' + str(mdr[i]) + '.' + str(dag[i]) + '.')
            print(str(h[i]) + '.' + str(m[i]))
            print(e)
    print(date)
    n_bins = len(df.columns.values)-8
    print(n_bins)
    mean_current = []
    minrange = 10226
    maxrange = 10369
    for i in range(minrange, maxrange):
        tmp_current = 0
        n_currents = 0
        for bin in range(n_bins):
            try:
                tmp_current += df.iloc[i, bin+8]
            except Exception as e:
                print(e)
            else:
                n_currents += 1
        if n_currents:
            mean_current.append(tmp_current / n_currents)
        else:
            mean_current.append(0)
    data = pd.DataFrame(mean_current)
    data.to_csv('test.csv')
    #diff = moving_average(abs(np.diff(mean_current)), 30)
    diff = abs(np.diff(mean_current))*2

    ax.plot(date[minrange:maxrange], mean_current)
    #ax.plot(moving_average(mean_current, 50))
    ax.plot(date[minrange+1:maxrange], diff)
    ax.set_ylim(0, 600)
    ax.xaxis.set_major_formatter(md.DateFormatter('%d. %b %H:%M'))
    ax.set_xlabel('Dato')
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    log_e()

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def vel_fil():
    global RDI_filnavn
    RDI_filnavn = filedialog.askopenfile(title='Vel RDI fíl', filetypes=(("txt Fílir", "*.txt"), ("csv Fílir", "*.csv"),
                                                                 ("all files", "*.*"))).name

def clear_figur(canvas):
    print('Slettar mynd')
    global fig
    fig.clf()
    fig.add_subplot(111)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    if 'levels' in globals():
        global levels
        del levels

def goymmynd(fig):
    log_b()
    filnavn = filedialog.asksaveasfilename(title="Goym mynd",
                                           filetypes=(("png Fílur", "*.png"), ("jpg Fílur", "*.jpg")))
    print('Goymir mynd')
    fig.savefig(filnavn, dpi=600, bbox_inches='tight')
    print('Liðugt')
    log_e()
