import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib as mpl
import utide


def tidal_analysis_for_depth(tin, uin, vin, lat=62,
              navn='tide.tex', caption='one layer', dest='LaTeX/', label=''):
    coef = utide.solve(tin, uin, vin, lat=lat)
    col = ['Const', 'Freq', 'E-ampl', 'E-gpl', 'N-ampl', 'N-gpl', 'Major', 'minor', 'Theta', 'Graphl', 'R']
    supcol = ['', 'c/hr', 'mm/sec', 'deg', 'mm/sec', 'deg', 'mm/sec', 'mm/sec', 'deg', 'deg', '']
    a = list(coef.name)
    rekkjur = min(len(coef.name), 15)
    coefE = utide.solve(tin, uin, lat=lat, constit=a)
    coefN = utide.solve(tin, vin, lat=lat, constit=a)
    reftime = coef.aux.reftime
    reftime = mdate.num2date(reftime).strftime('%Y-%m-%dT%H:%M:%S')

    tabel = '\\begin{tabular}{|' + (len(col)) * 'r|' + '}\n\\hline\n'
    tabel += col[0]
    for x in col[1:]:
        tabel += '&\t%s' % (x,)
    tabel += '\\\\'
    tabel += supcol[0]
    for x in supcol[1:]:
        tabel += '&\t%s' % (x,)
    tabel += '\\\\\\hline\n'

    for i in range(rekkjur):
        ei = np.argwhere(coefE.name == coef.name[i])[0][0]
        ni = np.argwhere(coefN.name == coef.name[i])[0][0]
        tabel += (4-len(coef.name[i]))*' ' + coef.name[i]
        tabel += '&\t%.8f' % (coef.aux.frq[i],)
        tabel += '&\t%5.0f' % (coefE.A[ei],)
        tabel += '&\t%5.0f' % (coefE.g[ei],)
        tabel += '&\t%5.0f' % (coefN.A[ni],)
        tabel += '&\t%5.0f' % (coefN.g[ni],)
        tabel += '&\t%5.0f' % (coef.Lsmaj[i],)
        tabel += '&\t%5.0f' % (abs(coef.Lsmin[i]),)
        tabel += '&\t%3.0f' % (coef.theta[i],)
        tabel += '&\t%3.0f' % (coef.g[i],)
        tabel += '&\t%s' % ('A' if coef.Lsmin[i]>0 else 'C',)
        tabel += '\\\\\n'
    tabel += '\\hline\n'
    tabel += '\\end{tabular}'
    texfil = open(dest + 'Talvur/%s' % (navn,), 'w')
    texfil.write(tabel)
    texfil.close()

    tide = utide.reconstruct(tin, coef)
    figwidth = 6
    figheight = 9
    fig, axs = plt.subplots(ncols=1, nrows=4, figsize=(figwidth, figheight))
    axs[0].plot(tin, uin, linewidth=.5)
    axs[0].plot(tin, tide.u, linewidth=.5)
    axs[1].plot(tin, uin - tide.u, linewidth=.5)
    axs[2].plot(tin, vin, linewidth=.5)
    axs[2].plot(tin, tide.v, linewidth=.5)
    axs[3].plot(tin, vin - tide.v, linewidth=.5)
    #plt.show()
    caption += ' Reftime = %s' % reftime

    return '\n\\begin{table}[!ht]%s' \
           '\n\\centering' \
           '\n\\resizebox{\\textwidth}{!}{' \
           '\n\\input{Talvur/%s}' \
           '\n}' \
           '\n\\caption{%s}' \
           '\n\\end{table}' % (label, navn, caption)
