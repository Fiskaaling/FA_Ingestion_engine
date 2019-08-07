from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import dates as mdate
import numpy as np
import os
import pandas as pd
import datetime as dt
import time
import bisect
from sidir.inlesstreym import inles
from sidir.streym import tegnahovmuller
from sidir.streym import speedbins
from sidir.streym import tekna_dist_rose
from sidir.streym import progressive_vector
from sidir.streym import frequencytabellir
from sidir.streym import duration_speed
from sidir.sjovarfall import tidal_analysis_for_depth_bins
from sidir.sjovarfall import tital_oll_dypir
from sidir.sjovarfall import tidal_non_tidal_bins
from sidir.sjovarfall import tidaldomines

#  inlesData
path_to_data = '../csv/DJUD1901/'
dest = '../LaTeX/DJUD1901/'
navn_a_fili = 'DJUD1901.tex'


# uppsetan til plottini

# hvussu nógvar kassars skal rósan teknast við
N = 31
axcolor = 'k'
axline = 0.5
alpha = 0.5

#  options til figurar
font = 8
figwidth = 6
figheight = 7.1
dpi = 800

mpl.rcParams['font.size'] = font

# hvissi eg skal velja top_mid_bot_layer sjálvur 
top_mid_bot_layer = False
# ovasta greinsan hjá Hovmuller
Hov_hadd = -10
#  haldi ikki at tak kemur at síggja godt ú at seta hetta til False
sama_aksa = True
#  ratningar vit skullu higgja eftir í Hovmuller
Hov_rat = [0, 90]
#  frequensir sum tidal_oll_dypir sakal brúka
tidal_oll_Frqs = ['M2', 'S2', 'N2', 'O1', 'K1', ]
#--------------------------------------------------------------------------------
#                         Hvat fyri plot skal verða við
#                       hettar skal sikkurt breitast uppá
#                   soleiðis man kan hava tað sama fleiri ferða
#                          og man kann velja til og frá
#--------------------------------------------------------------------------------
option_Hovmuller = True
option_speedbin = True
option_rosa = True
option_progressive = True
option_freqtabellir = True
option_durationtabellir = True
option_tidal_3_dypir = True
option_tidal_oll_dypir = True
option_tidal_non_tidal_bins = True
option_sjovarfalsdrivi = True
#--------------------------------------------------------------------------------

# inles alt dataði
#  TODO tjekka inles
date, dypir, max_bin, datadf, uvdatadf = inles(path_to_data)

# hvat fyri 3 bins skal eg brúka
#  top, mid, bot layer
if not top_mid_bot_layer:
    tempbin = bisect.bisect_right(dypir, -10) - 1
    top_mid_bot_layer = [tempbin, int((tempbin - 1) / 2) + 1, 1]

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

#  Setup Hovmuller
if option_Hovmuller:
    # finn hvat fyri bins vit skullu brúka til Hovmuller diagrammi
    bins = bisect.bisect_right(dypir, Hov_hadd)
    bins = list(range(1, bins + 1))

    indexes = [str(i) for i in bins]

    yaxis = dypir[:bins[-1]]
    colnames = indexes

    #  skal colorbar verða tað sama í báðum
    #  sama_aksa verður sett longri uppi
    if sama_aksa:
        #  finn ein góðan collorbar
        data = datadf[['mag' + x for x in colnames]].values.T
        absdata = [abs(x) for y in data for x in y]
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
        if ratning == 0:
            data = uvdatadf[['v' + x for x in colnames]].values.T
            caption = 'Hovmüller diagram of east/west velocities for the whole deployment period. The velocity scale is in mm/s'
        elif ratning == 90:
            data = uvdatadf[['u' + x for x in colnames]].values.T
            caption = 'Hovmüller diagram of north/south velocities for the whole deployment period. The velocity scale is in mm/s'
        else:
            data = uvdatadf[['v' + x for x in colnames]].values.T * np.cos(np.deg2rad(ratning)) + \
                    uvdatadf[['u' + x for x in colnames]].values.T * np.sin(np.deg2rad(ratning))
            caption = 'Hovmüller diagram of [%s] velocities for the whole deployment period. The velocity scale is in mm/s' % int(ratning)
        a = tegnahovmuller(data, yaxis, date, ratning=ratning, navn=navn, caption=caption, vmax=vmax, dest=dest, font=font, figwidth=figwidth, figheight=figheight)
        file.write(a)

#  tekna speedbins
if option_speedbin:
    a = speedbins(top_mid_bot_layer, date, datadf, dypir, dest=dest,
                 font=font, figwidth=figwidth, figheight=figheight)
    file.write(a)

#  tekna rósu
if option_rosa:
    umax = 4*(N-1)

    a = tekna_dist_rose(top_mid_bot_layer, uvdatadf, N, umax, dypir, dest=dest, dpi=200,
                       axcolor=axcolor, axline=axline, alpha=alpha,
                       font=font, figwidth=figwidth, figheight=figheight)
    file.write(a)

#  tekna Progressive vector diagrams at selected layers
if option_progressive:
    a = progressive_vector(top_mid_bot_layer, date, uvdatadf, dypir, dest=dest,
                          font=font, figwidth=figwidth, figheight=figheight)
    file.write(a)

#  tekna Frequens tabellir
if option_freqtabellir:
    a = frequencytabellir(datadf, dypir, dest=dest)
    file.write(a)

#  tekna duration_speed
if option_durationtabellir:
    a = duration_speed(top_mid_bot_layer, date, datadf, dypir, dest=dest)
    file.write(a)

#  rokna utide fyri 3 dýpir
if option_tidal_3_dypir:
    a = tidal_analysis_for_depth_bins(top_mid_bot_layer, date, datadf, dypir, lat=62, dest=dest)
    file.write(a)

#  sama frequens fyri øll dýpir
if option_tidal_oll_dypir:
    #  Hvat fyri bins skal eg gera hettar fyri
    tempbins = list(range(1, max_bin + 1))
    tempbins = tempbins[::-1]
    print(max_bin)
    a = tital_oll_dypir(date, tempbins, tidal_oll_Frqs, datadf, dypir, lat=62, dest=dest)
    file.write(a)

#  tekna u og v árðin vit hava tiki frequensarnir vekk og aftaná
if option_tidal_non_tidal_bins:
    a = tidal_non_tidal_bins(top_mid_bot_layer, date, datadf, dypir, lat=62, dest=dest)
    file.write(a)

if option_sjovarfalsdrivi:
    a = tidaldomines(top_mid_bot_layer, date, datadf, dypir, lat=62, dest=dest)
    file.write(a)

#  enda texdocument
if True:
    file.write('\n\\end{document}')
    file.close()
    print('Done')
