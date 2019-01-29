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


def Dagfør_matingar(frame, db_host='192.168.43.94', db_user='trondur', db_password='koda'):

    for widget in frame.winfo_children():
        widget.destroy()

    Label(frame, text='Dagfør mátingar', font='Helvetica 18 bold').pack(side=TOP)

    setup_dict = {'login': {'db_host': db_host, 'db_user': db_user, 'db_password': db_password},
                  'main_frame': frame,
                  'Path_to_RawData': 'Rawdata',
                  'Instroment': '',
                  'filenames': [],
                  'mappir': []}

    db_connection, cursor = fadblogin(setup_dict['login'])
    cursor.execute("SELECT id, Mátari, Start_tid, Path_to_data, Slag FROM Mátingar, Instumentir WHERE Mátari=navn")
    Bmatingar = cursor.fetchall()
    db_connection.disconnect()
    pprint.pprint(Bmatingar)

    menuFrame = Frame(frame)
    treeView_frame = Frame(frame)

    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    treeView_frame.pack(side=LEFT, fill=Y, expand=True)

    Button(menuFrame, text='Press me', command=lambda: print('hey')).pack(side=LEFT)

    tree = ttk.Treeview(treeView_frame)
    tree.column('#0', width=100)
    tree.heading("#0", text="Instromentir")
    tree.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    insert_instromentir_list(tree, Sløg, Instromentir)

    scrollbar = Scrollbar(treeView_frame, orient=VERTICAL)
    scrollbar.config(command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)





def fadblogin(creds):
    db_connection = \
        db.connect(user=creds['db_user'], password=creds['db_password'], database='fa_db', host=creds['db_host'])
    return db_connection, db_connection.cursor()
