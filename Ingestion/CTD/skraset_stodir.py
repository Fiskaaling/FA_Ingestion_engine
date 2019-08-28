import os
import numpy as np
from misc.faLog import *
from FA_DB_Interface.db_misc import get_dbinfo
import mysql.connector as db

def skraset_stodir(frame, root2):
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Skráset støðir').pack(side=TOP, anchor=W)
    ss_gui_control(root, frame)


def ss_gui_control(root, frame):
    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, anchor=W)
    Label(menuFrame, text="Valdur fílur:").pack(side=LEFT, anchor=N)
    textBox = Text(menuFrame, height=1, width=5)
    textBox.pack(side=LEFT, anchor=N)
    textBox.insert(END, '28')
    CTD_filir_frame = Frame(frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    CTD_filir_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    GPS_waypoints_frame = Frame(frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    GPS_waypoints_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    datasheet_frame = Frame(frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    datasheet_frame.pack(fill=BOTH, expand=True, side=RIGHT, anchor=N)

    log_frame = Frame(datasheet_frame, height=300, width=600, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

    vald_ctd_mappa = "./Ingestion/CTD/Lokalt_Data/2019-06-04/75_All_ASCII_Out"
    textsize = 16
    font = ("Courier", textsize)
    # Hettar fyllur ctd fílir kolonnina
    ctd_filnavn = os.listdir(vald_ctd_mappa)
    ctd_filnavn.sort()
    for filnavn in ctd_filnavn:
        print(filnavn)
        if os.path.isfile(vald_ctd_mappa + '/' + filnavn):
            Label(CTD_filir_frame, text=filnavn, font=font).pack(side=TOP, anchor=W)


    # Hettar er til gps waypoints
    # Fyst kanna um mátingin er í DB
    db_info = get_dbinfo()
    db_connection = db.connect(**db_info)
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Økir WHERE Máting_ID=" + textBox.get("1.0",END))
    results = cursor.fetchall()
    kolonnir = cursor.column_names
    #punktir["columns"] = kolonnir[1::]
    # punktir.column("#0", width=100)
    for result in results:
        print(result)
        Label(GPS_waypoints_frame, text=result[5] + ' ' + str(np.round(float(result[3]), 5)) + ' ' + str(np.round(float(result[4]), 5)), font=font).pack(side=TOP, anchor=W)
    #    punktir.heading(kolonnir[i], text=kolonnir[i])
    #    # punktir.column("#" + str(i), width=100)

    main_vald_ctd_mappa = os.path.dirname(vald_ctd_mappa)
    ctd_main_filnavn = os.listdir(main_vald_ctd_mappa)
    for filnavn in ctd_main_filnavn:
        if '.csv' in filnavn:
            pass