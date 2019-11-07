#from mpl_toolkits.mplot3d import Axes3D
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.interpolate import griddata
from misc.faLog import *
from tkinter import font
import tkinter.ttk as ttk
import cartopy.crs as ccrs
import cartopy.feature as cpf
from geopy import distance
import pyperclip # Kanska fjerna hettar seinni!
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from screeninfo import get_monitors
import matplotlib.image as mpimg
from Processing.les_og_tekna.chk_req import chk_req


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
    #  TODO hettar skal implomenterast ordiligt
    global path_to_nytt_kort
    path_to_nytt_kort = 'Kort_Data/kort_uppsetan.upp'
    global root
    root = Tk()
    root.geometry("1200x800")

    uhd = False
    for monitor in get_monitors():
        if '2160' in str(monitor):
            uhd = True

    if uhd:  # 4K bullshit, Alt er forbanna lítið
        root.geometry("3000x1600")
        f = font.Font(size=40)
        root.option_add("*Font", f)
        style = ttk.Style(root)
        style.configure('Button', font=f)
        style.configure('Treeview', rowheight=45)
        style.configure('Treeview.Heading', font=f)
        style.configure(".", font=f)


    app = Window(root)


    top = Toplevel()
    top.wm_attributes('-topmost', 1)
    top.withdraw()
    top.protocol('WM_DELETE_WINDOW', top.withdraw)

    menu_frame = Frame(app)
    menu_frame.pack(fill=X, expand=False, anchor=N)
    content_frame = Frame(app)
    content_frame.pack(fill=BOTH, expand=True, anchor=N)

    map_frame = Frame(content_frame)
    map_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)

    #fig = Figure()
    figsize = [8, 12]
    fig = Figure(figsize=figsize)
    #fig.set_size_inches((8, 12), forward=False)
    #fig = Figure(figsize=(2, 3), dpi=100)
    global ax
    #ax = fig.add_subplot(111, aspect=1)
    #ax.plot([1, 2, 1])
    global ccrs_projection
    ccrs_settings = {'central_longitude': 0, 'latitude_true_scale': 62, 'max_latitude': 63}#'central_longitude': -7, 'min_latitude': 61, 'max_latitude': 63,
    #global ccrs_projection
    ccrs_projection = ccrs.PlateCarree(-7)
    #ax = fig.add_axes([0, 0, 1, 1], projection=ccrs_projection, aspect=1, adjustable='box')
    #ax = fig.add_subplot(111, projection=ccrs_projection, adjustable='datalim') 01/04/19
    ax = fig.add_subplot(111, projection=ccrs_projection)

    ax.add_feature(cpf.COASTLINE)
    ax.add_feature(cpf.BORDERS, lw=0.5)

    canvas = FigureCanvasTkAgg(fig, master=map_frame)

    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)

    list_frame = Frame(content_frame)
    list_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    text_list = Text(list_frame)
    text_list.pack(fill=BOTH, expand=True)

    CommandEntry = Entry(content_frame, width=100)
    CommandEntry.pack(side=TOP, anchor=W)

    lowframe = Frame(content_frame, height=300)
    lowframe.pack(fill=X, expand=False, side=TOP, anchor=W)

    controls_frame = Frame(lowframe)
    controls_frame.pack(side=LEFT, anchor=W)

    log_frame = Frame(lowframe)
    log_frame.pack(fill=X, expand=False, side=TOP, anchor=W)
    gerlog(log_frame, root)

    global ctrl
    global shift
    shift = False
    ctrl = False

    def key(event):
        if ctrl:
            if event.keysym == 'a':
                print('Markera alt ')
                text_list.tag_add(SEL, "1.0", END)
                text_list.mark_set(INSERT, "1.0")
                text_list.see(INSERT)
            elif event.keysym == 'Return':
                les_og_tekna(text_list, fig, canvas, False, v_dic)
        elif shift:
            if event.keysym == 'Left':
                pan(-0.1, 0, canvas, True)
            elif event.keysym == 'Right':
                pan(0.1, 0, canvas, True)
            elif event.keysym == 'Up':
                pan(0, 0.1, canvas, True)
            elif event.keysym == 'Down':
                pan(0, -0.1, canvas, True)
            elif event.keysym == 'Return':
                innsetPan(text_list, fig, canvas, v_dic)
        elif event.keysym == 'Return':
            command = CommandEntry.get()
            if command != '':
                try:
                    eval(command)
                    CommandEntry.delete(0, 'end')
                except Exception as e:
                    log_w(e)

    def control_key(state, event=None):
        global ctrl
        ctrl = state

    def shift_key(state, event=None):
        global shift
        shift = state

    root.event_add('<<ShiftOn>>', '<KeyPress-Shift_L>', '<KeyPress-Shift_R>')
    root.event_add('<<ShiftOff>>', '<KeyRelease-Shift_L>', '<KeyRelease-Shift_R>')
    root.bind('<<ShiftOn>>', lambda e: shift_key(True))
    root.bind('<<ShiftOff>>', lambda e: shift_key(False))
    root.event_add('<<ControlOn>>', '<KeyPress-Control_L>', '<KeyPress-Control_R>')
    root.event_add('<<ControlOff>>', '<KeyRelease-Control_L>', '<KeyRelease-Control_R>')
    root.bind('<<ControlOn>>', lambda e: control_key(True))
    root.bind('<<ControlOff>>', lambda e: control_key(False))
    root.bind('<Key>', key)

    load_btn = Button(menu_frame, text='Les inn uppsetan', command=lambda: innlesFil(text_list)).pack(side=LEFT)
    save_btn = Button(menu_frame, text='Goym uppsetan', command=lambda: goymuppsetan(text_list)).pack(side=LEFT)

    nytt_kort = Button(menu_frame, text='Nýtt Kort', command=lambda: nyttkort(text_list, fig, canvas, root, v_dic)).pack(side=LEFT)

    tekna_btn = Button(menu_frame, text='Tekna Kort', command=lambda: les_og_tekna(text_list, fig, canvas)).pack(side=LEFT)
    teknaLinjur_btn = Button(menu_frame, text='Tekna Linjur', command=lambda: teknaLinjur(text_list, root)).pack(side=LEFT)
    teknaPrikkar_btn = Button(menu_frame, text='Tekna Prikkar', command=lambda: teknaPrikkar(text_list, root)).pack(side=LEFT)
    goymmynd_btn = Button(menu_frame, text='Goym Mynd', command=lambda: goymmynd(fig, canvas, figsize, v_dic)).pack(side=LEFT)

    pan_upp = Button(controls_frame, text='↑', font='Helvetica', command=lambda: pan(0, 0.1, canvas, True)).pack(side=TOP)
    controlsLR_frame = Frame(controls_frame)
    controlsLR_frame.pack(side=TOP, anchor=W)
    pan_vinstra = Button(controlsLR_frame, text='←', font='Helvetica', command=lambda: pan(-0.1, 0, canvas, True)).pack(side=LEFT)
    pan_høgra = Button(controlsLR_frame, text='→', font='Helvetica', command=lambda: pan(0.1, 0, canvas, True)).pack(side=LEFT)
    pan_niður = Button(controls_frame, text='↓', font='Helvetica', command=lambda: pan(0, -0.1, canvas, True)).pack(side=TOP)
    Label(controls_frame, text=' ').pack(side=TOP)
    v_dic = {}
    zoomin_btn = Button(controls_frame, text='+', command=lambda: zoom(0.01, text_list, v_dic)).pack(side=TOP)
    zoomout_btn = Button(controls_frame, text='-', command=lambda: zoom(-0.01, text_list, v_dic)).pack(side=TOP)

def innsetPan(text_list, fig, canvas, v_dic):
    print('Innsetur nýggj pan virðir')
    global ax
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    lon, lat = [xlim, ylim]
    raw_text = str(text_list.get("1.0", END))
    text = raw_text.split('\n')
    for command in text:
        if '=' in command:
            toindex = command.find('=') + 1
            variable = command[0:toindex - 1]
            if variable == 'latmax':
                v_dic['req']['latmax'] = float(command[toindex::])
                raw_text = raw_text.replace(command, "latmax=" + str(lat[1]))
            elif variable == 'latmin':
                v_dic['req']['latmin'] = float(command[toindex::])
                raw_text = raw_text.replace(command, "latmin=" + str(lat[0]))
            elif variable == 'lonmin':
                v_dic['req']['lonmin'] = float(command[toindex::])
                raw_text = raw_text.replace(command, "lonmin=" + str(lon[0]))
            elif variable == 'lonmax':
                v_dic['req']['lonmax'] = float(command[toindex::])
                raw_text = raw_text.replace(command, "lonmax=" + str(lon[1]))
    text_list.delete(1.0, END)
    text_list.insert(INSERT, raw_text)
    les_og_tekna(text_list.get("1.0", END), fig, canvas)

def pan(x, y, canvas, ccrs_projection, relative=False):
    global ax
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    if relative:
        xdiff = abs(xlim[0]-xlim[1])
        ydiff = abs(ylim[0] - ylim[1])
        ax.set_xlim([xlim[0] + xdiff*x, xlim[1] + xdiff*x], ccrs_projection)
        ax.set_ylim([ylim[0] + ydiff*y, ylim[1] + ydiff*y], ccrs_projection)
    else:
        ax.set_xlim([xlim[0] + x, xlim[1] + x])
        ax.set_ylim([ylim[0] + y, ylim[1] + y])
    canvas.draw()

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

def goymmynd(fig, canvas, figsize, v_dic):
    log_b()
    filnavn = filedialog.asksaveasfilename(parent=root, title="Goym mynd",  filetypes=(("pdf Fílur", "*.pdf"), ("png Fílur", "*.png"), ("jpg Fílur", "*.jpg")))
    print('Goymir mynd')
    #fig.savefig(filnavn, dpi=dpi, bbox_inches='tight') # 01/04 - 19
    #fig.savefig(filnavn, dpi=dpi, bbox_inches=tns.Bbox([[0, 0], [20, 20]]))
    fig.savefig(filnavn, dpi=v_dic['req']['dpi'])

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

def zoom(mongd, textbox, v_dic):
    print('zoom ' + str(mongd))
    raw_text = str(textbox.get("1.0", END))
    text = raw_text.split('\n')
    for command in text:
        if '=' in command:
            toindex = command.find('=')+1
            variable = command[0:toindex-1]
            if variable == 'latmax':
                v_dic['req']['latmax'] = float(command[toindex::])
                raw_text = raw_text.replace(command, "latmax="+str(-mongd + v_dic['req']['latmax']))
            elif variable == 'latmin':
                v_dic['req']['latmin'] = float(command[toindex::])
                raw_text = raw_text.replace(command, "latmin="+str(mongd + v_dic['req']['latmin']))
            elif variable == 'lonmin':
                v_dic['req']['lonmin'] = float(command[toindex::])
                raw_text = raw_text.replace(command, "lonmin=" + str(mongd + v_dic['req']['lonmin']))
            elif variable == 'lonmax':
                v_dic['req']['lonmax'] = float(command[toindex::])
                raw_text = raw_text.replace(command, "lonmax=" + str(-mongd + v_dic['req']['lonmax']))
    textbox.delete(1.0, END)
    textbox.insert(INSERT, raw_text)

def les_og_tekna(text, fig, canvas, silent=False, v_dic = {}):
    # TODO Ger varabil til max dýpið
    wh_mode = False
    log_clear()
    log_b()
    global ax
    VisProgress = False
    try:
        strtext = text.get("1.0", END)
    except AttributeError:
        strtext = text
    else:
        VisProgress = True
    strtext = strtext.split('\n')
    dybdarlinjur = False
    v_dic['req'] = {'latmax': 62.4, 'lonmax': -6.2, 'latmin': 61.35, 'lonmin': -7.7}
    v_dic['req']['dpi'] = 400
    breiddarlinjur = np.linspace(v_dic['req']['latmin'], v_dic['req']['latmax'], 10)
    longdarlinjur = np.linspace(v_dic['req']['lonmin'], v_dic['req']['lonmax'], 10)
    filnavn = 'test'
    landlitur = 'lightgray'
    btn_interpolation = 'nearest'
    btn_track = False
    btn_gridsize = 1000
    suppress_ticks = True
    linjuSlag = 'dotted'
    btn_striku_hvor = 5
    qskala = 0.001
    scatter_std = 1
    lin_farv='b'
    lin_legend=''
    scatter_farv = 'b'
    scatter_legend=''
    scatter_MarkerStyle = "o"
    show_legend = False
    quiverf_threshold = 1
    circle_stodd = 0.05
    renderengine='Standard Kort'
    s3 = 1 #z scale
    ncol = 1
    scatter_tekst = False
    clabel = False
    fontsize = 15
    tekstx = 0
    teksty = 0
    siglignsferd = 0 # Um ikki null verður tíðin tað tekur at sigla eftir lin_fil rokna
    tekna_land = True
    textsize = 5
    global ccrs_projection
    ccrs_projection = ccrs.PlateCarree(-7)
    for index, command in enumerate(strtext):
        if VisProgress:
            text.tag_add('aktiv_linja', str(index + 1.0), str(index + 2.0))
            text.tag_config('aktiv_linja', foreground='black', background='darkorange')
            text.tag_add('lidug_linja', '0.0', str(index+1.0))
            text.tag_config('lidug_linja', foreground='black', background='lightgreen')
        if not silent:
            print(command)
        if "=" in command:
            toindex = command.find('=')+1
            variable = command[0:toindex-1]
            value = command[toindex::]
            if chk_req(variable, value, v_dic):
                pass
            elif variable == 'renderengine':
                renderengine = command[toindex::]
            elif variable == 'landlitur':
                landlitur = command[toindex::]
            elif variable == 'title':
                ax.set_title(command[toindex::])
                filnavn = command[toindex::]
            elif variable == 'dpi':
                v_dic['req']['dpi'] = float(command[toindex::])
            elif variable == 'tekna_land':
                if command[toindex::] == 'False':
                    tekna_land = False
                elif command[toindex::] == 'True':
                    tekna_land = True

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
                    #ax.scatter(D_lon, D_lat, zorder=100, color=scatter_farv, label=scatter_legend, s=scatter_std,
                    #           marker=scatter_MarkerStyle)
                    D_dep = np.array(lis[i * j * 2: i * j * 3]).reshape((j, i))  # third  i*j instances
                    pda=[]
                    plon=[]
                    plat=[]
                    for iiiio, dep in enumerate(D_dep):
                        for i2o, depe in enumerate(dep):
                            if((61.62799 > D_lat[iiiio, i2o] > 61.59211) and (-6.9192 < D_lon[iiiio, i2o] < -6.80300)):
                                plon.append(D_lon[iiiio, i2o])
                                plat.append(D_lat[iiiio, i2o])
                                if D_dep[iiiio, i2o] == float(-99.9):
                                    pda.append(0)
                                else:
                                    pda.append(D_dep[iiiio, i2o])
                    print(len(plon))
                    qwery = {'d': pda, 'lon':plon, 'lat':plat}
                    fart = pd.DataFrame(qwery)
                    fart.to_csv('lvdypid.f')
                    levels = range(0, 80, 5)
                    c = ax.contour(D_lon, D_lat, D_dep, levels=levels)
                    #MD_lon, MD_lat = m(D_lon, D_lat)
                    #c = m.contour(MD_lon, MD_lat, D_dep,
                    #              ax=ax)
                    ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')
            elif variable == 'csv_dybdarkort':
                if 'csvData_heilt' not in locals():
                    csvData_heilt = pd.read_csv(command[toindex::])
                csvData = csvData_heilt
                rows_to_drop = []
                print('Tal av punktum áðrenn rudding: ' + str(len(csvData)))
                for row in range(len(csvData)-1, 0, -1):
                    if float(csvData.iloc[row, 0]) > (v_dic['req']['lonmax']+0.05):
                        rows_to_drop.append(row)
                    elif float(csvData.iloc[row, 0]) < (v_dic['req']['lonmin']-0.05):
                        rows_to_drop.append(row)
                    elif float(csvData.iloc[row, 1]) > (v_dic['req']['latmax']+0.05):
                        rows_to_drop.append(row)
                    elif float(csvData.iloc[row, 1]) < (v_dic['req']['latmin']-0.05):
                        rows_to_drop.append(row)
                #csvData = csvData.drop(rows_to_drop) # TODO: Útkommentera hettar
                print('Tal av punktum aftaná rudding: ' + str(len(csvData)))
                btn_lon = csvData['lon']
                btn_lat = csvData['lat']
                dypid = csvData['d']
                btn_x, btn_y = [btn_lon.values, btn_lat.values]
                #btn_x1, btn_y1 = np.meshgrid(btn_x, btn_y)

                meshgridy = np.linspace(v_dic['req']['latmin'], v_dic['req']['latmax'], btn_gridsize)
                meshgridx = np.linspace(v_dic['req']['lonmin'], v_dic['req']['lonmax'], btn_gridsize)
                print('Gridsize =' + str(btn_gridsize))
                meshgridx, meshgridy = [meshgridx, meshgridy]
                meshgridx, meshgridy = np.meshgrid(meshgridx, meshgridy)

                #ax.scatter(meshgridx, meshgridy, s=1)
                if btn_track:
                    if renderengine == '3D_botn':
                        ax.scatter(btn_lon.values, btn_lat.values, -dypid, s=scatter_std, zorder=100)
                    else:
                        ax.scatter(btn_lon.values, btn_lat.values, s=scatter_std, zorder=100, c=dypid)
                #grid_x, grid_y = np.mgrid[np.linspace(latmin, latmax, num=7312), np.linspace(lonmin, lonmax, num=7312)]
                #grid_x, grid_y = np.meshgrid(np.linspace(latmin, latmax, num=7312), np.linspace(lonmin, lonmax, num=7312))
                #grid_z0 = griddata((btn_x, btn_y), dypid.values, (meshgridx, meshgridy), method='linear')
                #print(grid_z0)
                #plt.contour(meshgridx, meshgridy, grid_z0)
                #ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')
            elif variable == 'btn_finn_int':
                tekst = command[toindex::]
                tekst = tekst.split(',')
                meir_enn = float(tekst[0])
                minni_enn = float(tekst[1])
                print('Finnur punktir størri enn ' + str(meir_enn) + ' og minni enn ' + str(minni_enn))
                d_out = []
                lat_out = []
                lon_out = []
                print(len(dypid))
                print(len(btn_lon))
                for i, d in enumerate(dypid):
                    if meir_enn < d < minni_enn:
                        #d_out.append(d)
                        lat_out.append(btn_lat.iloc[i])
                        lon_out.append(btn_lon.iloc[i])
                out_data = pd.DataFrame({'lon': lon_out, 'lat': lat_out})
                out_data.to_csv('btn_finn_int.csv', index=False)
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
                btn_striku_hvor= float(command[toindex::])
            elif variable == 'lin_fil':
                if wh_mode:
                    wh_data = pd.read_csv(command[toindex::], skiprows=16, sep='\t', index_col=0, decimal=",")
                    lineData = pd.DataFrame({'lon': wh_data.iloc[:, 11], 'lat': wh_data.iloc[:, 10]})

                else:
                    lineData = pd.read_csv(command[toindex::])
                avstandur = 0
                if renderengine == '3D_botn':
                    line_x_hj = lineData['lon'].values
                    line_y_hj = lineData['lat'].values
                    line_x = [y for i in range(len(line_x_hj)-1)
                              for y in np.linspace(line_x_hj[i] , line_x_hj[i+1], btn_gridsize)]
                    line_y = [y for i in range(len(line_x_hj) - 1)
                              for y in np.linspace(line_y_hj[i], line_y_hj[i+1], btn_gridsize)]
                    line_z = griddata((btn_lon.values, btn_lat.values), -dypid.values,
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
                    lonLine = lineData['lon'].values
                    latLine = lineData['lat'].values
                    if siglignsferd:
                        for i in range(len(lonLine)-1):
                            #print(distance.distance((latLine[i], lonLine[i]), (latLine[i+1], lonLine[i+1])).m)
                            ax.text(latLine[i], lonLine[i], distance.distance((latLine[i], lonLine[i]), (latLine[i+1], lonLine[i+1])).m, zorder=1000000, fontsize=100)
                            avstandur += distance.distance((latLine[i], lonLine[i]), (latLine[i+1], lonLine[i+1])).m
                        print(str(avstandur) + ' m')
                        print(str(avstandur/siglignsferd/60) + ' min')
                    ax.plot(lineData['lon'].values, lineData['lat'].values, lin_farv, linewidth=0.1, label=lin_legend)
            elif variable == 'scatter_std':
                scatter_std = float(command[toindex::])
            elif variable == 'scatter_fil':
                scatterData = pd.read_csv(command[toindex::])
                line_x = scatterData['lon'].values
                line_y = scatterData['lat'].values
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
                                   , color=scatter_farv, label=scatter_legend, s=scatter_std)
                    else:
                        lables = scatterData['legend'].values
                        for i in range(len(line_x)):
                            ax.scatter(line_x[i], line_y[i], line_z[i]
                                       , zorder=100, label=lables[i], s=scatter_std)
                            print('Funni legend :' + lables[i])
                        show_legend = True
                else:
                    if scatter_tekst:
                        lables = scatterData['legend'].values
                        for i in range(len(line_x)):
                            ax.scatter(line_x[i], line_y[i], zorder=100, c=scatter_farv, s=scatter_std)
                            ax.text(line_x[i], line_y[i], lables[i], horizontalalignment='left', zorder=1000000)
                    else:
                        if Samla:
                            ax.scatter(line_x, line_y, zorder=100, color=scatter_farv, label=scatter_legend, s=scatter_std, marker=scatter_MarkerStyle)

                        else:
                            lables = scatterData['legend'].values
                            for i in range(len(line_x)):
                                ax.scatter(line_x[i], line_y[i], zorder=100, label=lables[i], s=scatter_std, marker=scatter_MarkerStyle)
                                print('Funni legend :' + str(lables[i]))
                            show_legend = True
            elif variable == 'linjuSlag':
                if command[toindex::] == 'eingin':
                    linjuSlag = 'None'
                elif command[toindex::] == 'prikkut':
                    linjuSlag = 'dotted'
                elif command[toindex::] == 'heil':
                    linjuSlag = 'solid'
                else:
                    log_w('Ókent linjuslag')
            elif variable == 'siglignsferd':
                siglignsferd = float(command[toindex::])
            elif variable == 'breiddarlinjur':
                if not renderengine == '3D_botn':
                    breiddarlinjur = np.linspace(v_dic['req']['latmin'], v_dic['req']['latmax'], int(command[toindex::]))
                    #gl = ax.gridlines(ccrs_projection, linestyle=linjuSlag, ylocs=breiddarlinjur, xlocs=longdarlinjur, color='lightgray', draw_labels=True, zorder=100)
                    #gl.xlabels_top = False # TODO Ger hettar orduligt, eg havi útkommentera hettar tí okkurt riggar ikki
                    #gl.ylabels_left = False
            elif variable == 'longdarlinjur':
                if not renderengine == '3D_botn':
                    longdarlinjur = np.linspace(v_dic['req']['lonmin'], v_dic['req']['lonmax'], int(command[toindex::]))
                    gl = ax.gridlines(ccrs_projection, linestyle=linjuSlag, ylocs=breiddarlinjur, xlocs=longdarlinjur, color='lightgray', draw_labels=True, zorder=100)
                    gl.xlabels_top = False
                    gl.ylabels_left = False
            elif variable == 'suppress_ticks':
                if command[toindex::] == 'True':
                    suppress_ticks = True
                else:
                    suppress_ticks = False
            elif variable == 'kortSkala':
                pass
                #m.drawmapscale(lonmax - 0.006, latmax - 0.001, lonmax + 0.018, latmax - 0.015,
                # TODO: M riggar ikki longur, ger okkurt nýtt her
                #m.drawmapscale(v_dic['req']['latmax'] + 0.006, v_dic['req']['latmin'] + 0.001, v_dic['req']['lonmax']-v_dic['req']['lonmin'] + v_dic['req']['lonmin'], v_dic['req']['latmax']-v_dic['req']['latmin']+v_dic['req']['latmin'],
                #               # 500, units = 'm',
                #               int(command[toindex::]), units='km', format='%2.1f',
                #               barstyle='fancy', fontsize=14, yoffset=50,
                #               fillcolor1='whitesmoke', fillcolor2='gray', zorder=10000)
            elif variable == 'savefig':
                if show_legend:
                    print('Showing Legend')
                    leg = ax.legend(loc='best', ncol=ncol)
                    leg.set_zorder(3000)
                fig.savefig(command[toindex::], dpi=int(v_dic['req']['dpi']), bbox_inches='tight')
            elif variable == 'quiver':
                Qdata = pd.read_csv(command[toindex::])
                lon = Qdata['lon']
                lat = Qdata['lat']
                q = ax.quiver(lon.values, lat.values, Qdata['u']*qskala, Qdata['v']*qskala, scale=10, width=0.003, headwidth=5, zorder=100, transform=ccrs_projection)
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
                x_undir, y_undir = [lon_undir, lat_undir]
                x_yvir, y_yvir = [lon_yvir, lat_yvir]

                q = ax.quiver(x_undir, y_undir, u_undir, v_undir, color='g', scale=10, width=0.003, headwidth=5,
                             zorder=100, transform=ccrs_projection)
                ax.quiverkey(q, 0.85, 0.95 - 0 * 0.03, quiverf_threshold*qskala, label='Undir ' + str(quiverf_threshold) + ' m/s', labelpos='W') # 2.57222

                q = ax.quiver(x_yvir, y_yvir, u_yvir, v_yvir, color='r', scale=10, width=0.003, headwidth=5, zorder=100)
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
            elif variable == 'lin_farv' or variable == 'linfarv':
                lin_farv = command[toindex::]
            elif variable == 'lin_legend':
                lin_legend = command[toindex::]
                show_legend = True
            elif variable == 'circle_fil':
                print('Teknar rundingar')
                scatterData = pd.read_csv(command[toindex::])
                line_x = scatterData['lon'].values
                line_y = scatterData['lat'].values
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
                # Gevur næstu scatter plottunum eitt legend
                scatter_legend = command[toindex::]
                show_legend = True
            elif variable == 'scatter_tekst':
                # Ger tað møguligt at tendra og sløkka legend
                if command[toindex::] == 'True':
                    scatter_tekst = True
                else:
                    scatter_tekst = False
            elif variable == 'clabel':
                if command[toindex::] == 'True':
                    clabel = True
                else:
                    clabel = False
            elif variable == 'fontsize':
                fontsize = command[toindex::]
            elif variable == 'tekst':
                ax.text(tekstx, teksty, open(command[toindex::]).read(), fontsize=fontsize, zorder=11)
            elif variable == 'tekstxy':
                temp = command[toindex::].split()
                tekstx = np.float(temp[0])
                teksty = np.float(temp[1])
                print(str(np.float(temp[0])) + ',' + str(np.float(temp[1])))
                print(str(tekstx) + ',' + str(teksty))
            elif variable == 'scatter':
                pos = command[toindex::].split(',')
                lat = float(pos[0])
                lon = float(pos[1])
                ax.scatter(lon, lat, zorder=100, color=scatter_farv, label=scatter_legend, s=scatter_std)
            elif variable == 'scatter_MarkerStyle':
                scatter_MarkerStyle = command[toindex::]
            elif variable == 'wh_mode':
                if command[toindex::] == 'True':
                    wh_mode = True
                else:
                    wh_mode = False
            elif variable == 'nyttkortdir':
                global path_to_nytt_kort
                path_to_nytt_kort = command[toindex::]
            elif variable == 'lesmynd':
                img = mpimg.imread(command[toindex::])
                imgplot = ax.imshow(img, aspect='equal', extent=(-7.66666666, -6.3333333, 62.4166666, 61.4166666), transform=ccrs_projection)
                ax.set_aspect(1 / np.cos(np.deg2rad(((v_dic['req']['latmax'] + v_dic['req']['latmax']) / 2))))
            elif variable == 'textsize':
                textsize = float(command[toindex::])
            else:
                if '#' not in variable and command != '':
                    log_w('Ókend stýriboð ' + variable)
        else:

            if command == 'clf':
                fig.clf()
                #ax = fig.add_subplot(111)
                ax = fig.add_subplot(1, 1, 1, projection=ccrs_projection)
                ax.coastlines('50m')
                ax.set_aspect(1/np.cos(np.deg2rad(((v_dic['req']['latmax']+v_dic['req']['latmax'])/2))))
                #ax.set_aspect('equal', adjustable='box')
                #ax = plt.axes(projection=ccrs.PlateCarree())
            elif command == 'break':
                break
            elif command == 'Tekna kort':
                if renderengine == '3D_botn':
                    #m = Basemap(projection='merc', resolution=None,
                    #            llcrnrlat=latmin, urcrnrlat=v_dic['req']['latmax'],
                    #            llcrnrlon=lonmin, urcrnrlon=lonmax, ax=ax, suppress_ticks=suppress_ticks)
                    ax = fig.add_subplot(111, projection='3d')
                else:
                    if tekna_land:
                        for island in os.listdir('Kort_Data/Coasts'):
                            lo, aa, la = np.genfromtxt('Kort_Data/Coasts/' + island, delimiter=' ').T
                            ax.plot(lo, la, 'k', linewidth=1, transform=ccrs_projection)
                            ax.fill(lo, la, landlitur, zorder=10, transform=ccrs_projection)
                            #xpt, ypt = m(lo, la)
                            #plt.plot(xpt, ypt, 'k', linewidth=1)
                            #ax.fill(xpt, ypt, landlitur, zorder=10)
                    ax.set_extent([v_dic['req']['lonmin'], v_dic['req']['lonmax'], v_dic['req']['latmin'], v_dic['req']['latmax']], ccrs_projection)

            elif command == 'btn_contourf':
                grid_z0 = griddata((btn_lon.values, btn_lat.values), dypid.values, (meshgridx, meshgridy), method=btn_interpolation)
                #grid_z0 = interpolate.interp2d(btn_x, btn_y, dypid.values, kind='cubic')
                vmin = min(-70, min([-y for x in grid_z0 for y in x]))
                vmin = min([-y for x in grid_z0 for y in x])
                lv = list(frange(int(vmin/temp)*temp, float(btn_striku_hvor), float(btn_striku_hvor)))
                lv = np.round(list(frange(vmin, 0, float(btn_striku_hvor))), 3)
                print(lv)
                #lv = list(frange(int(vmin/btn_striku_hvor)*btn_striku_hvor, int(btn_striku_hvor), int(btn_striku_hvor)))
                if renderengine == '3D_botn':
                    cmap = plt.cm.viridis
                    for i in range(250, 256):
                        cmap.colors[i] = [0, 1, 0]
                    ax.plot_surface(meshgridx, meshgridy, -grid_z0, alpha=.85, rcount=50, ccount=50, vmax=0,
                                    cmap=cmap, zorder=21000)
                    ax.set_axis_off()
                    '''
                    print(max(meshgridx[0]))
                    print(meshgridx[0,0])
                    print(max(meshgridy[:,0]))
                    print(meshgridx[0, 0])
                    print(max([y for x in grid_z0 for y in x]))
                    '''
                    scalefactor = float(scatter_farv)                   #Plz fiza meg
                    v1 = max(max(meshgridx[0]), max(meshgridy[:, 0]))
                    v2 = max([y for x in grid_z0 for y in x])
                    ax.set_aspect(scalefactor * v2 / v1)
                else:
                    c = ax.contourf(meshgridx, meshgridy, -grid_z0, lv, transform=ccrs_projection)
                    ax.clabel(c, inline=1, fontsize=15, fmt='%2.0f')
                    #fig.colorbar(c)
                    if vmin >= -150:
                        confti=list(range(int(vmin/10)*10, int(10), int(10)))
                    else:
                        confti = list(range(int(vmin / 20) * 20, int(20), int(20)))
                    #fig.colorbar(c, orientation='horizontal', ax=ax, ticks=confti, pad=0.02)
                    fig.colorbar(c, ax=ax, pad=0.02)
            elif command == 'btn_contour':
                print('Number of points: ' + str(btn_lon.values) + ' ' + str(btn_lat.values) + ' ' + str(dypid.values))
                grid_z0 = griddata((btn_lon.values, btn_lat.values), dypid.values, (meshgridx, meshgridy), method=btn_interpolation)
                vmin = min(-70, min([-y for x in grid_z0 for y in x]))
                temp = btn_striku_hvor
                lv = list(frange(int(vmin/temp)*temp, float(btn_striku_hvor), float(btn_striku_hvor)))
                lv = np.round(list(frange(vmin, 0, float(btn_striku_hvor))), 3)
                print(lv)
                #grid_z0 = interpolate.interp2d(btn_x, btn_y, dypid.values, kind='cubic')
                if renderengine == '3D_botn':
                    ax.contour3D(meshgridx, meshgridy, -1 * grid_z0, levels=lv,
                                 colors='k',vmax=0 , linestyles='solid')
                else:
                    c = ax.contour(meshgridx, meshgridy, -grid_z0, lv, transform=ccrs_projection, colors='gray', linestyles='solid', linewidths=0.3)
                    if clabel:
                        #ax.clabel(c, inline=1, fontsize=fontsize, fmt='%2.0f', manual=False)
                        ax.clabel(c, inline=1, fontsize=fontsize, fmt='%2.0f', manual=True)
            elif command == 's3':
                s3 = float(command[toindex::])
            elif command == 'ncol':
                ncol = int(command[toindex::])
            else: # Ókend kommando!
                if '#' not in command and command != '':
                    log_w('Ókend stýriboð ' + command)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    if show_legend:
        print('Showing Legend')
        leg = ax.legend(loc='best', ncol=ncol)
        leg.set_zorder(3000)
    if renderengine == '3D_botn':
        s1 = v_dic['req']['latmax']
        s2 = v_dic['req']['latmax']
        sm = max(s1,s2)
        s1 = s1/sm
        s2 = s2/sm
        def short_proj():
            return np.dot(Axes3D.get_proj(ax), np.diag([s1, s2, 1, 1]))

        ax.get_proj = short_proj
        print('hello')
    if VisProgress:
        print(text.tag_names())
        tags = text.tag_names()
        for tag in tags:
            text.tag_delete(tag)
        #text.tag_add('alt', '0.0', END)
        #text.tag_config('alt', foreground='black', background='white')
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    log_e()
    global ispressed
    ispressed = False


    def onclick(event):
        global ispressed, zoom_x_fra, zoom_y_fra
        global a
        global b
        a, b = event.xdata, event.ydata
        ispressed = True
        zoom_x_fra, zoom_y_fra = event.xdata, event.ydata
        try:
            print('%f, %f' % (event.xdata, event.ydata))
        except TypeError:
            pass
        else:
            string = str(event.xdata) + ',' + str(event.ydata)
            pyperclip.copy(string)


    def onmove(event):
        global ispressed, zoom_x_fra, zoom_y_fra, ccrs_projection
        if ispressed:
            pan(zoom_x_fra-event.xdata, zoom_y_fra-event.ydata, canvas, ccrs_projection)


    def release(event):
        global ispressed
        ispressed = False


    #bid = fig.canvas.mpl_connect('motion_notify_event', onmove)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    fig.canvas.mpl_connect('button_release_event', release)

def nyttkort(text, fig, canvas, root, v_dic):
    global path_to_nytt_kort
    print(path_to_nytt_kort)
    F = open(path_to_nytt_kort, 'r')
    nyttkort_text = F.read()
    F.close()
    if len(text.get("1.0", END)) > 1:
        if messagebox.askyesno("Ávaring", "Vilt tú yvurskriva núverani kort?", parent=root):
            text.delete(1.0, END)
            text.insert(INSERT, nyttkort_text)
    else:
        text.insert(INSERT, nyttkort_text)
    les_og_tekna(text, fig, canvas, False, v_dic)
    print(path_to_nytt_kort)


def frange(x, y, jump):
  while x < y:
    yield x
    x += jump