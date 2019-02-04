import tkinter.messagebox
import tkinter.ttk as ttk
from tkinter import filedialog
import numpy as np
import mysql.connector as db
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import Processing.tekna_kort
from misc.faLog import *


def stovna_okid(frame, root2, db_info, mating_id=1):
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

    teknaButton = Button(buttonsFrame, text='Tekna', command=lambda: dagfor_kort(fig, canvas, latEntry.get(), lonEntry.get()))
    teknaButton.pack(side=LEFT, anchor=N)

    csvButton = Button(buttonsFrame, text='Les frá CSV', command=lambda: lesfraCSV(idEntry.get(), fig, canvas, Okidvariable, db_info, punktir, CRSvariable.get()))
    csvButton.pack(side=LEFT, anchor=N)

    stovnaButton = Button(buttonsFrame, text='Stovna Punkt', command=lambda: innset(idEntry.get(), Okidvariable.get(), latEntry.get(), lonEntry.get(), waypointEntry.get(), dypidEntry.get(), CRSvariable.get(), db_info, punktir))
    stovnaButton.pack(side=RIGHT, anchor=N)

    strikaButton = Button(buttonsFrame, text='Strika Punkt', command=lambda: strika(idLabel_var.get(), db_info, punktir))
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

    idLabel_var = StringVar(value="")
    idLabel = Label(controlsFrame, textvariable=idLabel_var)
    idLabel.pack(side=TOP, anchor=W)


    def change_dropdown(*args):
        pass



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
    dypidEntry = Entry(settings_frame, width=8)
    dypidEntry.pack(side=LEFT)




    kortFrame = Frame(lframe)
    kortFrame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    punktir = ttk.Treeview(rframe)
    punktir.bind("<Double-1>", lambda event, arg=punktir: OnDoubleClick(event, arg, idLabel_var, idEntry, CRSvariable, Okidvariable, latEntry, lonEntry, waypointEntry, dypidEntry, punktir, fig, canvas, db_info))
    scrollbar = Scrollbar(rframe, orient=VERTICAL)
    scrollbar.config(command=punktir.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    #fig = Figure(figsize=(5, 6), dpi=100)
    fig = Figure()
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=kortFrame)

    db_connection = db.connect(**db_info)
    cursor = db_connection.cursor()

    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root2)

    cursor.execute("SELECT * FROM Økir")
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
    dagfor_tree(result, punktir)

    tekstur = """
clf
Tekna kort
linjuSlag=eingin
longdarlinjur=5
breiddarlinjur=6
scatter_std=100""" + scatter_string

    Processing.tekna_kort.les_og_tekna(tekstur, fig, canvas, False)

    db_connection.disconnect()

def lesfraCSV(id_string, fig, canvas, Okidvariable, db_info, tree, CRSvariable):
    filnavn = filedialog.askopenfile(parent=root, title='Les inn csv fíl',
                                     filetypes=(('csv fíl', '*.csv'), ('Allir fílir', '*.*')))
    data = pd.read_csv(filnavn.name, skiprows=22)
    endLinesToDelete = 0
    scatter_string = '\n'
    lonData = data['lon']
    for i, item in enumerate(data['lat']):
        print(item)
        if np.isnan(float(item)):
            break
        else:
            scatter_string = scatter_string + 'scatter=' + item + ',' + lonData[i] + '\n'
            endLinesToDelete += 1

    scatter_string = scatter_string + 'scatter_farv=red'

    db_connection = db.connect(**db_info)

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM WL_Geografisk_okir WHERE Navn=%s", (Okidvariable.get(),))
    geo_result = cursor.fetchall()
    geookid = geo_result[0]
    db_connection.disconnect()
    tekna(fig, canvas, geookid[2], geookid[3], geookid[4], geookid[5], scatter_string)
    innset_var = tkinter.messagebox.askquestion("Innset mátingar", "Ert tú sikkur?", icon='warning')
    if innset_var == 'yes':
        waypoints = data['name']
        db_connection = db.connect(**db_info)
        cursor = db_connection.cursor()
        for i, item in enumerate(data['lat']):
            if np.isnan(float(item)):
                break
            else:
                print(id_string)
                print(Okidvariable.get())
                print(item)
                print(lonData[i])
                print(waypoints[i])
                print(CRSvariable)
                cursor.execute(
                    "INSERT INTO Økir (Máting_ID, Økið, Lat, Lon, Waypoint, Coordinate_Reference_System) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id_string, Okidvariable.get(), item, lonData[i], waypoints[i], CRSvariable))
        db_connection.commit()
        db_connection.disconnect()

    print(data)
    print(data['lat'])

def strika(OKID_ID, db_info, punktir):
    sletta = tkinter.messagebox.askquestion("Strika " + OKID_ID, "Ert tú sikkur?", icon='warning')
    if sletta == 'yes':
        db_connection = db.connect(**db_info)
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM Økir WHERE ID = %s", (OKID_ID, ))
        db_connection.commit()
        cursor.execute("SELECT * FROM Økir")
        result = cursor.fetchall()
        dagfor_tree(result, punktir)
        db_connection.close()


def innset(id_string, Okidvariable, latEntry, lonEntry, waypointEntry, dypidEntry, CRSvariable, db_info, punktir):
    if latEntry == '' or lonEntry == '':
        tkinter.messagebox.showerror('Feilur', 'lat ella lon virði manglar')
    else:
        db_connection = db.connect(**db_info)
        cursor = db_connection.cursor()
        if dypidEntry == '' and waypointEntry == '':
            cursor.execute(
                "INSERT INTO Økir (Máting_ID, Økið, Lat, Lon, Coordinate_Reference_System) VALUES (%s, %s, %s, %s, %s)",
                (id_string, Okidvariable, latEntry, lonEntry, CRSvariable))
        elif dypidEntry == '' and waypointEntry != '':
            cursor.execute(
                "INSERT INTO Økir (Máting_ID, Økið, Lat, Lon, Waypoint, Coordinate_Reference_System) VALUES (%s, %s, %s, %s, %s, %s)",
                (id_string, Okidvariable, latEntry, lonEntry, waypointEntry, CRSvariable))
        elif dypidEntry != '' and waypointEntry == '':
            cursor.execute(
                "INSERT INTO Økir (Máting_ID, Økið, Lat, Lon, Dýpið, Coordinate_Reference_System) VALUES (%s, %s, %s, %s, %s, %s)",
                (id_string, Okidvariable, latEntry, lonEntry, dypidEntry, CRSvariable))
        else:
            cursor.execute(
                "INSERT INTO Økir (Máting_ID, Økið, Lat, Lon, Waypoint, Dýpið, Coordinate_Reference_System) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (id_string, Okidvariable, latEntry, lonEntry, waypointEntry, dypidEntry, CRSvariable))


        db_connection.commit()
        cursor.execute("SELECT * FROM Økir")
        result = cursor.fetchall()
        dagfor_tree(result, punktir)
        db_connection.close()


def dagfor_kort(fig, canvas, latEntry, lonEntry):
    tekstur = """
clf\n
latmax=""" + str(float(latEntry)+0.2) + """
latmin=""" + str(float(latEntry)-0.2) + """
lonmin=""" + str(float(lonEntry)-0.2) + """
lonmax=""" + str(float(lonEntry)+0.2) + """
Tekna kort
linjuSlag=eingin
longdarlinjur=5
breiddarlinjur=6
scatter_std=100
scatter=""" + latEntry + ',' + lonEntry + """
"""
    print(tekstur)
    Processing.tekna_kort.les_og_tekna(tekstur, fig, canvas, True)

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


def dagfor_tree(result, punktir):
    punktir.delete(*punktir.get_children())
    for item in result:
        rekkja = item
        punktir.insert("", 0, text=rekkja[0], values=rekkja[1::])
    punktir.pack(fill=BOTH, expand=True, side=TOP, anchor=W)


def OnDoubleClick(event, arg, idLabel_var, idEntry, CRSvariable, Okidvariable, latEntry, lonEntry, waypointEntry, dypidEntry, tree, fig, canvas, db_info):
    item = tree.identify('item', event.x, event.y)
    item = tree.item(item, "text")
    idLabel_var.set(item)
    print(item)
    db_connection = db.connect(**db_info)
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Økir WHERE ID= %s", (item, ))
    result = cursor.fetchall()
    result = result[0]
    print(result)
    latEntry.delete(0, END)
    latEntry.insert(0, result[3])
    lonEntry.delete(0, END)
    lonEntry.insert(0, result[4])
    idEntry.delete(0, END)
    idEntry.insert(0, result[1])
    waypointEntry.delete(0, END)
    dypidEntry.delete(0, END)
    if result[5]:
        waypointEntry.insert(0, result[5])
    if result[6]:
        waypointEntry.insert(0, result[6])
    CRSvariable.set(result[7])
    if Okidvariable.get() != result[2]:
        Okidvariable.set(result[2])
    cursor.execute("SELECT * FROM WL_Geografisk_okir WHERE Navn=%s", (Okidvariable.get(),))
    geo_result = cursor.fetchall()
    geookid = geo_result[0]
    cursor.execute("SELECT * FROM Økir WHERE Máting_ID = %s", (idEntry.get(),))
    geo_result = cursor.fetchall()
    db_connection.disconnect()
    scatter_string = '\n'
    for item in geo_result:
        scatter_string = scatter_string + 'scatter=' + item[3] + ',' + item[4] + '\n'
    scatter_string = scatter_string + 'scatter_farv=red\nscatter=' + result[3] + ',' + result[4] + '\nscatter_farv=blue'
    tekna(fig, canvas, geookid[2], geookid[3], geookid[4], geookid[5], scatter_string)
