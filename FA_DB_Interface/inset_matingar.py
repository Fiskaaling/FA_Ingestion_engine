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

def inset_matingar(frame, db_host='192.168.43.94', db_user='trondur', db_password='koda'):
    for widget in frame.winfo_children():
        widget.destroy()
    setup_dict = {'login': {'db_host': db_host, 'db_user': db_user, 'db_password': db_password},
                  'main_frame': frame,
                  'Path_to_RawData': 'Rawdata',
                  'Instroment': '',
                  'filenames': [],
                  'mappir': []}

    #insamla Instromentir
    for _ in [0]:
        db_connection, cursor = fadblogin(setup_dict['login'])
        #TODO where stadment skal sikkurt breitast
        cursor.execute("SELECT * FROM Instumentir WHERE status='Upptikin';")
        Instromentir = cursor.fetchall()
        cursor.execute("SELECT Status FROM WL_Status")
        choices_status = ['alt'] + [x[0] for x in cursor.fetchall()]
        db_connection.disconnect()
        Sløg = []
        for x in Instromentir:
            if x[2] not in Sløg:
                Sløg.append(x[2])
        Sløg.sort()

    Label(frame, text='Inset mátingar', font='Helvetica 18 bold').pack(side=TOP)

    tk_status = StringVar(frame)
    if 'Upptikin' in choices_status:
        tk_status.set('Upptikin')
    else:
        tk_status.set(choices_status[0])
    pprint.pprint(choices_status)

    menuFrame = Frame(frame)
    treeView_frame = Frame(frame)
    mode_frame = Frame(treeView_frame)
    setup_frame = Frame(frame, bg='green')
    Date_frame = Frame(setup_frame)
    uppsetan_frame = Frame(setup_frame)
    filetree_frame = Frame(setup_frame)

    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    mode_frame.pack(side=TOP, fill=X, anchor=N)
    treeView_frame.pack(fill=Y, expand=False, side=LEFT, anchor=N)
    setup_frame.pack(side=LEFT, fill=BOTH, expand=True, anchor=N)
    Date_frame.grid(row=0, column=1, sticky=W + N + S)
    uppsetan_frame.grid(row=1, column=1, sticky=W + N + S)
    filetree_frame.grid(row=0, column=0, rowspan=3, sticky=W)

    instromentir_list = ttk.Treeview(treeView_frame)

    status_pop = OptionMenu(mode_frame, tk_status, *choices_status,
                            command=lambda status: update_treeView(status, instromentir_list, setup_dict))
    status_pop.pack()

    setup_dict['filetree'] = ttk.Treeview(filetree_frame)
    setup_dict['filetree'].column('#0', width=200)
    setup_dict['filetree'].heading("#0", text="Fílir")
    setup_dict['filetree'].pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    Button(menuFrame, text='Vel fil', command=lambda: velfilir(setup_dict)).pack(side=LEFT)
    Button(menuFrame, text='Vel Mappu', command=lambda: velmappu(setup_dict)).pack(side=LEFT)
    Button(menuFrame, text='koyr inn í DB', command=lambda: koyrmatingi_db(setup_dict, dato)).pack(side=LEFT)
    instromentir_list.bind("<Double-1>", lambda event, arg=instromentir_list: Doubletree(event, arg,
                                                                                         setup_dict, uppsetan_frame))
    #fill inn í instromentr_list
    for _ in [1]:
        scrollbar = Scrollbar(treeView_frame, orient=VERTICAL)
        scrollbar.config(command=instromentir_list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        instromentir_list.column('#0', width=100)
        instromentir_list.heading("#0", text="Instromentir")
        instromentir_list.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
        insert_instromentir_list(instromentir_list, Sløg, Instromentir)

    dato = datowid(Date_frame)

def velinstroment(Navn, setup_dict, frame):
    # TODO Møguligar_uppsetingar er bara fyri test
    for widget in frame.winfo_children():
        widget.destroy()
    setup_dict['Instroment'] = Navn
    # TODO SQL SELECT
    db_connection, cursor = fadblogin(setup_dict['login'])
    cursor.execute("SELECT * FROM Møguligar_uppsetingar WHERE Instrument_Navn='" + Navn + "';")
    temp = cursor.fetchall()
    setup_dict['uppsetwid'] = dict([(x[0], x[2]) for x in temp])
    temp = dict([(x[0], x[3]) for x in temp])
    i = 0
    for x in setup_dict['uppsetwid'].keys():
        Label(frame, text=setup_dict['uppsetwid'][x]).grid(row=i)
        setup_dict['uppsetwid'][x] = Entry(frame)
        setup_dict['uppsetwid'][x].insert(END, temp[x])
        setup_dict['uppsetwid'][x].grid(row=i, column=1)
        i += 1

def geruppsetan(setup_dict):
    temp = setup_dict['uppsetwid'].copy()
    for x in temp.keys():
        temp[x] = temp[x].get()
    setup_dict['uppsetan'] = temp

def koyrmatingi_db(setup_dict, dato):
    if setup_dict['Instroment'] == '':
        messagebox.showerror('Einki Instroment', 'Vel eitt instroment')
        return
    geruppsetan(setup_dict)
    inlesdato(setup_dict, dato)
    pprint.pprint(setup_dict)
    #TODO ger path til at vera unig í db
    #TODO tjekka um indexi er í db
    datamui = setup_dict['Dato']['Startdato'].strftime('%y%m%d')
    raw = setup_dict['Path_to_RawData'] + '/'
    destdir = setup_dict['Instroment']
    db_connection, cursor = fadblogin(setup_dict['login'])
    cursor.execute("SELECT id FROM Mátingar ORDER BY id DESC LIMIT 1;")
    id = cursor.fetchone()[0] + 1
    db_connection.disconnect()
    #TODO set inní DB árðin fílir vera kopyeraðir
    #TODO finn destdir ordiligt
    if datamui not in os.listdir(raw + destdir):
        os.makedirs(raw + destdir + '/' + datamui)
    else:
        i = 0
        while True:
            i += 1
            if datamui + str(i) not in os.listdir(raw + destdir):
                datamui += str(i)
                print(datamui)
                os.makedirs(raw + destdir + '/' + datamui)
                break
    #TODO tjekka um filenames er tómt
    #TODO tjekka um nakar filur eitur tað sama
    destdir += '/' + datamui

    db_connection, cursor = fadblogin(setup_dict['login'])
    if setup_dict['Dato']['Enddato'] == None:
        cursor.execute("INSERT into Mátingar (id, Mátari, Start_tid, Path_to_data) VALUE (%s, %s, %s, %s);",
                       (id, setup_dict['Instroment'], setup_dict['Dato']['Startdato'], destdir))
    else:
        cursor.execute(
            "INSERT into Mátingar (id, Mátari, Start_tid, Stop_tid, Path_to_data) VALUE (%s, %s, %s, %s, %s);",
            (id, setup_dict['Instroment'], setup_dict['Dato']['Startdato'], setup_dict['Dato']['Enddato'], destdir))
    for x in setup_dict['uppsetan']:
        if setup_dict['uppsetan'][x] != '':
            print((id, x, setup_dict['uppsetan'][x]))
            cursor.execute("INSERT into Uppsetingar (uppseting_id, uppseting, virði) VALUE (%s, %s, %s)",
                           (id, x, setup_dict['uppsetan'][x]))
    db_connection.commit()
    db_connection.disconnect()

    #TODO skal man brúka copy2
    for x in setup_dict['filenames']:
        shutil.copy(x, raw + destdir)
    #TODO riggar kanska ikki í windows
    for x in setup_dict['mappir']:
        shutil.copytree(x, raw + destdir + '/' + x.split('/')[-1])
    #ikki tann mest eleganta loysnin men hon riggar
    inset_matingar(setup_dict['main_frame'], setup_dict['login']['db_host'],
                   setup_dict['login']['db_user'], setup_dict['login']['db_password'])

def inlesdato(setup_dict, dato):
    tempdato = {}
    for i in dato.keys():
        print(dato.keys())
        try:
            Ar = int(dato[i]['Ár'].get())
            if Ar < 1900 or Ar > 3000:
                messagebox.showinfo("Feilur", i + ': Ár kann ikki verða ' + dato[i]['Ár'].get())
                tempdato = None
                break
        except:
            messagebox.showinfo("Feilur", i + ': Ár kann ikki verða ' + dato[i]['Ár'].get())
            tempdato = None
            break
        try:
            Man = int(dato[i]['M'].get())
            if Man < 1 or Man > 12:
                messagebox.showinfo("Feilur", i + ': M kann ikki verða ' + dato[i]['M'].get())
                tempdato = None
                break
        except:
            messagebox.showinfo("Feilur", i + ': M kann ikki verða ' + dato[i]['M'].get())
            tempdato = None
            break
        try:
            Dag = int(dato[i]['D'].get())
            if Man < 1 or Man > 31:
                messagebox.showinfo("Feilur", i + ': D kann ikki verða ' + dato[i]['D'].get())
                tempdato = None
                break
        except:
            messagebox.showinfo("Feilur", i + ': D kann ikki verða ' + dato[i]['D'].get())
            tempdato = None
            break
        try:
            tempdato[i] = dt.datetime(Ar, Man, Dag)
        except:
            messagebox.showinfo('Feilur', i + 'finnist ikki')
            tempdato = None
            break
        if dato['Enddato']['Ár'].get() == dato['Enddato']['M'].get() == dato['Enddato']['D'].get() == '':
            tempdato['Enddato'] = None
            break
    if tempdato != None:
        setup_dict['Dato'] = tempdato

def Doubletree(event, arg, setup_dict, frame):
    item = arg.identify('item', event.x, event.y)
    try:
        if item[0] == 'I':
            int(item[1::])
        else:
            int('error')
    except ValueError:
        return
    velinstroment(arg.item(item, "text"), setup_dict, frame)

def fadblogin(creds):
    db_connection = \
        db.connect(user=creds['db_user'], password=creds['db_password'], database='fa_db', host=creds['db_host'])
    return db_connection, db_connection.cursor()

def velfilir(setup_dict):
    #TODO møguliga datatypan hevur okkurt við instromenti at gera
    temp = filedialog.askopenfilenames(title='Velfil',
                                                          filetypes=(("all files", "*.*"), ("txt files", "*.txt")))
    #TODO tjekka um vit hava sama filin fleiri ferð
    #setup_dict['filenames'] += list(temp)
    #TODO veit ikki um hettar riggar í windows also split parturin
    for x in list(temp):
        if x not in setup_dict['filenames']:
            setup_dict['filenames'].append(x)
            setup_dict['filetree'].insert('', 'end', x, text=x.split('/')[-1])

def velmappu(setup_dict):
    temp = filedialog.askdirectory()
    #TODO veit ikki um hettar riggar í windows also split parturin
    if temp not in setup_dict['mappir']:
        setup_dict['mappir'].append(temp)
        setup_dict['filetree'].insert('', 0, temp, text=temp.split('/')[-1])
        for x in os.listdir(temp):
            setup_dict['filetree'].insert(temp, 'end', x, text=x.split('/')[-1])

def update_treeView(status, tree, setup_dict):
    db_connection, cursor = fadblogin(setup_dict['login'])
    if status == 'alt':
        cursor.execute("SELECT * FROM Instumentir")
    else:
        cursor.execute("SELECT * FROM Instumentir WHERE status=%s", (status,))
    Instromentir = cursor.fetchall()
    db_connection.disconnect()
    for x in tree.get_children():
        tree.delete(x)
    Sløg = []

    for x in Instromentir:
        if x[2] not in Sløg:
            Sløg.append(x[2])
    Sløg.sort()

    insert_instromentir_list(tree, Sløg, Instromentir)

    '''uppdatera trere'''

def insert_instromentir_list(tree,Sløg, Instromentir):
    for i in Sløg:
        tree.insert('', 'end', i, text=i)
    for i in Instromentir:
        tree.insert(i[2], 'end', text=i[0])