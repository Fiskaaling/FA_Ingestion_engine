from tkinter import *

def gerlog(log_frame):
    global log
    global root
    log = Text(log_frame, bg='#888888')
    log.pack(fill=X, expand=True)
    log.insert(1.0, 'Klárt\n')
    log.tag_add('fystalinja', '1.0', '2.0')
    log.tag_config('fystalinja', foreground='white', background='green')
    log.config(state=DISABLED)

def print(text, nl=True):
    log.config(state=NORMAL)
    if nl:
        log.insert(2.0, str(text) + '\n')
    else:
        log.insert(2.0, str(text))
    root.update()
    log.config(state=DISABLED)

def byrja_arb():
    log.config(state=NORMAL)
    log.delete(1.0, 2.0)
    log.insert(1.0, 'Arbeðir\n')
    log.tag_add('fystalinja', '1.0', '2.0')
    log.tag_config('fystalinja', foreground='white', background='red')
    root.update()

def enda_arb():
    log.config(state=NORMAL)
    log.delete(1.0, 2.0)
    log.insert(1.0, 'Liðugt\n')
    log.tag_add('fystalinja', '1.0', '2.0')
    log.tag_config('fystalinja', foreground='white', background='green')
    log.config(state=DISABLED)