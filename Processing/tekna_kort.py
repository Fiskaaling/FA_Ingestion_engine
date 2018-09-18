from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import os
import pandas as pd
from scipy.interpolate import griddata

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
    fig = Figure(figsize=(8, 12), dpi=100)

    root = Tk()
    root.geometry("1200x800")
    app = Window(root)

    top = Toplevel()
    top.wm_attributes('-topmost', 1)
    top.withdraw()
    top.protocol('WM_DELETE_WINDOW', top.withdraw)

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
    zoomin_btn = Button(menu_frame, text='+', command=lambda: zoom(0.01, text_list)).pack(side=LEFT)
    zoomout_btn = Button(menu_frame, text='-', command=lambda: zoom(-0.01, text_list)).pack(side=LEFT)
    teknaLinjur_btn = Button(menu_frame, text='Tekna Linjur', command=lambda: teknaLinjur(text_list, root)).pack(side=LEFT)


def teknaLinjur(text_list, root):
    filnavn = filedialog.askopenfilename(parent=root,title = "Vel Fíl",filetypes = (("csv Fílir","*.csv"),("all files","*.*")))
    text_list.insert(INSERT, '\nlin_fil=' + filnavn)
    print('test')

def zoom(mongd, textbox):
    print('zoom ' + str(mongd))
    raw_text = str(textbox.get("1.0", END))
    text = raw_text.split('\n')
    for command in text:
        if '=' in command:
            toindex = command.find('=')+1
            variable = command[0:toindex-1]
            if variable == 'latmax':
                latmax = float(command[toindex::])
                raw_text = raw_text.replace(command, "latmax="+str(-mongd + latmax))
            elif variable == 'latmin':
                latmin = float(command[toindex::])
                raw_text = raw_text.replace(command, "latmin="+str(mongd + latmin))
            elif variable == 'lonmin':
                lonmin = float(command[toindex::])
                raw_text = raw_text.replace(command, "lonmin=" + str(mongd + lonmin))
            elif variable == 'lonmax':
                lonmax = float(command[toindex::])
                raw_text = raw_text.replace(command, "lonmax=" + str(-mongd + lonmax))
    textbox.delete(1.0, END)
    textbox.insert(INSERT, raw_text)

def les_og_tekna(text, fig, canvas):
    text = text.split('\n')
    dpi = 400
    dybdarlinjur = False
    filnavn = 'test'
    landlitur = 'lightgray'
    btn_interpolation = 'nearest'
    btn_track = False
    btn_gridsize = 1000
    for command in text:
        if "=" in command:
            toindex = command.find('=')+1
            variable = command[0:toindex-1]
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
                filnavn = command[toindex::]
            elif variable == 'dpi':
                dpi = command[toindex::]
            elif variable == 'dybdarlinjur':
                if command[toindex::] != 'False':
                    dybdarlinjur = command[toindex::]
                    with open(dybdarlinjur) as f:
                        f.readline()
                        l = f.readline().split()
                        i, j = int(l[3]), int(l[5])
                        lis = [float(y) for x in f for y in x.split()]
                    D_lon = np.array(lis[0: i * j]).reshape((j, i))  # first  i*j instances
                    D_lat = np.array(lis[i * j: i * j * 2]).reshape((j, i))  # second i*j instances
                    D_dep = np.array(lis[i * j * 2: i * j * 3]).reshape((j, i))  # third  i*j instances
                    MD_lon, MD_lat = m(D_lon, D_lat)
                    c = m.contour(MD_lon, MD_lat, D_dep,
                                  ax=ax)  # Um kodan kiksar her broyt basemap fílin til // har feilurin peikar
                    ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')
            elif variable == 'csv_dybdarkort':
                csvData = pd.read_csv(command[toindex::])
                print(csvData.columns.values)
                btn_lon = csvData['lon']
                btn_lat = csvData['lat']
                dypid = csvData['d']
                btn_x, btn_y = m(btn_lon.values, btn_lat.values)
                #btn_x1, btn_y1 = np.meshgrid(btn_x, btn_y)

                meshgridy = np.linspace(latmin, latmax, btn_gridsize)
                meshgridx = np.linspace(lonmin, lonmax, btn_gridsize)
                print('Gridsize =' + str(btn_gridsize))
                meshgridx, meshgridy = m(meshgridx, meshgridy)
                meshgridx, meshgridy = np.meshgrid(meshgridx, meshgridy)

                #ax.scatter(meshgridx, meshgridy, s=1)
                if btn_track:
                    ax.scatter(btn_x, btn_y, s=0.1, zorder=100, color='black')
                #grid_x, grid_y = np.mgrid[np.linspace(latmin, latmax, num=7312), np.linspace(lonmin, lonmax, num=7312)]
                #grid_x, grid_y = np.meshgrid(np.linspace(latmin, latmax, num=7312), np.linspace(lonmin, lonmax, num=7312))
                #grid_z0 = griddata((btn_x, btn_y), dypid.values, (meshgridx, meshgridy), method='linear')
                #print(grid_z0)
                grid_z0 = griddata((btn_x, btn_y), dypid.values, (meshgridx, meshgridy), method=btn_interpolation)
                #plt.contour(meshgridx, meshgridy, grid_z0)
                #ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')
            elif variable == 'btn_interpolation':
                btn_interpolation = command[toindex::]
            elif variable ==  'btn_track':
                if command[toindex::] == 'True':
                    btn_track = True
            elif variable == 'btn_gridsize':
                btn_gridsize = command[toindex::]
            elif variable == 'lin_fil':
                lineData = pd.read_csv(command[toindex::])
                line_x, line_y = m(lineData['lon'].values, lineData['lat'].values)
                ax.plot(line_x, line_y, 'b', linewidth=1)
            elif variable == 'scatter_fil':
                scatterData = pd.read_csv(command[toindex::])
                line_x, line_y = m(scatterData['lon'].values, scatterData['lat'].values)
                ax.scatter(line_x, line_y, 'b', linewidth=1)
        else:
            if command == 'clf':
                fig.clf()
                ax = fig.add_subplot(111)
            elif command == 'Tekna kort':
                m = Basemap(projection='merc', resolution=None,
                            llcrnrlat=latmin, urcrnrlat=latmax,
                            llcrnrlon=lonmin, urcrnrlon=lonmax, ax=ax)
                for island in os.listdir('Kort_Data/Coasts'):
                    lo, aa, la = np.genfromtxt('Kort_Data/Coasts/' + island, delimiter=' ').T
                    xpt, ypt = m(lo, la)
                    m.plot(xpt, ypt, 'k', linewidth=1)
                    ax.fill(xpt, ypt, landlitur, zorder=100)
            elif command == 'btn_contourf':
                c = m.contourf(meshgridx, meshgridy, grid_z0, 30, ax=ax)  # Um kodan kiksar her broyt basemap fílin til // har feilurin peikar
                #ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')
                fig.colorbar(c)
            elif command == 'btn_contour':
                lv = np.arange(0, 150, 5)
                c = m.contour(meshgridx, meshgridy, grid_z0, lv, ax=ax)  # Um kodan kiksar her broyt basemap fílin til // har feilurin peik
                ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')
    #alioki_lat = [62.273790155, 62.272388430, 62.264901060, 62.266422648]
    #alioki_lon = [-6.727558225, -6.732274219, -6.722096577, -6.717137173]
    #alioki_x, alioki_y = m(alioki_lon, alioki_lat)
    #m.plot(alioki_x, alioki_y, 'b', linewidth=1)
    #ax.plot((alioki_x[0], alioki_x[3]), (alioki_y[0], alioki_y[3]), label='Uppskot til aliøki')

    fig.savefig(filnavn + '.png', dpi=int(dpi), bbox_inches='tight')

    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)


def nyttkort(text):
    #F = open('Processing/kort_uppsetan.upp', 'r')
    F = open('Processing/kort_uppsetan_husaeidi.upp', 'r')
    nyttkort_text = F.read()
    F.close()
    if len(text.get("1.0", END)) > 1:
        if messagebox.askyesno("Ávaring", "Vilt tú yvurskriva núverani kort?"):
            text.delete(1.0, END)
            text.insert(INSERT, nyttkort_text)
    else:
        text.insert(INSERT, nyttkort_text)
