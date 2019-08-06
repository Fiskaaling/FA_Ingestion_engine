from tkinter import *
import os

from .misc_streymmatingar import setupframe

def streym(frame, root):
    for widget in frame.winfo_children():
        widget.destroy()
    #----------------------------------------------------------------------
    #                    Start parametrar til alt
    #----------------------------------------------------------------------
    setup_dict = {'N'                   : 31,   # Hvussu nógvar kassar í rósini
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
                  'tidal_oll_Frqs'      : ['M2', 'S2', 'N2', 'O1', 'K1'] # Frq til tidal_oll_dypir
                 }
    #----------------------------------------------------------------------
    #                    Hvat fyri síðir skal við
    #                    eg havi ikki brúkt hettar
    #----------------------------------------------------------------------
    siduval_dict = {'Language'                  : 'FO', # Møgulig mál eru FO og EN
                    'Introducton'          : True, #
                    'Hovmuller'            : True, #
                    'speedbin'             : True, #
                    'rosa'                 : True, #
                    'progressive'          : True, #
                    'freqtabellir'         : True, #
                    'durationtabellir'     : True, #
                    'tidal_3_dypir'        : True, #
                    'tidal_oll_dypir'      : True, #
                    'tidal_non_tidal_bins' : True, #
                    'sjovarfalsdrivi'      : True  #
                }
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

    meta_frame = Frame(BodyFrame)
    meta_frame.grid(row=0, column=0)
    setupframe.setupmetaframe(meta_frame, setup_dict)


