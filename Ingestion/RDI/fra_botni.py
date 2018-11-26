from tkinter import filedialog
from misc.faLog import *
import pandas as pd
import numpy as np
import matplotlib.dates as md
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy import stats
from scipy.interpolate import interp1d

def init(ingestion_listbox):
    streymmatingar_stationert = ingestion_listbox.insert("", 0, text="RDI streymmátinar frá botni")
    ingestion_listbox.insert(streymmatingar_stationert, "end", text='Vind korrilation')
    ingestion_listbox.insert(streymmatingar_stationert, "end", text='Countour plot')


def check_click(item, RightFrame, root):
    if item == 'Vind korrilation':
        vk(RightFrame, root)


def vk(frame, root2):
    global root
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='RDI Streymmátari', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Vind korrelation').pack(side=TOP, anchor=W)
    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    Button(menuFrame, text='Vel vindfíl', command=lambda: velFilir('.csv')).pack(side=LEFT)
    Button(menuFrame, text='Vel RDIfíl', command=lambda: vel_fil()).pack(side=LEFT)
    Button(menuFrame, text='Rokna', command=lambda: rokna_korr(v.get(), bin_entry.get(), canvas)).pack(side=LEFT)

    Label(menuFrame, text='Bin:').pack(side=LEFT)
    bin_entry = Entry(menuFrame, width=3)
    bin_entry.pack(side=LEFT)
    bin_entry.insert(0, '9')
    v = IntVar()
    Radiobutton(menuFrame, text='U', variable=v, value=1).pack(side=LEFT)
    Radiobutton(menuFrame, text='V', variable=v, value=2).pack(side=LEFT)
    Button(menuFrame, text='CLF', command=lambda: clear_figur(canvas)).pack(side=RIGHT)
    log_frame = Frame(frame, height=300)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

    plot_frame = Frame(frame)
    plot_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    global fig
    global ax
    fig = Figure(figsize=(8, 16), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    fig.clf()
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3, 2, 4])
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)


def rokna_korr(aett, bin_index, canvas):
    log_b()
    print('ok')
    global RDI_filnavn
    df = pd.read_csv(RDI_filnavn, skiprows=11, sep='\t', index_col=0, decimal=",")
    print(df.columns.values)
    streymData = df[bin_index]
    print(streymData)
    ar = df['YR']
    mdr = df['MO']
    dag = df['DA']
    h = df['HH']
    m = df['MM']
    date = np.zeros((len(streymData)))
    for i in range(len(streymData)):
        try:
            date[i] = md.date2num(datetime.strptime(str(ar[i]) + '.' + str(mdr[i]) + '.' + str(dag[i]) + '.' + str(h[i]) + '.' + str(m[i]), '%y.%m.%d.%H.%M'))
        except Exception as e:
            print('Dugi ikki ' + str(i))
            print(e)
    print(date)
    print('Dato frá RDI liðugt')
    global filnavn
    vindDF = pd.read_csv(filnavn[0])
    vindU = vindDF['u']
    vindV = vindDF['v']
    vindDate = vindDF['date']
    vindMDdate = np.zeros((len(vindDF)))
    for i in range(len(vindDF)):
        vindMDdate[i] = md.date2num(datetime.strptime(vindDate[i], '%Y-%m-%d_%H:%M:%S'))
    print('Dato frá LV liðugt')
    print(vindMDdate)
    # Nú byrjar tað orduliga
    if aett == 1:
        f = interp1d(vindMDdate, vindU)
    else:
        f = interp1d(vindMDdate, vindV)
    minvinddate = np.min(vindMDdate)
    xval = []
    yval = []
    for i in range(len(streymData)):
        if date[i] != 0 and date[i] > minvinddate and not np.isnan(streymData[i]):
            xval.append(streymData[i])
            yval.append(f(date[i]))
    slope, intercept, r_value, p_value, std_err = stats.linregress(xval, yval)
    global fig
    global ax
    ax.scatter(xval, yval, s=0.5, alpha=0.2)
    xval = np.array(xval)
    print(type(xval))
    print(type(intercept))
    print(type(slope))
    ax.plot(xval, intercept + slope*xval, label=str(std_err))
    ax.legend()
    #ax.plot(np.unique(xval), np.poly1d(np.polyfit(xval, yval, 1))(np.unique(xval)))


    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    log_e()

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
def vel_fil():
    global RDI_filnavn
    RDI_filnavn = filedialog.askopenfile(title='Vel RDI fíl', filetypes=(("txt Fílir", "*.txt"), ("csv Fílir", "*.csv"),
                                                                 ("all files", "*.*"))).name

def clear_figur(canvas):
    print('Slettar mynd')
    global fig
    global ax
    fig.clf()
    ax = fig.add_subplot(111)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    if 'levels' in globals():
        global levels
        del levels
