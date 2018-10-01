from tkinter import *

def roknaQuiver(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    Label(frame, text='Streymmátingar', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Rokna Quiver Data').pack(side=TOP, anchor=W)

    velMappuBtn = Button(frame, text='Vel Mappu')
    velMappuBtn.pack(side=TOP, anchor=W)

    Label(frame, text='').pack(side=TOP)
    tilFraFrame = Frame(frame)
    tilFraFrame.pack(side=TOP, anchor=W, expand=False, fill=Y)
    Label(tilFraFrame, text='Frá túr index').pack(side=LEFT)
    fraIndex = Entry(tilFraFrame, width=2)
    fraIndex.pack(side=LEFT)
    fraIndex.insert(0,'1')
    Label(tilFraFrame, text='Til túr index').pack(side=LEFT)
    tilIndex = Entry(tilFraFrame, width=2)
    tilIndex.pack(side=LEFT)
    tilIndex.insert(0, '12')

    Label(frame, text='').pack(side=TOP, anchor=W)

    binSettingsFrame = Frame(frame)
    binSettingsFrame.pack(side=TOP, anchor=W, expand=False, fill=Y)
    Label(binSettingsFrame, text='Bins at rokna miðal frá ').pack(side=LEFT)
    bins = Entry(binSettingsFrame, width=60)
    bins.pack(side=LEFT)
    bins.insert(0, str(list(range(9, 9+15))))

    roknaBtn = Button(frame, text='Rokna')
    roknaBtn.pack(side=TOP, anchor=W)

    Label(frame, text='').pack(side=TOP, anchor=W)
    teknaKortBtn = Button(frame, text='Tekna Kort')
    teknaKortBtn.pack(side=TOP, anchor=W)

    log_frame = Frame(frame, height=300, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)

    global log
    log = Text(log_frame, bg='#888888')
    log.pack(fill=X, expand=True)
    log.insert(1.0, 'Klárt\n')
    log.tag_add('fystalinja', '1.0', '2.0')
    log.tag_config('fystalinja', foreground='white', background='green')
    log.config(state=DISABLED)