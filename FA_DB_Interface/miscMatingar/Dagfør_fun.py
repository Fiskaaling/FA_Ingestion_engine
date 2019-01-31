from tkinter import *
import os
import shutil
import datetime as dt
from FA_DB_Interface.miscMatingar import db_ting as db
from FA_DB_Interface.miscMatingar import init_fun as fun
from FA_DB_Interface import Matingar

def doublelefttree(id, setup_dict):
    setup_dict['inniliggjandimappir'] = []
    setup_dict['inniliggjandifilir'] = []
    righttree = setup_dict['righttree']
    righttree.delete(*righttree.get_children())
    print(id)
    temp = db.getdatepath(id, setup_dict)
    Date = setup_dict['dato']['Startdato']
    for x in Date.values():
        x.config(state=NORMAL)
    Date['Ár'].delete(0, END)
    Date['Ár'].insert(0, temp[0].year)
    Date['M'].delete(0, END)
    Date['M'].insert(0, temp[0].month)
    Date['D'].delete(0, END)
    Date['D'].insert(0, temp[0].day)
    for x in Date.values():
        x.config(state=DISABLED)
    print(temp)
    path = setup_dict['Path_to_RawData'] + '/' + temp[1]
    temp = os.listdir(path)
    print(temp)
    for x in temp:
        try:
            files = os.listdir(path + '/' + x)
            righttree.insert('', 0, x, text=x)
            for y in files:
                righttree.insert(x, 'end', text=y)
            setup_dict['inniliggjandimappir'].append(x)
        except NotADirectoryError:
            righttree.insert('', 'end', text=x)
            setup_dict['inniliggjandifilir'].append(x)
    Møguligarupp, upp = db.Dagførupp(id, setup_dict)
    print('\n\n')
    print(Møguligarupp)
    print('\n\n')
    print(upp)
    #TODO uppsetingar