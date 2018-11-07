from mpl_toolkits.mplot3d import Axes3D
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
from scipy import interpolate
from misc.faLog import *

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
    global root
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
    list_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    text_list = Text(list_frame)
    text_list.pack(fill=BOTH, expand=True)

    log_frame = Frame(content_frame, height=300, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=TOP, anchor=W)
    gerlog(log_frame, root)

    load_btn = Button(menu_frame, text='Les inn uppsetan', command=lambda: innlesFil(text_list)).pack(side=LEFT)
    save_btn = Button(menu_frame, text='Goym uppsetan', command=lambda: goymuppsetan(text_list)).pack(side=LEFT)
    nytt_kort = Button(menu_frame, text='Nýtt Kort', command=lambda: nyttkort(text_list, root)).pack(side=LEFT)
    tekna_btn = Button(menu_frame, text='Tekna Kort', command=lambda: les_og_tekna(text_list.get("1.0", END), fig, canvas)).pack(side=LEFT)
    zoomin_btn = Button(menu_frame, text='+', command=lambda: zoom(0.01, text_list)).pack(side=LEFT)
    zoomout_btn = Button(menu_frame, text='-', command=lambda: zoom(-0.01, text_list)).pack(side=LEFT)
    teknaLinjur_btn = Button(menu_frame, text='Tekna Linjur', command=lambda: teknaLinjur(text_list, root)).pack(side=LEFT)
    teknaPrikkar_btn = Button(menu_frame, text='Tekna Prikkar', command=lambda: teknaPrikkar(text_list, root)).pack(side=LEFT)
    goymmynd_btn = Button(menu_frame, text='Goym Mynd', command=lambda: goymmynd(fig, canvas)).pack(side=LEFT)
    pan_vinstra = Button(menu_frame, text='←', font='Helvetica').pack(side=LEFT)
    pan_høgra = Button(menu_frame, text='→', font='Helvetica').pack(side=LEFT)
    pan_upp = Button(menu_frame, text='↑', font='Helvetica').pack(side=LEFT)
    pan_niður = Button(menu_frame, text='↓', font='Helvetica').pack(side=LEFT)

def goymuppsetan(text):
    filnavn = filedialog.asksaveasfilename(parent=root, title='Goym uppsetan',
                                             filetypes=(('uppsetan Fílur', '*.upp'), ('Allir fílir', '*.*')))
    tekstur = text.get("1.0", END)
    print(filnavn)
    F = open(filnavn, 'w')
    F.write(tekstur)
    F.close()

def innlesFil(text):
    if len(text.get("1.0", END)) > 1:
        if messagebox.askyesno("Ávaring", "Vilt tú yvurskriva núverani kort?", parent=root):
            filnavn = filedialog.askopenfile(parent=root, title='Les inn uppsetan',
                                             filetypes=(('uppsetan Fílur', '*.upp'), ('Allir fílir', '*.*')))
            print(filnavn.name)
            F = open(filnavn.name, 'r')
            nyttkort_text = F.read()
            F.close()
            text.delete(1.0, END)
            text.insert(INSERT, nyttkort_text)
    else:
        filnavn = filedialog.askopenfile(parent=root, title='Les inn',
                                         filetypes=(('uppsetan Fílur', '*.upp'), ('Allir fílir', '*.*')))
        print(filnavn.name)
        F = open(filnavn.name, 'r')
        nyttkort_text = F.read()
        F.close()
        text.insert(INSERT, nyttkort_text)


def goymmynd(fig, canvas):
    log_b()
    filnavn = filedialog.asksaveasfilename(parent=root, title="Goym mynd",  filetypes=(("png Fílur", "*.png"), ("jpg Fílur", "*.jpg")))
    print('Goymir mynd')
    fig.savefig(filnavn, dpi=1200, bbox_inches='tight')
    print('Liðugt')
    log_e()

def teknaLinjur(text_list, root):
    filnavn = filedialog.askopenfilename(parent=root,title = "Vel Fíl",filetypes = (("csv Fílir","*.csv"),("all files","*.*")))
    if len(filnavn) > 0:
        text_list.insert(INSERT, '\nlin_fil=' + filnavn)

def teknaPrikkar(text_list, root):
    filnavn = filedialog.askopenfilename(parent=root,title = "Vel Fíl",filetypes = (("csv Fílir","*.csv"),("all files","*.*")))
    if len(filnavn) > 0:
        text_list.insert(INSERT, '\nscatter_fil=' + filnavn)

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
    log_b()
    text = text.split('\n')
    dpi = 400
    dybdarlinjur = False
    filnavn = 'test'
    landlitur = 'lightgray'
    btn_interpolation = 'nearest'
    btn_track = False
    btn_gridsize = 1000
    suppress_ticks = True
    linjuSlag = [1, 0]
    btn_striku_hvor = 5
    qskala = 0.001
    lin_farv='b'
    lin_legend=''
    scatter_farv = 'b'
    scatter_legend=''
    show_legend = False
    quiverf_threshold = 1
    circle_stodd = 0.05
    renderengine='Standard Kort'
    for command in text:
        print(command)
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
            elif variable == 'renderengine':
                renderengine = command[toindex::]
            elif variable == 'landlitur':
                landlitur = command[toindex::]
            elif variable == 'title':
                ax.set_title(command[toindex::])
                filnavn = command[toindex::]
            elif variable == 'dpi':
                dpi = command[toindex::]
            elif variable == 'dybdarlinjur':
                if command[toindex::] != 'False' or renderengine == '3D_botn':
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
                if 'csvData_heilt' not in locals():
                    csvData_heilt = pd.read_csv(command[toindex::])
                csvData = csvData_heilt
                rows_to_drop = []
                for row in range(len(csvData)-1, 0, -1):
                    if float(csvData.iloc[row, 0]) > (lonmax+0.05):
                        rows_to_drop.append(row)
                    elif float(csvData.iloc[row, 0]) < (lonmin-0.05):
                        rows_to_drop.append(row)
                    elif float(csvData.iloc[row, 1]) > (latmax+0.05):
                        rows_to_drop.append(row)
                    elif float(csvData.iloc[row, 1]) < (latmin-0.05):
                        rows_to_drop.append(row)
                csvData = csvData.drop(rows_to_drop)
                print(len(csvData))
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
                    if renderengine == '3D_botn':
                        ax.scatter(btn_x, btn_y, -dypid, s=0.1, zorder=100)
                    else:
                        ax.scatter(btn_x, btn_y, s=0.1, zorder=100, c=dypid)
                #grid_x, grid_y = np.mgrid[np.linspace(latmin, latmax, num=7312), np.linspace(lonmin, lonmax, num=7312)]
                #grid_x, grid_y = np.meshgrid(np.linspace(latmin, latmax, num=7312), np.linspace(lonmin, lonmax, num=7312))
                #grid_z0 = griddata((btn_x, btn_y), dypid.values, (meshgridx, meshgridy), method='linear')
                #print(grid_z0)
                #plt.contour(meshgridx, meshgridy, grid_z0)
                #ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')
            elif variable == 'btn_interpolation':
                btn_interpolation = command[toindex::]
            elif variable == 'btn_track':
                if command[toindex::] == 'True':
                    btn_track = True
                elif command[toindex::] == 'False':
                    btn_track = False
            elif variable == 'btn_gridsize':
                btn_gridsize = command[toindex::]
            elif variable == 'btn_striku_hvor':
                btn_striku_hvor= int(command[toindex::])
            elif variable == 'lin_fil':
                lineData = pd.read_csv(command[toindex::])
                if renderengine == '3D_botn':
                    line_x_hj, line_y_hj = m(lineData['lon'].values, lineData['lat'].values)
                    line_x = [y for i in range(len(line_x_hj)-1)
                              for y in np.linspace(line_x_hj[i] , line_x_hj[i+1], btn_gridsize)]
                    line_y = [y for i in range(len(line_x_hj) - 1)
                              for y in np.linspace(line_y_hj[i], line_y_hj[i+1], btn_gridsize)]
                    line_z = griddata((btn_x, btn_y), -dypid.values,
                                      (line_x, line_y), method=btn_interpolation)
                    ax.plot(line_x, line_y, line_z, color=lin_farv, linewidth=3,
                            linestyle='solid', label=lin_legend)
                    ax.plot(line_x, line_y, 0*line_z, color=lin_farv, linewidth=3,
                            linestyle='solid')
                    for i in line_x_hj:
                        j = line_x.index(i)
                        ax.plot([line_x[j], line_x[j]], [line_y[j], line_y[j]],[line_z[j], 0]
                                , color=lin_farv, linewidth=3
                                , linestyle='solid')
                else:
                    line_x, line_y = m(lineData['lon'].values, lineData['lat'].values)
                    ax.plot(line_x, line_y, lin_farv, linewidth=1, label=lin_legend)
            elif variable == 'scatter_fil':
                scatterData = pd.read_csv(command[toindex::])
                line_x, line_y = m(scatterData['lon'].values, scatterData['lat'].values)
                Samla = True
                z_sca_a_yvirfladu = True
                columns = scatterData.columns.values
                for i in range(len(columns)):
                    if columns[i] == 'legend':
                        Samla = False
                    if columns[i] == 'd':
                        z_sca_a_yvirfladu = False
                if renderengine == '3D_botn':
                    if z_sca_a_yvirfladu:
                        line_z = 0*line_x
                    else:
                        line_z = -scatterData['d'].values
                    if Samla:
                        ax.scatter(line_x, line_y, line_z, zorder=100
                                   , color=scatter_farv, label=scatter_legend)
                    else:
                        lables = scatterData['legend'].values
                        for i in range(len(line_x)):
                            ax.scatter(line_x[i], line_y[i], line_z[i]
                                       , zorder=100, label=lables[i])
                            print('Funni legend :' + lables[i])
                        show_legend = True
                else:
                    if Samla:
                        ax.scatter(line_x, line_y, zorder=100, color=scatter_farv, label=scatter_legend)
                    else:
                        lables = scatterData['legend'].values
                        for i in range(len(line_x)):
                            ax.scatter(line_x[i], line_y[i], zorder=100, label=lables[i])
                            print('Funni legend :' + lables[i])
                        show_legend = True
            elif variable == 'linjuSlag':
                if command[toindex::] == 'eingin':
                    linjuSlag = [0, 1]
                elif command[toindex::] == 'prikkut':
                    linjuSlag = [1, 1]
                elif command[toindex::] == 'heil':
                    linjuSlag = [1, 0]
            elif variable == 'breiddarlinjur':
                if not renderengine == '3D_botn':
                    breiddarlinjur = np.linspace(latmin, latmax, int(command[toindex::]))
                    m.drawparallels(breiddarlinjur, labels=[1, 0, 0, 0], zorder=1000, color='lightgrey', dashes=linjuSlag)
            elif variable == 'longdarlinjur':
                if not renderengine == '3D_botn':
                    longdarlinjur = np.linspace(lonmin, lonmax, int(command[toindex::]))
                    m.drawmeridians(longdarlinjur, labels=[0, 0, 0, 1], zorder=1000, color='lightgrey', dashes=linjuSlag)
            elif variable == 'suppress_ticks':
                if command[toindex::] == 'True':
                    suppress_ticks = True
                else:
                    suppress_ticks = False
            elif variable == 'kortSkala':
                #m.drawmapscale(lonmax - 0.006, latmax - 0.001, lonmax + 0.018, latmax - 0.015,
                m.drawmapscale(lonmin + 0.006, latmin + 0.001, lonmax-lonmin + lonmin, latmax-latmin+latmin,
                               # 500, units = 'm',
                               int(command[toindex::]), units='km', format='%2.1f',
                               barstyle='fancy', fontsize=14, yoffset=50,
                               fillcolor1='whitesmoke', fillcolor2='gray', zorder=10000)
            elif variable == 'savefig':
                fig.savefig(command[toindex::], dpi=int(dpi), bbox_inches='tight')
            elif variable == 'quiver':
                Qdata = pd.read_csv(command[toindex::])
                lon = Qdata['lon']
                lat = Qdata['lat']
                Qx, Qy = m(lon.values, lat.values)
                q = m.quiver(Qx, Qy, Qdata['u']*qskala, Qdata['v']*qskala, scale=10, width=0.003, headwidth=5, zorder=100)
            elif variable == 'quiverf':
                Qdata = pd.read_csv(command[toindex::])
                pos_lon = Qdata['lon']
                pos_lat = Qdata['lat']
                v_org = Qdata['v']/1000
                u_org = Qdata['u']/1000
                v = v_org*qskala
                u = u_org*qskala
                lon_undir = []
                lat_undir = []
                lon_yvir = []
                lat_yvir = []
                u_undir = []
                v_undir = []
                u_yvir = []
                v_yvir = []
                for arrow_index in range(len(u)):
                    print(np.sqrt(v[arrow_index] ** 2 + u[arrow_index] ** 2))
                    if np.sqrt(v_org[arrow_index] ** 2 + u_org[arrow_index] ** 2) > quiverf_threshold:
                        lon_yvir.append(pos_lon[arrow_index])
                        lat_yvir.append(pos_lat[arrow_index])
                        u_yvir.append(u[arrow_index])
                        v_yvir.append(v[arrow_index])
                    else:
                        lon_undir.append(pos_lon[arrow_index])
                        lat_undir.append(pos_lat[arrow_index])
                        u_undir.append(u[arrow_index])
                        v_undir.append(v[arrow_index])
                x_undir, y_undir = m(lon_undir, lat_undir)
                x_yvir, y_yvir = m(lon_yvir, lat_yvir)

                q = m.quiver(x_undir, y_undir, u_undir, v_undir, color='g', scale=10, width=0.003, headwidth=5,
                             zorder=100)
                ax.quiverkey(q, 0.85, 0.95 - 0 * 0.03, quiverf_threshold*qskala, label='Undir ' + str(quiverf_threshold) + ' m/s', labelpos='W') # 2.57222

                q = m.quiver(x_yvir, y_yvir, u_yvir, v_yvir, color='r', scale=10, width=0.003, headwidth=5, zorder=100)
                ax.quiverkey(q, 0.85, 0.95 - 1 * 0.03, quiverf_threshold*qskala, label='Yvir ' + str(quiverf_threshold) + ' m/s', labelpos='W')

            elif variable == 'quiverf_threshold':
                quiverf_threshold = float(command[toindex::])
            elif variable == 'quiverskala':
                qskala = float(command[toindex::])
            elif variable == 'qkey':
                if 'x_undir' in locals():
                    ax.quiverkey(q, 0.8, 0.95 - 2 * 0.03, float(command[toindex::])*qskala, label=command[toindex::] + ' m/s',
                                 labelpos='W')
                else:
                    ax.quiverkey(q, 0.8, 0.95, float(command[toindex::]*qskala), label=command[toindex::] + ' m/s', labelpos='W')
            elif variable == 'lin_farv':
                lin_farv = command[toindex::]
            elif variable == 'lin_legend':
                lin_legend = command[toindex::]
                show_legend = True
            elif variable == 'circle_fil':
                print('Teknar rundingar')
                scatterData = pd.read_csv(command[toindex::])
                line_x, line_y = m(scatterData['lon'].values, scatterData['lat'].values)
                Samla = True
                columns = scatterData.columns.values
                for i in range(len(columns)):
                    if columns[i] == 'legend':
                        Samla = False
                if Samla:
                    ax.scatter(line_x, line_y, s=circle_stodd, facecolor='none', edgecolor='black')
                    #plt.Circle((line_x, line_y), circle_stodd, color='black', fill=False)
                else:
                    lables = scatterData['legend'].values
                    for i in range(len(line_x)):
                        ax.scatter(line_x[i], line_y[i], s=circle_stodd, facecolor='none', edgecolor='black')
                        #circle = plt.Circle((line_x, line_y), circle_stodd, fill=False, label=lables[i], zorder=100)
                        print('Funni legend :' + lables[i])
                    show_legend = True
            elif variable == 'circle_stodd':
                circle_stodd = float(command[toindex::])
            elif variable == 'scatter_farv':
                scatter_farv=command[toindex::]
            elif variable == 'scatter_legend':
                scatter_legend = command[toindex::]
        else:

            if command == 'clf':
                fig.clf()
                ax = fig.add_subplot(111)
            elif command == 'Tekna kort':

                if renderengine == '3D_botn':
                    m = Basemap(projection='merc', resolution=None,
                                llcrnrlat=latmin, urcrnrlat=latmax,
                                llcrnrlon=lonmin, urcrnrlon=lonmax, ax=ax, suppress_ticks=suppress_ticks)
                    ax = fig.add_subplot(111, projection='3d')
                else:
                    m = Basemap(projection='merc', resolution=None,
                                llcrnrlat=latmin, urcrnrlat=latmax,
                                llcrnrlon=lonmin, urcrnrlon=lonmax, ax=ax, suppress_ticks=suppress_ticks)
                    for island in os.listdir('Kort_Data/Coasts'):
                        lo, aa, la = np.genfromtxt('Kort_Data/Coasts/' + island, delimiter=' ').T
                        xpt, ypt = m(lo, la)
                        plt.plot(xpt, ypt, 'k', linewidth=1)
                        ax.fill(xpt, ypt, landlitur, zorder=10)

            elif command == 'btn_contourf':
                grid_z0 = griddata((btn_x, btn_y), dypid.values, (meshgridx, meshgridy), method=btn_interpolation)
                #grid_z0 = interpolate.interp2d(btn_x, btn_y, dypid.values, kind='cubic')
                vmin = min(-150, min([-y for x in grid_z0 for y in x]))
                lv = range(vmin, btn_striku_hvor, btn_striku_hvor)
                if renderengine == '3D_botn':
                    ax.plot_surface(meshgridx, meshgridy, -grid_z0, alpha=.5, rcount=50, ccount=50, vmax=0,
                                    cmap='ocean', zorder=21000)
                else:
                    c = m.contourf(meshgridx, meshgridy, -grid_z0, lv, ax=ax)  # Um kodan kiksar her broyt basemap fílin til // har feilurin peikar
                    #ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')
                    fig.colorbar(c)
            elif command == 'btn_contour':
                grid_z0 = griddata((btn_x, btn_y), dypid.values, (meshgridx, meshgridy), method=btn_interpolation)
                vmin = min(-150, min([-y for x in grid_z0 for y in x]))
                lv = range(vmin, btn_striku_hvor, btn_striku_hvor)
                #grid_z0 = interpolate.interp2d(btn_x, btn_y, dypid.values, kind='cubic')
                #c = m.contour(meshgridx, meshgridy, -1*grid_z0, lv, ax=ax)  # Um kodan kiksar her broyt basemap fílin til // har feilurin peik
                if renderengine == '3D_botn':
                    ax.contour3D(meshgridx, meshgridy, -1 * grid_z0, levels=lv,
                                 colors='k',vmax=0 , linestyles='solid')
                else:
                    c = m.contour(meshgridx, meshgridy, -1 * grid_z0, lv, ax=ax, colors='black', linestyles='solid', linewidths=0.2)
                    #ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')
    if show_legend:
        print('Showing Legend')
        leg = ax.legend(loc='best')
        leg.set_zorder(3000)
    if renderengine == '3D_botn':
        s1, s2 = m(lonmax, latmax)
        sm = max(s1,s2)
        s1 = s1/sm
        s2 = s2/sm
        def short_proj():
            return np.dot(Axes3D.get_proj(ax), np.diag([s1, s2, 1, 1]))

        ax.get_proj = short_proj

    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    log_e()
    def onclick(event):
        nonlocal m
        lat, lon = m(event.xdata, event.ydata, inverse=True)
        print('%s click: lon=%f, lat=%f' %
              ('double' if event.dblclick else 'single', lat, lon))

    cid = fig.canvas.mpl_connect('button_press_event', onclick)


def nyttkort(text, root):
    F = open('Kort_Data/kort_uppsetan.upp', 'r')
    nyttkort_text = F.read()
    F.close()
    if len(text.get("1.0", END)) > 1:
        if messagebox.askyesno("Ávaring", "Vilt tú yvurskriva núverani kort?", parent=root):
            text.delete(1.0, END)
            text.insert(INSERT, nyttkort_text)
    else:
        text.insert(INSERT, nyttkort_text)
