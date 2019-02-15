from tkinter import *
import tkinter.ttk as ttk
from pprint import pprint
import FA_DB_Interface.miscleitamatingar.db_ting as db

def setupmenuframe(frame, setup_dict):
    Label(frame, text='mátari').pack(side=LEFT)
    tk_ting1 = StringVar(frame, setup_dict['main_frame'])
    tk_ting1.set('nr1')
    fun_pop = OptionMenu(frame, tk_ting1, 'nr1', 'nr2')
    fun_pop.pack(side=LEFT)

    tk_ting2 = StringVar(frame, setup_dict['main_frame'])
    tk_ting2.set('nr1')
    fun_pop = OptionMenu(frame, tk_ting2, 'nr1', 'nr2')
    fun_pop.pack(side=LEFT)

    tk_ting3 = StringVar(frame, setup_dict['main_frame'])
    tk_ting3.set('nr1')
    fun_pop = OptionMenu(frame, tk_ting3, 'nr1', 'nr2')
    fun_pop.pack(side=LEFT)

    Button(frame, text='print', command=lambda: pprint(setup_dict)).pack(side=LEFT)

    ADmiB = Button(frame, text='-', command=lambda: ADmi(ADplB, ADmiB, setup_dict))
    ADplB = Button(frame, text='+', command=lambda: ADpl(ADplB, ADmiB, setup_dict))
    ADplB.pack(side=RIGHT)

def setupbodyframe(frame, setup_dict):
    kolonnir = db.getcol(setup_dict)
    Items = ttk.Treeview(frame)
    Items['columns'] = kolonnir[1::]
    for i in range(1, len(kolonnir)):
        Items.heading(kolonnir[i], text=kolonnir[i])
    Items.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    for ting in db.getmatinger(setup_dict):
        Items.insert("", 'end', text=ting[0], values=ting[1::])

def setupadframe(frame, setup_dict):
    Label(frame, text='ADFrame').pack(side=LEFT)

def ADpl(ADplB, ADmiB, setup_dict):
    setup_dict['ADFrame'].pack(side=BOTTOM, fill=X)
    ADplB.pack_forget()
    ADmiB.pack(side=RIGHT)

def ADmi(ADplB, ADmiB, setup_dict):
    setup_dict['ADFrame'].pack_forget()
    ADmiB.pack_forget()
    ADplB.pack(side=RIGHT)
