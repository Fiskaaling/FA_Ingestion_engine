from tkinter import *
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import os


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        Frame.pack(self, side=BOTTOM)
        self.init_window()

    def init_window(self):
        self.master.title("Fiskaaling - Tekna Kort")
        self.pack(fill=BOTH, expand=1)

        # tools_frame = Frame(self, relief=RAISED, borderwidth=1)
        main_frame = Frame(self, borderwidth=1)
        main_frame.pack(fill=BOTH, expand=False, side=TOP)

    def client_exit(self):
        exit()


def teknakort():
    fig = Figure(figsize=(5, 4), dpi=100)

    root = Tk()
    root.geometry("1200x800")
    app = Window(root)
    menu_frame = Frame(app, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    menu_frame.pack(fill=X, expand=False, anchor=N)
    content_frame = Frame(app, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    content_frame.pack(fill=BOTH, expand=True, anchor=N)

    map_frame = Frame(content_frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    map_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=map_frame)


    list_frame = Frame(content_frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    list_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    text_list = Text(list_frame)
    text_list.pack(fill=BOTH, expand=True)

    load_btn = Button(menu_frame, text='Les inn').pack(side=LEFT)
    save_btn = Button(menu_frame, text='Goym').pack(side=LEFT)
    nytt_kort = Button(menu_frame, text='Nýtt Kort', command=lambda: nyttkort(text_list)).pack(side=LEFT)
    tekna_btn = Button(menu_frame, text='Tekna Kort', command=lambda: les_og_tekna(text_list.get("1.0", END), fig, canvas)).pack(side=LEFT)

def les_og_tekna(text, fig, canvas):
    text = text.split('\n')
    dpi = 400
    dybdarlinjur = False
    landlitur = 'lightgray'
    for command in text:
        if "=" in command:
            toindex = command.find('=')
            variable = command[0:toindex]
            toindex += 1
            if variable == 'latmax':
                latmax = float(command[toindex::])
            elif variable == 'latmin':
                latmin = float(command[toindex::])
            elif variable == 'lonmin':
                lonmin = float(command[toindex::])
            elif variable == 'lonmax':
                lonmax = float(command[toindex::])
            elif variable == 'landlitur':
                landlitur = command[toindex::]
            elif variable == 'title':
                ax.set_title(command[toindex::])
            elif variable == 'dpi':
                dpi = command[toindex::]
            elif variable == 'dybdarlinjur':
                dybdarlinjur = command[toindex::]
        else:
            if command == 'clf':
                fig.clf()
                ax = fig.add_subplot(111)
    m = Basemap(projection='merc', resolution=None,
                llcrnrlat=latmin, urcrnrlat=latmax,
                llcrnrlon=lonmin, urcrnrlon=lonmax, ax=ax)
    for island in os.listdir('Kort_Data/Coasts'):
        lo, aa, la = np.genfromtxt('Kort_Data/Coasts/'+island, delimiter = ' ').T
        xpt, ypt = m(lo, la)
        m.plot(xpt, ypt, 'k', linewidth=1)
        ax.fill(xpt, ypt, landlitur)

    if dybdarlinjur:
        with open(dybdarlinjur) as f:
            # skip one line and read i and j dimentions form next line
            f.readline()
            l = f.readline().split()
            # i, j = int(l[2]), int(l[4])
            i, j = int(l[3]), int(l[5])

            # iterate througt file and append values to list
            lis = [float(y) for x in f for y in x.split()]
        D_lon = np.array(lis[0: i * j]).reshape((j, i))  # first  i*j instances
        D_lat = np.array(lis[i * j: i * j * 2]).reshape((j, i))  # second i*j instances
        D_dep = np.array(lis[i * j * 2: i * j * 3]).reshape((j, i))  # third  i*j instances
        MD_lon, MD_lat = m(D_lon, D_lat)
        c = m.contour(MD_lon, MD_lat, D_dep, ax=ax)
        ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')

    fig.savefig('test.png', dpi=dpi, bbox_inches='tight')

    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)


def nyttkort(text):
    F = open('Processing/kort_uppsetan.upp', 'r')
    nyttkort_text = F.read()
    F.close()
    if len(text.get("1.0", END)) > 1:
        if messagebox.askyesno("Ávaring", "Vilt tú yvurskriva núverani kort?"):
            text.delete(1.0, END)
            text.insert(INSERT, nyttkort_text)
    else:
        text.insert(INSERT, nyttkort_text)
