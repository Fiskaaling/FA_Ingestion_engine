from tkinter import *
import tkinter.ttk as ttk
from pprint import pprint
import FA_DB_Interface.miscMatingar.init_fun as fun
import FA_DB_Interface.miscMatingar.Inset_fun as in_fun

def setupmenuframe(frame, setup_dict):
    tk_fun = StringVar(frame, setup_dict['main_frame'])
    tk_fun.set('inset')
    fun_pop = OptionMenu(frame, tk_fun, 'inset', 'Dagfør', command=lambda x: fun.chosefun(x, setup_dict))
    fun_pop.pack(side=LEFT)
    setup_dict['fun'] = tk_fun.get()

    Button(frame, text='Vel filr', command=lambda: fun.velfilir(setup_dict)).pack(side=LEFT)
    Button(frame, text='Vel mappu', command=lambda: fun.velmappu(setup_dict)).pack(side=LEFT)
    Button(frame, text='koyr inn í DB', command=lambda: fun.update_db(setup_dict)).pack(side=LEFT)
    Button(frame, text='print', command=lambda: pprint(setup_dict)).pack(side=LEFT)

def setuplefttree(frame, setup_dict):
    tree = ttk.Treeview(frame)
    tree.column('#0', width=200)
    tree.heading("#0", text="Instromentir")

    scrollbar = Scrollbar(frame, orient=VERTICAL)
    scrollbar.config(command=tree.yview)

    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True, side=TOP, anchor=N)
    setup_dict['lefttree'] = tree
    tree.bind("<Double-1>", lambda event: fun.Doublelefttree(event, setup_dict))

def setupfelagar(frame, setup_dict):
    tree = ttk.Treeview(frame)
    tree.column('#0', width=200)
    tree.heading("#0", text="Felagar")

    scrollbar = Scrollbar(frame, orient=VERTICAL)
    scrollbar.config(command=tree.yview)

    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    setup_dict['felagartree'] = tree
    tree.bind("<Double-1>", lambda event: fun.Doublefelagartree(event, setup_dict))

def setuprighttree(frame, setup_dict):
    tree = ttk.Treeview(frame)
    tree.column('#0', width=200)
    tree.heading("#0", text="Fílir")

    scrollbar = Scrollbar(frame, orient=VERTICAL)
    scrollbar.config(command=tree.yview)

    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    setup_dict['righttree'] = tree

def setupdato(frame, setup_dict):
    dato = {'Startdato': {}, 'Enddato': {}}
    i = 0
    j = 0
    Label(frame, text=list(dato.keys())[0]).grid(row=i, column=j, columnspan=2)
    i += 1
    Label(frame, text='Ár').grid(row=i, column=j)
    j += 1
    dato[list(dato.keys())[0]]['Ár'] = Entry(frame, width=4)
    dato[list(dato.keys())[0]]['Ár'].grid(row=i, column=j)
    j += 1
    Label(frame, text='M').grid(row=i, column=j)
    j += 1
    dato[list(dato.keys())[0]]['M'] = Entry(frame, width=2)
    dato[list(dato.keys())[0]]['M'].grid(row=i, column=j)
    j += 1
    Label(frame, text='D').grid(row=i, column=j)
    j += 1
    dato[list(dato.keys())[0]]['D'] = Entry(frame, width=2)
    dato[list(dato.keys())[0]]['D'].grid(row=i, column=j)
    i += 1
    j = 0
    Label(frame, text=list(dato.keys())[1]).grid(row=i, column=j, columnspan=2)
    i += 1
    Label(frame, text='Ár').grid(row=i, column=j)
    j += 1
    dato[list(dato.keys())[1]]['Ár'] = Entry(frame, width=4)
    dato[list(dato.keys())[1]]['Ár'].grid(row=i, column=j)
    j += 1
    Label(frame, text='M').grid(row=i, column=j)
    j += 1
    dato[list(dato.keys())[1]]['M'] = Entry(frame, width=2)
    dato[list(dato.keys())[1]]['M'].grid(row=i, column=j)
    j += 1
    Label(frame, text='D').grid(row=i, column=j)
    j += 1
    dato[list(dato.keys())[1]]['D'] = Entry(frame, width=2)
    dato[list(dato.keys())[1]]['D'].grid(row=i, column=j)
    setup_dict['dato'] = dato

def setupinfo(frame, setup_dict):
    Label(frame, text='felagi').grid(row=0, column=0, sticky=N + W)
    Felag = StringVar()
    Felag.set('Felag')
    Umbiði_av = StringVar()
    Umbiði_av.set('Umbiði_av')
    Label(frame, textvariable=Felag).grid(row=1, column=0, sticky=N + W)
    Label(frame, textvariable=Umbiði_av).grid(row=2, column=0, sticky=N + W)
    setup_dict['info'] = {'Felag': Felag, 'Umbiði_av': Umbiði_av}
