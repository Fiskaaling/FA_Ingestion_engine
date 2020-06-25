import pandas as pd
import numpy as np
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import simpledialog
from tkinter import filedialog
import platform


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        Frame.pack(self, side=BOTTOM)
        self.init_window()

    def init_window(self):
        self.master.title("Fiskaaling Ingestion Engine")
        self.pack(fill=BOTH, expand=1)
        main_frame = Frame(self, borderwidth=1)
        main_frame.pack(fill=BOTH, expand=False, side=TOP)

    @staticmethod
    def client_exit(self):
        exit()


def finnmax(data, under):
    maxi = []
    for i in range(len(data.iloc[1, :])):
        thisrow = data.iloc[:, i]
        maxc = -1000
        maxci = -1000
        for j, col in enumerate(thisrow):
            if (j > under) and not under == 0:
                continue
            if col > maxc:
                maxc = col
                maxci = j
        maxi.append(maxci)
    return maxi


def finnNextLargeDiff(data, limit=100):
    diff_data = np.diff(data)
    for i, d in enumerate(diff_data):
        if abs(d) > limit:
            return i
    return -1

def velFil():
    global filename
    global dataign
    filename = filedialog.askopenfile(title='Vel fíl', filetypes = (("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    print(filename)
    print("Reading data")
    data = pd.read_csv(filename)
    data = data.iloc[::-1]  # Eg haldi at hettar flippar
    print("Done")
    ignore_last = 50
    ignore_first = 400
    dataign = data.iloc[ignore_first:-ignore_last, :]
    dataign = pd.DataFrame(np.array(dataign))
    global fig
    global figS
    global ax
    global axS
    fig.clf()
    figS.clf()
    ax = fig.add_subplot(111)
    axS = figS.add_subplot(111)
    global max_index
    global lines
    global yNumbers
    max_index = finnmax(dataign, 800)
    yNumbers = np.arange(len(dataign.iloc[:, 1]))
    lines = ax.plot(max_index)
    ax.imshow(dataign, cmap='plasma', vmin=-120)
    canvas.draw()
    canvasSingle.draw()


def splitta_fil():
    filename = filedialog.askopenfile(title='Vel fíl', filetypes=(("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    data = pd.read_csv(filename)
    pings_per_file = 8000
    pings_left = len(data.iloc[1,:])
    counter = 0
    while pings_left > 0:
        if pings_left > pings_per_file:
            df_toWrite = data.iloc[:, len(data.iloc[1, :])-pings_left:len(data.iloc[1,:])-pings_left+pings_per_file]
        else:
            df_toWrite = data.iloc[:, len(data.iloc[1, :])-pings_left:]
        print('Writing file: ' + filename[:-4]+'_' + str(counter) + '.csv')
        pd.DataFrame.to_csv(df_toWrite, filename[:-4]+'_' + str(counter) + '.csv', index=False)
        pings_left -= pings_per_file
        print('Job Done!')
        counter += 1

    print(data)
    print(len(data.iloc[:,1]))
    print(len(data.iloc[1,:]))



root = Tk()
root.geometry("1200x800")
app = Window(root)

menu_frame = Frame(app)
menu_frame.pack(side=TOP, anchor=N)
velMappuBtn = Button(menu_frame, text='Vel Fíl', command=lambda: velFil())
velMappuBtn.pack(side=LEFT)

Label(menu_frame, text='Cursor position: ').pack(side=LEFT)
cLabel = Label(menu_frame, text='0')
cLabel.pack(side=LEFT)


splittaFilarBtn = Button(menu_frame, text='Splitta Fílir', command=lambda: splitta_fil())
splittaFilarBtn.pack(side=RIGHT, anchor=E)
fig = Figure(figsize=(12, 8), dpi=100)
figS = Figure(figsize=(8, 8), dpi=100)
singlePlot_frame = Frame(app, borderwidth=1, width=50, highlightbackground="green", highlightcolor="green", highlightthickness=1)
singlePlot_frame.pack(fill=Y, expand=False, side=LEFT, anchor=N)
plot_frame = Frame(app, borderwidth=1,width=100, highlightbackground="green", highlightcolor="green", highlightthickness=1)
plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvasSingle = FigureCanvasTkAgg(figS, master=singlePlot_frame)
fig.clf()
figS.clf()
ax = fig.add_subplot(111)
axS = figS.add_subplot(111)
axS.plot([1,2,3,2,6])

global max_index
global lines
global filename
filename = "/home/johannus/Documents/data/Echolodd/D20200224-T1112321.csv"

print("Reading data")



canvas.draw()
canvas.get_tk_widget().pack(fill=BOTH, expand=1)
canvasSingle.draw()
canvasSingle.get_tk_widget().pack(fill=BOTH, expand=1)
print('done')
cursor = 0
scatters = ax.scatter(0, 100, c='white')
#yNumbers = np.arange(len(dataign.iloc[:, 1]))
global yNumbers
yNumbers = np.arange(10)

answer = 0
max_ping_index = 0
thisPing = (1,2,3)
save_changes = False

visible_min = 0
visible_max = 1500
visible_range = visible_max - visible_min
ax.set_xlim([visible_min, visible_max])
okValues = []


def drawS(figS, dataign, yNumbers, bl_index, cursor, answer):
    figS.clf()
    axS = figS.add_subplot(111)
    axS.plot(dataign.iloc[:, cursor], yNumbers * -1)
    axS.axhline(y=-bl_index, c='k')
    axS.axhline(y=-float(answer), c='red')
    canvasSingle.draw()


pf = platform.platform()
if 'Linux' in pf:
    print('kul')

def key(event):
    global max_ping_index
    global answer
    global lines
    global scatters
    global cursor
    global figS
    global save_changes
    global axS
    global thisPing
    global okValues
    print(event.keysym)
    if event.keysym == '1':
        okValues.append(cursor)
        ax.scatter(cursor, 0, c='g')
    if event.keysym == 'onehalf':
        cursor = int(simpledialog.askstring("Input", "Flyt cursara til", parent=app))
        visible_min = cursor - 500
        if visible_min < 0:
            visible_min = 0
        visible_max = cursor + 500
        ax.set_xlim([visible_min, visible_max])
    if event.keysym == 'KP_0' or event.keysym == '0':
        cursor = 0
    if event.keysym == 'Right':
        cursor = cursor + 1
        drawS(figS, dataign, yNumbers, max_index[cursor], cursor, answer)
    if event.keysym == 'Left':
        cursor = cursor - 1
        drawS(figS, dataign, yNumbers, max_index[cursor], cursor, answer)
    if event.keysym == 'Up':
        max_ping_index += 1
        save_changes = True
        drawS(figS, dataign, yNumbers, max_ping_index, cursor, answer)
        axS.plot(thisPing, yNumbers * -1)
        # axS.axhline(y=-max_ping_index, c='k')
        axS.axhline(y=-float(answer), c='red')
    if event.keysym == 's':
        toSave = pd.DataFrame(max_index)
        toSave.to_csv(filename[:-4] + 'maxi.csv')
    if event.keysym == 'KP_Decimal' or event.keysym == 'comma':
        answer = simpledialog.askstring("Input", "Botnurin er undur?", parent=app)
        visible_max = cursor + 500
        max_index[cursor:visible_max] = finnmax(dataign.iloc[:,cursor:visible_max], float(answer))
        l = lines[0]
        l.remove()
        lines = ax.plot(max_index, c='lime')
    elif event.keysym == 'Tab':
        if save_changes:
            print('Do something')
            print(max_index[cursor])
            max_index[cursor] = max_ping_index
            print(max_index[cursor])
            save_changes = False
            l = lines[0]
            l.remove()
            lines = ax.plot(max_index, c='lime')
        last_cursorPos = cursor
        cursor = cursor + finnNextLargeDiff(max_index[last_cursorPos:]) + 1
        while cursor in okValues: # Um virði er sett til at verða ok, forset til næsta
            cursor = cursor + finnNextLargeDiff(max_index[last_cursorPos:])+1
        scatters.remove()
        scatters = ax.scatter(cursor, 100, c='white')

        drawS(figS, dataign, yNumbers, max_index[cursor], cursor, answer)

        visible_min = cursor - 500
        if visible_min < 0:
            visible_min = 0
        visible_max = cursor + 500

        ax.set_xlim([visible_min, visible_max])
        canvasSingle.draw()
    elif event.keysym == 'Delete':
        figS.clf()
        axS = figS.add_subplot(111)
        if not save_changes:
            save_changes = True
            thisPing = dataign.iloc[:, cursor]
            if max_index[cursor] > 2:
                thisPing[max_index[cursor] - 1] = -120
                thisPing[max_index[cursor]-2] = -120
            thisPing[max_index[cursor]] = -120
            thisPing[max_index[cursor]+1] = -120
            thisPing[max_index[cursor]+2] = -120
            max_ping_index = 0
            max_value = -5000
            for i, amp in enumerate(thisPing):
                if amp > max_value and (i < float(answer)):
                    max_value = amp
                    max_ping_index = i
            axS.axhline(y=-max_ping_index, c='k')
        else:
            thisPing[max_ping_index] = -120
            if max_ping_index > 2:
                thisPing[max_ping_index-1] = -120
                thisPing[max_ping_index-2] = -120
            thisPing[max_ping_index+1] = -120
            thisPing[max_ping_index+2] = -120
            max_ping_index = 0
            max_value = -5000
            for i, amp in enumerate(thisPing):
                if amp > max_value and (i < float(answer)):
                    max_value = amp
                    max_ping_index = i
            axS.axhline(y=-max_ping_index, c='k')
        axS.plot(thisPing, yNumbers * -1)
        # axS.axhline(y=-max_ping_index, c='k')
        axS.axhline(y=-float(answer), c='red')

        canvasSingle.draw()
    elif event.keysym == 'KP_Subtract' or event.keysym == 'minus':
        ax.set_xlim([0, len(dataign.iloc[1, :])])
    elif event.keysym == 'KP_Add' or event.keysym == 'plus':
        visible_min = cursor - 500
        if visible_min < 0:
            visible_min = 0
        visible_max = cursor + 500

        ax.set_xlim([visible_min, visible_max])





    canvas.draw()
    #canvas.get_tk_widget().pack(fill=BOTH, expand=1)
root.bind('<Key>', key)
root.mainloop()