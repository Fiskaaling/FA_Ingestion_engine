from tkinter import filedialog
from misc.faLog import *
import mysql.connector as db
import tkinter.ttk as ttk
import Processing.tekna_kort
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from misc.faLog import *


def stovna_geo_okid(frame, root2, db_host, db_user, db_password):
    global root
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Stovna nýtt Geografiskt økið', font='Helvetica 18 bold').pack(side=TOP)

    mainFrame = Frame(frame)
    mainFrame.pack(side=TOP, fill=BOTH, expand=TRUE, anchor=N)

    lframe = Frame(mainFrame)
    lframe.pack(side=LEFT, fill=BOTH, expand=TRUE, anchor=N)

    rframe = Frame(mainFrame)
    rframe.pack(side=LEFT, fill=BOTH, expand=TRUE, anchor=N)

    controlsFrame = Frame(lframe)
    controlsFrame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    buttonsFrame = Frame(controlsFrame)
    buttonsFrame.pack(side=TOP, fill=X)

    teknaButton = Button(buttonsFrame, text='Tekna', command=lambda: tekna(fig, canvas, latminEntry.get(), latmaxEntry.get(),
                                                                           lonminEntry.get(), lonmaxEntry.get()))
    teknaButton.pack(side=LEFT, anchor=N)

    stovnaButton = Button(buttonsFrame, text='Stovna Økið')
    stovnaButton.pack(side=RIGHT, anchor=N)

    strikaButton = Button(buttonsFrame, text='Strika Økið')
    strikaButton.pack(side=RIGHT, anchor=N)

    navnFrame = Frame(controlsFrame)
    navnFrame.pack(side=TOP, anchor=W)
    Label(navnFrame, text='Navn:').pack(side=LEFT)
    navnEntry = Entry(navnFrame, width=50)
    navnEntry.pack(side=LEFT)

    styttingFrame = Frame(controlsFrame)
    styttingFrame.pack(side=TOP, anchor=W)
    Label(styttingFrame, text='Stytting:').pack(side=LEFT)
    styttingEntry = Entry(styttingFrame, width=10)
    styttingEntry.pack(side=LEFT)

    latFrame = Frame(controlsFrame)
    latFrame.pack(side=TOP, anchor=W)
    Label(latFrame, text='Latmin:').pack(side=LEFT)
    latminEntry = Entry(latFrame,width=10)
    latminEntry.pack(side=LEFT)
    latminEntry.insert(0, "61.35")
    Label(latFrame, text='Latmax:').pack(side=LEFT)
    latmaxEntry = Entry(latFrame,width=10)
    latmaxEntry.pack(side=LEFT)
    latmaxEntry.insert(0, "62.4")

    lonFrame = Frame(controlsFrame)
    lonFrame.pack(side=TOP, anchor=W)
    Label(lonFrame, text='Lonmin:').pack(side=LEFT)
    lonminEntry = Entry(lonFrame,width=10)
    lonminEntry.pack(side=LEFT)
    lonminEntry.insert(0, "-7.7")

    Label(lonFrame, text='Lonmax:').pack(side=LEFT)
    lonmaxEntry = Entry(lonFrame,width=10)
    lonmaxEntry.pack(side=LEFT)
    lonmaxEntry.insert(0, "-6.2")




    kortFrame = Frame(lframe)
    kortFrame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    punktir = ttk.Treeview(rframe)
    scrollbar = Scrollbar(rframe, orient=VERTICAL)
    scrollbar.config(command=punktir.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    fig = Figure(figsize=(5, 6), dpi=100)
    global ax
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=kortFrame)

    db_connection = db.connect(user=db_user, password=db_password, database='fa_db', host=db_host)
    cursor = db_connection.cursor()

    cursor.execute("SELECT * FROM WL_Geografisk_okir")
    result = cursor.fetchall()
    kolonnir = cursor.column_names
    punktir["columns"] = kolonnir
    for i in range(len(kolonnir)):
        punktir.heading(kolonnir[i], text=kolonnir[i])
        punktir.column("#" + str(i), width=100)
    punktir.pack(fill=BOTH, expand=True, side=TOP, anchor=W)



    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

    tekstur = """
clf
Tekna kort
linjuSlag=eingin
longdarlinjur=5
breiddarlinjur=6
"""

    Processing.tekna_kort.les_og_tekna(tekstur, fig, canvas, True)

    db_connection.disconnect()
    print(cursor.column_names)
    print(result)

def tekna(fig, canvas, Latmin, Latmax, Lonmin, Lonmax):
    tekstur = """
clf\n
latmax=""" + Latmax + """
latmin=""" + Latmin + """
lonmin=""" + Lonmin + """
lonmax=""" + Lonmax + """
Tekna kort
linjuSlag=eingin
longdarlinjur=5
breiddarlinjur=6
"""
    Processing.tekna_kort.les_og_tekna(tekstur, fig, canvas, True)
