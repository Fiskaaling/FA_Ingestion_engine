from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np

def roknaQuiver(frame, root2):
    global root
    root = root2
    global mappunavn
    mappunavn = '/home/johannus/Documents/data/Streymmátingar/Hov/DATA_EXTRACTED'
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Streymmátingar', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Rokna Quiver Data').pack(side=TOP, anchor=W)

    velMappuBtn = Button(frame, text='Vel Mappu', command=lambda: velMappu())
    velMappuBtn.pack(side=TOP, anchor=W)

    Label(frame, text='').pack(side=TOP)
    tilFraFrame = Frame(frame)
    tilFraFrame.pack(side=TOP, anchor=W, expand=False, fill=Y)
    Label(tilFraFrame, text='Frá túr index').pack(side=LEFT)
    fraIndex = Entry(tilFraFrame, width=2)
    fraIndex.pack(side=LEFT)
    fraIndex.insert(0,'1')
    Label(tilFraFrame, text='Til túr index').pack(side=LEFT)
    tilIndex = Entry(tilFraFrame, width=2)
    tilIndex.pack(side=LEFT)
    tilIndex.insert(0, '13')

    Label(frame, text='').pack(side=TOP, anchor=W)

    punktPerPilFrame = Frame(frame)
    punktPerPilFrame.pack(side=TOP, anchor=W, expand=False, fill=Y)
    Label(punktPerPilFrame, text='Tal av punktum per píl ').pack(side=LEFT)
    punktPerPilEntry = Entry(punktPerPilFrame, width=3)
    punktPerPilEntry.pack(side=LEFT)
    punktPerPilEntry.insert(0, '30')

    Label(frame, text='').pack(side=TOP, anchor=W)

    binSettingsFrame = Frame(frame)
    binSettingsFrame.pack(side=TOP, anchor=W, expand=False, fill=Y)
    Label(binSettingsFrame, text='Bins at rokna miðal frá ').pack(side=LEFT)
    bins = Entry(binSettingsFrame, width=60)
    bins.pack(side=LEFT)
    bins.insert(0, '9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19')

    Label(frame, text='').pack(side=TOP, anchor=W)

    skipFrame = Frame(frame)
    skipFrame.pack(side=TOP, anchor=W, expand=False, fill=Y)
    Label(skipFrame, text='Leyp um ensembles við byŕjan ').pack(side=LEFT)
    skipEntry =Entry(skipFrame, width=50)
    skipEntry.pack(side=LEFT)
    skipEntry.insert(0, '0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0')
    Label(frame, text='').pack(side=TOP, anchor=W)


    roknaBtn = Button(frame, text='Rokna', command=lambda: rokna(int(fraIndex.get()), int(tilIndex.get()),
                      int(punktPerPilEntry.get()), [int(s) for s in bins.get().split(',')],
                                                                 [int(s) for s in skipEntry.get().split(',')]))
    roknaBtn.pack(side=TOP, anchor=W)

    Label(frame, text='').pack(side=TOP, anchor=W)
    teknaKortBtn = Button(frame, text='Tekna Kort')
    teknaKortBtn.pack(side=TOP, anchor=W)

    log_frame = Frame(frame, height=300, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)

    global log
    log = Text(log_frame, bg='#888888')
    log.pack(fill=X, expand=True)
    log.insert(1.0, 'Klárt\n')
    log.tag_add('fystalinja', '1.0', '2.0')
    log.tag_config('fystalinja', foreground='white', background='green')
    log.config(state=DISABLED)

def velMappu():
    global mappunavn
    mappunavn = filedialog.askdirectory(title='Vel mappu')
    print(mappunavn)

def print(text):
    log.config(state=NORMAL)
    log.insert(2.0, str(text) + '\n')
    root.update()
    log.config(state=DISABLED)


def rokna(fra, til, punktPerPil, bins, skip):
    log.config(state=NORMAL)
    log.delete(1.0, 2.0)
    log.insert(1.0, 'Arbeðir\n')
    log.tag_add('fystalinja', '1.0', '2.0')
    log.tag_config('fystalinja', foreground='white', background='red')
    root.update()
    n_trips = len(range(fra, til+1))
    for trip_index in range(0, n_trips):
        print('Lesur fíl :' + str(trip_index+1) + '_nav.txt')
        df_nav = pd.read_csv(mappunavn + '/' + str(trip_index+1) + '_nav.txt', skiprows=16, sep='\t', index_col=0,
                             decimal=",")
        df_u = pd.read_csv(mappunavn + '/' + str(trip_index+1) + '_u.txt', skiprows=16, sep='\t', index_col=0, decimal=",")
        df_v = pd.read_csv(mappunavn + '/' + str(trip_index+1) + '_v.txt', skiprows=16, sep='\t', index_col=0, decimal=",")
        n_ensembles = len(df_u.iloc[:, 1])
        n_arrows = int(np.floor((n_ensembles - skip[trip_index]) / punktPerPil))
        print('tal av pílum:' + str(n_arrows))
        mean_u = np.zeros((n_trips, n_arrows))
        mean_v = np.zeros((n_trips, n_arrows))
        lon = []
        lat = []
        for arrow_index in range(n_arrows):
            lon.append(df_nav.iloc[skip[trip_index] + arrow_index * punktPerPil, 11])
            lat.append(df_nav.iloc[skip[trip_index] + arrow_index * punktPerPil, 10])
            tmp_u = 0
            tmp_v = 0
            divideby = 0
            for bin_index in range(len(bins)):
                for ensemble_index in range(punktPerPil):
                    if not np.isnan(df_u.iloc[skip[trip_index] + ensemble_index + punktPerPil * arrow_index,
                                              bins[bin_index]]):
                        divideby += 1
                        tmp_u += df_u.iloc[skip[trip_index] + ensemble_index + punktPerPil * arrow_index, bins[bin_index]]
                        tmp_v += df_v.iloc[
                            skip[trip_index] + ensemble_index + punktPerPil * arrow_index, bins[bin_index]]
            if divideby != 0:
                mean_u[trip_index, arrow_index] = tmp_u / divideby
                mean_v[trip_index, arrow_index] = tmp_v / divideby
        print(len(lat))
        print(len(lon))
        print(len(mean_v[trip_index,:]))
        print(len(mean_u[trip_index, :]))
        turur = pd.DataFrame({'lat': lat, 'lon': lon, 'u': mean_u[trip_index, :], 'v': mean_v[trip_index]})
        turur.to_csv(str(trip_index) + '.csv', index=False)
    log.config(state=NORMAL)
    log.delete(1.0, 2.0)
    log.insert(1.0, 'Liðugt\n')
    log.tag_add('fystalinja', '1.0', '2.0')
    log.tag_config('fystalinja', foreground='white', background='green')
    log.config(state=DISABLED)
    root.update()
