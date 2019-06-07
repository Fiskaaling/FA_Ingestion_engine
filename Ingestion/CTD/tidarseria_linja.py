from tkinter import *
from tkinter import filedialog
from misc.faLog import *
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.dates as md

def CTDtidarseria_lin(frame, root2):
    global root
    global mappunavn
    mappunavn = '/home/johannus/Documents/data/SUN_timeseries'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Linjuplot tiðarseria').pack(side=TOP, anchor=W)

    controls_Frame = Frame(frame)
    controls_Frame.pack(side=TOP, anchor=W)

    velMappuBtn = Button(controls_Frame, text='Vel Fílir', command=lambda: velFil())
    velMappuBtn.pack(side=LEFT, anchor=N)

    processBtn = Button(controls_Frame, text='Processera', command=lambda: tekna(fig, canvas, mappunavn, int(stodEntry.get())))
    processBtn.pack(side=LEFT, anchor=N)

    Label(controls_Frame, text='Støð:').pack(side=LEFT)
    stodEntry = Entry(controls_Frame, width=3)
    stodEntry.pack(side=LEFT)
    stodEntry.insert(0, '0')

    Label(controls_Frame, text='DPI:').pack(side=LEFT)
    dpiEntry = Entry(controls_Frame, width=3)
    dpiEntry.pack(side=LEFT)
    dpiEntry.insert(0, '300')
    Button(controls_Frame, text='Goym Mynd', command=lambda: goymmynd(fig, canvas, dpiEntry.get())).pack(side=RIGHT)


    fig = Figure(figsize=(12, 8), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)

    log_frame = Frame(frame, height=300, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

def velFil():
    global mappunavn
    mappunavn = filedialog.askdirectory(title='Vel túramappu')
    print('Mappa: ' + mappunavn)


def tekna(fig, canvas, mappunavn, valdstod):
    fig.clf()
    log_clear()
    ax = fig.subplots()
    turar = os.listdir(mappunavn)
    stodir = ['SUN 22', 'SUN 32', 'SUN 12', 'SUN 33', 'SUN 34', 'SUN 03', 'SUN 35', 'SUN 36', 'SUN 37']
    #dypir = [20, 40, -1]
    dypir = [30, 50, -1]
    for dypi in dypir:
        print(dypi)
        datapoints = []
        dates = []
        for tur in turar:
            print(tur)
            turnummar = tur[3:]
            stodfil = pd.read_csv(mappunavn + '/' + tur + '/stodfil' + turnummar + '.csv', skiprows=14)
            stodnames = stodfil.stodname
            ctd_filnames = stodfil.CTD_file
            ascii_filnavn = ''
            for i, stodnavn in enumerate(stodnames):
                if stodnavn == stodir[valdstod]:
                    ascii_filnavn = ctd_filnames[i]
            if ascii_filnavn == '':
                log_w('Fann ongan fíl til ' + str(tur))
            else:
                # Dato
                hydrfil = pd.read_csv(mappunavn + '/' + tur + '/hydr' + turnummar + '.dat')
                if '-' in hydrfil.iloc[0, 10]:
                    dates.append(md.date2num(datetime.strptime(hydrfil.iloc[0, 10], '%d-%m-%Y')))
                else:
                    dates.append(md.date2num(datetime.strptime(hydrfil.iloc[0, 10], '%d/%m/%y')))
                # Data
                data = pd.read_csv(mappunavn + '/' + tur + '/ascii/' + str(ascii_filnavn) + '.asc', encoding='latin')
                #ox_mgl = data['Sbeox0Mg/L'] # Sbeox0Mg/L

                #ox_mgl = data['Sbeox0PS']
                ox_mgl = data['T068C']
                depth = data['DepSM']
                if dypi > max(depth):
                    log_w(tur + ' Max dypi ' + str(max(depth)) + ' er minni enn ' + str(dypi) + ' m')
                if dypi == -1:
                    datapoints.append(ox_mgl[len(ox_mgl) - 1])
                else:
                    for d_index, d in enumerate(depth):
                        if np.round(d) >= np.round(dypi):
                            datapoints.append(ox_mgl[d_index])
                            break
        ax.set_title(stodir[valdstod])
        try:
            dates, datapoints = zip(*sorted(zip(dates, datapoints)))
            if dypi == -1:
                ax.plot(dates, datapoints, label='1 m frá botni')
            else:
                ax.plot(dates, datapoints, label=str(dypi) + ' m')
        except ValueError:
            log_w('Datapunkt mangla')
        dates_string = []
        for index in range(len(dates)):
            dates_string.append(datetime.strftime(md.num2date(dates[index]), '%d-%m-%Y'))
        pandas_dataframe = pd.DataFrame({'dato': dates_string, 'virdi': datapoints})

        pandas_dataframe.to_csv('temp' +str(dypi) + ' ' + stodir[valdstod] + '.csv')
        ax.legend()
        ax.set_xticks(dates)
        ax.set(ylabel='Hiti [C]')
        #ax.set(ylabel='Oxygen [mg/l]')
        ax.set_title(stodir[valdstod])
        ax.set_xlim(min(dates), max(dates))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        #ax.set_xticks(rotation=70)
        ax.xaxis.set_major_formatter(md.DateFormatter('%d/%m/%y'))
        ax.grid(linestyle='-', color = '222222')
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    pass

def goymmynd(fig, canvas, dpisetting):
    filnavn = filedialog.asksaveasfilename(parent=root, title="Goym mynd",  filetypes=(("pdf Fílur", "*.pdf"), ("png Fílur", "*.png"), ("jpg Fílur", "*.jpg")))
    print('Goymir mynd')
    fig.savefig(filnavn, dpi=int(dpisetting), bbox_inches='tight')
    print('Liðugt')