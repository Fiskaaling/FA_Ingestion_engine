from tkinter import *

def gerlog(log_frame, root2):
    global log
    global root
    global nw
    nw = 2.0
    root = root2
    log = Text(log_frame, bg='#888888')
    log.pack(fill=X, expand=True)
    log.insert(1.0, 'Klárt\n')
    log.tag_add('fystalinja', '1.0', '2.0')
    log.tag_config('fystalinja', foreground='white', background='green')
    log.config(state=DISABLED)

def print(text, nl=True):
    global root
    log.config(state=NORMAL)
    if nl:
        log.insert(nw, str(text) + '\n')
    else:
        log.insert(nw, str(text))
    log.config(state=DISABLED)
    root.update()


def log_w(text):
    global root
    global nw
    log.config(state=NORMAL)
    log.insert(nw, str(text) + '\n')
    nw += 1
    log.tag_add('fystaWlinja', '2.0', str(nw))
    log.tag_config('fystaWlinja', foreground='black', background='darkorange')
    root.update()

def log_clear():
    global root
    global nw
    nw = 2.0
    log.config(state=NORMAL)
    log.delete(0.0, END)
    log.config(state=DISABLED)
    root.update()

def log_b():
    log.config(state=NORMAL)
    log.delete(1.0, 2.0)
    log.insert(1.0, 'Arbeðir\n')
    log.tag_add('fystalinja', '1.0', '2.0')
    log.tag_config('fystalinja', foreground='white', background='red')
    root.update()

def log_e():
    log.config(state=NORMAL)
    log.delete(1.0, 2.0)
    log.insert(1.0, 'Liðugt\n')
    log.tag_add('fystalinja', '1.0', '2.0')
    log.tag_config('fystalinja', foreground='white', background='green')
    log.config(state=DISABLED)