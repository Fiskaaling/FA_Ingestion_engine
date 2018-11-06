from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdate
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import time
import datetime as dt

def botnmatPlt(frame, root2):
    global root

    global stru

    global strv

    stru = 'Kort_Data/u.txt'

    strv = 'Kort_Data/v.txt'

    longd = 10

    hædd = 4.8

    startdato_str = '20.05.18'

    endadato_str = '30.07.18'

    dato_a_xksa = 8  # sikkurt +1

    takast_av = 0  # metrar takast av toppinum

    takast_av_botni = 0

    fpbadi = 'B'  # (F) farvu, (P) píl, (B) Bæði

    hvatskalplottast = 'abs'  # U V ella abs

    titil = 'Harast streymur í juli'  # titil

    vmin_max = True

    boolabs = False

    talavpilum = 24




    filnavn = '/home/johannus/Documents/FA_Ingestion_engine/Kort_Data/Syðradalur.txt'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Streymmátinar frá botni', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Streymmátinar frá botni').pack(side=TOP, anchor=W)

    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)

    veluMappuBtn = Button(menuFrame, text='Vel U Fíl', command=lambda: veluFil())
    veluMappuBtn.pack(side=LEFT)

    velvMappuBtn = Button(menuFrame, text='Vel V Fíl', command=lambda: velvFil())
    velvMappuBtn.pack(side=LEFT)

    teknaPltBtn = Button(menuFrame, text='Tekna Plot', command=lambda: tekna(stru, strv, fraEntry.get(), tilEntry.get(),
                                                                             dato_a_xksa,takast_av, takast_av_botni,
                                                                             FPBEntry.get(), UVaEntry.get(), titil, vmin_max,
                                                                             boolabs, talavpilum,fig,canvas))
    teknaPltBtn.pack(side=LEFT)

    Label(menuFrame, text='Frá:').pack(side=LEFT)

    fraEntry = Entry(menuFrame, width=8)
    fraEntry.pack(side=LEFT)
    fraEntry.insert(0, startdato_str)

    Label(menuFrame, text='Til:').pack(side=LEFT)
    tilEntry = Entry(menuFrame, width=8)
    tilEntry.pack(side=LEFT)
    tilEntry.insert(0, endadato_str)

    Label(menuFrame, text='FPB:').pack(side=LEFT)
    FPBEntry = Entry(menuFrame, width=1)
    FPBEntry.pack(side=LEFT)
    FPBEntry.insert(0, fpbadi)

    Label(menuFrame, text='UV/abs:').pack(side=LEFT)
    UVaEntry = Entry(menuFrame, width=3)
    UVaEntry.pack(side=LEFT)
    UVaEntry.insert(0, hvatskalplottast)

    fig = Figure(figsize=(8, 12), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)

def veluFil():
    global stru
    stru = filedialog.askopenfile(title='Vel fíl', filetypes = (("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    print(stru)

def velvFil():
    global strv
    strv = filedialog.askopenfile(title='Vel fíl', filetypes = (("csv Fílir", "*.csv"), ("all files", "*.*"))).name
    print(strv)

def tekna(stru, strv, startdato_str, endadato_str, dato_a_xksa,
    takast_av, takast_av_botni, fpbadi, hvatskalplottast, titil, vmin_max, boolabs, talavpilum, fig, canvas):
    fig.clf()
    ax = fig.add_subplot(111)
    if fpbadi == 'F':
        pil = False
    elif fpbadi == 'P':
        pil = True
        hvatskalplottast = 'off'
    else:
        pil = True

    # inles u og v
    def inles_uv(stru, strv):
        df_u = pd.read_csv(stru, skiprows=11, sep='\t', index_col=0, decimal=",")
        df_v = pd.read_csv(strv, skiprows=11, sep='\t', index_col=0, decimal=",")
        i = list(df_u.keys()).index('1')
        data_u = np.array(df_u.iloc[:, i::])
        j = 0

        while np.isnan(data_u[j, 0]):
            j += 1

        data_u = data_u[j::, 0:len(data_u[0, :])]
        data_v = np.array(df_v.iloc[j::, i::])
        data_u = np.transpose(data_u) / 1000
        data_v = np.transpose(data_v) / 1000
        data_abs = np.sqrt(np.square(data_u) + np.square(data_v))

        # setup dato

        #plt.figure(figsize=[longd, hædd])

        Bin_Size_u = 4.00  # ger hettar automatist

        temp = list(df_u.keys()).index('YR')
        datodata = np.array(df_u.iloc[j::, temp:temp + 6])
        dato = [mdate.date2num(dt.datetime(x[0]+2000,x[1],x[2],x[3],x[4],x[5])) for x in datodata]

        return data_u, data_v, data_abs, Bin_Size_u, dato

    def meshsetup(startdato_str, endadato_str, takast_av, takast_av_botni, Bin_Size_u, data_u, data_v, data_abs, dato):
        startdato = max(dato[0],mdate.date2num(dt.datetime.strptime(startdato_str,'%d.%m.%y')))
        endadato = min(dato[-1],mdate.date2num(dt.datetime.strptime(endadato_str,'%d.%m.%y')))
        print(dato.index(startdato))
        print(dato.index(endadato))
        time.sleep(3600)
        startdato_i = dato.index(startdato)
        endadato_i  = dato.index(endadato)

        '''
        alt er ok í meshsetup her og til'''






        ll = endadato - startdato
        ll_step = int(max(ll / dato_a_xksa, 1))

        # setup plot
        topav = int(np.ceil(takast_av / Bin_Size_u))
        botnpav = int(np.ceil(takast_av_botni / Bin_Size_u))

        X, Y = np.meshgrid(np.arange(startdato_i, endadato_i),
                           np.arange(Bin_Size_u * (len(data_u[:, 0]) - botnpav), topav * Bin_Size_u, -Bin_Size_u))
        data_plot_u = data_u[botnpav:len(data_u[:, 0]) - topav, startdato_i: endadato_i]
        data_plot_v = data_v[botnpav:len(data_v[:, 0]) - topav, startdato_i: endadato_i]
        data_plot_abs = data_abs[botnpav:len(data_abs[:, 0]) - topav, startdato_i: endadato_i]
        return startdato, endadato, startdato_i, endadato_i, ll, ll_step, X, Y, data_plot_u, data_plot_v, data_plot_abs

    def drawcontour(X, Y, data_plot, vmin_max=True, boolabs=False):
        cs = plt.contourf(X, Y, data_plot)
        if boolabs:
            cmap = 'Reds'
            extend = 'max'
        else:
            cmap = 'coolwarm'
            extend = 'both'

        if vmin_max:
            # finn 95% intervaL
            temp = np.reshape(data_plot, (np.product(np.shape(data_plot)), 1))

            temp2 = [x for x in temp if not np.isnan(x)]
            temp2.sort()

            if boolabs:
                vmin = 0
            else:
                vmin = temp2[int(0.025 * len(temp2))] * 1.5
            vmax = temp2[int(0.975 * len(temp2))] * 1.5
            levels = np.arange(vmin, vmax, (vmax - vmin) / 100)
            #fig = plt.contourf(cs, levels=levels, cmap=cmap, extend=extend)
            return cs, levels, cmap, extend
        else:
            levels = np.arange(-10, 10, 1)
            return cs, levels, cmap, extend

    def drawquiver(talavpilum, X, Y, data_plot_u, data_plot_v, data_plot_abs):
        a = talavpilum
        l = len(X[0, :])
        X, Y = np.meshgrid(X[0, 0:l:int(l / a)], Y[:, 0])
        data_plot1 = data_plot_u[:, 0:l:int(l / a)]
        data_plot2 = data_plot_v[:, 0:l:int(l / a)]
        divisor = data_plot_abs[:, 0:l:int(l / a)]
        data_plot1 = np.divide(data_plot1, divisor)
        data_plot2 = np.divide(data_plot2, divisor)

        # plot
        #fig = plt.quiver(X, Y, data_plot1, data_plot2, pivot='mid')
        pivot = 'mid'
        return X, Y, data_plot1, data_plot2, pivot

    data_u, data_v, data_abs, Bin_Size_u, dato = inles_uv(stru, strv)

    startdato, endadato, startdato_i, endadato_i, ll, ll_step, X, Y, data_plot_u, data_plot_v, data_plot_abs = \
        meshsetup(startdato_str, endadato_str, takast_av, takast_av_botni, Bin_Size_u, data_u, data_v, data_abs, dato)

    if hvatskalplottast == 'U':
        data_plot = data_plot_u
    elif hvatskalplottast == 'V':
        data_plot = data_plot_v
    else:
        data_plot = data_plot_abs
        boolabs = True
    if hvatskalplottast != 'off':
        temp = drawcontour(X, Y, data_plot, vmin_max, boolabs)
        ax.contourf(temp[0], levels=temp[1], cmap=temp[2], extend=temp[3])
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Streymur ' + r'$\left(\frac{m}{s}\right)$')
    if pil:
        #fig2 = drawquiver(talavpilum, X, Y, data_plot_u, data_plot_v, data_plot_abs)
        X, Y, data_plot1, data_plot2, pivot = drawquiver(talavpilum, X, Y, data_plot_u, data_plot_v, data_plot_abs)
        ax.quiver(X,Y , data_plot1,data_plot2 , pivot = pivot)

    plt.title(titil)
    plt.xlabel('Date')
    plt.ylabel('djúpd (m)')
    plt.gca().invert_yaxis()
    plt.xticks(datoskift[startdato:startdato + ll:ll_step], dato[startdato:startdato + ll:ll_step])  # rotate
    temp = ax.axis()
    ax.axis((temp[0], temp[1], temp[3], temp[2]))

    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    #plt.savefig(titil)
    #plt.show()