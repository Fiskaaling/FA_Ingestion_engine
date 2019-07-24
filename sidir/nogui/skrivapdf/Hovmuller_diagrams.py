import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.cm as cm
import matplotlib.patches as mpatches
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
            F[Ebin][Nbin] += 1
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
            prelabel = 'c) Buttom layer'
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
                 bins[1], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange),
                 bins[2], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange))

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
            prelabel = 'c) Buttom layer'
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
                 bins[1], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange),
                 bins[2], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange))

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
            prelabel = 'c) Buttom layer'
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
                 bins[1], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange),
                 bins[2], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange))

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
            prelabel = 'Buttom layer'
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
                 bins[1], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange),
                 bins[2], get_dypid(bins[0], fultdypid, Bin_Size, firstbinrange))

    return '\n\\newpage\n\\section{%s}\n\\begin{figure}[h!]\n\\includegraphics[scale=1]{myndir/%s}' \
           '\n\\caption{%s}\n\\end{figure}\n\\newpage' % (section, navn, caption)


def frequencytabellir(magdf, fultdypid, Bin_Size, firstbinrange,
              navn='Frqtabel.tex', sections=['Frequency of high speeds', 'Frequency of low speeds']):
    #  Freequency of high speeds
    inforows = ['no.', 'm']
    #  TODO skal eg koyra hettar inn sum eitt input til funktiónina
    infospeed = [str(x) for x in [50, 100, 150, 200, 250, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1500]]
    inforows += infospeed
    #  gera klárt til tabellina
    highstr = '\\begin{tabular}{|' + len(inforows)*'r|' + '}\n\\hline\n Bin&\tDepth&\t' \
                                                          '\multicolumn{%s}{|c|}{Speed [mm/s]}\\\\\\hline\n'\
              % (len(inforows)-2,)
    highstr += (4-len(inforows[0]))*' ' + inforows[0]
    for x in inforows[1::]:
        highstr += '&\t' + (4-len(x))*' ' + x
    lowstr = highstr
    for key in magdf.keys():
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
        highstr += '\\\\\n' + (4-len(key))*' ' + key + '&\t' + (4-len(str(int(Depth))))*' ' + str(int(Depth))
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
        lowstr += '\\\\\n' + (4-len(key))*' ' + key + '&\t' + (4-len(str(int(Depth))))*' ' + str(int(Depth))
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


def duration_speed(bins, dato, magdf, fultdypid, Bin_Size, firstbinrange,
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
        texstr += '\\hline\nSpeed&\t\\multicolumn{%s}{|c|}{Duration (minutes)}\\\\\\hline\n' % (len(duration),)
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
            prelabel = 'Buttom layer'
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
           'Flagged ensembles are ignored.' \
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

