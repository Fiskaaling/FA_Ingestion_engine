import fileinput
import getpass
import os
import subprocess
import tempfile
from shutil import copyfile
from tkinter import Label, TOP, N, W, LEFT, RIGHT, BOTTOM, Frame, Button, BOTH, X, Entry
from tkinter import messagebox, filedialog

import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Ingestion.CTD.misc.ctd_pump import pumpstatus
import Ingestion.CTD.cruise_overview
from misc.faLog import gerlog, log_print, log_w


def align_ctd_frame(frame, root2, selectNewFolder=True, mappunavn='./Ingestion/CTD/Lokalt_Data/2019-01-17/Processed/2_Filter', filIndex=0):
    print('Filindex: ' + str(filIndex))
    if mappunavn != './Ingestion/CTD/Lokalt_Data/2019-01-17/Processed/2_Filter':
        selectNewFolder = False
    mappunavn_dict = {'mappunavn': mappunavn}
    mappunavn_dict['filur'] = filIndex
    mappunavn_dict['frame'] = frame
    mappunavn_dict['root2'] = root2
    root = root2
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame, text='Seabird SBE 25 CTD', font='Helvetica 18 bold').pack(side=TOP)
    Label(frame, text='Align CTD').pack(side=TOP, anchor=W)

    mappunavn_dict['controlsFrame'] = Frame(frame)
    mappunavn_dict['controlsFrame'].pack(side=TOP, anchor=W)

    fig = Figure(figsize=(10, 8), dpi=100)
    plot_frame = Frame(frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    plot_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)

    Right_frame = Frame(frame)
    Right_frame.pack(fill=BOTH, expand=False, side=RIGHT, anchor=N)

    info_frame = Frame(Right_frame)
    info_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    log_frame = Frame(Right_frame, height=300, width=600, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    log_frame.pack(fill=X, expand=False, side=BOTTOM, anchor=W)
    gerlog(log_frame, root)

    processBtn = Button(mappunavn_dict['controlsFrame'], text='Vel túr', command=lambda: align_ctd(root, fig, canvas, info_frame, selectNewFolder, mappunavn_dict))
    processBtn.pack(side=LEFT, anchor=W)
    mappunavn_dict['ox_advance'] = 3
    mappunavn_dict['ox_stepsize'] = 1

    align_ctd(root, fig, canvas, info_frame, selectNewFolder, mappunavn_dict)


def align_ctd(root, fig, canvas, info_frame, selectNewFolder, mappunavn_dict):

    if selectNewFolder:
        mappunavn_dict['mappunavn'] = filedialog.askdirectory(title='Vel túramappu', initialdir='./Ingestion/CTD/Lokalt_Data/')

    if mappunavn_dict['mappunavn'] == ():
        return
    list_of_casts = os.listdir(mappunavn_dict['mappunavn'])
    list_of_casts.sort()
    mappunavn_dict['list_of_casts'] = list_of_casts
    refresh_infoframe(info_frame, list_of_casts, mappunavn_dict)

    mappunavn_dict['ax'] = fig.subplots()
    mappunavn_dict['ax'].set_xlabel('Raw oxygen [V]')
    mappunavn_dict['ax2'] = mappunavn_dict['ax'].twiny()
    mappunavn_dict['ax2'].set_xlabel('Conductivity [c0mS/cm]')
    mappunavn_dict['ax'].set_ylabel('Temperature [C]')
    #mappunavn_dict['ax'].set_ylabel('Pressure [db]')

    def key(event):
        print(event.keysym)
        call_refresh_infoframe = False
        if event.keysym == 'w':
            if mappunavn_dict['filur'] < len(list_of_casts) - 1:
                mappunavn_dict['filur'] += 1
                call_refresh_infoframe = True
        elif event.keysym == 'q':
            if mappunavn_dict['filur'] != 0:
                mappunavn_dict['filur'] -= 1
                call_refresh_infoframe = True
        elif event.keysym == 'BackSpace':
            Ingestion.CTD.cruise_overview.cruise_overview_frame(mappunavn_dict['frame'], mappunavn_dict['root2'], mappunavn_dict['filur'])
        #elif event.keysym == 'Return':
        elif event.keysym == 'KP_Enter' or event.keysym == 'Return':
            if os.path.exists(mappunavn_dict['mappunavn'].split('Processed')[0] + 'turMetadata.csv'):
                metadatas = pd.read_csv(mappunavn_dict['mappunavn'].split('Processed')[0] + 'turMetadata.csv', index_col=False)
                print('turMetadata.csv funnin')
            else:
                metadatas = pd.DataFrame(columns=['key', 'value'])
                print('Eingin turMetadata.csv funnin')

            keyname = 'alignCTD'+list_of_casts[mappunavn_dict['filur']]
            if keyname in metadatas.key.values:
                metadatas.loc[metadatas.key == keyname,'value'] = mappunavn_dict['ox_advance']
            else:
                metadatas = metadatas.append({'key': keyname, 'value': mappunavn_dict['ox_advance']}, ignore_index=True)

            print('metadata: ', metadatas)
            metadatas.to_csv(mappunavn_dict['mappunavn'].split('Processed')[0] + 'turMetadata.csv', index=False)


            print('done')
        elif event.keysym == 'KP_Add':
            mappunavn_dict['ox_advance'] += 1 * mappunavn_dict['ox_stepsize']
            mappunavn_dict['ax'].set_title('Ox Advance:' + str(mappunavn_dict['ox_advance']))
            mappunavn_dict['ox_ad_entry'].delete(0, 'end')
            mappunavn_dict['ox_ad_entry'].insert(0, str(mappunavn_dict['ox_advance']))
            canvas.draw()
        elif event.keysym == 'KP_Subtract':
            mappunavn_dict['ox_advance'] -= 1 * mappunavn_dict['ox_stepsize']
            mappunavn_dict['ax'].set_title('Ox Advance:' + str(mappunavn_dict['ox_advance']))
            mappunavn_dict['ox_ad_entry'].delete(0, 'end')
            mappunavn_dict['ox_ad_entry'].insert(0, str(mappunavn_dict['ox_advance']))
            canvas.draw()
        elif event.keysym == 'KP_Multiply':
            mappunavn_dict['ox_stepsize'] *= 2
            log_print('Stepsize :' + str(mappunavn_dict['ox_stepsize']))
        elif event.keysym == 'KP_Divide':
            mappunavn_dict['ox_stepsize'] /= 2
            log_print('Stepsize :' + str(mappunavn_dict['ox_stepsize']))
        elif event.keysym == 'space':

            # Fyrst rokna

            winedir = '/home/' + getpass.getuser() + '/.wine/drive_c/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/'

            copyfile(winedir + 'AlignCTD_(custom)_original.psa', winedir + 'AlignCTD_(custom).psa')
            ikki_funni_linju = True
            with fileinput.FileInput(winedir + 'AlignCTD_(custom).psa', inplace=True) as file:
                for line in file:
                    ikki_funni_linju = False
                    print(line.replace('-77', str(mappunavn_dict['ox_advance'])), end='')
            if ikki_funni_linju:
                messagebox.showerror('Feilur við export', 'Customstart fílur ikki funnin!')

            tempdir = tempfile.mkdtemp('tempOx')

            #turdato = os.path.dirname(os.path.dirname(mappunavn_dict['mappunavn'])).split('Lokalt_Data/')[-1]
            turdato = mappunavn_dict['mappunavn'].split('Processed')[0].split('Lokalt_Data')[1].replace('/', '')

            print(turdato)
            print(mappunavn_dict['mappunavn'])
            print(os.path.dirname(mappunavn_dict['mappunavn']))
            subprocess.call(['wine',
                             'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                             "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/3_Align_CTD_(custom).txt",
                             str('Z:' + os.getcwd() + '/Ingestion/CTD/Lokalt_Data/' + turdato + '/Processed/2_Filter/' + list_of_casts[mappunavn_dict['filur']].split('.')[0]),
                             str('Z:/' + tempdir),
                             '#m'])

            # So les inn

            n_rows_to_skip = 0
            col_names = []
            with open(tempdir + '/' + list_of_casts[mappunavn_dict['filur']], 'r', encoding='latin-1') as f:
                lines = f.read().split("\n")
            for i, line in enumerate(lines):
                # finding row where data begins
                if '*END*' in line:
                    n_rows_to_skip = i
                # finding names of data columns
                if '# name' in line:
                    col_names.append(line.split()[4][0:-1])
            print(n_rows_to_skip)

            data = pd.read_csv(tempdir + '/' + list_of_casts[mappunavn_dict['filur']], encoding='latin-1', skiprows=n_rows_to_skip + 1, delimiter=r"\s+", names=col_names)  # Les fíl

            tempfiles = os.listdir(tempdir)
            for file in tempfiles:
                os.remove(tempdir + '/' + file)
            os.removedirs(tempdir)

            # Finn nær pumpa tendrar og sløknar
            print(mappunavn_dict['mappunavn'])
            print(mappunavn_dict['list_of_casts'][mappunavn_dict['filur']])
            [pump_on, pump_off] = pumpstatus(mappunavn_dict['mappunavn'], mappunavn_dict['list_of_casts'][mappunavn_dict['filur']])

            midlingstid = 2  # sek
            n_midlingspunktir = int(np.ceil(midlingstid / (max(data.timeS) / len(data))))

            # finna downcast/upcast
            maxd = max(data.prdM)
            maxdi = -1
            for i, d in enumerate(data.prdM):
                if d == maxd:
                    maxdi = i
            upcast_stop = -1
            for i in list(range(maxdi, len(data.prdM))):
                if np.var(data.prdM[i:i + n_midlingspunktir]) > 0.01:
                    upcast_stop = i

            for i in range(len(mappunavn_dict['ax'].lines)):
                mappunavn_dict['ax'].lines.pop(0)
            for i in range(len(mappunavn_dict['ax2'].lines)):
                mappunavn_dict['ax2'].lines.pop(0)

            # mappunavn_dict['ax'].plot(data.Sbeox0PS[pump_on+16:upcast_stop], -data.DepSM[pump_on+16:upcast_stop])

            oxd = mappunavn_dict['ax'].plot(data.sbeox0V[pump_on + 64:maxdi], data.t090C[pump_on + 64:maxdi], c='g', label='ox Downcast')
            oxu = mappunavn_dict['ax'].plot(data.sbeox0V[maxdi:upcast_stop], data.t090C[maxdi:upcast_stop], c='r', label='ox Upcast')

            #oxd = mappunavn_dict['ax'].plot(data.sbeox0V[pump_on + 64:maxdi], -data.prdM[pump_on + 64:maxdi], c='g', label='ox Downcast')
            #oxu = mappunavn_dict['ax'].plot(data.sbeox0V[maxdi:upcast_stop], -data.prdM[maxdi:upcast_stop], c='r', label='ox Upcast')

            mappunavn_dict['ax'].set_xlim(min(data.sbeox0V[pump_on + 64:upcast_stop]) - 0.01, max(data.sbeox0V[pump_on + 64:upcast_stop]) + 0.01)
            mappunavn_dict['ax'].set_ylim(min(data.t090C[pump_on + 64:upcast_stop]) - 0.1, max(data.t090C[pump_on + 64:upcast_stop]) + 0.1)
            #mappunavn_dict['ax'].set_ylim(min(-data.prdM[pump_on + 64:upcast_stop]) - 1, max(-data.prdM[pump_on + 64:upcast_stop]) + 1)
            mappunavn_dict['ax'].set_title('Ox Advance:' + str(mappunavn_dict['ox_advance']))

            #condd = mappunavn_dict['ax2'].plot(data['c0mS/cm'][pump_on + 64:maxdi], -data.prdM[pump_on + 64:maxdi], c='orangered', alpha=0.5, label='c Downcast')
            #condu = mappunavn_dict['ax2'].plot(data['c0mS/cm'][maxdi:upcast_stop], -data.prdM[maxdi:upcast_stop], c='gold', alpha=0.5, label='c Upcast')
            #mappunavn_dict['ax2'].set_xlim(min(data['c0mS/cm'][pump_on + 64:upcast_stop]) - 0.1, max(data['c0mS/cm'][pump_on + 64:upcast_stop]) + 0.1)
            #mappunavn_dict['ax2'].set_ylim(min(-data.prdM[pump_on + 64:upcast_stop]) - 1, max(-data.prdM[pump_on + 64:upcast_stop]) + 1)

            lns = oxd + oxu #lns = oxd + oxu + condd + condu
            labs = [l.get_label() for l in lns]
            mappunavn_dict['ax'].legend(lns, labs, loc=0)
            # mappunavn_dict['ax2'].legend(loc=0)
            canvas.draw()
        if call_refresh_infoframe:
            refresh_infoframe(info_frame, list_of_casts, mappunavn_dict)

    root.bind('<Key>', key)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)


def refresh_infoframe(info_frame, list_of_casts, mappunavn_dict):
    for widget in info_frame.winfo_children():  # Tømur quality frame
        widget.destroy()
    adFrame = Frame(info_frame)
    adFrame.pack(side=TOP, anchor=W)
    Label(adFrame, text='Advance: ').pack()
    mappunavn_dict['ox_ad_entry'] = Entry(adFrame)
    mappunavn_dict['ox_ad_entry'].insert(0, str(mappunavn_dict['ox_advance']))
    mappunavn_dict['ox_ad_entry'].pack(side=TOP, anchor=W)
    for i, filename in enumerate(list_of_casts):
        print(i)
        print(mappunavn_dict['filur'])
        if mappunavn_dict['filur'] == i:
            Label(info_frame, text=filename[:-4], font=("Courier", 16, 'underline')).pack(side=TOP, anchor=W)
        else:
            Label(info_frame, text=filename[:-4], font=("Courier", 16)).pack(side=TOP, anchor=W)
