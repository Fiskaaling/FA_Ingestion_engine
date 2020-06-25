import pandas as pd
import numpy as np
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import simpledialog
from tkinter import filedialog

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
    ignore_first = 500
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
    max_index = finnmax(dataign, 800)
    lines = ax.plot(max_index)
    ax.imshow(dataign, cmap='plasma', vmin=-120)
    canvas.draw()
    canvasSingle.draw()



root = Tk()
root.geometry("1200x800")
app = Window(root)

menu_frame = Frame(app)
menu_frame.pack(side=TOP, anchor=N)
velMappuBtn = Button(menu_frame, text='Vel Fíl', command=lambda: velFil())
velMappuBtn.pack(side=LEFT)

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
data = pd.read_csv(filename)
data = data.iloc[::-1] # Eg haldi at hettar flippar
print("Done")
ignore_last = 50
ignore_first = 500
global dataign
dataign = data.iloc[ignore_first:-ignore_last, :]
dataign = pd.DataFrame(np.array(dataign))

max_index = finnmax(dataign, 800)

lines = ax.plot(max_index)
ax.imshow(dataign, cmap='plasma', vmin=-120)

canvas.draw()
canvas.get_tk_widget().pack(fill=BOTH, expand=1)
canvasSingle.draw()
canvasSingle.get_tk_widget().pack(fill=BOTH, expand=1)
print('done')
cursor = 0
scatters = ax.scatter(0, 100, c='white')
yNumbers = np.arange(len(dataign.iloc[:,1]))
answer = 0
max_ping_index = 0
thisPing = dataign.iloc[:, cursor]
save_changes = False

visible_min = 0
visible_max = 1500
visible_range = visible_max - visible_min
ax.set_xlim([visible_min, visible_max])
okValues = []
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
    if event.keysym == 'KP_0':
        cursor = 0
    if event.keysym == 'Right':
        cursor = cursor + 1
    if event.keysym == 'Left':
        cursor = cursor - 1
    if event.keysym == 's':
        toSave = pd.DataFrame(max_index)
        toSave.to_csv(filename[:-4] + 'maxi.csv')
    if event.keysym == 'KP_Decimal':
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
        figS.clf()
        axS = figS.add_subplot(111)
        axS.plot(dataign.iloc[:, cursor], yNumbers*-1)
        print(max_index[cursor])
        axS.axhline(y=-max_index[cursor], c='k')
        axS.axhline(y=-float(answer), c='red')

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
            thisPing[max_index[cursor]] = -120
            thisPing[max_index[cursor]-1] = -120
            thisPing[max_index[cursor]+1] = -120
            thisPing[max_index[cursor]-2] = -120
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
            thisPing[max_ping_index-1] = -120
            thisPing[max_ping_index+1] = -120
            thisPing[max_ping_index-2] = -120
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
    elif event.keysym == 'KP_Subtract':
        ax.set_xlim([0, len(dataign.iloc[1, :])])
    elif event.keysym == 'KP_Add':
        visible_min = cursor - 500
        if visible_min < 0:
            visible_min = 0
        visible_max = cursor + 500

        ax.set_xlim([visible_min, visible_max])





    canvas.draw()
    #canvas.get_tk_widget().pack(fill=BOTH, expand=1)
root.bind('<Key>', key)
root.mainloop()