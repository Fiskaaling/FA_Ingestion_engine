from tkinter import *
import os

from pprint import pprint

from .menuframe import menu_fun
from .metaframe import meta_fun, setupfun

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

    setupfun.inset_feltir(meta)

    setup_dict['meta'] = meta
