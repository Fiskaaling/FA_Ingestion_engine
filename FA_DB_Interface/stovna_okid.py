import tkinter.messagebox
import tkinter.ttk as ttk
import numpy as np
import mysql.connector as db
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import Processing.tekna_kort
from misc.faLog import *


def stovna_okid(frame, root2, db_info, mating_id=1):
    global root
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Stovna nýtt økið', font='Helvetica 18 bold').pack(side=TOP)

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

    teknaButton = Button(buttonsFrame, text='Tekna', command=lambda: tekna(fig, canvas, latEntry.get(), lonEntry.get(),
                                                                           db_info, idEntry.get()))
    teknaButton.pack(side=LEFT, anchor=N)

    stovnaButton = Button(buttonsFrame, text='Stovna Punkt', command=lambda: innset(idEntry.get(), Okidvariable.get(), latEntry.get(), lonEntry.get(), waypointEntry.get(), dypidEntry.get(), CRSvariable.get(), db_info))
    stovnaButton.pack(side=RIGHT, anchor=N)

    strikaButton = Button(buttonsFrame, text='Strika Punkt', command=lambda: strika(navnEntry.get(), db_user, db_password, db_host))
    strikaButton.pack(side=RIGHT, anchor=N)


    # Hettar ger eina dropdown lista av møguligum Geografiskum økum --- TODO Møguliga broyt hettar til eina Combo box
    geookidFrame = Frame(controlsFrame)
    geookidFrame.pack(side=TOP, anchor=W, fill=X)
    Label(geookidFrame, text='Økið:').pack(side=LEFT)
    db_connection = db.connect(**db_info)
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM WL_Geografisk_okir")
    result = cursor.fetchall()
    GeoOkir = []
    for row in result:
        GeoOkir.append(row[0])
    Okidvariable = StringVar(geookidFrame)
    w = OptionMenu(geookidFrame, Okidvariable, *GeoOkir)
    Okidvariable.set("Føroyar")  # default value
    w.pack(side=RIGHT)

    # Hettar ger eina dropdown lista av møguligum CRS
    crsFrame = Frame(controlsFrame)
    crsFrame.pack(side=TOP, anchor=W, fill=X)
    Label(crsFrame, text='Coordinate Reference System:').pack(side=LEFT)
    cursor.execute("SELECT * FROM wl_coordinate_reference_systems")
    result = cursor.fetchall()
    CRS = []
    for row in result:
        CRS.append(row[0])
    CRSvariable = StringVar(crsFrame)
    w2 = OptionMenu(crsFrame, CRSvariable, *CRS)
    CRSvariable.set("WGS 84 (GPS)")  # default value
    w2.pack(side=RIGHT)

    # ID entry -- Todo ger read only
    idFrame = Frame(controlsFrame)
    idFrame.pack(side=TOP, anchor=W, fill=X)
    Label(idFrame, text='Máting ID:').pack(side=LEFT)
    idEntry = Entry(idFrame, width=10)
    idEntry.pack(side=RIGHT)
    idEntry.insert(0, str(mating_id))


    def change_dropdown(*args):
            print(Okidvariable.get())
            db_connection = db.connect(**db_info)
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM WL_Geografisk_okir WHERE Navn=%s", (Okidvariable.get(), ))
            result = cursor.fetchall()
            geookid = result[0]
            cursor.execute("SELECT * FROM Økir WHERE Máting_ID = %s", (idEntry.get(), ))
            result = cursor.fetchall()
            db_connection.disconnect()
            scatter_string = '\n'
            for item in result:
                scatter_string = scatter_string + 'scatter=' + item[3] + ',' + item[4] + '\n'
            tekna(fig, canvas, geookid[2], geookid[3], geookid[4], geookid[5], scatter_string)


    Okidvariable.trace('w', change_dropdown)

    Label(controlsFrame, text=" ").pack(side=TOP)


    koordinatframe = Frame(controlsFrame)
    koordinatframe.pack(side=TOP, anchor=W)
    Label(koordinatframe, text='Lat:').pack(side=LEFT)
    latEntry = Entry(koordinatframe, width=10)
    latEntry.pack(side=LEFT)
    latEntry.insert(0, str(62 + np.random.randn()*0.1))
    Label(koordinatframe, text='Lon:').pack(side=LEFT)
    lonEntry = Entry(koordinatframe, width=10)
    lonEntry.pack(side=LEFT)
    lonEntry.insert(0, str(-7 + np.random.randn()*0.1))

    settings_frame = Frame(controlsFrame)
    settings_frame.pack(side=TOP, anchor=W)
    Label(settings_frame, text='Waypoint:').pack(side=LEFT)
    waypointEntry = Entry(settings_frame,width=5)
    waypointEntry.pack(side=LEFT)

    Label(settings_frame, text='Dýpið:').pack(side=LEFT)
    dypidEntry = Entry(settings_frame, width=7)
    dypidEntry.pack(side=LEFT)




    kortFrame = Frame(lframe)
    kortFrame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    global punktir
    punktir = ttk.Treeview(rframe)
    punktir.bind("<Double-1>", lambda event, arg=punktir: OnDoubleClick(event, arg, navnEntry, styttingEntry, latminEntry, latmaxEntry, lonminEntry, lonmaxEntry, db_host, db_user, db_password, fig, canvas))
    scrollbar = Scrollbar(rframe, orient=VERTICAL)
    scrollbar.config(command=punktir.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    #fig = Figure(figsize=(5, 6), dpi=100)
    fig = Figure()

    global ax
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=kortFrame)

    db_connection = db.connect(**db_info)
    cursor = db_connection.cursor()

    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

    cursor.execute("SELECT * FROM Økir WHERE Máting_ID = %s", (idEntry.get(), ))
    result = cursor.fetchall()
    kolonnir = cursor.column_names
    punktir["columns"] = kolonnir[1::]
    #punktir.column("#0", width=100)
    for i in range(1, len(kolonnir)):
        punktir.heading(kolonnir[i], text=kolonnir[i])
        #punktir.column("#" + str(i), width=100)
    scatter_string = '\n'
    for item in result:
        scatter_string = scatter_string + 'scatter=' + item[3] + ',' + item[4] + '\n'
    dagfor_tree(result)

    tekstur = """
clf
Tekna kort
linjuSlag=eingin
longdarlinjur=5
breiddarlinjur=6
scatter_std=100""" + scatter_string

    Processing.tekna_kort.les_og_tekna(tekstur, fig, canvas, False)

    db_connection.disconnect()



def strika(Navn, db_user, db_password, db_host):
    sletta = tkinter.messagebox.askquestion("Strika " + Navn, "Ert tú sikkur?", icon='warning')
    if sletta == 'yes':
        db_connection = db.connect(user=db_user, password=db_password, database='fa_db', host=db_host)
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM WL_Geografisk_okir WHERE Navn = \'" + Navn + "\'", )
        db_connection.commit()
        cursor.execute("SELECT * FROM WL_Geografisk_okir")
        result = cursor.fetchall()
        dagfor_tree(result)
        db_connection.close()


def innset(id, Okidvariable, latEntry, lonEntry, waypointEntry, dypidEntry, CRSvariable, db_info):
    if latEntry == '' or lonEntry == '':
        tkinter.messagebox.showerror('Feilur', 'lat ella lon virði manglar')
    else:
        db_connection = db.connect(**db_info)
        cursor = db_connection.cursor()
        if dypidEntry == '' and waypointEntry == '':
            cursor.execute(
                "INSERT INTO Økir (Máting_ID, Økið, Lat, Lon, Coordinate_Reference_System) VALUES (%s, %s, %s, %s, %s)",
                (id, Okidvariable, latEntry, lonEntry, CRSvariable))
        elif dypidEntry == '' and waypointEntry != '':
            cursor.execute(
                "INSERT INTO Økir (Máting_ID, Økið, Lat, Lon, Waypoint, Coordinate_Reference_System) VALUES (%s, %s, %s, %s, %s, %s)",
                (id, Okidvariable, latEntry, lonEntry, waypointEntry, CRSvariable))
        elif dypidEntry != '' and waypointEntry == '':
            cursor.execute(
                "INSERT INTO Økir (Máting_ID, Økið, Lat, Lon, Dýpið, Coordinate_Reference_System) VALUES (%s, %s, %s, %s, %s, %s)",
                (id, Okidvariable, latEntry, lonEntry, dypidEntry, CRSvariable))
        else:
            cursor.execute(
                "INSERT INTO Økir (Máting_ID, Økið, Lat, Lon, Waypoint, Dýpið, Coordinate_Reference_System) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (id, Okidvariable, latEntry, lonEntry, waypointEntry, dypidEntry, CRSvariable))


        db_connection.commit()
        cursor.execute("SELECT * FROM Økir")
        result = cursor.fetchall()
        dagfor_tree(result)
        db_connection.close()




def tekna(fig, canvas, Latmin, Latmax, Lonmin, Lonmax, Additional_commands):
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
scatter_std=100
""" + Additional_commands
    Processing.tekna_kort.les_og_tekna(tekstur, fig, canvas, True)

def dagfor_tree(result):
    global punktir
    punktir.delete(*punktir.get_children())
    for i in range(len(result)):
        rekkja = result[i]
        punktir.insert("", 0, text=rekkja[0], values=rekkja[1::])
    punktir.pack(fill=BOTH, expand=True, side=TOP, anchor=W)


def OnDoubleClick(event, tree, navnEntry, styttingEntry, latminEntry, latmaxEntry, lonminEntry, lonmaxEntry, db_info, fig, canvas):
    item = tree.identify('item', event.x, event.y)
    item = tree.item(item, "text")
    navnEntry.delete(0, END)
    navnEntry.insert(0, item)
    db_connection = db.connect(**db_info)
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM WL_Geografisk_okir WHERE Navn=\'" + item + "\'")
    result = cursor.fetchall()
    db_connection.close()
    result = result[0]
    styttingEntry.delete(0, END)
    styttingEntry.insert(0, result[1])
    latminEntry.delete(0, END)
    latminEntry.insert(0, result[2])
    latmaxEntry.delete(0, END)
    latmaxEntry.insert(0, result[3])
    lonminEntry.delete(0, END)
    lonminEntry.insert(0, result[4])
    lonmaxEntry.delete(0, END)
    lonmaxEntry.insert(0, result[5])
    tekna(fig, canvas, result[2], result[3], result[4], result[5])
