from tkinter import filedialog
from misc.faLog import *
import pandas as pd
# Kodan samlar dataði frá ymisum fílum til ein


def samla(frame, root2):
    global root
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Botnkort', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Samla til ein fíl').pack(side=TOP, anchor=W)
    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    Button(menuFrame, text='Vel Fíl', command=lambda: velFilir()).pack(side=LEFT)
    Button(menuFrame, text='Rokna', command=lambda: tilCSV()).pack(side=LEFT)

    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

def tilCSV():
    log_b()
    global filnavn
    lon = []
    lat = []
    d = []
    for i in range(len(filnavn)):
        print(filnavn[i])
        data = pd.read_csv(filnavn[i])
        for index, row in data.iterrows():
            lat.append(row['lat'])
            lon.append(row['lon'])
            d.append(row['d'])
        #lat.append(data.iloc[:, 1].values)
        #lon.append(data.iloc[:, 0].values)
        #d.append(data.iloc[:, 2].values)
    punktirAtGoyma = pd.DataFrame({'lon': lon, 'lat': lat, 'd': d})
    punktirAtGoyma.to_csv('samla.csv', index=False)
    print('ok')
    log_e()

def velFilir(typa='std'):
    global filnavn
    print('Vel fíl ' + typa)
    if typa == 'std':
        filnavn = filedialog.askopenfilenames(title='Vel fílir', filetypes=(("csv Fílir", "*.csv"),
                                                                            ("txt Fílir", "*.txt"),
                                                                            ("all files", "*.*")))
    else:
        filnavn = filedialog.askopenfilenames(title='Vel ' + typa + ' fílir', filetypes=((typa + " Fílir", "*" + typa),
                                                                                                ("all files", "*.*")))