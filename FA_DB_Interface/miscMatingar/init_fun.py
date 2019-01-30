from tkinter import *
import FA_DB_Interface.miscMatingar.db_ting as db

def inset(frame, setup_dict):
    rudda()
    tk_status = StringVar(frame, setup_dict['main_frame'])
    choices_status = db.status(setup_dict)

    if 'Upptikin' in choices_status:
        tk_status.set('Upptikin')
    else:
        tk_status.set(choices_status[0])

    fun_pop = OptionMenu(frame, tk_status, *choices_status, command=lambda x: insetlefttree(x, setup_dict))
    fun_pop.pack(side=LEFT)

    insetlefttree(tk_status.get(), setup_dict)

def insetlefttree():
    pass

def rudda(frame, setup_dict):
    pass