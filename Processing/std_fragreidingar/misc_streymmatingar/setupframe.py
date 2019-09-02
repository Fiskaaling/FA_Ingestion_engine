from tkinter import *
import tkinter.ttk as ttk
import os

from pprint import pprint

from .menuframe import menu_fun
from .metaframe import meta_fun
from .moguligarsidur import moguligar
from .valdarsidur import valdar

def setupmenuframe(frame, setup_dict, siduval_dict):
    Button(frame, text='print', command=lambda: pprint(setup_dict)).pack(side=LEFT)
    Button(frame, text='germappu', command=lambda: menu_fun.germappu(setup_dict, siduval_dict)).pack(side=LEFT)
    Button(frame, text='test', command=lambda: menu_fun.germetafilin(setup_dict)).pack(side=LEFT)

def setupmetaframe(frame, setup_dict):
    path_to_data = StringVar()
    path_to_data.set('path')
    path_to_dest = StringVar()
    path_to_dest.set(os.path.dirname(os.path.dirname(__file__)))
    path_to_mynd = StringVar()
    path_to_mynd.set('path')
    navn_a_tex = StringVar()
    navn_a_tex.set('path')

    setup_dict['path'] = {'data'    : path_to_data,
                          'dest'    : path_to_dest,
                          'mynd'    : path_to_mynd
                         }
    meta = {}

    Button(frame, text='Vel data', command=lambda: meta_fun.vel_data(frame, setup_dict))\
                                                            .grid(row=0)
    Label(frame, textvariable=path_to_data).grid(row=0, column=1)

    Button(frame, text='Vel dest', command=lambda: meta_fun.vel_dest(frame, setup_dict))\
                                                            .grid(row=1)
    Label(frame, textvariable=path_to_dest).grid(row=1, column=1)

    Button(frame, text='Vel mynd', command=lambda: meta_fun.vel_mynd(frame, setup_dict))\
                                                            .grid(row=2)
    Label(frame, textvariable=path_to_mynd).grid(row=2, column=1)

    Label(frame, text='Heiti').grid(row=3)
    meta['heiti'] = Entry(frame, width=100)
    meta['heiti'].grid(row=3, column=1)

    Label(frame, text='Undirheiti').grid(row=4)
    meta['undirheiti'] = Entry(frame, width=100)
    meta['undirheiti'].grid(row=4, column=1)

    Label(frame, text='dokumentslag').grid(row=5)
    meta['dokumentslag'] = Entry(frame, width=100)
    meta['dokumentslag'].grid(row=5, column=1)

    Label(frame, text='Høvundar').grid(row=6)
    meta['hovundar'] = Entry(frame, width=100)
    meta['hovundar'].grid(row=6, column=1)

    Label(frame, text='Status').grid(row=7)
    meta['status'] = Entry(frame, width=100)
    meta['status'].grid(row=7, column=1)

    Label(frame, text='Frágreiðingar nummar').grid(row=8)
    meta['fragrnr'] = Entry(frame, width=100)
    meta['fragrnr'].grid(row=8, column=1)

    Label(frame, text='Verkatlan').grid(row=9)
    meta['verkatlan'] = Entry(frame, width=100)
    meta['verkatlan'].grid(row=9, column=1)

    Label(frame, text='Dagfesting').grid(row=10)
    meta['dagfest'] = Entry(frame, width=100)
    meta['dagfest'].grid(row=10, column=1)

    Label(frame, text='Ábyrdarhavandi').grid(row=11)
    meta['abyrgd'] = Entry(frame, width=100)
    meta['abyrgd'].grid(row=11, column=1)

    Label(frame, text='Góðkent').grid(row=12)
    meta['godkent'] = Entry(frame, width=100)
    meta['godkent'].grid(row=12, column=1)

    Label(frame, text='Samandráttur').grid(row=13)
    meta['samandr'] = Entry(frame, width=100)
    meta['samandr'].grid(row=13, column=1)

    Label(frame, text='Leitiorð').grid(row=14)
    meta['leitiord'] = Entry(frame, width=100)
    meta['leitiord'].grid(row=14, column=1)

    setup_dict['meta'] = meta

def moguligarsidur(frame, siduval_dict, siduval_list):
    moguleikar_tree = ttk.Treeview(frame, height=20)
    moguleikar_tree.column('#0', width=200)
    moguleikar_tree.heading("#0", text="Møguligar síður")

    moguleikar_tree.grid(row=0, column=0)
    moguleikar_tree.bind("<Double-1>", lambda event: moguligar.velsidu(event, siduval_dict))
    moguligar.filltradi(moguleikar_tree, siduval_dict, siduval_list)
    siduval_dict['møguleikar_tree'] = moguleikar_tree

def valdarsigur(frame, siduval_dict):
    valdar_tree = ttk.Treeview(frame, height=20)
    valdar_tree.column('#0', width=200)
    valdar_tree.heading("#0", text="Valdar síður")

    valdar_tree.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    Button(frame, text='upp', command= lambda: valdar.upp(siduval_dict)).pack(side=LEFT)
    Button(frame, text='niður', command= lambda: valdar.nidur(siduval_dict)).pack(side=LEFT)

    valdar_tree.bind("<Double-1>", lambda event: valdar.fjerna(event, siduval_dict))
    valdar.setup(valdar_tree)
    siduval_dict['valdar_tree'] = valdar_tree

def parametur(frame, setup_dict, parlist):
    meta = dict()
    for i, key in enumerate(setup_dict):
        if key in parlist:
            Label(frame, text=key).grid(row=i)
            meta[key] = Entry(frame, width=75)
            meta[key].grid(row=i, column=1)
            meta[key].delete(0, END)
            meta[key].insert(0, setup_dict[key])
    setup_dict['gui_par']  = meta
