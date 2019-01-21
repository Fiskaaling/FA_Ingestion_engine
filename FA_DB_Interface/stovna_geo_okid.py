from tkinter import filedialog
from misc.faLog import *
import mysql.connector as db


def stovna_geo_okid(frame, root2, db_host, db_user, db_password):
    global root
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Stovna nýtt Geografiskt økið', font='Helvetica 18 bold').pack(side=TOP)
    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)