from tkinter import *
from tkinter import filedialog
from misc.faLog import *
import pandas as pd
import getpass # Til at fáa brúkaranavn
import numpy as np
import platform
import os
from shutil import copyfile
import subprocess
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
from misc.sha2calc import get_hash
import Ingestion.CTD.bin_average_aux.ba_gui as ba_gui
from Ingestion.CTD.bin_average_aux.quality_control import qcontrol
textsize = 16


def bin_average_frame(frame, root2):
    global root
    global mappunavn
    #mappunavn = './Ingestion/CTD/Lokalt_Data/2019-01-31/75_All_ASCII_Out'
    mappunavn = './Ingestion/CTD/Lokalt_Data/2019-06-04/75_All_ASCII_Out'
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Bin Average').pack(side=TOP, anchor=W)
    controlsFrame = Frame(frame)
    controlsFrame.pack(side=TOP, anchor=W)
    velMappuBtn = Button(controlsFrame, text='Vel Fílir', command=velFil)
    velMappuBtn.pack(side=LEFT, anchor=W)

    processBtn = Button(controlsFrame, text='Processera', command=lambda: processera(fig, canvas, Quality_frame))
    processBtn.pack(side=LEFT, anchor=W)

    Right_frame = Frame(frame)
    Right_frame.pack(fill=BOTH, expand=False, side=RIGHT, anchor=N)

    fig = Figure(figsize=(12, 8), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)

    Quality_frame = Frame(Right_frame)
    Quality_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    log_frame = Frame(Right_frame, height=300, width=600, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)
    global filur
    filur = 0

    processera(fig, canvas, Quality_frame)

def velFil():
    global mappunavn
    mappunavn = filedialog.askdirectory(title='Vel túramappu', initialdir='./Ingestion/CTD/Lokalt_Data/')

def processera(fig, canvas, Quality_frame):
    global mappunavn
    log_b()
    midlingstid = 2 # sek
    fig.clf()
    ax = fig.subplots()
    filnavn = os.listdir(mappunavn)
    filnavn.sort()
    global filur
    data = pd.read_csv(mappunavn + '/' + filnavn[filur], encoding='latin-1') # Les fíl

    for widget in Quality_frame.winfo_children(): # Tømur quality frame
        widget.destroy()
    list_of_casts = os.listdir(mappunavn)
    list_of_casts.sort()
    parent_folder = os.path.dirname(mappunavn)
    for cast in list_of_casts:
        casttext = cast
        if os.path.exists(parent_folder + '/ASCII_Downcast/' + cast.split('.')[0] + '_metadata.csv'):
            casttext += ' ✓'
        if os.path.exists(parent_folder + '/ASCII_Downcast/' + cast.split('.')[0] + '_do_not_use_.csv'):
            casttext += ' X'
        if cast == filnavn[filur]:
            Label(Quality_frame, text=casttext, font=("Courier", textsize, 'underline')).pack(side=TOP, anchor=W)
        else:
            Label(Quality_frame, text=casttext, font=("Courier", textsize)).pack(side=TOP, anchor=W)

    Label(Quality_frame, text=('―'*20), font=("Courier", textsize)).pack(side=TOP, anchor=W)
    quality_subframe = Frame(Quality_frame)
    quality_subframe.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

    depth = data[data.columns[0]]
    time_fulllength = data['TimeS']
    print(time_fulllength)
    maxd = max(depth)
    start_index = 0
    for time in data.TimeS:
        start_index +=1
        if time > 0:
            break
    timeAx = data.TimeS[start_index:]
    ax.plot(timeAx, depth[start_index:])
    ax.set_ylim(-1, maxd+1)
    ax.set_xlabel('Tíð [?]')
    ax.set_ylabel('Dýpið', color='k')
    #ax2 = ax.twinx()
    #ax2.tick_params('y', colors='b')
    myvar = []
    n_midlingspunktir = int(np.ceil(midlingstid / (max(data.TimeS) / len(data))))
    dypid = data[data.columns[0]]
    for i in range(len(data[data.columns[0]])-2):
        myvar.append(np.var(dypid[i:i+n_midlingspunktir]))

    # Rokna ferð á CTD
    diff_d = []
    for i in range(1, len(depth)):
        diff_d.append((depth[i-1]-depth[i])/(time_fulllength.iloc[i-1]-time_fulllength.iloc[i]))
    #ax2.plot(timeAx, myvar)
    #ax2.plot(time_fulllength[1:], diff_d)
    #ax2.set_ylim([-1, 1])
    #diff_d = np.diff(data[data.columns[0]])
    states = ["PreSoak", "soak_start", "soak_stop", "downcast_start", "downcast_stop", "upcast_start", "upcast_stop"]
    current_stat = states[0]
    print(current_stat)
    global soak_start, soak_stop, downcast_start, downcast_stop, upcast_stop
    soak_start = -1
    soak_stop = -1
    soaktime = -1
    soak_depth = -1
    downcast_start = -1
    downcast_stop = -1
    upcast_stop = -1
    for i, d in enumerate(depth): # Hettar er kodan ið finnur nær tey ymsku tingini henda
        if current_stat == "PreSoak": # Bíða 5 sek áðrenn byrja verður at leita eftir hvar soak byrjar
            print(time_fulllength[i])
            if time_fulllength[i] > 5:
                current_stat = "soak_start"
        if current_stat == "soak_start":
            if d < 5:
                continue
            else:
                if np.var(dypid[i:i+n_midlingspunktir]) < 0.01:
                    soak_start = i
                    current_stat = "soak_stop"
                #    print('Farts '+ str(i))
        elif current_stat == "soak_stop":
            if np.var(dypid[i:i+n_midlingspunktir]) > 0.01:
                soak_stop = i + n_midlingspunktir
                soaktime = time_fulllength[soak_stop] - time_fulllength[soak_start]
                soak_depth = np.round(np.mean(dypid[soak_start:soak_stop]), 3)
                current_stat = "downcast_prepare"
        elif current_stat == "downcast_prepare":
            if d > 5:
                continue
            else:
                if d < 2 and np.var(dypid[i:i+n_midlingspunktir]) < 0.01:
                    current_stat = "downcast_start"
        elif current_stat == "downcast_start":
            if np.var(dypid[i:i+n_midlingspunktir]) > 0.01:
                downcast_start = i + n_midlingspunktir
                current_stat = "downcast_stop"
        elif current_stat == "downcast_stop":
            #if np.var(dypid[i:i+n_midlingspunktir]) < 0.01 and d > 5:
            #    downcast_stop = i
            #    current_stat = "upcast_start"
            if d == maxd:
                downcast_stop = i
                current_stat = "upcast_stop"
        elif current_stat == "upcast_stop":
            if np.var(dypid[i:i + n_midlingspunktir]) > 0.01:
                upcast_stop = i
        else:
            pass

    if os.path.isdir(parent_folder + '/0_RAW_DATA'):
        raw_filar = os.listdir(parent_folder + '/0_RAW_DATA/')
        raw_filnavn = '-1'
        hesin_filur = filnavn[filur].upper()
        for raw_file in raw_filar: # Hettar finnur rætta xml fílin
            print(raw_file)
            print(hesin_filur)
            if raw_file[0:17].upper() == hesin_filur[0:17]:
                print('Alright')
                raw_filnavn = raw_file
        if raw_filnavn == '-1':
            log_w('Eingin raw fílur funnin')
            return
        #raw_filnavn = raw_filar[filur]
        print('Lesur raw fíl: ' + raw_filnavn)
        with open(parent_folder + '/0_RAW_DATA/' + raw_filnavn, 'r') as raw_file:
            raw_data = raw_file.read()
        raw_data = raw_data.split('*END*')
        raw_data = raw_data[1].split('\n')
        pump_on = -1
        pump_off = -1
        lastLine = 0
        for i in range(len(raw_data)):
            line = raw_data[i]
            if line:
                if line[0] == '1' and lastLine == '0':
                    pump_on = i
                elif line[0] == '0' and lastLine == '1':
                    pump_off = i
                lastLine = line[0]
        print('Pump ' + str(pump_on))
        if pump_on != -1:
            ax.plot([pump_on/16, pump_on/16], [-100, 100], ':')
            print('Pumpan tendraði aftaná: ' + str(pump_on/16) + ' sek')

        if pump_off != -1:
            print('Pumpan sløknaði aftaná: ' + str(pump_off/16) + ' sek')
            ax.plot([pump_off/16, pump_off/16], [-100, 100], ':')
        bin_stodd = 1 # [m]
    if downcast_start != -1:
        downcast_start_d = dypid[downcast_start]
    if downcast_stop != -1:
        downcast_stop_d = dypid[downcast_stop]
        #downcast_stop_line = ax.plot([time_fulllength[downcast_stop], time_fulllength[downcast_stop]], [-100, 100], 'k')
    bins = np.arange(1,5+.2,.2)

    event_dict = {'time_fulllength': time_fulllength, 'soak_start': soak_start, 'soak_stop': soak_stop, 'downcast_start': downcast_start, 'downcast_stop': downcast_stop, 'upcast_stop': upcast_stop}

    global soak_start_line, soak_stop_line, downcast_start_line, downcast_stop_line, upcast_stop_line

    ba_gui.kanna_events(event_dict, log_w)

    soak_start_line = ax.plot([time_fulllength[event_dict['soak_start']], time_fulllength[event_dict['soak_start']]], [-100, 100], 'k')
    soak_stop_line = ax.plot([time_fulllength[event_dict['soak_stop']], time_fulllength[event_dict['soak_stop']]], [-100, 100], 'k')
    downcast_start_line = ax.plot([time_fulllength[event_dict['downcast_start']], time_fulllength[event_dict['downcast_start']]], [-100, 100], 'k')
    downcast_stop_line = ax.plot([time_fulllength[event_dict['downcast_stop']], time_fulllength[event_dict['downcast_stop']]], [-100, 100], 'k')
    upcast_stop_line = ax.plot([time_fulllength[event_dict['upcast_stop']], time_fulllength[event_dict['upcast_stop']]], [-100, 100], 'k')

    global selected_event
    selected_event = 0

    global zoomed_in
    zoomed_in = False

    global annotation
    annotation = ax.annotate('Soak Start',
                             xy=(time_fulllength[soak_start], maxd + 1),
                             xytext=(time_fulllength[soak_start], maxd + 2),
                             xycoords='data',
                             textcoords='data',
                             ha='center',
                             arrowprops=dict(arrowstyle="->"))

    qcontrol(quality_subframe, depth, event_dict, pump_on, filnavn[filur])

    def key(event):
        global soak_start, soak_stop, downcast_start, downcast_stop, upcast_stop
        global selected_event, filur
        print(event.keysym)
        update_annotations = False
        update_qframe = False
        global zoomed_in
        if zoomed_in:
            move_amount = 1
        else:
            move_amount = 8

        if event.keysym == 'w':
            if filur < len(filnavn)-1:
                filur += 1
                update_qframe = True
        elif event.keysym == 'q':
            if filur != 0:
                filur -= 1
                update_qframe = True
        elif event.keysym == 'Return':
            log_b()
            print('Calculating')
            print(data.columns.values)
            downcast_Data = pd.DataFrame(
                {'DepSM': data.DepSM.iloc[downcast_start:downcast_stop], 'T068C': data.T068C.iloc[downcast_start:downcast_stop], 'FlECO-AFL': data['FlECO-AFL'].iloc[downcast_start:downcast_stop], 'Sal00': data['Sal00'].iloc[downcast_start:downcast_stop],
                 'Sigma-é00': data['Sigma-é00'].iloc[downcast_start:downcast_stop], 'Sbeox0Mg/L': data['Sbeox0Mg/L'].iloc[downcast_start:downcast_stop]}) ## TODO: ger hettar betri. Set hettar í egna funku
            if not os.path.isdir(parent_folder + '/ASCII_Downcast'):
                os.mkdir(parent_folder + '/ASCII_Downcast')
            downcast_Data.to_csv(parent_folder + '/ASCII_Downcast/' + filnavn[filur], index=False)
            print('Assesing quality')
            summary = qcontrol(quality_subframe, depth, time_fulllength, soak_start, soak_stop, downcast_start, downcast_stop, upcast_stop, pump_on, filnavn[filur])

            confirmation = False
            if summary['downcast_quality'] < 0:
                if messagebox.askyesno('Vátta', 'Ávaring!\nKvaliteturin á kastinum er undir 0\n Vátta at allir parametrar eru rættir'):
                    confirmation = True
            else:
                confirmation = True
            if confirmation:
                metadatafile = 'key,value\n'
                metadatafile += 'Data_File_Name,' + filnavn[filur] + '\n'
                sha256_hash = get_hash(parent_folder + '/ASCII_Downcast/' + filnavn[filur])
                metadatafile += 'sha256_hash,' + sha256_hash + '\n'
                metadatafile += 'processed_by,' + getpass.getuser() + '\n'
                for key, value in summary.items():
                    metadatafile += key + ',' + str(value) + '\n'
                print(metadatafile)

                text_file = open(parent_folder + '/ASCII_Downcast/' + filnavn[filur].split('.')[0] + '_metadata.csv', "w")
                text_file.write(metadatafile)
                text_file.close()
                print('Done exporting')

            log_e()
        elif event.keysym == 'l':
            if not zoomed_in:
                selected_event += 1
                update_annotations = True
        elif event.keysym == 'h':
            if not zoomed_in:
                selected_event -= 1
                update_annotations = True
        elif event.keysym == 'j':
            if selected_event == 0:
                soak_start -= move_amount
                event_dict['soak_start'] -= move_amount
            elif selected_event == 1:
                soak_stop -= move_amount
                event_dict['soak_stop'] -= move_amount
            elif selected_event == 2:
                downcast_start -= move_amount
                event_dict['downcast_start'] -= move_amount
            elif selected_event == 3:
                downcast_stop -= move_amount
                event_dict['downcast_stop'] -= move_amount
            elif selected_event == 4:
                upcast_stop -= move_amount
                event_dict['upcast_stop'] -= move_amount
        elif event.keysym == 'k':
            if selected_event == 0:
                soak_start += move_amount
                event_dict['soak_start'] += move_amount
            elif selected_event == 1:
                soak_stop += move_amount
                event_dict['soak_stop'] += move_amount
            elif selected_event == 2:
                downcast_start += move_amount
                event_dict['downcast_start'] += move_amount
            elif selected_event == 3:
                downcast_stop += move_amount
                event_dict['downcast_stop'] += move_amount
            elif selected_event == 4:
                upcast_stop += move_amount
                event_dict['upcast_stop'] += move_amount
        elif event.keysym == 'i':
            if not zoomed_in:
                zoomed_in = True
                ba_gui.zoom_in(selected_event, ax, event_dict, depth)
                canvas.draw()
        elif event.keysym == 'o':
            ax.set_xlim(0, time_fulllength[len(time_fulllength)-1])
            ax.set_ylim(-1, maxd + 1)
            zoomed_in = False
            canvas.draw()
        elif event.keysym == 'space':
            log_clear()
            processera(fig, canvas, Quality_frame)
        elif event.keysym == 'onehalf':
            qcontrol(quality_subframe, depth, time_fulllength, soak_start, soak_stop, downcast_start, downcast_stop,
                     upcast_stop, pump_on, filnavn[filur])
        elif event.keysym == 'Delete':
            if os.path.exists(parent_folder + '/ASCII_Downcast/' + filnavn[filur].split('.')[0] + '_do_not_use_.csv'):
                if messagebox.askyesno('Vátta', 'Strika at casti ikki skal brúkast?'):
                    os.remove(parent_folder + '/ASCII_Downcast/' + filnavn[filur].split('.')[0] + '_do_not_use_.csv')
            else:
                if messagebox.askyesno('Vátta', 'Markera hettar casti sum tað ikki skal brúkast?'):
                    text_file = open(parent_folder + '/ASCII_Downcast/' + filnavn[filur].split('.')[0] + '_do_not_use_.csv', "w")
                    text_file.write('Hesin fílurin er brúktur til at markera at hettar casti ikki skal brúkast')
                    text_file.close()

        if selected_event == -1: # Fyri at ikki kunna velja eina linju ið ikki er til
            selected_event = 0
        elif selected_event == 5:
            selected_event = 4

        if event.keysym == 'j' or event.keysym == 'k':
            global soak_start_line, soak_stop_line, downcast_start_line, downcast_stop_line, upcast_stop_line
            if selected_event == 0:
                soak_start_line.pop(0).remove()
                soak_start_line = ax.plot([time_fulllength[soak_start], time_fulllength[soak_start]], [-100, 100], 'k')
            if selected_event == 1:
                soak_stop_line.pop(0).remove()
                soak_stop_line = ax.plot([time_fulllength[soak_stop], time_fulllength[soak_stop]], [-100, 100], 'k')
            if selected_event == 2:
                downcast_start_line.pop(0).remove()
                downcast_start_line = ax.plot([time_fulllength[downcast_start], time_fulllength[downcast_start]], [-100, 100], 'k')
            if selected_event == 3:
                downcast_stop_line.pop(0).remove()
                downcast_stop_line = ax.plot([time_fulllength[downcast_stop], time_fulllength[downcast_stop]], [-100, 100], 'k')
            if selected_event == 4:
                upcast_stop_line.pop(0).remove()
                upcast_stop_line = ax.plot([time_fulllength[upcast_stop], time_fulllength[upcast_stop]], [-100, 100], 'k')
            #update_annotations = True
            canvas.draw()
        if update_annotations:
            global annotation
            annotation.remove()
            annotation = ba_gui.update_annotations(selected_event, ax, event_dict, maxd)

            canvas.draw()
        if update_qframe:
            print('Valdur filur: ' + str(filur))
            for widget in Quality_frame.winfo_children():  # Tømur quality frame
                widget.destroy()
            global mappunavn
            for cast in list_of_casts:
                casttext = cast
                if os.path.exists(parent_folder + '/ASCII_Downcast/' + cast.split('.')[0] + '_metadata.csv'):
                    casttext += ' ✓'
                if os.path.exists(parent_folder + '/ASCII_Downcast/' + cast.split('.')[0] + '_do_not_use_.csv'):
                    casttext += ' ⃠'
                if cast == filnavn[filur]:
                    Label(Quality_frame, text=casttext, font=("Courier", textsize), bg="Green").pack(side=TOP, anchor=W)
                else:
                    Label(Quality_frame, text=casttext, font=("Courier", textsize)).pack(side=TOP, anchor=W)
            Label(Quality_frame, text=('―' * 20), font=("Courier", textsize)).pack(side=TOP, anchor=W)

    root.bind('<Key>', key)

    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    log_e()
