import tkinter as tk


def csvPlot(frame, root):
    global filnavn
    filnavn = ''
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=tk.TOP)
    tk.Label(frame, text='Plot Ascii').pack(side=tk.TOP, anchor=tk.W)
