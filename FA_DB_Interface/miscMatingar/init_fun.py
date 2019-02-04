from tkinter import *
import tkinter.ttk as ttk
import os
from tkinter import messagebox
import datetime as dt
import FA_DB_Interface.miscMatingar.db_ting as db
import FA_DB_Interface.miscMatingar.Inset_fun as Insert_fun
import FA_DB_Interface.miscMatingar.Dagfør_fun as Dagfør_fun


def chosefun(tk_fun, setup_dict):
    setup_dict['fun'] = tk_fun
    if tk_fun == 'inset':
        inset(setup_dict['funFrame'], setup_dict)
    elif tk_fun == 'Dagfør':
        Dagfør(setup_dict['funFrame'], setup_dict)

def inset(frame, setup_dict):
    rudda(frame, setup_dict)
    tk_status = StringVar(frame, setup_dict['main_frame'])
    choices_status = ['alt'] + db.status(setup_dict)

    if 'Upptikin' in choices_status:
        tk_status.set('Upptikin')
    else:
        tk_status.set(choices_status[0])

    fun_pop = OptionMenu(frame, tk_status, *choices_status, command=lambda x: insetlefttree(x, setup_dict))
    fun_pop.pack(side=LEFT)
    insetlefttree(tk_status.get(), setup_dict)

def Dagfør(frame, setup_dict):
    rudda(frame, setup_dict)
    Button(frame, text='Print meg', command=lambda: print('meg')).pack(side=LEFT)
    for x in setup_dict['dato']['Startdato'].values():
        x.config(state=DISABLED)
    Dagførlefttree(setup_dict)

def insetlefttree(staus, setup_dict):
    Instromentir = db.listinstrumentir(staus, setup_dict)
    lefttree = setup_dict['lefttree']
    lefttree.delete(*lefttree.get_children())
    Sløg = list(set([x[2] for x in Instromentir]))
    Sløg.sort()
    for x in Sløg:
        lefttree.insert('', 'end', x, text=x)
    for x in Instromentir:
        lefttree.insert(x[2], 'end', text=x[0])

def Dagførlefttree(setup_dict):
    matingar = db.stopnull(setup_dict)
    lefttree = setup_dict['lefttree']
    for x in matingar:
        lefttree.insert('', 'end', x[0], text=x[2].strftime('%d/%m-%Y') + ' ' + x[1])

def rudda(frame, setup_dict):
    for widget in frame.winfo_children():
        widget.destroy()
    for widget in setup_dict['uppsetan_frame'].winfo_children():
        widget.destroy()
    setup_dict['lefttree'].delete(*setup_dict['lefttree'].get_children())
    setup_dict['righttree'].delete(*setup_dict['righttree'].get_children())
    for x in setup_dict['dato'].values():
        for y in x.values():
            y.config(state=NORMAL)
            y.delete(0, END)

def Doublelefttree(event, setup_dict):
    item = setup_dict['lefttree'].identify('item', event.x, event.y)
    if setup_dict['fun'] == 'inset':
        Insert_fun.doublelefttree(item, setup_dict)
    elif setup_dict['fun'] == 'Dagfør':
        Dagfør_fun.doublelefttree(item, setup_dict)

def velfilir(setup_dict):
    # TODO møguliga datatypan hevur okkurt við instromenti at gera
    temp = filedialog.askopenfilenames(title='Velfil',
                                       filetypes=(("all files", "*.*"), ("txt files", "*.txt")))
    # TODO veit ikki um hettar riggar í windows also split parturin
    for x in list(temp):
        if x not in setup_dict['innsettirfilir'] and x.split('/')[-1] not in setup_dict['inniliggjandifilir']:
            setup_dict['innsettirfilir'].append(x)
            setup_dict['righttree'].insert('', 'end', x, text=x.split('/')[-1])
        else:
            messagebox.showwarning('Feilur', 'Har er ein fýla sum eitur ' + x.split('/')[-1])

def velmappu(setup_dict):
    temp = filedialog.askdirectory()
    #TODO veit ikki um hettar riggar í windows also split parturin
    if temp not in setup_dict['innsettarmappir'] and temp.split('/')[-1] not in setup_dict['inniliggjandimappir']:
        setup_dict['innsettarmappir'].append(temp)
        setup_dict['righttree'].insert('', 0, temp, text=temp.split('/')[-1])
        for x in os.listdir(temp):
            setup_dict['righttree'].insert(temp, 'end', x, text=x.split('/')[-1])
    else:
        messagebox.showwarning('Feilur', 'Har er ein mappa sum eitur ' + temp.split('/')[-1])

def update_db(setup_dict):
    if setup_dict['fun'] == 'inset':
        Insert_fun.update_db(setup_dict)
    elif setup_dict['fun'] == 'Dagfør':
        Dagfør_fun.update_db(setup_dict)

def geruppsetan(setup_dict):
    temp = setup_dict['uppsetwid'].copy()
    for x in temp.keys():
        temp[x] = temp[x].get()
    setup_dict['uppsetan'] = temp

def inlesdato(setup_dict):
    dato = setup_dict['dato']
    tempdato = {}
    for i in dato.keys():
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
            messagebox.showinfo('Feilur', i + ' finnist ikki')
            tempdato = None
            break
        if dato['Enddato']['Ár'].get() == dato['Enddato']['M'].get() == dato['Enddato']['D'].get() == '':
            tempdato['Enddato'] = None
            break
    if tempdato != None:
        setup_dict['Utfiltdato'] = tempdato
