from tkinter import *


def hello():
    print('hello')

def streym(frame, root):
    print('sup')
    for widget in frame.winfo_children():
        widget.destroy()
    #----------------------------------------------------------------------
    #                    Start parametrar til alt
    #----------------------------------------------------------------------
    setup_dict = {'path_to_data'        : None, # Hvar er csv fílurin
                  'path_to_dest'        : None, # Hvar skal LaTeX doc
                  'Navn_a_fili'         : None, # Hvat skal texfilurin eita
                  'N'                   : 31,   # Hvussu nógvar kassar í rósini
                  'axcolor'             : 0.5,
                  'alpha'               : 0.5,
                  'font'                : 8,    # Font á plottum
                  'figwidth'            : 6,    # Stødd á plottum fulla síðu (tummar)
                  'figheight'           : 7.1,  # Stødd á plottum fulla síðu (tummar)
                  'dpi'                 : 800,
                  'top_mid_bot_layer'   : False, # Set inn hvat fyrði bins skullu brúkast
                  'Hov_hadd'            : -10,  # Ovara greinsa á Hovmuller
                  'sama_aksa'           : True,
                  'Hov_rat'             : [0, 90], # Ratning á Hov
                  'tidal_oll_frqs'      : ['M2', 'S2', 'N2', 'O1', 'K1'] # Frq til tidal_oll_dypir
                 }
    #----------------------------------------------------------------------
    #                    Hvat fyri síðir skal við
    #----------------------------------------------------------------------
    vel_sidir = {'Hovmuller'            : True, # 
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

    Label(frame, text='streym', font='Helvetica 18 bold').pack(side=TOP)

    menuFrame = Frame(frame)

    print(setup_dict['N'])
