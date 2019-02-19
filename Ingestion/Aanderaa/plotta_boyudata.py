import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

def csvPlot(frame, root):
    global filnavn
    filnavn = ''
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text='Aanderaa', font='Helvetica 18 bold').pack(side=tk.TOP)
    tk.Label(frame, text='Plot csv').pack(side=tk.TOP, anchor=tk.W)

    menuFrame = tk.Frame(frame)
    menuFrame.pack(side=tk.TOP, anchor=tk.W)

    velMappuBtn = tk.Button(menuFrame, text='Vel Fíl', command=lambda: velFil())
    velMappuBtn.pack(side=tk.LEFT)

    teknaBtn = tk.Button(menuFrame, text='Tekna', command=lambda: tekna(fig, canvas))
    teknaBtn.pack(side=tk.LEFT)

    fig = Figure(figsize=(12, 8), dpi=100)
    plot_frame = tk.Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, anchor=tk.N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)

def tekna(fig, canvas):
    fig.clf()
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3])
    global filnavn
    data = pd.read_csv(filnavn, sep='\t', header=None)
    csvData = []
    tmp = data[0]
    print(tmp[0])
    thisTimestamp = tmp[0]
    thisRow = [tmp[0]]
    del tmp
    for item in data.iterrows(): # Ger dataframe við col
        itemting = item[1]
        if thisTimestamp != itemting[0]:
            thisTimestamp = itemting[0]
            csvData.append(thisRow)
            thisRow = []
            thisRow.append(itemting[0])
        thisRow.append(itemting[2])
    # Finn Col lables
    header = ["Date/Time"]
    for item in data.iterrows():
        tmp = item[1]
        if str(tmp[1]) not in header:
            header.append(str(tmp[1]))
        else:
            break

    df = pd.DataFrame(csvData)
    df.to_csv('Kort_Data/test.csv', index=False)
    #print(csvData)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    print('done')


def velFil():
    global filnavn
    filnavn = filedialog.askopenfile(title='Vel fíl', filetypes = (("txt Fílir", "*.txt"), ("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    print(filnavn)