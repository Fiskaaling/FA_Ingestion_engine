from tkinter import *
from tkinter import filedialog
from misc.faLog import *


def CTDtidarseria_lin(frame, root2):
    global root
    global mappunavn
    filnavn = ''
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Linjuplot tiðarseria').pack(side=TOP, anchor=W)

    velMappuBtn = Button(frame, text='Vel Fílir', command=lambda: velFil())
    velMappuBtn.pack(side=TOP, anchor=W)

    processBtn = Button(frame, text='Processera', command=lambda: processera(mappunavn))
    processBtn.pack(side=TOP, anchor=W)

    log_frame = Frame(frame, height=300, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

def velFil():
    global mappunavn
    mappunavn = filedialog.askdirectory(title='Vel túramappu')
    print('Mappa: ' + mappunavn)