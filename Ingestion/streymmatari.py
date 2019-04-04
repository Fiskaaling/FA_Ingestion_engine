from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
#from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os.path
from misc.faLog import *
R = 6373  # Radius av jørð (km)


def roknaMidalstreym(frame, root2):
    global root
    root = root2
    global mappunavn
    mappunavn = '/home/johannus/Documents/data/Streymmátingar/Hov/DATA_EXTRACTED'
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Streymmátingar', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Rokna Miðal streym í punktum').pack(side=TOP, anchor=W)

    setup_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    setup_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)


    leftFrame = Frame(setup_frame)
    leftFrame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)

    knottarFrame = Frame(leftFrame)
    knottarFrame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    treeView_frame = Frame(setup_frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    treeView_frame.pack(fill=Y, expand=False, side=RIGHT, anchor=N)

    punktir = ttk.Treeview(treeView_frame)
    scrollbar = Scrollbar(treeView_frame, orient=VERTICAL)
    scrollbar.config(command=punktir.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    punktir["columns"] = ("lon", "lat")
    punktir.column("#0", width=100)
    punktir.column("#1", width=100)
    punktir.column("#2", width=100)
    punktir.heading("lon", text="lon")
    punktir.heading("lat", text="lat")
    punktir.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    # Knøttar
    velPunktirBtn = Button(knottarFrame, text='Vel Punktir', command=lambda: velPunktir(punktir))
    velPunktirBtn.pack(side=LEFT, anchor=W)
    velMappuBtn = Button(knottarFrame, text='Vel Mappu', command=lambda: velMappu())
    velMappuBtn.pack(side=LEFT, anchor=W)
    roknaBtn = Button(knottarFrame, text='Rokna', command=lambda: rokna_Midalstreym(punktir, fig, canvas))
    roknaBtn.pack(side=LEFT, anchor=W)
    Button(knottarFrame, text='Goym Mynd', command=lambda: goymmynd(fig, canvas)).pack(side=LEFT)

    fig = Figure(figsize=(10, 15), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)

    log_frame = Frame(leftFrame, height=300, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=TOP, anchor=W)
    gerlog(log_frame, root)

def rokna_Midalstreym(punktir, fig, canvas):
    log_b()
    fig.clf()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    punkt = punktir.get_children()
    lon = []
    lat = []
    text = []
    for i in range(len(punkt)):
        tmp = punktir.item(punkt[i])["values"]
        lon.append(float(tmp[0]))
        lat.append(float(tmp[1]))
        text.append(punktir.item(punkt[i])["text"])
    n_trips = 1
    funnifil = True
    while funnifil:
        if os.path.isfile(mappunavn + '/' + str(n_trips) + '_nav.txt'):
            n_trips += 1
        else:
            funnifil = False
    print('Funnið ' + str(n_trips) + ' fílir')
    urslit = np.zeros((len(lat), n_trips))
    midal_vinkul = np.zeros((len(lat), n_trips))
    lonPunktir = []
    latPunktir = []
    for punkt_index in range(len(lat)):
        print('Roknar punkt ' + text[punkt_index])
        print('|' + '-'*n_trips + '|')
        print('')
        print('|', False)
        x_lables = []
        for route_index in range(n_trips):
            print('_', False)
            #print('Túrur nr. ' + str(route_index))
            df_nav = pd.read_csv(mappunavn + '/' + str(route_index) + '_nav.txt', skiprows=16, sep='\t', index_col=0,
                                 decimal=",")
            df_u = pd.read_csv(mappunavn + '/' + str(route_index) + '_u.txt', skiprows=16, sep='\t', index_col=0,
                               decimal=",")
            df_v = pd.read_csv(mappunavn + '/' + str(route_index) + '_v.txt', skiprows=16, sep='\t', index_col=0,
                               decimal=",")
            innanfyri = []
            for ensemble_index in range(len(df_nav)):
                # Finnur avstandin til hvørt punkt
                delta_lon = np.deg2rad(lon[punkt_index]) - np.deg2rad(df_nav.iloc[ensemble_index, 11])
                delta_lat = np.deg2rad(lat[punkt_index]) - np.deg2rad(df_nav.iloc[ensemble_index, 10])
                a = np.sin(delta_lat / 2) ** 2 + np.cos(np.deg2rad(lat[punkt_index])) * np.cos(
                    np.deg2rad(df_nav.iloc[ensemble_index, 10])) * np.sin(delta_lon / 2) ** 2
                c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
                distance = R * c
                # Um tað er innanfyri 50 m
                if distance < 0.05:
                    lonPunktir.append(df_nav.iloc[ensemble_index, 11])
                    latPunktir.append(df_nav.iloc[ensemble_index, 10])
                    innanfyri.append(ensemble_index)
            tmp_u = 0
            tmp_v = 0
            divideby = 0
            for funnidPunktIndex in range(len(innanfyri)):
                for bin_index in range(9, 9 + 10):
                    if not np.isnan(df_u.iloc[innanfyri[funnidPunktIndex], bin_index]):
                        tmp_u += df_u.iloc[innanfyri[funnidPunktIndex], bin_index]
                        tmp_v += df_v.iloc[innanfyri[funnidPunktIndex], bin_index]
                        divideby += 1
            if divideby != 0:
                tmp_u = tmp_u / divideby
                tmp_v = tmp_v / divideby
                midal_vinkul[punkt_index, route_index] = np.mod(90 - np.arctan2(tmp_v, tmp_u) * 180 / np.pi, 360)
                urslit[punkt_index, route_index] = np.sqrt(tmp_u**2+tmp_v**2)/1000
            x_lables.append(str(df_nav.iloc[int(len(df_nav)/2), 3]) + ":" + str(df_nav.iloc[int(len(df_nav)/2), 4]))
        print('|', False)
        ax1.plot(x_lables, urslit[punkt_index, :], label=text[punkt_index])
        ax2.plot(x_lables, midal_vinkul[punkt_index, :])
    if True:  # Ger ein checkbox seinni!
        punktirAtPlotta = pd.DataFrame({'lat': latPunktir, 'lon': lonPunktir})
        punktirAtPlotta.to_csv('punktir.csv', index=False)
        print(punktirAtPlotta)
    print('Teknar')
    ax1.legend()
    ax1.set_ylabel('Miðal streymur [m/s]')
    ax1.set_xlabel('Tíð')
    ax2.set_xlabel('Tíð')
    ax2.set_ylabel('Miðal ætt')
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    log_e()


def goymmynd(fig, canvas):
    log_b()
    filnavn = filedialog.asksaveasfilename(parent=root, title="Goym mynd",  filetypes=(("pdf Fílur", "*.pdf"), ("png Fílur", "*.png"), ("jpg Fílur", "*.jpg")))
    print('Goymir mynd')
    fig.savefig(filnavn, dpi=600, bbox_inches='tight')
    print('Liðugt')
    log_e()


def velPunktir(punktir):
    filnavn = filedialog.askopenfile(title='Vel punktir frá fíli', filetypes=(('csv fílur', '*.csv'),
                                                                              ('Allir fílir', '*.*')))
    data = pd.read_csv(filnavn)
    lon = data['lon'].values
    lat = data['lat'].values
    punktir.delete(*punktir.get_children())
    Samla = True
    columns = data.columns.values
    for i in range(len(columns)):
        if columns[i] == 'legend':
            Samla = False
    if Samla:
        for i in range(len(data)):
            punktir.insert("", 0, text=str(len(data)-i-1), values=(lon[len(data)-i-1], lat[len(data)-i-1]))
    else:
        legends = data['legend'].values
        for i in range(len(data)):
            punktir.insert("", 0, text=legends[len(data)-i-1], values=(lon[len(data)-i-1], lat[len(data)-i-1]))


# Alt undur her er til at rokna Quiver
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
    gerlog(log_frame, root)

def velMappu():
    global mappunavn
    mappunavn = filedialog.askdirectory(title='Vel mappu')
    print(mappunavn)


def rokna(fra, til, punktPerPil, bins, skip):
    log_b()
    n_trips = len(range(fra, til+1))
    for trip_index in range(0, n_trips):
        print('Lesur fíl :' + str(trip_index) + '_nav.txt')
        df_nav = pd.read_csv(mappunavn + '/' + str(trip_index) + '_nav.txt', skiprows=16, sep='\t', index_col=0,
                             decimal=",")
        df_u = pd.read_csv(mappunavn + '/' + str(trip_index) + '_u.txt', skiprows=16, sep='\t', index_col=0, decimal=",")
        df_v = pd.read_csv(mappunavn + '/' + str(trip_index) + '_v.txt', skiprows=16, sep='\t', index_col=0, decimal=",")
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
        turur.to_csv(str(trip_index+1) + '.csv', index=False)
    log_e()

def init(ingestion_listbox):
    streymmatingar_frabati = ingestion_listbox.insert("", 0, text="RDI Streymmátingar frá báti")
    ingestion_listbox.insert(streymmatingar_frabati, "end", text='Kopiera data frá feltteldu')
    ingestion_listbox.insert(streymmatingar_frabati, "end", text='Evt. Reprocessera')
    ingestion_listbox.insert(streymmatingar_frabati, "end", text='Exportera csv fílar')
    ingestion_listbox.insert(streymmatingar_frabati, "end", text='Rokna quiver data')
    ingestion_listbox.insert(streymmatingar_frabati, "end", text='Rokna miðal streym')
    ingestion_listbox.insert(streymmatingar_frabati, "end", text='Tekna Kort')