import pandas as pd
import numpy as np
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import simpledialog, messagebox
from tkinter import filedialog
import platform


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        Frame.pack(self, side=BOTTOM)
        self.init_window()

    def init_window(self):
        self.master.title("Echosounder Export Machine 6000s+")
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

def finnmaxRanger(data, lastOk, search_range=100, under=600):
    maxi = []
    ok_nextRound = lastOk

    maxi = []
    for i in range(len(data.iloc[1, :])):
        thisrow = data.iloc[:, i]
        maxc = -1000
        maxci = -1000
        for j, col in enumerate(thisrow):
            if j > under:
                continue
            if col > maxc:
                maxc = col
                maxci = j
        if abs(maxci-ok_nextRound) > search_range:
            print('Uha, hopp')
            maxc = -1000
            maxciR = -1000
            for j, col in enumerate(thisrow.iloc[ok_nextRound-search_range:ok_nextRound+search_range]):
                if col > maxc:
                    maxc = col
                    maxciR = j
            if (maxciR+ok_nextRound-search_range)>under:
                messagebox.showinfo("Fuck", "Helviti, eg kiksaði. Hygg væl eftir áðrenn tú fert víðari")
                if maxci < 0:
                    maxci = 0
                maxi.append(maxci)
                ok_nextRound = maxci
            else:
                if maxciR+ok_nextRound-search_range < 0:
                    maxi.append(0)
                else:
                    maxi.append(maxciR+ok_nextRound-search_range)
            print(maxciR+ok_nextRound-search_range)
            ok_nextRound= maxciR+ok_nextRound-search_range
        else:
            maxi.append(maxci)
            ok_nextRound = maxci
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
    ignore_first = 300
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
    global cursor
    cursor = 0
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


def export_stuff():
    print('Hello, World!')
    filename = filedialog.askopenfiles(title='Vel fílir at klistra saman til at síðani eksportera', filetypes=(("csv Fílir", "*.csv"), ("all files", "*.*")))
    #filename = ['~/Documents/data/Echolodd/D20200220-T0857511_0.csv', '~/Documents/data/Echolodd/D20200220-T0857511_1.csv']
    #filename = ['~/Documents/data/Echolodd/D20200220-T0857511_0.csv']
    timeFilename = filename[0].name.split('_')[0]
    #timeFilename = filename[0].split('_')[0]
    timeFilename = timeFilename[:-1] + '-T.csv'
    print(timeFilename)
    timeData = pd.read_csv(timeFilename)
    stuff_to_export = pd.DataFrame(columns=['Tíð', 'Dýpi', 'Sv'])


    SpeedOfSound = 1500     # m/s
    SampleTime = 0.000025   # s
    distancePerSample = SpeedOfSound*SampleTime/2

    for fileIndex, file in enumerate(filename):
        print('Nú rokni eg uppá fíl ' + file.name)
        disMaxi = pd.read_csv(file.name[:-4] + 'maxi.csv')
        #disMaxi = pd.read_csv(file[:-4] + 'maxi.csv')
        disData = pd.read_csv(file.name)
        #disData = pd.read_csv(file)
        ignore_last = 50
        processed = disData.copy()


        for i in range(len(disData.iloc[1, :])):
            tmp = disData.iloc[disMaxi.iloc[i, 1]:-ignore_last, i]
            tmp = np.append(tmp, list(np.ones([disMaxi.iloc[i, 1] + ignore_last]) * -200))
            processed.iloc[:, i] = tmp

        disData = processed

        for exportPingIndex in range(int(len(disData.iloc[1, :])/75)):
            # Hettar loop'ið inkrementerar hvørjar 5 minuttir
            # Fyri hvørja tíð í intervalinum rokna miðal SV
            for exportDepthIndex in range(int(len(disData.iloc[:, 1])/6)):
                meanSvSubDepthTimeList = []
                for subTimeStep in range(75):
                    meanSvSubDepth = 0
                    divideby = 0
                    for subDepth in range(6):# Fyri hvørjar 20 cm
                        #print('Depth Index: ' + str(exportDepthIndex*7+subDepth))
                        #print('Time Index: ' + str(exportPingIndex*75+subTimeStep))
                        if not np.isnan(disData.iloc[exportDepthIndex*6+subDepth, exportPingIndex*75+subTimeStep]):
                            meanSvSubDepth += 10**(disData.iloc[exportDepthIndex*6+subDepth, exportPingIndex*75+subTimeStep]/10) #Ger til linscale og rokna miðal
                            divideby += 1
                    if divideby and not np.isnan(meanSvSubDepth):
                        meanSvSubDepthTimeList.append(meanSvSubDepth/divideby)
                    else:
                        meanSvSubDepthTimeList.append(-201)
                meanSvSubDepthTime = 10 * np.log10(np.mean(meanSvSubDepthTimeList))
                if not np.isnan(meanSvSubDepthTime):
                    if meanSvSubDepthTime != -200.0:
                        # Set inn eina nýggja linju í tingi
                        disTid = str(timeData.iloc[exportPingIndex*75]).split('\\t')[1].split('\n')[0]
                        #print('Innsett dýpið: ' + str((exportDepthIndex*6*distancePerSample)))
                        stuff_to_export = stuff_to_export.append({'Tíð': disTid.split('.')[0], 'Dýpi': np.round(exportDepthIndex*6*distancePerSample, 3), 'Sv': np.round(meanSvSubDepthTime,3)}, ignore_index=True)
    stuff_to_export.to_csv(filename[0].split('_')[0]+'_Export.csv', index=False)





    print('ding dong done!')

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

exportStuffBtn = Button(menu_frame, text='Eksportera ting', command=lambda: export_stuff())
exportStuffBtn.pack(side=RIGHT)

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
        print('Goymur....')
        toSave.to_csv(filename[:-4] + 'maxi.csv')
        print('Liðugt, ver so glað ása')
        bad_joke = np.floor(np.random.random()*16)
        joke = "text"
        if bad_joke == 0:
            joke = "How do you spell Canda? C,eh,N,eh,D,eh"
        elif bad_joke == 1:
            joke = "I saw a French rifle on eBay today It's never been fired but I heard it was dropped once."
        elif bad_joke == 2:
            joke = "A Mexican fireman had twin boys He named them Jose and Hose B"
        elif bad_joke == 3:
            joke = "My ex-wife still misses me... But her aim is gettin better."
        elif bad_joke == 4:
            joke = "If you have a parrot and you don't teach it to say,\"Help, they've turned me into a parrot.\" you are wasting everybody's time."
        elif bad_joke == 5:
            joke = " What do you call a fish with a tie? soFISHticated"
        elif bad_joke == 6:
            joke = " What do sea monsters eat? Fish and ships."
        elif bad_joke == 7:
            joke = " What party game do fish like to play? Salmon Says."
        elif bad_joke == 8:
            joke = " How does an octopus go to war? Well-armed!"
        elif bad_joke == 9:
            joke = " What do you call a big fish who makes you an offer you can't refuse? The Codfather!"
        elif bad_joke == 10:
            joke = "What’s a pirate’s favorite letter? \n R? \n No. It be the C!"
        elif bad_joke == 11:
            joke = "Have you heard any good pirate jokes? Well, neither have ayyyye"
        elif bad_joke == 12:
            joke = "Why does it take pirates so long to learn the alphabet? Because they can spend years at C."
        elif bad_joke == 13:
            joke = "How do pirates prefer to communicate? A: Aye to aye!"
        elif bad_joke == 14:
            joke = " Why did nobody want to play cards with the pirate? Because he was standing on the deck."
        elif bad_joke == 15:
            joke = "Why is pirating so addictive? They say once ye lose yer first hand, ye get hooked!"
        messagebox.showinfo("Goymt", joke)
    if event.keysym == 'KP_Decimal' or event.keysym == 'comma':
        answer = simpledialog.askstring("Input", "Botnurin er undur?", parent=app)
        visible_max = cursor + 500
        max_index[cursor:visible_max] = finnmax(dataign.iloc[:,cursor:visible_max], float(answer))
        l = lines[0]
        l.remove()
        lines = ax.plot(max_index, c='lime')
    if event.keysym == '3':
        visible_max = cursor + 500
        max_index[cursor:visible_max] = finnmaxRanger(dataign.iloc[:, cursor:visible_max], max_index[cursor], search_range=20, under=float(answer))
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
#export_stuff()
root.bind('<Key>', key)
root.mainloop()