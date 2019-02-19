from tkinter import *
import tkinter.ttk as ttk
import FA_DB_Interface.miscleitamatingar.db_ting as db
from FA_DB_Interface.datowid import datowid
from FA_DB_Interface.miscleitamatingar import update
from pprint import pprint
import datetime as dt


def setupmenuframe(frame, setup_dict):
    setup_dict['LowerBool'] = False
    Label(frame, text='mátari:(').pack(side=LEFT)
    Label(frame, text='slag').pack(side=LEFT)

    tk_slag = setup_dict['tk_slag']
    temp = ['Øll'] + [x[0] for x in db.get_slag(setup_dict)]
    tk_slag.set(temp[0])
    fun_pop1 = OptionMenu(frame, tk_slag, *temp, command=lambda x: popinstframe(setup_dict, x, pop2frame, tk_inst))
    fun_pop1.pack(side=LEFT)

    Label(frame, text='Mátari').pack(side=LEFT)
    pop2frame = Frame(frame)
    pop2frame.pack(side=LEFT)
    tk_inst = setup_dict['tk_inst']
    popinstframe(setup_dict, tk_slag.get(), pop2frame, tk_inst)

    Label(frame, text=') Start tíð:').pack(side=LEFT)

    Button(frame, text='tíð', command=lambda: startid(setup_dict)).pack(side=LEFT)

    Button(frame, text='print', command=lambda: pprint(setup_dict)).pack(side=LEFT)

    Button(frame, text='update', command=lambda: setupbodyframe(setup_dict)).pack(side=LEFT)
    admiB = Button(frame, text='-', command=lambda: ADmi(setup_dict))
    adplB = Button(frame, text='+', command=lambda: ADpl(setup_dict))
    setup_dict['ADknob'] = {'ADmiB': admiB, 'ADplB': adplB}
    adplB.pack(side=RIGHT)


def setupbodyframe(setup_dict):
    frame = setup_dict['BodyFrame']
    for widget in frame.winfo_children():
        widget.destroy()
    items = ttk.Treeview(frame)
    items.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    kolonnir, innihald = update.update(setup_dict)

    items['columns'] = kolonnir[1::]
    innihald_tree = [list(x) for x in innihald]

    #setup av formati av hvussu kolonnunar skullu síggja út
    items.column('#0', minwidth=40, width=60)
    for i, j in enumerate(kolonnir):
        if j == 'mátingar.Mátari':
            items.column('#' + str(i), minwidth=90, width=140)
        elif j == 'mátingar.Start_tid':
            items.column('#' + str(i), minwidth=90, width=140)
            for k in range(len(innihald_tree)):
                innihald_tree[k][i] = innihald_tree[k][i].strftime('%d %b-%Y')
        elif j == 'mátingar.Stop_tid':
            items.column('#' + str(i), minwidth=90, width=140)
            for k in range(len(innihald_tree)):
                if innihald_tree[k][i] == None:
                    innihald_tree[k][i] = 'ígongd'
                else:
                    innihald_tree[k][i] = innihald_tree[k][i].strftime('%d %b-%Y')
        elif j == 'mátingar.Path_to_data':
            items.column('#' + str(i), minwidth=100, width=150)
        elif j == 'mátingar.Umbiði_av':
            items.column('#' + str(i), minwidth=250, width=400)
            temp = db.get_felagar(setup_dict)
            for k in range(len(innihald_tree)):
                for felagi in temp:
                    if innihald_tree[k][i] == felagi[0]:
                        innihald_tree[k][i] = felagi[2] + ' (' + felagi[1] + ')'
        elif j == 'mátingar.Embargo_til':
            items.column('#' + str(i), minwidth=90, width=140)
            temp = dt.datetime.now()
            for k in range(len(innihald_tree)):
                tid = innihald_tree[k][i] - temp
                if tid.days > 500:
                    innihald_tree[k][i] = str(tid.days//365) + ' Ár'
                elif tid.days >= 0:
                    innihald_tree[k][i] = str(tid.days) + ' Dagar'
                elif tid.days < 0:
                    innihald_tree[k][i] = 'ligut'


    for i in range(1, len(kolonnir)):
        items.heading(kolonnir[i], text=kolonnir[i].split('.')[-1])
    for ting in innihald_tree:
        items.insert("", 'end', text=ting[0], values=ting[1::])


def setupadframe(frame, setup_dict):
    Label(frame, text='ADFrame').pack(side=LEFT)


def setuptidframe(frame, setup_dict):
    dato = datowid(frame)
    dato['Startdato']['Ár'].insert(0, 1900)
    dato['Startdato']['M'].insert(0, 1)
    dato['Startdato']['D'].insert(0, 1)
    dato['Enddato']['Ár'].insert(0, 2100)
    dato['Enddato']['M'].insert(0, 12)
    dato['Enddato']['D'].insert(0, 31)
    setup_dict['dato'] = dato


def ADpl(setup_dict):
    for widget in setup_dict['LowerFrame'].winfo_children():
        widget.pack_forget()
    ADplB = setup_dict['ADknob']['ADplB']
    ADmiB = setup_dict['ADknob']['ADmiB']
    ADplB.pack_forget()
    ADmiB.pack(side=RIGHT)

    setup_dict['ADFrame'].pack(side=BOTTOM, fill=X)
    setup_dict['LowerFrame'].pack(side=BOTTOM, fill=X)
    setup_dict['LowerBool'] = True

def ADmi(setup_dict):
    for widget in setup_dict['LowerFrame'].winfo_children():
        widget.pack_forget()
    ADplB = setup_dict['ADknob']['ADplB']
    ADmiB = setup_dict['ADknob']['ADmiB']
    ADmiB.pack_forget()
    ADplB.pack(side=RIGHT)

    setup_dict['LowerFrame'].pack_forget()
    setup_dict['LowerBool'] = False

def popinstframe(setup_dict, slag, frame, var):
    for widget in frame.winfo_children():
        widget.destroy()
    options = ['Øll'] + [x[0] for x in db.get_instrumentir(setup_dict, slag)]
    var.set(options[0])
    fun_pop2 = OptionMenu(frame, var, *options)
    fun_pop2.pack(side=LEFT)

def startid(setup_dict):
    for widget in setup_dict['LowerFrame'].winfo_children():
        widget.pack_forget()

    setup_dict['tidFrame'].pack(side=BOTTOM, fill=X)

    if not setup_dict['LowerBool']:
        setup_dict['ADknob']['ADplB'].pack_forget()
        setup_dict['ADknob']['ADmiB'].pack(side=RIGHT)
        setup_dict['LowerFrame'].pack(side=BOTTOM, fill=X)
        setup_dict['LowerBool'] = True
