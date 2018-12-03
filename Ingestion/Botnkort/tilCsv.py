from tkinter import filedialog
from misc.faLog import *
import pandas as pd

def init(ingestion_listbox):
    streymmatingar_stationert = ingestion_listbox.insert("", 0, text="Botnkort")
    ingestion_listbox.insert(streymmatingar_stationert, "end", text='Til CSV')


def check_click(item, RightFrame, root):
    if item == 'Til CSV':
        tilcsv(RightFrame, root)

def tilcsv(frame, root2):
    global root
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Botnkort', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Til CSV').pack(side=TOP, anchor=W)
    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    Button(menuFrame, text='Vel Fíl', command=lambda: velFilir()).pack(side=LEFT)
    Button(menuFrame, text='Rokna', command=lambda: tilCSV()).pack(side=LEFT)

    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

def tilCSV():
    global filnavn
    for i in range(len(filnavn)):
        data = pd.read_fwf(filnavn[i], skiprows=2)
        cols = data.columns.values
        print(data.iloc[:, 0])
        print(data.iloc[:, 1])
        print(data.columns.values)
        punktirAtGoyma = pd.DataFrame({'lon': data.iloc[:, 0], 'lat': data.iloc[:, 1], 'd': data.iloc[:, 2]})
        punktirAtGoyma.to_csv(filnavn[0]+'.csv', index=False)
    print('ok')

def velFilir(typa='std'):
    global filnavn
    print('Vel fíl ' + typa)
    if typa == 'std':
        filnavn = filedialog.askopenfilenames(title='Vel fílir', filetypes=(("txt Fílir", "*.txt"),
                                                                            ("csv Fílir", "*.csv"),
                                                                            ("all files", "*.*")))
    else:
        filnavn = filedialog.askopenfilenames(title='Vel ' + typa + ' fílir', filetypes=((typa + " Fílir", "*" + typa),
                                                                                                ("all files", "*.*")))