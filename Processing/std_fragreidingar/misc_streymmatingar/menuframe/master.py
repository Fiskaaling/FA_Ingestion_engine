import os
import bisect
import time


from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import dates as mdate
import numpy as np
import pandas as pd
import datetime as dt
from pprint import pprint


from .hovus import hovusratningur

from .sidir.inlesstreym import inles

from .sidir.inleiding import gersamadratt

from .sidir.streym import tegnahovmuller
from .sidir.streym import speedbins
from .sidir.streym import tekna_dist_rose
from .sidir.streym import progressive_vector
from .sidir.streym import frequencytabellir
from .sidir.streym import duration_speed

from .sidir.sjovarfall import tidal_analysis_for_depth_bins
from .sidir.sjovarfall import tital_oll_dypir
from .sidir.sjovarfall import tidal_non_tidal_bins
from .sidir.sjovarfall import tidaldomines

def skriva_doc(setup_dict, siduval_dict):
    #  inlesData
    path_to_data = setup_dict['path']['data'].get() + '/'
    dest = setup_dict['path']['dest'].get() + '/LaTeX/'
    navn_a_fili = 'master.tex'


    # uppsetan til plottini

    # hvussu nógvar kassars skal rósan teknast við
    N = setup_dict['N']
    axcolor = setup_dict['axcolor']
    axline = setup_dict['axline']
    alpha = setup_dict['alpha']

    #  options til figurar
    font = setup_dict['font']
    figwidth = setup_dict['figwidth']
    figheight = setup_dict['figheight']
    dpi = setup_dict['dpi']

    mpl.rcParams['font.size'] = font

    #  skriva vit føroyskt
    mal = setup_dict['Language']
    # hvissi eg skal velja top_mid_bot_layer sjálvur 
    top_mid_bot_layer = setup_dict['top_mid_bot_layer']
    # ovasta greinsan hjá Hovmuller
    Hov_hadd = setup_dict['Hov_hadd']
    # ovasta dypi til at desina cmap
    Hov_cmap = setup_dict['Hov_cmap']
    #  haldi ikki at tak kemur at síggja godt ú at seta hetta til False
    sama_aksa = setup_dict['sama_aksa']
    #  ratningar vit skullu higgja eftir í Hovmuller
    Hov_rat = setup_dict['Hov_rat']
    #  frequensir sum tidal_oll_dypir sakal brúka
    tidal_oll_Frqs = setup_dict['tidal_oll_Frqs']
    #  speedbin skal eg hava subsections
    minmax = setup_dict['minmax']
    #--------------------------------------------------------------------------------

    #  inles alt dataði
    date, dypir, max_bin, datadf, uvdatadf = inles(path_to_data)

    # hvat fyri 3 bins skal eg brúka
    #  top, mid, bot layer
    if not top_mid_bot_layer:
        #  finn hvar 10 m er 
        tempbin = bisect.bisect_right(dypir, -10) - 1
        #  brúka 10m ístaðinfyri tempbin
        top_mid_bot_layer = ['10m', int((tempbin - 1) / 2) + 1, 1]
    # finn høvus ratning
    hovisrat = hovusratningur(uvdatadf, max_bin)

    # master fílurin
    file = open(dest + navn_a_fili, 'w')
    #  preamble og startur til doc
    file.write(r"""\include{setup/dokumentstilur}
\include{setup/kommandoir}
\include{setup/metadata}
\include{setup/titlepage}
\include{setup/opna}
\include{setup/hyphenation}
\usepackage{placeins}
\usepackage{rotating}
\usepackage{hyperref}

%\usepackage{showframe} %fjerna meg
%\usepackage[icelandic]{babel}
%\usepackage{subcaption}
%\usepackage{float}
\usepackage{calc}

\begin{document}
\frontmatter
\pagestyle{empty}
\titlepage
\opn
\mainmatter
\pagestyle{mergedstyle}
%\markboth{Content}
\renewcommand{\contentsname}{Innihaldsyvurlit}
\renewcommand{\figurename}{Mynd}
\renewcommand{\tablename}{Talva}
\tableofcontents*
\openany
\newpage""")

    print(siduval_dict['valdar_tree'].get_children(''))
    mangullisti=[]
    for case in siduval_dict['valdar_tree'].get_children(''):
        # Introduction
        if case == 'Introduction':
            a = 'Ókent mál'
            if mal == 'FO':
                a = "\\\FloatBarrier\n\\newpage\n\\section{Innleiðing}\\\\" + 'Eftir umbøn frá '+setup_dict['umb_av']+' eru kanningar gjørdar fyri at lýsa rákið í '  + setup_dict['stadarnavn'] + '. ' +\
                    'Hendan frágreiðingin lýsir hvussu úrslitini av hesum kanningum' + '\\newpage\n'
                a += '\\section{Økið}\n' \
                     'Økið har máta verður blabblabla'
            elif mal == 'EN':
                pass
                #a =  '\n\\FloatBarrier\n\\newpage\n\\section{%s}\n\\begin{figure}[h!]\\label{Hov%2.1f}\n\\includegraphics[scale=1]{myndir/%s}' \
                #       '\n\\caption{%s}\n\\end{figure}\n\\newpage\n' % (section, ratning, navn, caption)
            file.write(a)

        elif case == 'test':
            a = gersamadratt(datadf, uvdatadf, dypir, max_bin, dest=dest, date=date)
            file.write(a)

        #  Setup Hovmuller
        elif case == 'Hovmuller':
            # finn hvat fyri bins vit skullu brúka til Hovmuller diagrammi
            bins = bisect.bisect_right(dypir, Hov_hadd)
            bins = list(range(1, bins + 1))

            indexes = [str(i) for i in bins]

            yaxis = dypir[:bins[-1]]
            colnames = indexes

            bins_cmap = bisect.bisect_right(dypir, Hov_hadd)
            print(bins_cmap)
            bins_cmap = list(range(1, bins_cmap + 1))

            indexes_cmap = [str(i) for i in bins]

            yaxis_cmap = dypir[:bins[-1]]
            colnames_cmap = indexes

            if sama_aksa: #  skal colorbar verða tað sama í báðum
                #  finn ein góðan collorbar
                data = datadf[['mag' + x for x in colnames_cmap]].values.T
                absdata = [abs(x) for y in data for x in y if not np.isnan(x)]
                absdata = np.sort(absdata)
                temp = int(.95 * len(absdata))
                vmax = 1.1 * absdata[temp]
                templog = -np.floor(np.log10(vmax)) + 1
                vmax = np.ceil(vmax * 10**templog)/(10**templog)
            else:
                vmax = None

            for ratning in Hov_rat:
                navn = 'Hovmuller%1.0f.png' % ratning
                #data = magdf[colnames].values.T * np.cos(np.deg2rad(dirdf[colnames].values.T - ratning))
                ratning = ratning%360
                if ratning == 0:
                    data = uvdatadf[['v' + x for x in colnames]].values.T
                    if mal == 'EN':
                        caption = 'Hovmüller diagram of north/south velocities for the whole deployment period. The velocity scale is in mm/s'
                    else:
                        caption = 'Streymuferð í norður (reyður litur) og suður (bláur litur). litásin er í mm/s'
                elif ratning == 90:
                    data = uvdatadf[['u' + x for x in colnames]].values.T
                    if mal == 'EN':
                        caption = 'Hovmüller diagram of east/west velocities for the whole deployment period. The velocity scale is in mm/s'
                    else:
                        caption = 'Streymuferð í eystan (reyður litur) og Vestan (bláur litur). litásin er í mm/s'
                else:
                    data = uvdatadf[['v' + x for x in colnames]].values.T * np.cos(np.deg2rad(ratning)) + \
                            uvdatadf[['u' + x for x in colnames]].values.T * np.sin(np.deg2rad(ratning))
                    if mal == 'EN':
                        caption = 'Hovmüller diagram of [%s] velocities for the whole deployment period. The velocity scale is in mm/s' % int(ratning)
                    else:
                        caption = 'Streymuferð í %2.1f (reyður litur) og %2.1f (bláur litur). litásin er í mm/s' % (ratning, (ratning + 180)%360)
                a = tegnahovmuller(data, yaxis, date, mal=mal, ratning=ratning, navn=navn, caption=caption, vmax=vmax, dest=dest, font=font, figwidth=figwidth, figheight=figheight)
                file.write(a)

        #  tekna speedbins
        elif case == 'speedbin':
            a = speedbins(top_mid_bot_layer, date, datadf, max_bin, dypir, hovusratningur=hovisrat,
                          minmax=minmax, mal=mal,
                          dest=dest, font=font, figwidth=figwidth, figheight=figheight)
            file.write(a)


        #  tekna rósu
        elif case == 'rosa':
            umax = 4*(N-1)

            a = tekna_dist_rose(top_mid_bot_layer, uvdatadf, N, umax, dypir, mal=mal, dest=dest, dpi=200,
                               axcolor=axcolor, axline=axline, alpha=alpha,
                               font=font, figwidth=figwidth, figheight=figheight)
            file.write(a)

        #  tekna Progressive vector diagrams at selected layers
        elif case == 'progressive':
            a = progressive_vector(top_mid_bot_layer, date, uvdatadf, dypir, mal=mal, dest=dest,
                                  font=font, figwidth=figwidth, figheight=figheight)
            file.write(a)

        #  tekna Frequens tabellir
        elif case == 'freqtabellir':
            a = frequencytabellir(datadf, dypir, mal=mal, dest=dest)
            file.write(a)

        #  tekna duration_speed
        elif case == 'durationtabellir':
            a = duration_speed(top_mid_bot_layer, date, datadf, dypir, mal=mal, dest=dest)
            file.write(a)

        #  rokna utide fyri 3 dýpir
        elif case == 'tidal_3_dypir':
            a = tidal_analysis_for_depth_bins(top_mid_bot_layer, date, datadf, dypir, mal=mal, lat=62, dest=dest)
            file.write(a)

        #  sama frequens fyri øll dýpir
        elif case == 'tidal_oll_dypir':
            #  Hvat fyri bins skal eg gera hettar fyri
            tempbins = list(range(1, max_bin + 1))
            tempbins = tempbins[::-1]
            print(max_bin)
            a = tital_oll_dypir(date, tempbins, tidal_oll_Frqs, datadf, dypir, mal=mal, lat=62, dest=dest)
            file.write(a)

        #  tekna u og v árðin vit hava tiki frequensarnir vekk og aftaná
        elif case == 'tidal_non_tidal_bins':
            a = tidal_non_tidal_bins(top_mid_bot_layer, date, datadf, dypir, mal=mal, lat=62, dest=dest)
            file.write(a)

        elif case == 'sjovarfalsdrivi':
            a = tidaldomines(top_mid_bot_layer, date, datadf, dypir, lat=62, dest=dest)
            file.write(a)
        else:
            print(case)
            mangullisti.append(case)

    print(mangullisti)
    #  enda texdocument
    if True:
        file.write('\n\\end{document}')
        file.close()
        print('Done')
