from tkinter import *
import tkinter.ttk as ttk
import mysql.connector as db
import datetime as dt
from tkinter import messagebox
from tkinter import filedialog
import pprint
import os
import shutil
from FA_DB_Interface.datowid import datowid
import FA_DB_Interface.miscMatingar.setupframe as setupframe
import FA_DB_Interface.miscMatingar.init_fun as init_fun

def inset_matingar(frame, db_host='192.168.43.94', db_user='trondur', db_password='koda'):
    for widget in frame.winfo_children():
        widget.destroy()
    setup_dict = {'login': {'host': db_host, 'user': db_user, 'password': db_password, 'database': 'fa_db'},
                  'main_frame': frame,
                  'Path_to_RawData': 'Rawdata',
                  'Instroment': '',
                  'filenames': [],
                  'mappir': []}

    Label(frame, text='Inset mátingar', font='Helvetica 18 bold').pack(side=TOP)

    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    setupframe.setupmenuframe(menuFrame, setup_dict)

    funFrame = Frame(frame)
    funFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    BodyFrame = Frame(frame, bg='green')
    BodyFrame.pack(fill=BOTH, expand=True, anchor=N + W)

    lefttree_frame = Frame(BodyFrame)
    lefttree_frame.grid(row=0, column=0, rowspan=8)
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

    init_fun.inset(funFrame, setup_dict)

    pprint.pprint(setup_dict)
