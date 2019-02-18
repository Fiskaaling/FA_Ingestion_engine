from tkinter import *
import tkinter.ttk as ttk
from pprint import pprint
import FA_DB_Interface.miscleitamatingar.db_ting as db
from pprint import pprint

def setupmenuframe(frame, setup_dict):
    Label(frame, text='mátari:(').pack(side=LEFT)
    Label(frame, text='slag').pack(side=LEFT)

    tk_slag = setup_dict['tk_slag']
    temp = ['Øll'] + db.get_slag(setup_dict)
    tk_slag.set(temp[0])
    fun_pop1 = OptionMenu(frame, tk_slag, *temp, command=lambda x: popinstframe(setup_dict, x[0], pop2frame, tk_inst))
    fun_pop1.pack(side=LEFT)

    pop2frame = Frame(frame)
    pop2frame.pack(side=LEFT)
    tk_inst = setup_dict['tk_inst']
    popinstframe(setup_dict, tk_slag.get(), pop2frame, tk_inst)

    tk_ting3 = StringVar(frame, setup_dict['main_frame'])
    tk_ting3.set('nr1')
    fun_pop3 = OptionMenu(frame, tk_ting3, 'nr1', 'nr2')
    fun_pop3.pack(side=LEFT)

    Button(frame, text='print', command=lambda: pprint(setup_dict)).pack(side=LEFT)

    Button(frame, text='update', command=lambda: setupbodyframe(setup_dict)).pack(side=LEFT)

    ADmiB = Button(frame, text='-', command=lambda: ADmi(ADplB, ADmiB, setup_dict))
    ADplB = Button(frame, text='+', command=lambda: ADpl(ADplB, ADmiB, setup_dict))
    ADplB.pack(side=RIGHT)

def setupbodyframe(setup_dict):
    frame = setup_dict['BodyFrame']
    for widget in frame.winfo_children():
        widget.destroy()
    kolonnir = db.getcol(setup_dict)
    Items = ttk.Treeview(frame)
    Items['columns'] = kolonnir[1::]
    for i in range(1, len(kolonnir)):
        Items.heading(kolonnir[i], text=kolonnir[i])
    for ting in db.getmatinger(setup_dict):
        Items.insert("", 'end', text=ting[0], values=ting[1::])
    Items.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

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

def popinstframe(setup_dict, slag, frame, var):
    for widget in frame.winfo_children():
        widget.destroy()
    options = ['Øll'] + list(db.get_instrumentir(setup_dict, slag))
    var.set(options[0])
    fun_pop2 = OptionMenu(frame, var, *options)
    fun_pop2.pack(side=LEFT)
