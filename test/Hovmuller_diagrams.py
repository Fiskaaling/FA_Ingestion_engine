import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import utide
from scipy.interpolate import griddata


def get_dypid(bin_nr, d, bin_size=4, firstbinrange=6.15):
    """
    gevur dýpið av mátingini
    :param bin_nr:          hvat fyri bin eru vit intreseraði í
    :param d:               dýpið á mátistaðnum
    :param bin_size:        hvussu langt er millum mátingarnar
    :param firstbinrange:   hvar er tan fyrsta mátingin
    :return:                hvar er bin nr 'bin'
    """
    return d - firstbinrange - bin_size * (bin_nr - .5)


def tegnahovmuller(data, dypid, dato, ratning=0, nrplots=11, figwidth=6, figheight=7.1,
                   vmax=None, dest='', navn='Hovmuller.pdf', caption='caption', dpi=200):
    """
    :param data:        numpy array við einari rekkju fyri hvørt dýpið og eina colonnu fyri hvørja máting
    :param dypid:       listi av hvussu djúpar allar binninar eru
    :param dato:        dato á øllum mátingunum
    :param ratning:     hvønn veg máta vit í
    :param nrplots:     hvussu nógv plott skullu á síðina (er verður gjørdur ein axi til colorbar eyka)
    :param figwidth:    breiddin á fig
    :param figheight:   hæddin á fig
    :param vmax:        longdin av ásinum, hviss hettar er None verður rokna hvat tað skal verða
    :param dest:        mappan sum filurin skal goymast sum
    :param navn:        navn á filinum sum verður goymdur
    :param caption:     caption sum sakal standa undir myndini
    :param dpi:         dpi á fig sum verður goymdur
    :return:            ein fig
    """

    print('byrja uppá ' + navn)
    if ratning == 90:
        section = 'Hovmüller diagrams of east/west velocities'
    elif ratning == 0:
        section = 'Hovmüller diagrams of north/south velocities'
    else:
        section = 'Hovmüller diagrams of %2.1f velocities' % ratning

    fig, axs = plt.subplots(ncols=1, nrows=nrplots + 1, figsize=(figwidth, figheight), dpi=dpi)
    n = len(data[0])

    if vmax is None:
        absdata = [abs(x) for y in data for x in y]
        vmax = max(absdata)
        #  TODO finn fitt interval min 95%
        temp = 10 ** int(np.log10(vmax))
        vmax = np.ceil(vmax / temp) * temp
        temp /= 10
        #  TODO fá hettar at rigga
        while False:
            print(len([x for x in absdata if x < vmax - temp]) / len(absdata))
            if len([x for x in absdata if x < vmax - temp]) / len(absdata) > .95:
                vmax -= temp
            else:
                break

    for i in range(nrplots):
        m = i * n // nrplots
        M = (i + 1) * n // nrplots
        X, Y = np.meshgrid(dato[m:M], dypid)
        date_fmt = mdate.DateFormatter('%d %b')
        a = axs[i].contourf(X, Y, data[::, m:M], levels=list(np.linspace(-vmax, vmax, 256)), cmap=cm.seismic)
        axs[i].xaxis.set_major_formatter(date_fmt)
        axs[i].set_ylabel('Djúbd')
        axs[i].tick_params(axis='x', which='major', pad=0)
    fig.colorbar(a, cax=axs[nrplots], orientation='horizontal', ticks=np.linspace(-vmax, vmax, 9))

    mpl.rcParams['font.size'] = 7
    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, wspace=0.5, hspace=0.5)
    mpl.rcParams['xtick.major.pad'] = 0
    fig.savefig(dest + 'myndir/' + navn, dpi=dpi)
    print('enda ' + navn)
    return '\n\\newpage\n\\section{%s}\n\\begin{figure}[h!]\n\\includegraphics[scale=1]{myndir/%s}' \
           '\n\\caption{%s}\n\\end{figure}\n\\newpage' % (section, navn, caption)


def plotrose2(ax, N, umax, lv, Es, Ns, eind='mm/s', axline=.5, axcolor='k', alpha=.5, kon=True):
    '''
    teknar eina rósu har eg fari at reina at gera tað møguligt at tekna tað í bins og í confidens interval

    :param ax: axin sum rósan skal plottast á
    :param N: hvussu nógvar bins dataði skal sorterast í av fyrstan tíð
    :param umax: hvar greinsunar á ásunum skullu verða
    :param lv: hvar levels á contour plottinum skullu verða
    :param Es: u data   Haldi eg  í hvussu er data Est
    :param Ns: v data   Haldi eg  í hvussu er data North
    :param eind: eindin á Es og Ns sum skal verða tað sama
    :param axline: tjúktin á linjunum
    :param axcolor: farvan á linjunum
    :param alpha: alpha á linjunum
    :param kon: hvissi True plottar tað konfidens intarvali um false plotta vit bins
    :return: figurin út aftur við øllum breitingunum (veit ikki um tað er neyðut at returna hann)
    '''
    #  variablin har eg samli dataði í
    F = np.zeros(shape=(N, N))

    #  her filli eg inn í bins
    for k in range(len(Ns)):
        #  hvat fyri bin skal hendan mátingin inní
        Ebin = int(N * ((Es[k] + umax) / (2 * umax)) + .5)
        Nbin = int(N * ((Ns[k] + umax) / (2 * umax)) + .5)
        if 0 <= Ebin < N and 0 <= Nbin < N:
            F[Nbin][Ebin] += 1
    #  Normalisera fyri øll ikki NaN elementini har Note alti alt gevur hettar sikkurt ikki 100% tí at okkurt liggur
    #  uttan fyri ásarnar
    F /= len(Ns)
    #  hvat er index á binnunum
    x = np.linspace(-umax, umax, N)

    #  F er normilasera so hettar gevur brotpartin sum vit kunnu seta í eitt av bins
    part = sum([y for x in F for y in x])
    #  hettar er har eg fari at finna konfidens interval
    X, Y = np.meshgrid(x, x)
    #  ger eitt interpolering uppá eitt størri data sett eftir hvat er í F til at gera eitt stórt contour til confidens
    if kon:
        xs = np.linspace(-umax, umax, 1001)
        Xi, Yi = np.meshgrid(xs, xs)
        Zi = griddata((X.flatten(), Y.flatten()), F.flatten(), (Xi, Yi), method='linear')

        #  normalisera Zi soleis at totali summurin er tað vit hava fingið við frá Rádatainum
        Zi *= part / sum([y for x in Zi for y in x])
        #  byrja at sortera dataði soleis at eg kann gera eitt konfidens interval
        sh = Zi.shape
        Zj = Zi.flatten()
        #  set ein parametur til at sortera aftur eftir tá eg havi set virðir inn til at gera konfidens interval
        Zj = [[k, Zj[k]] for k in range(sh[0] * sh[1])]
        #  sortera ratt
        Zj = sorted(Zj, key=lambda x: x[1])
        count = 1
        for k in range(len(Zj)):
            #  set virðini inn til at gera konfidens interval
            temp = count - Zj[k][1]
            Zj[k][1] = count
            count = temp

        #  set elimentini uppá pláss aftur
        Zj = sorted(Zj, key=lambda x: x[0])
        Zj = [Zj[k][1] for k in range(sh[0] * sh[1])]
        Zj = np.array(Zj)
        #  enda við at forma dataði uppá pláss aftur
        Zi = np.reshape(Zj, sh)
        con = ax.contourf(Xi, Yi, Zi, levels=lv, cmap=cm.jet_r)
        cb = plt.colorbar(con, ax=ax)
        cb.set_label('Confidens økir')
    else:
        con = ax.contourf(X, Y, F, levels=lv, cmap=cm.jet)
        cb = plt.colorbar(con, ax=ax)
        cb.set_ticks([])

    #  tekna allar aksarnir vannratt loddratt diagonalt og ein sirkul á [0,0] radius 100
    ax.plot([0, 0], [-umax, umax], c=axcolor, linewidth=axline, alpha=alpha)
    ax.plot([-umax, umax], [0, 0], c=axcolor, linewidth=axline, alpha=alpha)
    ax.plot([-umax, umax], [umax, -umax], c=axcolor, linewidth=axline / 2, alpha=alpha)
    ax.plot([-umax, umax], [-umax, umax], c=axcolor, linewidth=axline / 2, alpha=alpha)
    p = mpatches.Circle((0, 0), 100, fill=False, color=axcolor, linewidth=axline / 2, alpha=alpha)
    ax.add_patch(p)

    #  TODO kodan yvir hettar skal sirgja fyri at variablarnir sum skullu plottast hava tey røttu nøvnini
    ax.set_aspect(1)
    ax.set_xlabel('E (' + eind + ')')
    ax.set_ylabel('N (' + eind + ')')


#  TODO hettar skal kunna taka u og v
def tekna_dist_rose(bins, magdf, dirdf, N, umax, fultdypid, Bin_Size, firstbinrange, dpi=200,
                    navn='Rosa.pdf', section='Rose diagrams at selected layers'):

    if len(bins) != 3:
        print(bins)
        raise ValueError('bins skal hava 3 bins')
    fig, axs = plt.subplots(ncols=2, nrows=3, figsize=(6, 7.1), dpi=dpi)
    for (i, bin) in enumerate(bins):
        if i == 0:
            prelabel = 'a) Surface layer'
        elif i == 1:
            prelabel = 'b) Center layer'
        else:
            prelabel = 'c) Bottom layer'
        tempdf = pd.concat([magdf[str(bin)], dirdf[str(bin)]], axis=1)
        tempdf.columns = ['mag', 'dir']
        tempdf.dropna(inplace=True)
        Es = tempdf['mag'].values * np.sin(np.deg2rad(tempdf['dir'].values))
        Ns = tempdf['mag'].values * np.cos(np.deg2rad(tempdf['dir'].values))
        plotrose2(axs[i, 0], N, magdf[str(bin)].describe(percentiles=[.975])['97.5%'], lv=10, Es=Es, Ns=Ns,
             kon=False)
        axs[i, 0].set_ylabel(prelabel + '\n' + axs[i, 0].get_ylabel())
        plotrose2(axs[i, 1], N, umax, lv=10, Es=Es, Ns=Ns,
             kon=False)
        axs[i, 1].set_ylabel('')
    caption = 'Distribution of velocity vectors: ' \
              'a) Bin %s at %2.0f m depth, b) Bin %s at %2.0f m depth, and c) Bin %s at %2.0f m depth.' \
              % (bins[0], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange),
                 bins[1], get_dypid(bins[1], fultdypid, Bin_Size, firstbinrange),
                 bins[2], get_dypid(bins[2], fultdypid, Bin_Size, firstbinrange))

    plt.gca().set_aspect('equal', adjustable='box')
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.0, hspace=0.5)
    fig.savefig('myndir/' + navn)
    return '\n\\newpage\n\\section{%s}\n\\begin{figure}[h!]\n\\includegraphics[scale=1]{myndir/%s}' \
           '\n\\caption{%s}\n\\end{figure}\n\\newpage' % (section, navn, caption)


def tekna_confidens_rose(bins, magdf, dirdf, N, umax, fultdypid, Bin_Size, firstbinrange, dpi=200,
                    navn='Rosa.pdf', section='Rose diagrams at selected layers'):

    if len(bins) != 3:
        raise ValueError('bins skal hava 3 bins')
    fig, axs = plt.subplots(ncols=2, nrows=3, figsize=(6, 7.1), dpi=dpi)
    for (i, bin) in enumerate(bins):
        if i == 0:
            prelabel = 'a) Surface layer'
        elif i == 1:
            prelabel = 'b) Center layer'
        else:
            prelabel = 'c) Bottom layer'
        tempdf = pd.concat([magdf[str(bin)], dirdf[str(bin)]], axis=1)
        tempdf.columns = ['mag', 'dir']
        tempdf.dropna(inplace=True)
        Es = tempdf['mag'].values * np.sin(np.deg2rad(tempdf['dir'].values))
        Ns = tempdf['mag'].values * np.cos(np.deg2rad(tempdf['dir'].values))
        plotrose2(axs[i, 0], N, magdf[str(bin)].describe(percentiles=[.975])['97.5%'],
                  lv=[0, .05, .25, .5, .75, .95, 1], Es=Es, Ns=Ns)
        axs[i, 0].set_ylabel(prelabel + '\n' + axs[i, 0].get_ylabel())
        plotrose2(axs[i, 1], N, umax, lv=[0, .05, .25, .5, .75, .95, 1], Es=Es, Ns=Ns)
        axs[i, 1].set_ylabel('')
    caption = 'Confidens space of velocity vectors: ' \
              'a) Bin %s at %2.0f m depth, b) Bin %s at %2.0f m depth, and c) Bin %s at %2.0f m depth.' \
              % (bins[0], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange),
                 bins[1], get_dypid(bins[1], fultdypid, Bin_Size, firstbinrange),
                 bins[2], get_dypid(bins[2], fultdypid, Bin_Size, firstbinrange))

    plt.gca().set_aspect('equal', adjustable='box')
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.0, hspace=0.5)
    fig.savefig('myndir/' + navn)
    return '\n\\newpage\n\\section{%s}\n\\begin{figure}[h!]\n\\includegraphics[scale=1]{myndir/%s}' \
           '\n\\caption{%s}\n\\end{figure}\n\\newpage' % (section, navn, caption)


#  TODO finn útav hvussu hvat fyri bins man skal brúka verður rokna
def speedbins(bins, dato, magdf, fultdypid, Bin_Size, firstbinrange, dpi=200,
              navn='streymstyrkiyvirtid.pdf', section='Timeseries of speed at selected layers'):
    if len(bins) != 3:
        raise ValueError('bins skal hava 3 bins')
    fig, axs = plt.subplots(ncols=1, nrows=3, figsize=(6, 7.1), dpi=dpi)
    date_fmt = mdate.DateFormatter('%d %b')
    for (i, bin) in enumerate(bins):
        if i == 0:
            prelabel = 'a) Surface layer'
        elif i == 1:
            prelabel = 'b) Center layer'
        else:
            prelabel = 'c) Bottom layer'
        axs[i].plot(dato, magdf[str(bin)], linewidth=.5, c='k')
        axs[i].xaxis.set_major_formatter(date_fmt)
        axs[i].set_ylabel('speed [mm/t]')
        axs[i].tick_params(axis='x', which='major', pad=0)
        axs[i].set_title(prelabel)
        axs[i].set_xlim(dato[0], dato[-1])
        axs[i].set_ylim(bottom=0)

    caption = 'Timeseries of speed at three selected bins: a) Bin %s at %2.0f m depth, b) Bin %s at %2.0f m depth' \
              ' and c) Bin %s at %2.0f m depth.' \
              % (bins[0], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange),
                 bins[1], get_dypid(bins[1], fultdypid, Bin_Size, firstbinrange),
                 bins[2], get_dypid(bins[2], fultdypid, Bin_Size, firstbinrange))

    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, wspace=0.0, hspace=0.2)
    fig.savefig('myndir/%s' % navn, dpi=dpi)
    return '\n\\newpage\n\\section{%s}\n\\begin{figure}[h!]\n\\includegraphics[scale=1]{myndir/%s}' \
           '\n\\caption{%s}\n\\end{figure}\n\\newpage' % (section, navn, caption)


# TODO skriva onkrastanið at eg havi brúk fyri at tíðin er í mdate
def progressive_vector(bins, dato, magdf, dirdf, fultdypid, Bin_Size, firstbinrange, dpi=200,
              navn='progressive_vector.pdf', section='Progressive vector diagrams at selected layers'):
    if len(bins) != 3:
        raise ValueError('bins skal hava 3 bins')
    fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(6, 7.1), dpi=dpi)
    date_fmt = mdate.DateFormatter('%d %b')
    plots = []
    for (i, bin) in enumerate(bins):
        #  kanska dropna
        #  skal man convertera til km
        #  TODO eg mangli at fáa tíðar parameturin ordiligt inn

        # [km/dag]/[mm/s]
        dmdmms = (60*60*24)/1e6
        xs = magdf[str(bin)].values.T * np.sin(np.deg2rad(dirdf[str(bin)].values.T)) * dmdmms
        ys = magdf[str(bin)].values.T * np.cos(np.deg2rad(dirdf[str(bin)].values.T)) * dmdmms
        punktir = [[0], [0]]
        for k in range(len(xs) - 1):
            punktir[0].append(punktir[0][-1] + xs[k] * (dato[k+1] - dato[k]))
            punktir[1].append(punktir[1][-1] + ys[k] * (dato[k+1] - dato[k]))
        plots.append(punktir)
    for i in range(len(plots)):
        if i == 0:
            prelabel = 'Surface layer'
        elif i == 1:
            prelabel = 'Center layer'
        else:
            prelabel = 'Bottom layer'
        axs.plot(*plots[i], linewidth=.5, label=prelabel)
    axs.legend()
    plt.subplots_adjust(left=0.1, bottom=0.075, right=0.95, top=0.95, wspace=0.0, hspace=0.2)
    axs.set_xlabel('Distance [Km]')
    axs.set_ylabel('Distance [Km]')
    plt.axis('equal')
    fig.savefig('myndir/%s' % navn, dpi=dpi)

    caption = 'Progressive vector diagrams at three selected layers: Surface (Bin %s at %2.0f m depth),' \
              ' center (Bin %s at %2.0f m depth) and bottom layer (Bin %s at %2.0f m depth).' \
              % (bins[0], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange),
                 bins[1], get_dypid(bins[1], fultdypid, Bin_Size, firstbinrange),
                 bins[2], get_dypid(bins[2], fultdypid, Bin_Size, firstbinrange))

    return '\n\\newpage\n\\section{%s}\n\\begin{figure}[h!]\n\\includegraphics[scale=1]{myndir/%s}' \
           '\n\\caption{%s}\n\\end{figure}\n\\newpage' % (section, navn, caption)


def frequencytabellir(magdf, fultdypid, Bin_Size, firstbinrange,
              navn='Frqtabel.tex', sections=['Frequency of high speeds', 'Frequency of low speeds']):
    # TODO her manglar ein hline

    #  Freequency of high speeds
    inforows = ['no.', 'm']
    #  TODO skal eg koyra hettar inn sum eitt input til funktiónina
    infospeed = [str(x) for x in [50, 100, 150, 200, 250, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1500]]
    inforows += infospeed
    #  gera klárt til tabellina
    highstr = '\\begin{tabular}{|' + len(inforows)*'r|' + '}\n\\hline\n Bin&\tDepth&\t' \
                                                          '\multicolumn{%s}{c|}{Speed [mm/s]}\\\\\\hline\n'\
              % (len(inforows)-2,)
    highstr += (4-len(inforows[0]))*' ' + inforows[0]
    for x in inforows[1::]:
        highstr += '&\t' + (4-len(x))*' ' + x
    highstr += '\\\\\\hline'
    lowstr = highstr
    for nyggregla, key in enumerate(magdf.keys()):
        #  TODO tá eg brúki ordiligar csv fílar skal eg higgja eftir hesum
        try:
            Depth = get_dypid(int(key), fultdypid, Bin_Size, firstbinrange)
        except ValueError:
            continue
        data = magdf[key].values
        sortboxir = [int(x) for x in infospeed] + [np.inf]
        tally = [0 for _ in sortboxir]

        for x in data:
            for (i, y) in enumerate(sortboxir):
                if x < y:
                    tally[i] += 1
                    break
        # tally er hvussu nógv data er minni enn tað samsvarandi virði í sortboxir
        print(len(data) - sum(tally))
        tally = [1000*x/sum(tally) for x in tally]
        lowspeedtabel = tally
        #  rokna tey ordiligu tølini sum skullu til lowspeed
        for i in range(1, len(tally)):
            lowspeedtabel[i] = lowspeedtabel[i-1] + tally[i]
        #  rokna tey ordiligu tølini sum skullu til highspeed
        highspeedtabel = [1000 - x for x in lowspeedtabel]
        highspeedtabelround = highspeedtabel
        #  finn tølini sum skullu í high speed tabellina
        for (i, x) in enumerate(highspeedtabelround):
            if 0.005 < x < 1:
                highspeedtabelround[i] = np.round(x, 2)
            else:
                highspeedtabelround[i] = int(np.round(x, 0))
        #  skriva eina reglu til highspeed tabellina
        if nyggregla == 0:
            highstr += '\n' + (4-len(key))*' ' + key + '&\t' + (4-len(str(int(Depth))))*' ' + str(int(Depth))
        else:
            highstr += '\\\\\n' + (4 - len(key)) * ' ' + key + '&\t' + (4 - len(str(int(Depth)))) * ' ' + str(
                int(Depth))

        for x in highspeedtabelround[0:-1]:
            highstr += '&\t' + (4-len(str(x)))*' ' + str(x)
        #  finn tølini sum skullu í lowspeed tabellina
        lowspeedtabelround = lowspeedtabel
        for (i, x) in enumerate(lowspeedtabelround):
            if 0.005 < x < 1:
                lowspeedtabelround[i] = np.round(x, 2)
            else:
                lowspeedtabelround[i] = int(np.round(x, 0))
        #  skriva tølini sum skullu í lowspeed tabellina
        if nyggregla == 0:
            lowstr += '\n' + (4-len(key))*' ' + key + '&\t' + (4-len(str(int(Depth))))*' ' + str(int(Depth))
        else:
            lowstr += '\\\\\n' + (4 - len(key)) * ' ' + key + '&\t' + (4 - len(str(int(Depth)))) * ' ' + str(int(Depth))
        for x in lowspeedtabelround[0:-1]:
            lowstr += '&\t' + (4-len(str(x)))*' ' + str(x)
    highstr += '\\\\\\hline\n\\end{tabular}'
    lowstr += '\\\\\\hline\n\\end{tabular}'
    file = open('Talvur/high_' + navn, 'w')
    file.write(highstr)
    file.close()
    file = open('Talvur/low_' + navn, 'w')
    file.write(lowstr)
    file.close()

    caption = ['Frequency (in parts per thousand) of speeds equal to or exeeding speified values.',
               'Frequency (in parts per thousand) of speeds less than speified values.']
    return '\n\\newpage' \
           '\n\\section{%s}' \
           '\n\\begin{table}[h!]' \
           '\n\\resizebox{\\textwidth}{!}{' \
           '\n\\input{Talvur/high_%s}' \
           '\n}' \
           '\n\\caption{%s}' \
           '\n\\end{table}' \
           '\n' \
           '\n\\section{%s}' \
           '\n\\begin{table}[h!]' \
           '\n\\resizebox{\\textwidth}{!}{' \
           '\n\\input{Talvur/low_%s}' \
           '\n}' \
           '\n\\caption{%s}' \
           '\n\\end{table}' \
           '\n\\newpage' % (sections[0], navn, caption[0], sections[1], navn, caption[1])


def duration_high_speed(bins, dato, magdf, fultdypid, Bin_Size, firstbinrange,
              navn='Duration_high.tex', section='Duration of high speed periods'):
    if len(bins) != 3:
        raise ValueError('bins skal hava 3 bins')
    duration = list(range(60, 1080, 60))
    speed = [50, 100, 150, 200, 300, 400, 500, 600, 800, 1000]
    filnovn = []
    caption = []
    for (rekkja_i_bin, bin) in enumerate(bins):
        data = magdf[str(bin)].values
        total = 0
        tabell = np.zeros((len(speed), len(duration)))
        #  heldur eyða við hvussu langt síðan tað var at vit vóru undir forskelligum speeds
        durationspeeds = [0 for _ in speed]
        i = 0
        while i < len(data):
            if ~np.isnan(data[i]):
                break
            i += 1
        dato0 = dato[i]
        for (i, magnetude) in enumerate(data):
            if np.isnan(magnetude):
                continue
            total += 1
            delta_tid = (dato[i] - dato0) * (24 * 60)       #  min
            dato0 = dato[i]
            #  uppdatera durationspeeds
            for k in range(len(speed)):
                if speed[k] <= magnetude:
                    durationspeeds[k] += delta_tid
                else:
                    durationspeeds[k] = 0
            for d in range(len(duration)):
                for s in range(len(speed)):
                    if durationspeeds[s] >= duration[d]:
                        tabell[s][d] += 1
        #  skriva tex tabell
        texstr = '\\begin{tabular}{|' + (1 + len(duration))*'r|' + '}\n'
        texstr += '\\hline\nSpeed&\t\\multicolumn{%s}{c|}{Duration (minutes)}\\\\\\hline\n' % (len(duration),)
        texstr += 'mm/s'
        for x in duration:
            texstr += '&\t' + (4-len(str(x)))*' ' + str(x)
        texstr += '\\\\\\hline\n'
        for s in range(len(speed)):
            texstr += (4-len(str(speed[s])))*' ' + str(speed[s])
            for d in range(len(duration)):
                #  temp er tað nasta talið sum skal inní tabellina
                temp = 1000 * tabell[s][d]/total
                if 0.005 < temp < 1:
                    temp = np.round(temp, 2)
                else:
                    temp = int(np.round(temp, 0))
                texstr += '&\t' + (4-len(str(temp)))*' ' + str(temp)
            texstr += '\\\\\n'
        texstr += '\\hline'
        texstr += '\n\\end{tabular}'

        if rekkja_i_bin == 0:
            prelabel = 'Surface layer'
        elif rekkja_i_bin == 1:
            prelabel = 'Center layer'
        else:
            prelabel = 'Bottom layer'
        filnovn.append(prelabel.replace(' ', '_') + '_' + navn)
        texfil = open('Talvur/' + filnovn[-1], 'w')
        texfil.write(texstr)
        texfil.close()
        caption.append('%s, bin no: %s. at %2.0fm Depth'
                       % (prelabel, bin, get_dypid(int(bin), fultdypid, Bin_Size, firstbinrange)))
    return '\n\\newpage' \
           '\n\\section{%s}' \
           '\nOccurrence (in parts per thousand) of contiguous periods longer than or equal to ' \
           'specified duration with speeds equal to or exceeding specified threshold values (Speed). ' \
           '\n\\begin{table}[h!]' \
           '\n\\centering' \
           '\n\\resizebox{\\textwidth}{!}{' \
           '\n\\input{Talvur/%s}' \
           '\n}' \
           '\n\\caption{%s}' \
           '\n\\end{table}' \
           '\n' \
           '\n\\begin{table}[h!]' \
           '\n\\centering' \
           '\n\\resizebox{\\textwidth}{!}{' \
           '\n\\input{Talvur/%s}' \
           '\n}' \
           '\n\\caption{%s}' \
           '\n\\end{table}' \
           '\n' \
           '\n\\begin{table}[h!]' \
           '\n\\centering' \
           '\n\\resizebox{\\textwidth}{!}{' \
           '\n\\input{Talvur/%s}' \
           '\n}' \
           '\n\\caption{%s}' \
           '\n\\end{table}' \
           '\n\\newpage' % (section, filnovn[0], caption[0], filnovn[1], caption[1], filnovn[2], caption[2])


def duration_low_speed(bins, dato, magdf, fultdypid, Bin_Size, firstbinrange,
              navn='Duration_low.tex', section='Duration of low speed periods'):
    if len(bins) != 3:
        raise ValueError('bins skal hava 3 bins')
    duration = list(range(60, 1080, 60))
    speed = [50, 100, 150, 200, 300, 400, 500, 600, 800, 1000]
    filnovn = []
    caption = []
    for (rekkja_i_bin, bin) in enumerate(bins):
        data = magdf[str(bin)].values
        total = 0
        tabell = np.zeros((len(speed), len(duration)))
        #  TODO hettar skal vera undir
        #  heldur eyða við hvussu langt síðan tað var at vit vóru yvir forskelligum speeds
        durationspeeds = [0 for _ in speed]
        i = 0
        #  ignoera øll nan í byrjanini set upp inisial value fyri loopið kanska skal dato flytast eitt
        while i < len(data):
            if ~np.isnan(data[i]):
                break
            i += 1
        dato0 = dato[i]
        for (i, magnetude) in enumerate(data):
            if np.isnan(magnetude):
                continue
            total += 1
            delta_tid = (dato[i] - dato0) * (24 * 60)       #  min
            dato0 = dato[i]
            #  uppdatera durationspeeds
            for k in range(len(speed)):
                if speed[k] >= magnetude:
                    durationspeeds[k] += delta_tid
                else:
                    durationspeeds[k] = 0
            for d in range(len(duration)):
                for s in range(len(speed)):
                    if durationspeeds[s] >= duration[d]:
                        tabell[s][d] += 1
        #  skriva tex tabell
        texstr = '\\begin{tabular}{|' + (1 + len(duration))*'r|' + '}\n'
        texstr += '\\hline\nSpeed&\t\\multicolumn{%s}{c|}{Duration (minutes)}\\\\\\hline\n' % (len(duration),)
        texstr += 'mm/s'
        for x in duration:
            texstr += '&\t' + (4-len(str(x)))*' ' + str(x)
        texstr += '\\\\\\hline\n'
        for s in range(len(speed)):
            texstr += (4-len(str(speed[s])))*' ' + str(speed[s])
            for d in range(len(duration)):
                #  temp er tað nasta talið sum skal inní tabellina
                temp = 1000 * tabell[s][d]/total
                if 0.005 < temp < 1:
                    temp = np.round(temp, 2)
                else:
                    temp = int(np.round(temp, 0))
                texstr += '&\t' + (4-len(str(temp)))*' ' + str(temp)
            texstr += '\\\\\n'
        texstr += '\\hline'
        texstr += '\n\\end{tabular}'

        if rekkja_i_bin == 0:
            prelabel = 'Surface layer'
        elif rekkja_i_bin == 1:
            prelabel = 'Center layer'
        else:
            prelabel = 'Bottom layer'
        filnovn.append(prelabel.replace(' ', '_') + '_' + navn)
        texfil = open('Talvur/' + filnovn[-1], 'w')
        texfil.write(texstr)
        texfil.close()
        caption.append('%s, bin no: %s. at %2.0fm Depth'
                       % (prelabel, bin, get_dypid(int(bin), fultdypid, Bin_Size, firstbinrange)))
    return '\n\\newpage' \
           '\n\\section{%s}' \
           '\nOccurrence (in parts per thousand) of contiguous periods longer than or equal to ' \
           'specified duration with speeds less than specified threshold values (Speed)' \
           '\n\\begin{table}[h!]' \
           '\n\\centering' \
           '\n\\resizebox{\\textwidth}{!}{' \
           '\n\\input{Talvur/%s}' \
           '\n}' \
           '\n\\caption{%s}' \
           '\n\\end{table}' \
           '\n' \
           '\n\\begin{table}[h!]' \
           '\n\\centering' \
           '\n\\resizebox{\\textwidth}{!}{' \
           '\n\\input{Talvur/%s}' \
           '\n}' \
           '\n\\caption{%s}' \
           '\n\\end{table}' \
           '\n' \
           '\n\\begin{table}[h!]' \
           '\n\\centering' \
           '\n\\resizebox{\\textwidth}{!}{' \
           '\n\\input{Talvur/%s}' \
           '\n}' \
           '\n\\caption{%s}' \
           '\n\\end{table}' \
           '\n\\newpage' % (section, filnovn[0], caption[0], filnovn[1], caption[1], filnovn[2], caption[2])

def Tidal_analysis_for_depth(tin, uin, vin, lat=62,
              navn='tide.tex', caption='one layer'):
    #TODO tjekka um u og v eru røtt
    coef = utide.solve(tin, uin, vin, lat=lat)
    col = ['Const', 'Freq', 'E-ampl', 'E-gpl', 'N-ampl', 'N-gpl', 'Major', 'minor', 'Theta', 'Graphl']
    supcol = ['', 'c/hr', 'mm/sec', 'deg', 'mm/sec', 'deg', 'mm/sec', 'mm/sec', 'deg', 'deg']
    a = list(coef.name)
    rekkjur = min(len(coef.name), 15)
    coefE = utide.solve(tin, uin, lat=lat, constit=a)
    coefN = utide.solve(tin, vin, lat=lat, constit=a)

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
        tabel += '&\t%5.0f' % (coef.Lsmin[i],)
        tabel += '&\t%3.0f' % (coef.theta[i],)
        tabel += '&\t%3.0f' % (coef.g[i],)
        tabel += '\\\\\n'
    tabel += '\\hline\n'
    tabel += '\\end{tabular}'
    texfil = open('Talvur/%s' % (navn,), 'w')
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

    return '\n\\begin{table}[!ht]' \
           '\n\\centering' \
           '\n\\resizebox{\\textwidth}{!}{' \
           '\n\\input{Talvur/%s}' \
           '\n}' \
           '\n\\caption{%s}' \
           '\n\\end{table}' % (navn, caption)

def Tidal_analysis_for_depth_bins(bins, dato, dirdf, magdf, fultdypid, Bin_Size, firstbinrange, lat=62,
                                  section='Tidal analysis for selected depths'):
    out = '\\newpage\n\\section{%s}\n' % (section,)
    for i, mytempbin in enumerate(bins):
        if i == 0:
            prelabel = 'Surface layer'
        elif i == 1:
            prelabel = 'Center layer'
        else:
            prelabel = 'Bottom layer'
            out += '\\newpage\n'
        u = magdf[str(mytempbin)].values * np.sin(np.deg2rad(dirdf[str(mytempbin)].values))
        v = magdf[str(mytempbin)].values * np.cos(np.deg2rad(dirdf[str(mytempbin)].values))
        caption = '%s, bin no: %s. at %2.0fm Depth' % (prelabel, mytempbin, get_dypid(mytempbin, fultdypid, Bin_Size, firstbinrange))
        out += Tidal_analysis_for_depth(np.array(dato), u, v, lat=lat,
                                     navn='tide%s.tex' % (mytempbin,), caption=caption)
    out += '\n\\newpage\n'
    return out

def Tital_oll_dypir(dato, bins, Frqs, dirdf, magdf, fultdypid, Bin_Size, firstbinrange, lat=62, verbose = True,
                    Section = 'Tidal variation with depth', caption='Harmonic constants for constituent ',
                    tabel_navn='tital_variation_with_depth'):
    coefs = [None for _ in range(len(bins))]
    coefsE = coefs.copy()
    coefsN = coefs.copy()
    tin = np.array(dato)
    for i in range(len(coefs)):
        u = magdf[str(i + 1)].values * np.sin(np.deg2rad(dirdf[str(i + 1)].values))
        v = magdf[str(i + 1)].values * np.cos(np.deg2rad(dirdf[str(i + 1)].values))
        coefs[i] = utide.solve(tin, u, v, lat=lat, constit=Frqs, verbose=verbose)
        coefsE[i] = utide.solve(tin, u, lat=lat, constit=Frqs, verbose=verbose)
        coefsN[i] = utide.solve(tin, v, lat=lat, constit=Frqs, verbose=verbose)
    depts = [get_dypid(x, fultdypid, Bin_Size, firstbinrange) for x in bins]


    out = '\n\\newpage\n\\section{%s}' % (Section,)
    col = ['Bin', 'Depth', 'E-ampl', 'E-gpl', 'N-ampl', 'N-gpl', 'Major', 'minor', 'Theta', 'Graphl']
    supcol = ['', 'm', 'mm/sec', 'deg', 'mm/sec', 'deg', 'mm/sec', 'mm/sec', 'deg', 'deg']

    for i, frq in enumerate(Frqs):
        tabel = '\\begin{tabular}{|' + (len(col)) * 'r|' + '}\n\\hline\n'
        tabel += col[0]
        for x in col[1:]:
            tabel += '&\t%s' % (x,)
        tabel += '\\\\'
        tabel += supcol[0]
        for x in supcol[1:]:
            tabel += '&\t%s' % (x,)
        tabel += '\\\\\\hline\n'
        master_index = np.argwhere(coefs[i].name == frq)[0][0]
        e_index = np.argwhere(coefsE[i].name == frq)[0][0]
        n_index = np.argwhere(coefsN[i].name == frq)[0][0]
        for j, bin in enumerate(bins):
            tabel += str(bin)
            tabel += '&\t%s' % (int(depts[j]),)
            tabel += '&\t%5.0f' % (coefsE[j].A[e_index],)
            tabel += '&\t%5.0f' % (coefsE[j].g[e_index],)
            tabel += '&\t%5.0f' % (coefsN[j].A[n_index],)
            tabel += '&\t%5.0f' % (coefsN[j].g[n_index],)
            tabel += '&\t%5.0f' % (coefs[j].Lsmaj[master_index],)
            tabel += '&\t%5.0f' % (coefs[j].Lsmin[master_index],)
            tabel += '&\t%5.0f' % (coefs[j].theta[master_index],)
            tabel += '&\t%5.0f' % (coefs[j].g[master_index],)
            tabel += '\\\\\n'
        tabel += '\\hline\n\\end{tabular}'
        tabel_fil = open('Talvur/%s_%s.tex' % (tabel_navn, frq), 'w')
        tabel_fil.write(tabel)
        tabel_fil.close()
        #  TODO tjekka hvussu nógvar tabellir skullu á hvørja síðu lat okkum siga 3 men tað skala avhana av nr av bins
        if i % 2 == 0 and i != 0:
            out += '\n\\newpage'
        out += '\n\\begin{table}[!ht]'
        out += '\n\\centering'
        out += '\n\\resizebox{\\textwidth}{!}{'
        out += '\n\\input{Talvur/%s_%s.tex}' % (tabel_navn, frq)
        out += '\n}'
        out += '\n\\caption{%s}' % (caption + frq,)
        out += '\n\\end{table}'
    out += '\n\\newpage'
    return out

def tidal_non_tidal_plot(dato, direct, mag, figwidth=6, figheight=7.1, dpi=200,
                         lat=62, verbose=True, figname='tidal_and_nontidal.pdf'):
    """
    plottar tíðar seriuna í Eystur og Norð, á einum dýpið (goymur eina mynd inni á myndir)
    :param dato: ein list like inniheldur mdate dato fyri tíðarseriuna
    :param dirdf: eitt list like inniheldur dir data í °
    :param magdf: eitt list like inniheldur mag í mm/s abs
    :param fultdypid: float/int hvussu djúpt tað er
    :param Bin_Size: Bin_Size á mátingunum
    :param firstbinrange: 1st Bin Range (m) á mátingini
    :param figwidth: breiddin á figurinum
    :param figheight: hæddin á figurinum
    :param dpi: dpi á figurinum
    :param lat: breiddarstig
    :param verbose: skal utide sleppa at tosa
    :param figname: navnið á fýlini sum verður goymd
    """


    tin = np.array(dato)
    u = mag * np.sin(np.deg2rad(direct))
    v = mag * np.cos(np.deg2rad(direct))
    coef = utide.solve(tin, u, v, lat=lat, verbose=verbose, trend=True)
    #  TODO skal eg fjerna mean
    coef.umean = float(0)
    coef.vmean = float(0)
    reconstruckt = utide.reconstruct(tin, coef=coef, verbose=verbose)
    fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(figwidth, figheight), dpi=dpi)
    date_fmt = mdate.DateFormatter('%d %b')
    axs[0].plot(tin, u, linewidth=.2, label='Original time series')
    axs[0].plot(tin, u - reconstruckt.u, linewidth=.2, label='Original time series minus prediction')
    axs[0].set_ylabel('E [mm/s]')
    axs[0].xaxis.set_major_formatter(date_fmt)
    axs[0].set_xlim([tin[0], tin[-1]])
    axs[0].legend()
    axs[1].plot(tin, v, linewidth=.2, label='Original time series')
    axs[1].plot(tin, v - reconstruckt.v, linewidth=.2, label='Original time series minus prediction')
    axs[1].xaxis.set_major_formatter(date_fmt)
    axs[1].set_ylabel('N [mm/s]')
    axs[1].set_xlim([tin[0], tin[-1]])
    axs[1].legend()
    mpl.rcParams['font.size'] = 7
    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, wspace=0.1, hspace=0.1)
    fig.savefig('myndir/' + figname)


def tidal_non_tidal_bins(bins, dato, dirdf, magdf, fultdypid, Bin_Size, firstbinrange,
                         lat=62, verbose=True, section='Tidal and non-tidal currents'):
    out = '\n\\newpage'
    out += '\n\\section{%s}' % (section,)
    #  TODO partur av analysini er í caption ??? :/
    for i, bin in enumerate(bins):
        figname = 'tidal_and_nontidal_%s.pdf' % (bin,)
        caption = 'this is a caption'  # TODO del me
        if i == 0:
            prelabel = 'Surface layer'
        elif i == 1:
            prelabel = 'Center layer'
        else:
            prelabel = 'Bottom layer'
        caption = '%s bin %s at %3.0f m' % (prelabel, bin, get_dypid(int(bin), fultdypid, Bin_Size, firstbinrange))
        tidal_non_tidal_plot(dato, dirdf[str(bin)].values, magdf[str(bin)].values, lat=lat, verbose=verbose,
                             figname=figname)
        out += '\n\\begin{figure}[!ht]'
        out += '\n\\centering'
        out += '\n\\includegraphics[scale=1]{myndir/%s}' % (figname,)
        out += '\n\\caption{%s}' % (caption,)
        out += '\n\\end{figure}'
        out += '\n\\newpage\n'
    return out

