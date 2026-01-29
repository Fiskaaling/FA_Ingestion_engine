import os
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import getpass  # Til at fáa brúkaranavn
import subprocess
import xml.etree.ElementTree as ET

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import Ingestion.CTD.cruise_overview
from misc.faLog import gerlog, log_e, log_b, log_print, log_w, log_clear
from misc.sha2calc import get_hash

import Ingestion.CTD.misc.ba_gui as ba_gui
from Ingestion.CTD.misc.quality_control import qcontrol
import Ingestion.CTD.skraset_stodir
from Ingestion.CTD.misc.ctd_pump import pumpstatus

#from shutil import copyfile
textsize = 16

SEA_BIRD_WINE_PATH = 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/'


def bin_average_frame(frame, root2, mappunavn='./Ingestion/CTD/Lokalt_Data/2019-01-17/Processed/ASCII_ALL'):
    mappunavn_dict = {'mappunavn': mappunavn}
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Bin Average').pack(side=TOP, anchor=W)
    mappunavn_dict['controlsFrame'] = Frame(frame)
    mappunavn_dict['controlsFrame'].pack(side=TOP, anchor=W)
    mappunavn_dict['sensorsFrame'] = Frame(mappunavn_dict['controlsFrame'])
    mappunavn_dict['sensorsFrame'].pack(side=LEFT, anchor=N)
    velMappuBtn = Button(mappunavn_dict['controlsFrame'], 
                         text='Vel Fílir', 
                         command=lambda: velFil(mappunavn_dict))
    velMappuBtn.pack(side=LEFT, anchor=W)

    processBtn = Button(mappunavn_dict['controlsFrame'], 
                        text='Les inn', 
                        command=lambda: processera(root, fig, canvas, 
                                                   Quality_frame, mappunavn_dict))
    processBtn.pack(side=LEFT, anchor=W)

    # Right frame
    Right_frame = Frame(frame)
    Right_frame.pack(fill=BOTH, expand=False, side=RIGHT, anchor=N)

    # Plot frame
    fig = Figure(figsize=(12, 8), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, 
                       highlightbackground="green", highlightcolor="green", 
                       highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)

    #Quality frame
    Quality_frame = Frame(Right_frame)
    Quality_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    log_frame = Frame(Right_frame, height=300, width=600, borderwidth=1, 
                      highlightbackground="green", highlightcolor="green", 
                      highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)
    mappunavn_dict['filur'] = 0

    mappunavn_dict['continuebtn'] = Button(Quality_frame, 
                                           text='Halt áfram', 
                                           command=lambda: Ingestion.CTD.skraset_stodir(frame, root2))
    mappunavn_dict['continuebtn'].pack(side=TOP, 
                                       anchor=W)

    processera(root, fig, canvas, Quality_frame, mappunavn_dict, frame)



def velFil(mappunavn):
    mappunavn['mappunavn'] = filedialog.askdirectory(title='Vel túramappu', 
                                                     initialdir='./Ingestion/CTD/Lokalt_Data/')



def processera(root, fig, canvas, Quality_frame, mappunavn_dict, frame):
    mappunavn = mappunavn_dict['mappunavn']
    log_b()
    midlingstid = 2  # sek
    fig.clf()
    mappunavn_dict['ax'] = fig.subplots()
    if os.path.exists(mappunavn):
        filnavn = os.listdir(mappunavn)
    else:
        messagebox.showerror("Feilur", "Mappan er ikki til")
        return
    filnavn.sort()
    mappunavn_dict['toggle_ax'] = 0
    mappunavn_dict['toggle_temp'] = 0
    mappunavn_dict['toggle_FlECO'] = 0
    mappunavn_dict['toggle_Sbeox0PS'] = 0
    mappunavn_dict['toggle_Sal00'] = 0
    mappunavn_dict['toggle_par'] = 0
    mappunavn_dict['toggle_C0mS'] = 0
    print('Loading data')
    print(f"File number: {mappunavn_dict['filur']}")
    print(f"File path: {mappunavn}{filnavn[mappunavn_dict['filur']]}")
    
    # Load data
    data = pd.read_csv(f"{mappunavn}/{filnavn[mappunavn_dict['filur']]}", 
                       encoding='latin-1')  # Les fíl

    list_of_casts = os.listdir(mappunavn)
    list_of_casts.sort()
    print(f'Mappunavn: {mappunavn}')
    
    parent_folder = mappunavn.split('Processed')[0]
    print(f'Parent folder: {parent_folder}')
    
    # Kanna um metadatamappan er til
    if not os.path.isdir(parent_folder + '/ASCII/metadata'):
        os.makedirs(parent_folder + '/ASCII/metadata')  # Um ikki, ger hana

    metadata, finished_processing = ba_gui.refresh_qframe(Quality_frame, list_of_casts, 
                                                          parent_folder, filnavn, 
                                                          mappunavn_dict)
    log_print('Finished_processing?: ' + str(finished_processing))
    if finished_processing:
        pass
    #        mappunavn_dict['continuebtn'].lift()
    Label(Quality_frame, text=('―' * 20), font=("Courier", textsize)).pack(side=TOP, anchor=W)
    quality_subframe = Frame(Quality_frame)
    quality_subframe.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    dypid = data['PrdM']
    maxd = max(dypid)
    time_fulllength = data['TimeS']
    start_index = 1
    timeAx = data.TimeS[start_index:]

    # Plottar Dýpið
    x_aksi = timeAx
    mappunavn_dict['start_index'] = start_index
    mappunavn_dict['x_aksi'] = timeAx
    mappunavn_dict['d_plot'] = mappunavn_dict['ax'].plot(x_aksi, dypid[start_index:])
    mappunavn_dict['ax'].set_ylim(-1, maxd + 1)
    mappunavn_dict['ax'].set_xlabel('Tíð [s]')
    mappunavn_dict['ax'].set_ylabel('Dýpið [m]', color='k')

    myvar = []
    n_midlingspunktir = int(np.ceil(midlingstid / (max(data.TimeS) / len(data))))
    for i in range(len(data[data.columns[0]]) - 2):
        myvar.append(np.var(dypid[i:i + n_midlingspunktir]))

    # Rokna ferð á CTD
    diff_d = []
    for i in range(1, len(dypid)):
        diff_d.append((dypid[i - 1] - dypid[i]) / (time_fulllength.iloc[i - 1] - time_fulllength.iloc[i]))
    
    var_greinsa = 0.01 # Fyrr 0.01
    [pump_on, pump_off] = pumpstatus(mappunavn_dict['mappunavn'], filnavn[mappunavn_dict['filur']])
    
    # states = ["PreSoak", "soak_start", "soak_stop", "downcast_start", "downcast_stop", "upcast_start", "upcast_stop"]
    # current_stat = states[0]
    # log_print(current_stat)
    if not metadata:
        soak_start = -1
        soak_stop = -1
        downcast_start = -1
        downcast_stop = -1
        upcast_start = -1
        upcast_stop = -1

        # Hettar er kodan ið finnur nær tey ymsku tingini henda
        # states = ["PreSoak", "soak_start", "soak_stop", "downcast_start", "downcast_stop", "upcast_start", "upcast_stop"]
        current_stat = "PreSoak"
        for i, d in enumerate(dypid):  
            # Bíða 5 sek áðrenn byrja verður at leita eftir hvar soak byrjar
            if current_stat == "PreSoak":  
                if time_fulllength[i] > 5:
                    current_stat = "soak_start"

            elif current_stat == "soak_start":
                # bíða til eftir 3m at kanna
                if d < 3:
                    continue
                # set rímilig virði um einki soak er
                elif d > 20:
                    soak_start = int(i / 2)
                    soak_stop = pump_on
                    current_stat = "downcast_prepare"
                # finn hvar dypið stabiliserar seg og set 'soak start'
                else:
                    if np.var(dypid[i:i + n_midlingspunktir]) < var_greinsa:
                        soak_start = i
                        current_stat = "soak_stop"

            elif current_stat == "soak_stop":
                # finn hvar dypið byrjar at broytast og set 'soak stop'
                if np.var(dypid[i:i + n_midlingspunktir]) > var_greinsa*5:
                    soak_stop = i-1 + n_midlingspunktir
                    current_stat = "downcast_prepare"

            elif current_stat == "downcast_prepare":
                if d > 15:
                    current_stat = "downcast_start"
                if d > 3:
                    continue
                else:
                    # finn hvar dypið stabiliserar seg og kanna downcast start
                    if d < 2 and np.var(dypid[i:i + n_midlingspunktir]) < var_greinsa:
                        current_stat = "downcast_start"

            elif current_stat == "downcast_start":
                # um einki soak, set 'downcast start' til pump on
                if d > 15:
                    downcast_start = pump_on + 50
                    current_stat = "downcast_stop"
                # finn hvar dypið byrjar at broytast og set 'downcast start'
                elif np.var(dypid[i:i + n_midlingspunktir]) > var_greinsa:
                    downcast_start = i + n_midlingspunktir
                    current_stat = "downcast_stop"

            elif current_stat == "downcast_stop":
                if d == maxd:
                    downcast_stop = i
                    upcast_start = i+32
                    current_stat = "upcast_stop"

            elif current_stat == "upcast_stop":
                if np.var(dypid[i:i + n_midlingspunktir]) > var_greinsa:
                    upcast_stop = i
            else:
                pass
    
    # Um metadata eru        
    else:
        log_print('Lesur goymd event virðir')
        soak_start = int(metadata['soak_start'])
        soak_stop = int(metadata['soak_stop'])
        downcast_start = int(metadata['downcast_start'])
        downcast_stop = int(metadata['downcast_stop'])
        upcast_start = int(metadata['upcast_start'])
        upcast_stop = int(metadata['upcast_stop'])



    if pump_on != -1:
        mappunavn_dict['ax'].plot([pump_on / 16, pump_on / 16], [-100, maxd + 1], ':')
        log_print('Pumpan tendraði aftaná: ' + str(pump_on / 16) + ' sek')

    if pump_off != -1:
        log_print('Pumpan sløknaði aftaná: ' + str(pump_off / 16) + ' sek')
        mappunavn_dict['ax'].plot([pump_off / 16, pump_off / 16], [-100, maxd + 1], ':')

    event_dict = {'time_fulllength': time_fulllength, 
                  'soak_start': soak_start, 'soak_stop': soak_stop, 
                  'downcast_start': downcast_start, 'downcast_stop': downcast_stop, 
                  'upcast_start': upcast_start, 'upcast_stop': upcast_stop}

    ba_gui.kanna_events(event_dict, log_w)

    soak_line_dict = {'soak_start_line': mappunavn_dict['ax'].plot([x_aksi[event_dict['soak_start']], 
                                                                    x_aksi[event_dict['soak_start']]], 
                                                                   [-100, maxd + 1], 'k'), 
                      'soak_stop_line': mappunavn_dict['ax'].plot([x_aksi[event_dict['soak_stop']], 
                                                                   x_aksi[event_dict['soak_stop']]], 
                                                                   [-100, maxd + 1], 'k'),
                      'downcast_start_line': mappunavn_dict['ax'].plot([x_aksi[event_dict['downcast_start']], 
                                                                        x_aksi[event_dict['downcast_start']]], 
                                                                        [-100, maxd + 1], 'k'),
                      'downcast_stop_line': mappunavn_dict['ax'].plot([x_aksi[event_dict['downcast_stop']], 
                                                                       x_aksi[event_dict['downcast_stop']]], 
                                                                       [-100, maxd + 1], 'k'),
                      'upcast_start_line': mappunavn_dict['ax'].plot([x_aksi[event_dict['upcast_start']], 
                                                                     x_aksi[event_dict['upcast_start']]], 
                                                                     [-100, maxd + 1], 'k'),
                      'upcast_stop_line': mappunavn_dict['ax'].plot([x_aksi[event_dict['upcast_stop']], 
                                                                     x_aksi[event_dict['upcast_stop']]], 
                                                                     [-100, maxd + 1], 'k')}

    event_dict['selected_event'] = 0
    zoomed_in_dict = {'zoomed_in': False, 'onlyDowncast': False}
    if soak_start != -1:
        soak_line_dict['annotation'] = mappunavn_dict['ax'].annotate('Soak Start',
                                                                     xy=(time_fulllength[soak_start], maxd + 1),
                                                                     xytext=(time_fulllength[soak_start], maxd + 2),
                                                                     xycoords='data',
                                                                     textcoords='data',
                                                                     ha='center',
                                                                     arrowprops=dict(arrowstyle="->"))

    if True:  # Um flaggi ikki er 0, markera mátingina reyða
        fra = 0
        til = 1
        lastflag = 0
        for i, flag in enumerate(data.Flag):
            if lastflag == 0 and flag != 0:
                fra = i
                til = 1
            if lastflag != 0 and flag == 0:
                til = i
                farvaHer = np.zeros((len(data), 1))
                farts = []
                for i in range(len(data)):
                    fra = int(fra)
                    til = int(til)
                    if (i > fra) and (i < til):
                        farvaHer[i] = 1
                        farts.append(True)
                    else:
                        farts.append(False)
                mappunavn_dict['ax'].fill_between(data.TimeS, maxd + 1, 0, 
                                                  where=farts, facecolor='red', alpha=0.1)

            lastflag = flag

    qcontrol(quality_subframe, dypid, event_dict, pump_on, filnavn[mappunavn_dict['filur']])

    def key(event):
        update_annotations = False
        update_qframe = False
        x_aksi = mappunavn_dict['x_aksi']

        if zoomed_in_dict['zoomed_in']:
            move_amount = 1
        else:
            move_amount = 8

    
    # CHOSE CAST FILE

        # next file
        if event.keysym == 'w':
            if mappunavn_dict['filur'] < len(filnavn) - 1:
                mappunavn_dict['filur'] += 1
                update_qframe = True

        # previous file
        elif event.keysym == 'q':
            if mappunavn_dict['filur'] != 0:
                mappunavn_dict['filur'] -= 1
                update_qframe = True


    # EVENT LINES

        # CHANGING LINES
        # go to previous event line
        elif event.keysym == 'h':
            # if not in zoomed state and if not at line 0
            if not zoomed_in_dict['zoomed_in']:
                if event_dict['selected_event'] != 0:
                    event_dict['selected_event'] -= 1
                    update_annotations = True

        # go to next event line
        elif event.keysym == 'l':
            if not zoomed_in_dict['zoomed_in']:
                if event_dict['selected_event'] != 5:
                    event_dict['selected_event'] += 1
                    update_annotations = True
 

        # MOVING LINES
        # move event line to the right
        elif event.keysym == 'j':
            if event_dict['selected_event'] == 0:
                event_dict['soak_start'] -= move_amount
            elif event_dict['selected_event'] == 1:
                event_dict['soak_stop'] -= move_amount
            elif event_dict['selected_event'] == 2:
                event_dict['downcast_start'] -= move_amount
            elif event_dict['selected_event'] == 3:
                event_dict['downcast_stop'] -= move_amount
            elif event_dict['selected_event'] == 4:
                event_dict['upcast_start'] -= move_amount
            elif event_dict['selected_event'] == 5:
                event_dict['upcast_stop'] -= move_amount

        # move event line to the left
        elif event.keysym == 'k':
            if event_dict['selected_event'] == 0:
                event_dict['soak_start'] += move_amount
            elif event_dict['selected_event'] == 1:
                event_dict['soak_stop'] += move_amount
            elif event_dict['selected_event'] == 2:
                event_dict['downcast_start'] += move_amount
            elif event_dict['selected_event'] == 3:
                event_dict['downcast_stop'] += move_amount
            elif event_dict['selected_event'] == 4:
                event_dict['upcast_start'] += move_amount
            elif event_dict['selected_event'] == 5:
                event_dict['upcast_stop'] += move_amount

    # TOGGLE ZOOM
        # in
        elif event.keysym == 'i':
            if not zoomed_in_dict['zoomed_in']:
                zoomed_in_dict['zoomed_in'] = True
                ba_gui.zoom_in(event_dict['selected_event'], mappunavn_dict['ax'], event_dict, dypid)
                canvas.draw()
        # out
        elif event.keysym == 'o':
            mappunavn_dict['ax'].set_xlim(0, time_fulllength[len(time_fulllength) - 1])
            mappunavn_dict['ax'].set_ylim(-1, maxd + 1)
            zoomed_in_dict['zoomed_in'] = False
            canvas.draw()
        # downcast only
        elif event.keysym == 'e':
            if zoomed_in_dict['onlyDowncast']:
                zoomed_in_dict['onlyDowncast'] = False
                mappunavn_dict['ax'].set_xlim(0, time_fulllength[len(time_fulllength) - 1])
                log_print('Downcast')
            else:
                zoomed_in_dict['onlyDowncast'] = True
                log_print('All')
                mappunavn_dict['ax'].set_xlim(time_fulllength[event_dict['downcast_start']], 
                                              time_fulllength[event_dict['downcast_stop']])
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)    


        elif event.keysym == 'Shift_L':
            if mappunavn_dict['toggle_ax']:
                print('Toggle ax off')
                mappunavn_dict['toggle_ax'] = 0
                log_clear()
                processera(root, fig, canvas, Quality_frame, mappunavn_dict, frame)
            else:
                print('Toggle ax on')
                mappunavn_dict['toggle_ax'] = 1
                # mappunavn_dict['ax'].axis('off')
                for i in range(len(mappunavn_dict['ax'].lines)):
                    mappunavn_dict['ax'].lines.pop(0)
                # Sbeox0PS
                mappunavn_dict['x_aksi'] = data.DepSM[mappunavn_dict['start_index']:]
                mappunavn_dict['ax'].set_ylim(min(data.DepSM[event_dict['soak_stop']:event_dict['upcast_stop']]) - 0.1, 
                                              max(data.DepSM[event_dict['soak_stop']:event_dict['upcast_stop']]) + 0.1)
                mappunavn_dict['ax'].set_xlim(min(data.DepSM[event_dict['soak_stop']:event_dict['upcast_stop']]) - 0.1, 
                                              max(data.DepSM[event_dict['soak_stop']:event_dict['upcast_stop']]) + 0.1)
                mappunavn_dict['ax'].set_xlabel('Dýpið [m]')
                mappunavn_dict['ax'].plot(data.DepSM, data.DepSM, c='k')
                canvas.draw()

    
# TOGGLE LINE
        # temperature
        elif event.keysym == '1':
            if mappunavn_dict['toggle_temp'] == 0:
                mappunavn_dict['toggle_temp'] = 1
                mappunavn_dict['ax2'] = mappunavn_dict['ax'].twinx()
                mappunavn_dict['yplt2'] = mappunavn_dict['ax2'].plot(x_aksi, data.T090C[start_index:], color='red')
                mappunavn_dict['ax2'].set_ylabel('T090C', color='k')
                mappunavn_dict['ax2'].set_ylim(min(data.T090C[event_dict['downcast_start']:event_dict['upcast_stop']]) - 0.01, 
                                               max(data.T090C[event_dict['downcast_start']:event_dict['upcast_stop']]) + 0.01)
            else:
                mappunavn_dict['toggle_temp'] = 0
                mappunavn_dict['yplt2'].pop(0).remove()
                mappunavn_dict['ax2'].axis('off')
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        # conductivity
        elif event.keysym == '2':
            if mappunavn_dict['toggle_C0mS'] == 0:
                mappunavn_dict['toggle_C0mS'] = 1
                mappunavn_dict['ax7'] = mappunavn_dict['ax'].twinx()
                mappunavn_dict['yplt7'] = mappunavn_dict['ax7'].plot(x_aksi, data['C0mS/cm'][start_index:], color='gold')
                mappunavn_dict['ax7'].set_ylabel('C0mS/cm', color='k')
                mappunavn_dict['ax7'].set_ylim(min(data['C0mS/cm'][event_dict['downcast_start']:event_dict['upcast_stop']]) - 0.05, 
                                               max(data['C0mS/cm'][event_dict['downcast_start']:event_dict['upcast_stop']]) + 0.05)
            else:
                mappunavn_dict['toggle_C0mS'] = 0
                mappunavn_dict['yplt7'].pop(0).remove()
                mappunavn_dict['ax7'].axis('off')
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        # salinity
        elif event.keysym == '3':
            if mappunavn_dict['toggle_Sal00'] == 0:
                mappunavn_dict['toggle_Sal00'] = 1
                mappunavn_dict['ax6'] = mappunavn_dict['ax'].twinx()
                mappunavn_dict['yplt6'] = mappunavn_dict['ax6'].plot(x_aksi, data['Sal00'][start_index:], color='lightgreen')
                mappunavn_dict['ax6'].set_ylabel('Sal00', color='k')
                mappunavn_dict['ax6'].set_ylim(min(data['Sal00'][event_dict['downcast_start']:event_dict['upcast_stop']]) - 0.01, 
                                               max(data['Sal00'][event_dict['downcast_start']:event_dict['upcast_stop']]) + 0.01)
            else:
                mappunavn_dict['toggle_Sal00'] = 0
                mappunavn_dict['yplt6'].pop(0).remove()
                mappunavn_dict['ax6'].axis('off')
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        # oxygen
        elif event.keysym == '4':
            if mappunavn_dict['toggle_Sbeox0PS'] == 0:
                mappunavn_dict['toggle_Sbeox0PS'] = 1
                mappunavn_dict['ax4'] = mappunavn_dict['ax'].twinx()
                mappunavn_dict['yplt4'] = mappunavn_dict['ax4'].plot(x_aksi, data['Sbeox0PS'][start_index:], color='lightblue')
                mappunavn_dict['ax4'].set_ylabel('Oxygen %', color='k')
                # mappunavn_dict['ax4'].set_ylim(max(0,min(data['Sbeox0PS'][event_dict['downcast_start']:event_dict['upcast_stop']])) - 2, 
                #                                min(150,max(data['Sbeox0PS'][event_dict['downcast_start']:event_dict['upcast_stop']])) + 2)
                mappunavn_dict['ax4'].set_ylim(40,100)
            else:
                mappunavn_dict['toggle_Sbeox0PS'] = 0
                mappunavn_dict['yplt4'].pop(0).remove()
                mappunavn_dict['ax4'].axis('off')
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        # fluorescence
        elif event.keysym == '5':
            if mappunavn_dict['toggle_FlECO'] == 0:
                mappunavn_dict['toggle_FlECO'] = 1
                mappunavn_dict['ax3'] = mappunavn_dict['ax'].twinx()
                mappunavn_dict['yplt3'] = mappunavn_dict['ax3'].plot(x_aksi, data['FlECO-AFL'][start_index:], color='green')
                mappunavn_dict['ax3'].set_ylabel('Fluorescence', color='k')
                mappunavn_dict['ax3'].set_ylim(min(data['FlECO-AFL'][event_dict['downcast_start']:event_dict['upcast_stop']]) - 0.1, 
                                               max(data['FlECO-AFL'][event_dict['downcast_start']:event_dict['upcast_stop']]) + 0.1)
            else:
                mappunavn_dict['toggle_FlECO'] = 0
                mappunavn_dict['yplt3'].pop(0).remove()
                mappunavn_dict['ax3'].axis('off')
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        # par
        elif event.keysym == '6':
            if mappunavn_dict['toggle_par'] == 0:
                mappunavn_dict['toggle_par'] = 1
                mappunavn_dict['ax5'] = mappunavn_dict['ax'].twinx()
                mappunavn_dict['yplt5'] = mappunavn_dict['ax5'].plot(x_aksi, data['Par/sat/log'][start_index:], color='peru')
                mappunavn_dict['ax5'].set_ylabel('Par/sat/log', color='k')
                mappunavn_dict['ax5'].set_ylim(0, max(data['Par/sat/log'][event_dict['downcast_start']:event_dict['upcast_stop']]) + 5)
            else:
                mappunavn_dict['toggle_par'] = 0
                mappunavn_dict['yplt5'].pop(0).remove()
                mappunavn_dict['ax5'].axis('off')
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)


    # PROCESS CAST
        elif event.keysym == 'Return' or event.keysym == 'Shift_R':
            log_b()
            log_print('Calculating')
            log_print(data.columns.values)
            log_print(event.keysym)

            # Settings depending on up- or downcast
            if event.keysym == 'Return':
                # Bin Average settings
                ScansToSkip = 'downcast_start'
                CastToProcess = 1
                # Metadata
                meta_up_down = 'downcast'
            else: 
                # Bin Average settings
                ScansToSkip = 'upcast_start'
                CastToProcess = 2
                meta_up_down = 'upcast'

            # Gather relevant data for up- and downcast
            downcast_Data = data.loc[event_dict['downcast_start']:event_dict['downcast_stop'],
                                     ['DepSM','TimeS','C0mS/cm','T090C','PrdM','FlECO-AFL',
                                      'Par/sat/log','Sal00','Sigma-é00','Sbeox0Mg/L','Sbeox0PS','Flag']].round(7)
            upcast_Data = data.loc[event_dict['upcast_start']:event_dict['upcast_stop'],
                                     ['DepSM','TimeS','C0mS/cm','T090C','PrdM','FlECO-AFL',
                                      'Par/sat/log','Sal00','Sigma-é00','Sbeox0Mg/L','Sbeox0PS','Flag']].round(7)
            # Save relevant data
            downcast_Data.to_csv(parent_folder + '/ASCII/Down/' +filnavn[mappunavn_dict['filur']], index=False)
            upcast_Data.to_csv(parent_folder + '/ASCII/Up/' +filnavn[mappunavn_dict['filur']], index=False)
            
            # Calculate quality
            log_print('Assesing quality')
            summary = qcontrol(quality_subframe, dypid, event_dict, pump_on, filnavn[mappunavn_dict['filur']])
            confirmation = False
            if summary['downcast_quality'] < 0:
                if messagebox.askyesno('Vátta', 
                                       'Ávaring!\nKvaliteturin á kastinum er undir 0\n Vátta at allir parametrar eru rættir'):
                    confirmation = True
            else:
                confirmation = True
            if confirmation:
                # Hettar ger metadatafílin
                metadatafile = 'key,value\n'
                metadatafile += 'Data_File_Name,' + filnavn[mappunavn_dict['filur']] + '\n'
                sha256_hash = get_hash(parent_folder + '/ASCII/Down/' + filnavn[mappunavn_dict['filur']])
                metadatafile += 'sha256_hash,' + sha256_hash + '\n'
                metadatafile += 'processed_by,' + getpass.getuser() + '\n'
                for key, value in summary.items():
                    metadatafile += key + ',' + str(value) + '\n'
                metadatafile += 'soak_start,' + str(event_dict['soak_start']) + '\n'
                metadatafile += 'soak_stop,' + str(event_dict['soak_stop']) + '\n'
                metadatafile += 'downcast_start,' + str(event_dict['downcast_start']) + '\n'
                metadatafile += 'downcast_stop,' + str(event_dict['downcast_stop']) + '\n'
                metadatafile += 'upcast_start,' + str(event_dict['upcast_start']) + '\n'
                metadatafile += 'upcast_stop,' + str(event_dict['upcast_stop']) + '\n'
                metadatafile += 'cast_used,' + meta_up_down + '\n'
                log_print(metadatafile)
                
                # Og her verður metadata fílurin goymdur
                text_file = open(parent_folder + '/ASCII/metadata/' + 
                                 filnavn[mappunavn_dict['filur']].split('.')[0] + '_metadata.csv', "w")
                text_file.write(metadatafile)
                text_file.close()
                update_qframe = True

                if os.name == 'nt':
                    winedir = f"{os.getcwd()}/Ingestion/CTD/Settings/"
                else:
                    winedir = f"{os.getcwd()}/Ingestion/CTD/Settings/"
                
                # Broyta BinAverage fílu so hon passar við nýtggj viðri í downcast ella upcast
                tree = ET.parse(f"{os.getcwd()}/Ingestion/CTD/Settings/BinAvg.psa")
                # set filter A for variables C, T and B for P
                tree.find('./ScansToSkip').attrib['value'] = str(ScansToSkip)
                tree.find('./CastToProcess').attrib['value'] = str(CastToProcess)
                tree.write(f"{os.getcwd()}/Ingestion/CTD/Settings/BinAvg.psa", encoding="UTF-8", xml_declaration=True)


                turdato = mappunavn.split('Processed')[0]
                turdato = turdato.split('Lokalt_Data')[1]
                print('Túrdato:' + turdato)

                if os.name == 'nt':
                    commands = ['C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe']
                else:
                    commands = ['wine', f'{SEA_BIRD_WINE_PATH}SBEBatch.exe']
                subprocess.call(commands +
                                [f"{os.getcwd()}/ingestion/CTD/Settings/8_Bin_Average.txt",
                                 # 1: program, 2: in, 3: out
                                 f"{os.getcwd()}/ingestion/CTD/Settings/BinAvg.psa",
                                 str(os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/7_Window_Filter/' + filnavn[mappunavn_dict['filur']].split('.')[0]),
                                 str(os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/8_Bin_Average'), '#m'])
                print('bin avg complete')

                subprocess.call(commands + [f"{os.getcwd()}/ingestion/CTD/Settings/9_ASCII_Out.txt",
                                # 1: program, 2: in, 3: out
                                f"{os.getcwd()}/ingestion/CTD/Settings/ASCII_Out.psa",
                                str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/8_Bin_Average/' + filnavn[mappunavn_dict['filur']].split('.')[0]),
                                str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/ASCII'), '#m'])
                print('Ascii out complete')
                log_print('Done exporting')
            log_e()

        # back to trip overview
        elif event.keysym == 'BackSpace':
            turdato = mappunavn.split('Processed')[0]
            turdato = turdato.split('Lokalt_Data')[1]
            Ingestion.CTD.cruise_overview.cruise_overview_frame(frame, root, selectedCruse='')
        
        # reloads the data to the figure 
        elif event.keysym == 'space':
            log_clear()
            processera(root, fig, canvas, Quality_frame, mappunavn_dict, frame)

        # tuns quality control again
        elif event.keysym == 'onehalf':
            qcontrol(quality_subframe, dypid, event_dict, pump_on, filnavn[mappunavn_dict['filur']])

        # delets cast from process
        elif event.keysym == 'Delete':
            if os.path.exists(parent_folder + '/ASCII/Down/metadata/' + filnavn[mappunavn_dict['filur']].split('.')[0] + '_do_not_use_.csv'):
                if messagebox.askyesno('Vátta', 'Strika at casti ikki skal brúkast?'):
                    os.remove(parent_folder + '/ASCII/Down/metadata/' + filnavn[mappunavn_dict['filur']].split('.')[0] + '_do_not_use_.csv')
            else:
                if messagebox.askyesno('Vátta', 'Markera hettar casti sum tað ikki skal brúkast?'):
                    text_file = open(parent_folder + '/ASCII/Down/metadata/' + filnavn[mappunavn_dict['filur']].split('.')[0] + '_do_not_use_.csv', "w")
                    text_file.write('Hesin fílurin er brúktur til at markera at hettar casti ikki skal brúkast')
                    text_file.close()

        # saves plot to file
        elif event.keysym == 'p':
            turdato = os.path.dirname(os.path.dirname(mappunavn)).split('/')[-1]
            if not os.path.exists('Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/Figures/'):
                os.mkdir('Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/Figures/')
            fig.savefig('Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/Figures/' + filnavn[mappunavn_dict['filur']].split('.')[0] + '.pdf')

        # updates line placement on figure
        if event.keysym == 'j' or event.keysym == 'k':
            if event_dict['selected_event'] == 0:
                soak_line_dict['soak_start_line'][0].set_data([time_fulllength[event_dict['soak_start']], 
                                                               time_fulllength[event_dict['soak_start']]], 
                                                               [0, maxd+1])
            if event_dict['selected_event'] == 1:
                soak_line_dict['soak_stop_line'][0].set_data([time_fulllength[event_dict['soak_stop']], 
                                                              time_fulllength[event_dict['soak_stop']]], 
                                                              [0, maxd+1])
            if event_dict['selected_event'] == 2:
                soak_line_dict['downcast_start_line'][0].set_data([time_fulllength[event_dict['downcast_start']], 
                                                                   time_fulllength[event_dict['downcast_start']]], 
                                                                   [0, maxd+1])
            if event_dict['selected_event'] == 3:
                soak_line_dict['downcast_stop_line'][0].set_data([time_fulllength[event_dict['downcast_stop']], 
                                                                  time_fulllength[event_dict['downcast_stop']]], 
                                                                  [0, maxd+1])
            if event_dict['selected_event'] == 4:
                soak_line_dict['upcast_start_line'][0].set_data([time_fulllength[event_dict['upcast_start']], 
                                                                time_fulllength[event_dict['upcast_start']]], 
                                                                [0, maxd+1])
            if event_dict['selected_event'] == 5:
                soak_line_dict['upcast_stop_line'][0].set_data([time_fulllength[event_dict['upcast_stop']], 
                                                                time_fulllength[event_dict['upcast_stop']]], 
                                                                [0, maxd+1])
            canvas.draw()

        if update_annotations:
            soak_line_dict['annotation'].remove()
            soak_line_dict['annotation'] = ba_gui.update_annotations(event_dict['selected_event'], 
                                                                     mappunavn_dict['ax'], 
                                                                     event_dict, 
                                                                     maxd)
            canvas.draw()
            
        if update_qframe:
            ba_gui.refresh_qframe(Quality_frame, list_of_casts, parent_folder, filnavn, mappunavn_dict)

    root.bind('<Key>', key)

    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    log_e()
