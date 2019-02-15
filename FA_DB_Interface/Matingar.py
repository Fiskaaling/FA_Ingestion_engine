from tkinter import *
import tkinter.ttk as ttk
import mysql.connector as db
import datetime as dt
from tkinter import messagebox
from tkinter import filedialog
import pprint
import os
import shutil
import pandas as pd
from FA_DB_Interface.datowid import datowid
import FA_DB_Interface.miscMatingar.setupframe as setupframe
import FA_DB_Interface.miscMatingar.init_fun as init_fun

def inset_matingar(frame, db_host, db_user, db_password):
    for widget in frame.winfo_children():
        widget.destroy()
    #TODO ikki koyra inn í db uttan at faa filarnar inn
    #TODO path_to_RawData skal eisini riggar allastani
    setup_dict = {'login': {'host': db_host, 'user': db_user, 'password': db_password, 'database': 'fa_db'},
                  'main_frame': frame,
                  'Path_to_RawData': r'Rawdata',
                  'Instroment': '',
                  'innsettirfilir': [],
                  'innsettarmappir': [],
                  'inniliggjandifilir': [],
                  'inniliggjandimappir': []}

    if 'setup.txt' in os.listdir('FA_DB_Interface'):
        try:
            setup_dict.update(dict(pd.read_csv('FA_DB_Interface/setup.txt', sep='\t').values))
        except:
            messagebox.showinfo('fekk ikki inlisi setup.txt')

    Label(frame, text='Inset mátingar', font='Helvetica 18 bold').pack(side=TOP)

    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    setupframe.setupmenuframe(menuFrame, setup_dict)

    funFrame = Frame(frame)
    funFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    BodyFrame = Frame(frame, bg='green')
    BodyFrame.pack(fill=BOTH, expand=True, anchor=N + W)

    lefttree_frame = Frame(BodyFrame)
    lefttree_frame.grid(row=0, column=0, rowspan=8, sticky=N + W + S)
    setupframe.setuplefttree(lefttree_frame, setup_dict)

    righttree_frame = Frame(BodyFrame)
    righttree_frame.grid(row=0, column=1, rowspan=3)
    setupframe.setuprighttree(righttree_frame, setup_dict)

    dato_frame = Frame(BodyFrame)
    dato_frame.grid(row=0, column=2, sticky=N)
    setupframe.setupdato(dato_frame, setup_dict)

    uppsetan_frame = Frame(BodyFrame)
    uppsetan_frame.grid(row=1, column=2, sticky=N+W+S)
    setup_dict['uppsetan_frame'] = uppsetan_frame

    felaga_frame = Frame(BodyFrame)
    felaga_frame.grid(row=4, column=1, sticky=W)
    setupframe.setupfelagar(felaga_frame, setup_dict)

    info_frame = Frame(BodyFrame)
    info_frame.grid(row=5, column=1, sticky=N + W)
    setupframe.setupinfo(info_frame, setup_dict)

    init_fun.inset(funFrame, setup_dict)
    setup_dict['funFrame'] = funFrame
