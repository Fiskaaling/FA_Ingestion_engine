from tkinter import *
from tkinter import filedialog
from misc.faLog import *
import pandas as pd
import scipy.signal as sig
import os
import tkinter.ttk as ttk

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

    velMappuBtn = Button(menuFrame, text='Les inn kaliberingskofficientar', command=lambda: velFil())
    velMappuBtn.pack(side=LEFT)

    treeView_frame = Frame(frame)
    treeView_frame.pack(fill=Y, expand=False, side=RIGHT, anchor=N)
    punktir = ttk.Treeview(treeView_frame)
    punktir["columns"] = ("a", "b")
    punktir.column("#0", width=100)
    punktir.column("#1", width=100)
    punktir.column("#2", width=100)

    punktir.heading("a", text="a")
    punktir.heading("b", text="b")
    punktir.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)


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
    filnavn = filedialog.askopenfilenames(title='Vel fíl', filetypes=(("txt Fílir", "*.txt"), ("csv Fílir", "*.csv"),
                                                                      ("all files", "*.*")))
    print(filnavn)


def velFil():
    global filnavn
    filnavn = filedialog.askopenfile(title='Vel fíl', filetypes=(("csv Fílir", "*.csv"), ("txt Fílir", "*.txt"),
                                                                 ("all files", "*.*"))).name
    print(filnavn)


def rokna(q):
    log_b()
    global filnavn
    if not os.path.isdir(str(os.path.dirname(filnavn[0]))+'/'+str(q)):
        os.mkdir(os.path.dirname(filnavn[0])+'/'+str(q))
    for fil_index in range(len(filnavn)):
        print('Lesur fíl ' + filnavn[fil_index])
        fil_data = pd.read_csv(filnavn[fil_index], encoding='latin', skiprows=25, sep='\s+')
        print(fil_data.columns.values)
        raw_data = fil_data['Time']
        print('Decimerar data')
        decimated_data = sig.decimate(raw_data, q, 3, ftype='fir')
        decimated_time = []
        print('Decimerar tíð')
        date = fil_data['Date']
        time = fil_data['&']
        for i in range(len(fil_data)):
            if i % q == 0:
                decimated_time.append(date[i] + '_' + time[i])
        nyttfilnavn = filnavn[fil_index]
        nyttfilnavn = os.path.dirname(filnavn[fil_index]) + '/' + str(q) + '/' + nyttfilnavn[len(os.path.dirname(filnavn[fil_index]))+1:len(filnavn[fil_index]) - 13] + 'd' + str(q) + '.csv'
        print('Goymur fíl ' + nyttfilnavn)
        filur_at_goyma = pd.DataFrame({'time': decimated_time, 'signal': decimated_data})
        filur_at_goyma.to_csv(nyttfilnavn, index=False)

    log_e()