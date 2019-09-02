from tkinter import *
import os

import pandas as pd

from .misc_streymmatingar import setupframe

def streym(frame, root):
    for widget in frame.winfo_children():
        widget.destroy()
    #----------------------------------------------------------------------
    #                    Start parametrar til alt
    #----------------------------------------------------------------------
    setup_dict = {'Language'            : 'FO', # Møgulig mál eru FO og EN
                  'N'                   : 25,   # Hvussu nógvar kassar í rósini
                  'axcolor'             : 'k',
                  'axline'              : 0.5,
                  'alpha'               : 0.5,
                  'font'                : 8,    # Font á plottum
                  'figwidth'            : 6,    # Stødd á plottum fulla síðu (tummar)
                  'figheight'           : 7.1,  # Stødd á plottum fulla síðu (tummar)
                  'dpi'                 : 800,
                  'top_mid_bot_layer'   : False, # Set inn hvat fyrði bins skullu brúkast
                  'Hov_hadd'            : -10,  # Ovara greinsa á Hovmuller
                  'sama_aksa'           : True,
                  'Hov_rat'             : [0, 90], # Ratning á Hov
                  'tidal_oll_Frqs'      : ['M2', 'S2', 'N2', 'O1', 'K1'], # Frq til tidal_oll_dypir
                  'minmax'              : True # speedbin subsections
                 }
    #----------------------------------------------------------------------
    #                    Hvat fyri síðir skal við
    #                    eg havi ikki brúkt hettar
    #----------------------------------------------------------------------
    siduval_dict = {}
    siduval_list = ['Introduction', 'Hovmuller', 'speedbin', 'rosa', 'progressive',
                    'freqtabellir', 'durationtabellir', 'tidal_3_dypir',
                    'tidal_oll_dypir', 'tidal_non_tidal_bins', 'sjovarfalsdrivi']
    #----------------------------------------------------------------------
    #                    GUI
    #----------------------------------------------------------------------

    Label(frame, text='Streym', font='Helvetica 18 bold').pack(side=TOP)

    # Menu ovast
    menuFrame = Frame(frame)
    menuFrame.pack(side=TOP, fill=X, expand=False, anchor=N)
    setupframe.setupmenuframe(menuFrame, setup_dict, siduval_dict)

    # Framin sum alt verður sett á
    BodyFrame = Frame(frame, bg='green')
    BodyFrame.pack(fill=BOTH, expand=True, anchor=N + W)

    # Framin har metadataði verður sett inn
    meta_frame = Frame(BodyFrame)
    meta_frame.grid(row=0, column=0, columnspan=3)
    setupframe.setupmetaframe(meta_frame, setup_dict)

    # Framin har síðinar vera valdar frá
    siduval_frame = Frame(BodyFrame)
    siduval_frame.grid(row=1, column=0)
    setupframe.moguligarsidur(siduval_frame, siduval_dict, siduval_list)

    # Framin har vit hava valt síðir
    valdarsidir_frame = Frame(BodyFrame)
    valdarsidir_frame.grid(row=1, column=1)
    setupframe.valdarsigur(valdarsidir_frame, siduval_dict)

    # Framin til at til at seta nakrar parametrar
    parlist = ['Language', 'N', 'dpi', 'top_mid_bot_layer',
               'Hov_hadd', 'Hov_rat', 'tidal_oll_Frqs', 'minmax']
    parametur_frame = Frame(BodyFrame)
    parametur_frame.grid(row=1, column=2, columnspan=2)
    setupframe.parametur(parametur_frame, setup_dict, parlist)


    # inlesur setup.txt
    path = os.path.dirname(__file__)
    if 'setup.txt' in os.listdir(path):
        try:
            temp = dict(pd.read_csv(path + '/setup.txt', header=None)
                        .dropna(how='all').values)
        except:
            messagebox.showinfo('fekk ikki inlisi setup.txt')

    for key in temp:
        if key in setup_dict['meta'].keys():
            setup_dict['meta'][key].delete(0, END)
            if str(temp[key]) != 'nan':
                setup_dict['meta'][key].insert(0, temp[key].strip())
        elif key in setup_dict['path'].keys():
            setup_dict['path'][key].set(temp[key].strip())
        elif key in siduval_list:
            if temp[key].strip().lower() == 'true' and not siduval_dict['valdar_tree'].exists(key):
                siduval_dict['valdar_tree'].insert('', 'end', key, text=key)
        elif key in setup_dict['gui_par'].keys():
            setup_dict['gui_par'][key].delete(0, END)
            setup_dict['gui_par'][key].insert(0, temp[key].strip())
        else:
            print(key, temp[key].strip())
