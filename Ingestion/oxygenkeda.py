from tkinter import *
from tkinter import filedialog
from misc.faLog import *
import pandas as pd
import scipy.signal as sig
import os
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.dates as md
from datetime import datetime
import numpy as np
from scipy import interpolate
from scipy.interpolate import griddata
from scipy.interpolate import RectBivariateSpline
from matplotlib.ticker import MaxNLocator
import pylab

def init(ingestion_listbox):
    termistorkeda = ingestion_listbox.insert("", 0, text="Termistor Keda")
    oxygenmatarir = ingestion_listbox.insert(termistorkeda, 0, text="Oxygen mátarir")
    tempraturmatarir = ingestion_listbox.insert(termistorkeda, 0, text="Hitamálarir")
    ingestion_listbox.insert(oxygenmatarir, "end", text="Decimering")
    ingestion_listbox.insert(tempraturmatarir, "end", text="Decimering")
    ingestion_listbox.insert(oxygenmatarir, "end", text="Kalibrering")
    ingestion_listbox.insert(oxygenmatarir, "end", text="Fyrireika Seaguard data")
    ingestion_listbox.insert(tempraturmatarir, "end", text="Fyrireika Seaguard data")
    ingestion_listbox.insert(oxygenmatarir, "end", text="Rokna upploystiligheit (mg/l)")
    ingestion_listbox.insert(oxygenmatarir, "end", text="Ger Countour plot")
    ingestion_listbox.insert(tempraturmatarir, "end", text="Ger Countour plot")


def check_click(item, RightFrame, root):
    if item == 'Decimering':
        decimering(RightFrame, root)
    elif item == 'Kalibrering':
        kalibering(RightFrame, root)
    elif item == 'Fyrireika Seaguard data':
        seaguard_data(RightFrame, root)
    elif item == 'Ger Countour plot':
        termistorkeda_contourplot(RightFrame, root)


########################################################################################################################
#                                                                                                                      #
#                                                     Contour plot                                                     #
#                                                                                                                      #
########################################################################################################################

def termistorkeda_contourplot(frame, root2):
    global root
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Termistorkeda', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Plotta contour data').pack(side=TOP, anchor=W)

    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    Button(menuFrame, text='Vel dýpir', command=lambda: vel_dypir()).pack(side=LEFT)
    Button(menuFrame, text='Vel datafílir', command=lambda: velFilir()).pack(side=LEFT)
    Button(menuFrame, text='Tekna', command=lambda: rokna_og_tekna_contour(canvas, int(fra_entry.get()),
           int(til_entry.get()))).pack(side=LEFT)
    Button(menuFrame, text='Goym mynd', command=lambda: goymmynd(fig)).pack(side=RIGHT)
    Label(menuFrame, text='Dýpið frá:').pack(side=LEFT)
    fra_entry = Entry(menuFrame, width=3)
    fra_entry.pack(side=LEFT)
    fra_entry.insert(0, '0')
    Label(menuFrame, text='til').pack(side=LEFT)
    til_entry = Entry(menuFrame, width=3)
    til_entry.pack(side=LEFT)
    til_entry.insert(0, '100')

    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=TOP, anchor=W)
    gerlog(log_frame, root)
    plot_frame = Frame(frame)
    plot_frame.pack(fill=BOTH, expand=True, side=BOTTOM, anchor=W)
    global fig
    global ax
    fig = Figure(figsize=(8, 12), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    fig.clf()
    ax = fig.add_subplot(111)


def rokna_og_tekna_contour(canvas, d_fra, d_til):
    log_b()
    global ax
    global fig
    global dfilnavn
    dypirfil = pd.read_csv(dfilnavn)
    global filnavn
    signal = []
    timestamp = []
    print('Lesur datafílir')
    for i in range(len(filnavn)):
        print(filnavn[i])
        data = pd.read_csv(filnavn[i])
        signal.append(data['signal'].values)
        timestamp.append(data['time'])
    print('Roknar um til datetime')
    flat_timestamp = []
    flat_signal = []
    starttid = 100000000000
    stoptid = 0
    dypir = []
    dypir_sernr = dypirfil['serial']
    dypir_virdir = dypirfil['d']
    stostadypid = 1
    for i in range(len(dypir_virdir)):
        if float(dypir_virdir[i]) > stostadypid:
            stostadypid = dypir_virdir[i]
    print(np.linspace(0, stostadypid, 10))
    ctr = 0
    for i in range(len(filnavn)):
        print('Fílur' + str(i))
        # Finn dýpi á fíli
        hettardypid = -99.9
        print(len(dypirfil))
        for j in range(len(dypirfil)):
            if str(dypir_sernr[j]) in filnavn[i]:
                print('funnið dypir á fíli ' + str(dypir_sernr[j]))
                hettardypid = -dypir_virdir[j]
        for j in range(len(timestamp[i])):
            try:
                flat_timestamp.append(md.date2num(datetime.strptime(timestamp[i][j], '%Y-%m-%d_%H:%M:%S.%f')))
                flat_signal.append(float(signal[i][j]))
                dypir.append(hettardypid)
                ctr += 1
            except:
                try:
                    flat_timestamp.append(md.date2num(datetime.strptime(timestamp[i][j], '%d.%m.%y_%H:%M:%S')))
                    flat_signal.append(float(signal[i][j]))
                    dypir.append(hettardypid)
                    ctr += 1
                except:
                    print('Hjálp ' + timestamp[i][j])
                    print(filnavn[i])
    tmp = pd.DataFrame(flat_timestamp)
    tmp.to_csv('farts.csv')
    print('Finnur endapunkt í tíðsaksanum')
    for j in range(len(flat_timestamp)):
        if flat_timestamp[j] > stoptid:
            stoptid = flat_timestamp[j]
        if flat_timestamp[j] < starttid:
            starttid = flat_timestamp[j]
    n = 1000
    #X, Y = np.meshgrid(flat_timestamp, dypir)
    #f = griddata((flat_timestamp, dypir), flat_signal, (X, Y), method='linear', rescale=False)
    #f = interpolate.interp2d((flat_timestamp, dypir), flat_signal, (X, Y), kind='linear')

    flat_signal = flat_signal[0::100]
    flat_timestamp = flat_timestamp[0::100]
    dypir = dypir[0::100]
    print('Ger meshgrid')
    X, Y = np.meshgrid(np.linspace(starttid, stoptid, n), np.linspace(d_fra, -d_til, len(flat_timestamp)))
    #X, Y = np.mgrid[starttid-10:stoptid+10:100j, -stostadypid-10:d_fra+10]
    print('Interpolerar')
    flat_signal = np.array(flat_signal)
    flat_timestamp = np.array(flat_timestamp)
    dypir = np.array(dypir)
    f = griddata((flat_timestamp, dypir), flat_signal, (X, Y), method='linear', rescale=False)

    levels_exists = False
    if 'levels' in globals():
        levels_exists = True

    global levels

    if levels_exists:
        c = ax.contourf(X, Y, f, levels=levels, cmap='jet', extend='both')
    else:
        levels = np.round(np.linspace(75, 115, 200), 1)
        c = ax.contourf(X, Y, f, levels=levels, cmap='jet', extend='both')
        fig.colorbar(c)

    ax.set_ylim(-d_til, -d_fra)

    ax.xaxis.set_major_locator(MaxNLocator(10))
    xt = ax.get_xticks()
    text_timestamps = []
    for i in range(len(xt)):
        tmp = md.num2date(float(xt[i]))
        text_timestamps.append(tmp.strftime("%d %b"))
    try:
        ax.set_xticks(text_timestamps)
    except:
        print('nooo')
    try:
        ax.set_xticklabels(text_timestamps)
    except:
        print('bapokafs')
    ax.scatter(flat_timestamp, dypir, alpha=.2, s=.5, c='black')
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    fig.savefig('tmp.png', figsize=(8, 12), dpi=300)
    log_e()



def vel_dypir():
    global dfilnavn
    dfilnavn = filedialog.askopenfile(title='Vel Dýpid fíl',
                                      filetypes=(("csv Fílir", "*.csv"), ("all files", "*.*"))).name


def goymmynd(fig):
    log_b()
    filnavn = filedialog.asksaveasfilename(parent=root, title="Goym mynd",  filetypes=(("png Fílur", "*.png"), ("jpg Fílur", "*.jpg")))
    print('Goymir mynd')
    fig.savefig(filnavn, dpi=1200, bbox_inches='tight')
    print('Liðugt')
    log_e()

########################################################################################################################
#                                                                                                                      #
#                                                  Seaguard data                                                       #
#                                                                                                                      #
########################################################################################################################

def seaguard_data(frame, root2):
    global root
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Termistorkeda', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Les seaguard data').pack(side=TOP, anchor=W)

    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    Button(menuFrame, text='Vel Seaguard fíl', command=lambda: vel_fil()).pack(side=LEFT)

    Button(menuFrame, text='Eksportera fíl', command=lambda: eksportera()).pack(side=LEFT)

    v = IntVar()
    temp_radBtn = Radiobutton(frame, text='Tempratur', variable=v, value=1)
    temp_radBtn.pack(side=TOP, anchor=W)
    o2metn = Radiobutton(frame, text='Oxygen metningur', variable=v, value=2)
    o2metn.pack(side=TOP, anchor=W)
    o2cong = Radiobutton(frame, text='Oxygen upploysiligheit', variable=v, value=3)
    o2cong.pack(side=TOP, anchor=W)



    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

def eksportera():
    log_b()
    global filnavn
    data = pd.read_csv(filnavn, sep='\t', skiprows=1)
    print(data.columns.values)
    timestamp = data['Time tag (Gmt)'].values
    print(timestamp[0])
    for i in range(len(timestamp)):
        timestamp[i] = timestamp[i].replace(' ', '_')
    print(timestamp[0])
    o2 = data['AirSaturation']
    savefilnavn = filedialog.asksaveasfilename(title='Goym fíl', filetypes=(("csv Fílir", "*.csv"), ("all files", "*.*")))
    data_tosave = pd.DataFrame({'time': timestamp, 'signal': o2})
    data_tosave.to_csv(savefilnavn, index=False)
    log_e()

def vel_fil():
    global filnavn
    filnavn = filedialog.askopenfile(title='Vel Seaguard fíl', filetypes=(("txt Fílir", "*.txt"), ("csv Fílir", "*.csv"),
                                                                 ("all files", "*.*"))).name

########################################################################################################################
#                                                                                                                      #
#                                                   Kalibrering                                                        #
#                                                                                                                      #
########################################################################################################################


def kalibering(frame, root2):
    global root
    global filnavn
    filnavn = '/home/johannus/Documents/FA_Ingestion_engine/Kort_Data/Syðradalur.txt'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Termistorkeda', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Liner Kalibrering (y=ax+b)').pack(side=TOP, anchor=W)
    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    velMappuBtn = Button(menuFrame, text='Les inn kaliberingskofficientar', command=lambda: les_kalib_kofficientar(kalib_tree))
    velMappuBtn.pack(side=LEFT)

    velfilir_Btn = Button(menuFrame, text='Vel fílir at kalibrera', command=lambda: velFilir())
    velfilir_Btn.pack(side=LEFT)

    rokna_btn = Button(menuFrame, text='Rokna', command=lambda: rokna_kalib(kalib_tree))
    rokna_btn.pack(side=LEFT)

    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

    treeView_frame = Frame(frame)
    treeView_frame.pack(fill=Y, expand=False, side=RIGHT, anchor=N)
    kalib_tree = ttk.Treeview(treeView_frame)
    kalib_tree["columns"] = ("a", "b")
    kalib_tree.column("#0", width=100)
    kalib_tree.column("#1", width=100)
    kalib_tree.column("#2", width=100)
    scrollbar = Scrollbar(treeView_frame, orient=VERTICAL)
    scrollbar.config(command=kalib_tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    kalib_tree.heading("a", text="a")
    kalib_tree.heading("b", text="b")
    kalib_tree.pack(fill=BOTH, expand=True, side=TOP, anchor=W)


def rokna_kalib(kalib_tree):
    global filnavn
    kalib_tree_ting = kalib_tree.get_children()
    a = []
    b = []
    text = []
    if not os.path.isdir(str(os.path.dirname(filnavn[0]))+'/kalib'):
        os.mkdir(os.path.dirname(filnavn[0])+'/kalib')
    for i in range(len(kalib_tree_ting)):
        tmp = kalib_tree.item(kalib_tree_ting[i])["values"]
        a.append(float(tmp[0]))
        b.append(float(tmp[1]))
        text.append(kalib_tree.item(kalib_tree_ting[i])["text"])

    for i in range(len(filnavn)):
        print('Lesur ' + filnavn[i])
        data = pd.read_csv(filnavn[i])
        kalibrera_data = a[i] * data['signal'] + b[i]
        nyttfilnavn = filnavn[i]
        nyttfilnavn = os.path.dirname(filnavn[i]) + '/kalib/' + nyttfilnavn[len(os.path.dirname(filnavn[i])):len(filnavn[i])] + '_kalib.csv'
        print('Goymur fíl ' + nyttfilnavn)
        filur_at_goyma = pd.DataFrame({'time': data['time'], 'signal': kalibrera_data})
        filur_at_goyma.to_csv(nyttfilnavn, index=False)


    print('TODO')

########################################################################################################################
#                                                                                                                      #
#                                                    Decimering                                                        #
#                                                                                                                      #
########################################################################################################################

def decimering(frame, root2):
    global root
    global filnavn
    filnavn = '/home/johannus/Documents/FA_Ingestion_engine/Kort_Data/Syðradalur.txt'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Termistorkeda', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Decimering').pack(side=TOP, anchor=W)

    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    velMappuBtn = Button(menuFrame, text='Vel Fíl', command=lambda: velFilir())
    velMappuBtn.pack(side=LEFT)

    rokna_btn = Button(menuFrame, text='Rokna', command=lambda: rokna(int(n_entry.get())))
    rokna_btn.pack(side=LEFT)

    Label(menuFrame, text='Decimeringskofficientur:').pack(side=LEFT)

    n_entry = Entry(menuFrame, width=2)
    n_entry.pack(side=LEFT)
    n_entry.insert("end", '2')

    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)


def velFilir():
    global filnavn
    filnavn = filedialog.askopenfilenames(title='Vel fílir', filetypes=(("txt Fílir", "*.txt"), ("csv Fílir", "*.csv"),
                                                                      ("all files", "*.*")))
    print(filnavn)



def les_kalib_kofficientar(kalib_tree):
    global kalib_filnavn
    kalib_filnavn = filedialog.askopenfile(title='Vel fíl', filetypes=(("csv Fílir", "*.csv"), ("txt Fílir", "*.txt"),
                                                                 ("all files", "*.*"))).name
    print(kalib_filnavn)
    kalib_tree.delete(*kalib_tree.get_children())
    data = pd.read_csv(kalib_filnavn)
    a_data = data['a'].values
    b_data = data['b'].values
    legends = data['serial'].values
    print(legends)
    for i in range(len(data)):
        kalib_tree.insert("", 0, text=legends[len(data)-i-1], values=(a_data[len(data) - i - 1], b_data[len(data) - i - 1]))


def rokna(q):
    log_b()
    global filnavn
    if not os.path.isdir(str(os.path.dirname(filnavn[0]))+'/'+str(q)):
        os.mkdir(os.path.dirname(filnavn[0])+'/'+str(q))
    for fil_index in range(len(filnavn)):
        print('Lesur fíl ' + filnavn[fil_index])
        decimated_time = []
        if 'd' in filnavn[fil_index]:
            fil_data = pd.read_csv(filnavn[fil_index])
            raw_data = fil_data['signal']
            date = fil_data['time']
            print('Decimerar tíð')
            for i in range(len(fil_data)):
                if i % q == 0:
                    decimated_time.append(date[i])
        else:
            fil_data = pd.read_csv(filnavn[fil_index], encoding='latin', skiprows=25, sep='\s+')
            raw_data = fil_data['Time']
            date = fil_data['Date']
            time = fil_data['&']
            print('Decimerar tíð')
            for i in range(len(fil_data)):
                if i % q == 0:
                    decimated_time.append(date[i] + '_' + time[i])

        print('Decimerar data')
        decimated_data = sig.decimate(raw_data, q, 3, ftype='fir')

        nyttfilnavn = filnavn[fil_index]
        nyttfilnavn = os.path.dirname(filnavn[fil_index]) + '/' + str(q) + '/' + nyttfilnavn[len(os.path.dirname(filnavn[fil_index]))+1:len(filnavn[fil_index]) - 13] + 'd' + str(q) + '.csv'
        print('Goymur fíl ' + nyttfilnavn)
        filur_at_goyma = pd.DataFrame({'time': decimated_time, 'signal': decimated_data})
        filur_at_goyma.to_csv(nyttfilnavn, index=False)

    log_e()