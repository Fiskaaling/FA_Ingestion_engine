from tkinter import *
import tkinter.ttk as ttk

def setupmenuframe(frame, setup_dict):
    tk_fun = StringVar(frame, setup_dict['main_frame'])
    tk_fun.set('Inset')
    fun_pop = OptionMenu(frame, tk_fun, 'Inset', 'Dagfør', command=print)
    fun_pop.pack(side=LEFT)

def setuplefttree(frame, setup_dict):
    tree = ttk.Treeview(frame)
    tree.column('#0', width=200)
    tree.heading("#0", text="Instromentir")

    scrollbar = Scrollbar(frame, orient=VERTICAL)
    scrollbar.config(command=tree.yview)

    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    setup_dict['lefttree'] = tree

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

