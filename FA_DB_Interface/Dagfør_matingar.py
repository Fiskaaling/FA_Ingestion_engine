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
    BodyFrame = Frame(frame, bg='green')
    '''
    BodyFrame.columnconfigure(0, weight=1)
    BodyFrame.columnconfigure(1, weight=1)
    BodyFrame.columnconfigure(2, weight=1)
    BodyFrame.rowconfigure(0, weight=1)
    BodyFrame.rowconfigure(1, weight=1)
    '''

    treeView_frame = Frame(BodyFrame)#, width=200)
    filetree_frame = Frame(BodyFrame)
    Date_frame = Frame(BodyFrame)


    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    Button(menuFrame, text='Press me', command=lambda: print('hey')).pack(side=LEFT)

    BodyFrame.pack(fill=BOTH, expand=True, anchor=N+W)
    treeView_frame.grid(row=0, column=0, rowspan=8)
    filetree_frame.grid(row=0, column=1, rowspan=3)
    Date_frame.grid(row=0, column=2, sticky=N)

    tree = ttk.Treeview(treeView_frame)
    tree.column('#0', width=200)
    tree.heading("#0", text="Instromentir")
    insert_tree(tree, Bmatingar)
    tree.bind("<Double-1>", lambda event, arg=tree: Doubletree(event, arg, setup_dict))

    scrollbar = Scrollbar(treeView_frame, orient=VERTICAL)
    scrollbar.config(command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    filetree = ttk.Treeview(filetree_frame)
    setup_dict['filetree'] = filetree
    filetree.column('#0', width=200)
    filetree.heading("#0", text="Fílir")
    filetree.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    dato = datowid(Date_frame)

def insert_tree(tree, Bmatingar):
    Sløg = list(set([x[4] for x in Bmatingar]))
    for x in Sløg:
        tree.insert('', 'end', x, text=x)
    for x in Bmatingar:
        #TODO fix eftir at økir eru komin til beta
        tree.insert(x[4], 'end', x[0], text=x[2].strftime('%d/%m-%Y') + ' ' + x[1])

def fyllut_filir(id, setup_dict):
    out = {}
    db_connection, cursor = fadblogin(setup_dict['login'])
    cursor.execute("SELECT Path_to_data FROM Mátingar where id=%s", (id,))
    path = setup_dict['Path_to_RawData'] + '/' + cursor.fetchone()[0]
    print(path)
    ls = os.listdir(path)
    print(ls)
    print('hey')
    for i in range(len(ls)):
        try:
            out[ls[i]] = os.listdir(path + '/' + ls[i])
            print(os.listdir(path + '/' + ls[i]))
            ls[i] = ''
        except NotADirectoryError:
            pass
    print([x for x in ls if x != ''])
    out[''] = [x for x in ls if x != '']
    pprint.pprint(out)
    for x in out.keys():
        if x == '':
            for y in out[x]:
                setup_dict['filetree'].insert(x, 'end', y, text=y)
                setup_dict['filenames'].append(y)
        else:
            setup_dict['mappir'].append(x)
            setup_dict['filetree'].insert('', 0, x, text=x)
            for y in out[x]:
                setup_dict['filetree'].insert(x, 'end', y, text=y)
    '''arbeið viðarai uppa hettar'''

def Doubletree(event, arg, setup_dict):
    item = arg.identify('item', event.x, event.y)
    print(item)
    setup_dict['filetree'].delete(*setup_dict['filetree'].get_children())
    setup_dict['filenames'] = []
    setup_dict['mappir'] = []
    #TODO depop
    pprint.pprint(setup_dict)
    fyllut_filir(item, setup_dict)
    fyllut_dato(item, setup_dict)

def fadblogin(creds):
    db_connection = \
        db.connect(user=creds['db_user'], password=creds['db_password'], database='fa_db', host=creds['db_host'])
    return db_connection, db_connection.cursor()
