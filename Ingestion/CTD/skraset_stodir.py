from misc.faLog import *

def skraset_stodir(frame, root2):
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Skráset støðir').pack(side=TOP, anchor=W)