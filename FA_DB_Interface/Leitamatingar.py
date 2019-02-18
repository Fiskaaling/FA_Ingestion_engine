from tkinter import *
from tkinter import messagebox
import pandas as pd
import os
import FA_DB_Interface.miscleitamatingar.setupframe as setupframe

def Leita(frame, db_host, db_user, db_password):
    for widget in frame.winfo_children():
        widget.destroy()
    #TODO path_to_RawData skal eisini riggar allastani
    setup_dict = {'login': {'host': db_host, 'user': db_user, 'password': db_password, 'database': 'fa_db'},
                  'main_frame': frame,
                  'Path_to_RawData': r'Rawdata'}

    if 'setup.txt' in os.listdir('FA_DB_Interface'):
        try:
            setup_dict.update(dict(pd.read_csv('FA_DB_Interface/setup.txt', sep='\t').values))
        except:
            messagebox.showinfo('fekk ikki inlisi setup.txt')

    Label(frame, text='Leita eftir Mátingum', font='Helvetica 18 bold').pack(side=TOP)

    upperframe = Frame(frame)
    upperframe.pack(side=TOP, fill=X, expand=False, anchor=N)

    menuFrame = Frame(upperframe)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    setup_dict['menuFrame'] = menuFrame
    setvar(setup_dict)
    setupframe.setupmenuframe(menuFrame, setup_dict)

    LowerFrame = Frame(upperframe)
    setup_dict['LowerFrame'] = LowerFrame

    ADFrame = Frame(LowerFrame)
    setup_dict['ADFrame'] = ADFrame
    setupframe.setupadframe(ADFrame, setup_dict)

    tidFrame = Frame(LowerFrame)
    setup_dict['tidFrame'] = tidFrame
    setupframe.setuptidframe(tidFrame, setup_dict)

    BodyFrame = Frame(frame, bg='green')
    setup_dict['BodyFrame'] = BodyFrame
    BodyFrame.pack(fill=BOTH, expand=True, anchor=N + W)
    setupframe.setupbodyframe(setup_dict)

def setvar(setup_dict):
    frame = setup_dict['menuFrame']
    tk_slag = StringVar(frame, setup_dict['main_frame'])
    setup_dict['tk_slag'] = tk_slag

    tk_inst = StringVar(frame, setup_dict['main_frame'])
    setup_dict['tk_inst'] = tk_inst
