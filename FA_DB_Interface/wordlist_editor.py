#from misc.faLog import *

import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector as db
import mysql

def scrub(table_name):
    return ''.join( chr for chr in table_name if chr.isalnum() )

def  wl_edtitor(frame, root, db_info):
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text='Wordlist Editor', font='Helvetica 18 bold').pack(side=tk.TOP)

    leftFrame = tk.Frame(frame)
    leftFrame.pack(side=tk.LEFT, anchor=tk.N, expand=tk.TRUE, fill=tk.BOTH)

    rightFrame = tk.Frame(frame)
    rightFrame.pack(side=tk.LEFT, anchor=tk.N, expand=tk.TRUE, fill=tk.BOTH)

    buttonsFrame = tk.Frame(rightFrame)
    buttonsFrame.pack(side=tk.TOP, anchor=tk.W)

    innsetButton = tk.Button(buttonsFrame, text='Innset Orð', command=lambda: innset(db_info, ordEntry, aktivTabelVar.get(), ordTree))
    innsetButton.pack(side=tk.LEFT)

    stikaButton = tk.Button(buttonsFrame, text='Strika Orð', command=lambda: strika(db_info, ordEntry, aktivTabelVar.get(), ordTree))
    stikaButton.pack(side=tk.LEFT)

    ordEntry = tk.Entry(buttonsFrame, width=30)
    ordEntry.pack(side=tk.LEFT)


    tk.Label(buttonsFrame, text='Aktiv tabel:').pack(side=tk.LEFT)

    ordalistarTree = ttk.Treeview(leftFrame)
    ordalistarTree.pack(fill=tk.BOTH, expand=True)
    ordalistarTree.bind("<Double-1>",
                 lambda event, arg=ordalistarTree: doubleClickTabel(event, ordalistarTree, arg, aktivTabelVar, db_info, ordTree))

    aktivTabelVar = tk.StringVar(value="")
    tk.Label(buttonsFrame, textvariable=aktivTabelVar).pack(side=tk.LEFT)

    ordTree = ttk.Treeview(rightFrame)
    ordTree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    ordTree.bind("<Double-1>", lambda event, arg=ordTree: doubleClickOrd(event, arg, ordTree, ordEntry))


    db_connection = db.connect(**db_info)
    cursor = db_connection.cursor()

    # Finn tabellir ið hava navn wl
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    list_of_wl = []
    for item in result:
        if 'wl_' in item[0]:
            list_of_wl.append(item[0])

    # Finn wl ið einans hava eina kolonnu
    for item in list_of_wl:
        cursor.execute("SELECT Count(*) FROM INFORMATION_SCHEMA.Columns where TABLE_NAME = %s", (item, ))
        result = cursor.fetchall()
        result = result[0]
        if result[0] == 1:
            ordalistarTree.insert("", 0, text=item)

    db_connection.disconnect()


def strika(db_info, input_ord, tabell, ordTree):
    if input_ord.get() != '':
        sletta = tk.messagebox.askquestion("Strika " + input_ord.get(), "Ert tú sikkur?", icon='warning')
        if sletta == 'yes':
            db_connection = db.connect(**db_info)
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM " + tabell)
            result = cursor.fetchall()
            kolonnir = cursor.column_names
            sqlstring = "DELETE FROM `" + tabell + "` WHERE `" + kolonnir[0] + "` = '" + input_ord.get() + "'"
            try:
                cursor.execute(sqlstring)
                db_connection.commit()
            except mysql.connector.Error as err:
                print("Striking miseyndaðist, tað er nokk onkurt í peikar á hettar\n\n" + str(err))
                tk.messagebox.showerror("Error", "Striking miseyndaðist, tað er nokk onkurt í peikar á hettar\n\n" + str(err))

            input_ord.delete(0, tk.END)
            ordTree.delete(*ordTree.get_children())
            #cursor.execute("SELECT * FROM " + scrub(tabell))
            cursor.execute('SELECT * FROM {}'.format(tabell))
            result = cursor.fetchall()
            for word in result:
                ordTree.insert("", 0, text=word[0])

            db_connection.disconnect()


def innset(db_info, input_ord, tabell, ordTree):
    db_connection = db.connect(**db_info)
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM " + tabell)
    result = cursor.fetchall()
    kolonnir = cursor.column_names
    sqlstring = "INSERT INTO " + tabell + " (" + kolonnir[0] + ") VALUES ('" + input_ord.get() + "')"
    cursor.execute(sqlstring)
    db_connection.commit()

    input_ord.delete(0, tk.END)
    ordTree.delete(*ordTree.get_children())
    cursor.execute("SELECT * FROM " + tabell)
    result = cursor.fetchall()
    for word in result:
        ordTree.insert("", 0, text=word[0])

    db_connection.disconnect()


def doubleClickOrd(event, arg, tree, ordEntry):
    item = tree.identify('item', event.x, event.y)
    item = tree.item(item, "text")
    ordEntry.delete(0, tk.END)
    ordEntry.insert(0, item)


def doubleClickTabel(event, arg, tree, aktivTabelVar, db_info, ordTree):
    item = tree.identify('item', event.x, event.y)
    item = tree.item(item, "text")
    aktivTabelVar.set(item)
    ordTree.delete(*ordTree.get_children())
    db_connection = db.connect(**db_info)
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM " + item)
    result = cursor.fetchall()
    kolonnir = cursor.column_names
    ordTree.heading('#0', text=kolonnir[0], anchor='center')
    for word in result:
        ordTree.insert("", 0, text=word[0])

    db_connection.disconnect()
