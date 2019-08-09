from tkinter import *
import os

from .misc_streymmatingar import setupframe

def streym(frame, root):
    for widget in frame.winfo_children():
        widget.destroy()
    #----------------------------------------------------------------------
    #                    Start parametrar til alt
    #----------------------------------------------------------------------
    setup_dict = {'Language'            : 'FO', # Møgulig mál eru FO og EN
                  'N'                   : 31,   # Hvussu nógvar kassar í rósini
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
    siduval_dict = {'Introduction'         : False, #
                    'Hovmuller'            : False, #
                    'speedbin'             : True, #
                    'rosa'                 : False, #
                    'progressive'          : False, #
                    'freqtabellir'         : False, #
                    'durationtabellir'     : False, #
                    'tidal_3_dypir'        : False, #
                    'tidal_oll_dypir'      : False, #
                    'tidal_non_tidal_bins' : False, #
                    'sjovarfalsdrivi'      : False  #
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

    # Framin har metadataði verður sett inn
    meta_frame = Frame(BodyFrame)
    meta_frame.grid(row=0, column=0, columnspan=10)
    setupframe.setupmetaframe(meta_frame, setup_dict)

    # Framin har síðinar vera valdar frá
    siduval_frame = Frame(BodyFrame)
    siduval_frame.grid(row=1, column=0)
    setupframe.moguligarsidur(siduval_frame, siduval_dict)

    # Framin har vit hava valt síðir
    valdarsidir_frame = Frame(BodyFrame)
    valdarsidir_frame.grid(row=1, column=1)
    setupframe.valdarsigur(valdarsidir_frame, siduval_dict)
    # TODO okkurt til at velja parametrarnar
