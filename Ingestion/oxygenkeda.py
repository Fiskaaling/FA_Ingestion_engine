from tkinter import *
from tkinter import filedialog

def decimering(frame, root2):
    global root
    global filnavn
    filnavn = '/home/johannus/Documents/FA_Ingestion_engine/Kort_Data/Syðradalur.txt'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Landsverk', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Veðurstøðir').pack(side=TOP, anchor=W)