import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib as mpl
import utide

from .misc import myprelabel


def sjovarfallmax(uvdata, date, dypir, max_bin, lat=62, navn='intro_max.pdf',
                  dpi=200, font=7, figwidth=6, figheight=7.1,
                 figut = True):
    '''
    finnur eitt yvirmát av hvat utide sigur at hagsti streymur fer at verða
    :param uvdata:      dataframe við uvdata
    :param date:        ein listi sum sigur tiðina á hvørjari máting
    :param dypir:       ein listi sum sigur hvat dýpið er á hvørjari bin
    :param max_bin:     ein int sum sigur hvat tann sísta bin sum eg skal hyggja eftir er
    :param lat:         lat á mátingini input fyri utide ikki ordiliga sikkur hvat tað ger
    :param navn:        navn á figurinum sum kemur út
    :param dpi:         dpi á figurinum sum kemur út
    :param font:        font á figurinum sum kemur út
    :param figwidth:    víddin á figurinum sum kemur út
    :param figheight:   hæddin á figurinum sum kemur út
    :param figut:       skal er hava eina figur ella skal eg hava eina talvu
    '''
    fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(figwidth, figheight), dpi=dpi)
    mpl.rcParams['font.size'] = font
    dypir = [dypir[x] for x in range(max_bin)]
    date = np.array(date)
    mylist = []
    index = np.arange(max_bin)

    for i in range(1, max_bin+1):
        print(i, ' ', end='')
        coef = utide.solve(date, uvdata['u' + str(i)].values, uvdata['v' + str(i)].values,
                           lat=lat, verbose=False, trend=False)
        a = sum(coef['Lsmaj'])
        a += np.sqrt(coef['umean']**2 + coef['vmean']**2)
        mylist.append(a)
    print()

    temp = mylist
    temp = np.sort(temp)
    mymax = min(2 * temp[int(.5*len(temp))], 1.2 * temp[-1])

    #  TODO skriva hesa linjuna ordiligt
    if figut:
        fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(figwidth, figheight), dpi=dpi)
        mpl.rcParams['font.size'] = font

        axs.plot(index, mylist)
        axs.xaxis.set_ticks(index)
        axs.set_xticklabels([int(-x) for x in dypir])
        axs.set_ylim(0, mymax)
        print('her verður ikki goymdur nakar figurur')
        fig.show()
    else:
        return mylist, mymax


def intro_bar(datadf, max_bin, dypir, navn='intro_bar.pdf', dest='LaTeX/',
              caption=None, max_sj=False,
              dpi=200, font=7, figwidth=6, figheight=7.1,
              uvdata=None, date=None, linja=False):
    '''
    Hettar vísur hvussu harður streymurin er í teimun forskelligu dýpinum
    :param datadf:      magdir data
    :param max_bin:     eitt tal sum sigur hvat tað sísta bin sum eg skal higgja eftir
    :param dypir:       ein listi sum sigur hvussu djúpt alt er
    :param navn:        navn á figurinum
    :param dest:        Path to master.tex
    :param caption:     caption á figuri
    :param max_sj:      skal eg hava eitt yvirmát av sjovarfallinum við
    :param dpi:         dpi á figurinum
    :param font:        font stødd á figurinum
    :param figwidth:    víddin á figurinum
    :param figheight:   hæddin á figurinum
    :param uvdata:      uvdata hvissi eg skal tekna maxsjovarfall inní fig
    :param date:        tíðspunktini á mátingunum hviss eg havi brúk fyri tíð
    :param linja:       skal eg hava eina svarta linju sum vísur eitt yvirmát av sjovarfall

    :return:            ein string at koyra í master.tex
    '''
    dypir = [dypir[x] for x in range(max_bin)]
    stod = [25, 50, 75, 95, 99.5]
    bars = [[] for _ in stod]
    bars_sj = [[] for _ in stod]
    for i in range(1, max_bin + 1):
        temp = [x for x in datadf['mag' + str(i)].values if not np.isnan(x)]
        temp = np.sort(temp)
        longd = len(temp)
        for j, brok in enumerate(stod):
            if brok > 100:
                raise ValueError('brok er ov stort')
            elif brok == 100:
                bars[j].append(temp[-1])
            elif brok <= 0:
                raise ValueError('brok er ov litið')
            else:
                bars[j].append(temp[int(brok*longd/100)])

    if max_sj and uvdata is not None and date is not None:
        tin = np.array(date)
        for i in range(1, max_bin + 1):
            u = np.array(datadf['mag' + str(i)] * np.cos(np.deg2rad(datadf['dir' + str(i)] - 90)))
            v = np.array(datadf['mag' + str(i)] * np.cos(np.deg2rad(datadf['dir' + str(i)])))
            coef = utide.solve(tin, u, v, lat=62)
            tide = utide.reconstruct(tin, coef)
            temp = [np.sqrt(x**2+y**2) for x, y in zip(tide['u'], tide['v'])]
            temp = [x for x in temp if not np.isnan(x)]
            temp = np.sort(temp)
            longd = len(temp)
            for j, brok in enumerate(stod):
                if brok > 100:
                    raise ValueError('brok er ov stort')
                elif brok == 100:
                    bars_sj[j].append(temp[-1])
                elif brok <= 0:
                    raise ValueError('brok er ov litið')
                else:
                    bars_sj[j].append(temp[int(brok*longd/100)])

    fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(figwidth, figheight), dpi=dpi)
    mpl.rcParams['font.size'] = font


    index = np.arange(max_bin)
    plots = []
    vidd = .33
    plots.append(axs.bar([x-vidd/2 for x in index], bars[0], vidd, label=str(stod[0])+'%', edgecolor='k'))
    for i in range(1, len(stod)):
        plots.append(axs.bar([x-vidd/2 for x in index], [x - y for x, y in zip(bars[i], bars[i-1])],
                                     vidd, bottom=bars[i-1], label=str(stod[i])+'%', edgecolor='k'))

    plt.gca().set_prop_cycle(None)
    plots.append(axs.bar([x + vidd/2 for x in index], bars_sj[0], vidd, edgecolor='k', hatch='//'))
    for i in range(1, len(stod)):
        plots.append(axs.bar([x + vidd/2 for x in index], [x - y for x, y in zip(bars_sj[i], bars_sj[i-1])],
                                     vidd, bottom=bars_sj[i-1], edgecolor='k', hatch='//'))
    axs.xaxis.set_ticks(index)
    axs.set_xticklabels([int(-x) for x in dypir])
    axs.set_ylabel('Streymferð (mm/s)')
    axs.set_xlabel('Dýpi (m)')
    temp = bars[-1]
    temp = np.sort(temp)
    mymax = min(2 * temp[int(.5*len(temp))], 1.2*temp[-1])

    #  eg havi bara sett lat til defult lat=62
    if max_sj and uvdata is not None and date is not None and linja:
        templist, maxcand = sjovarfallmax(uvdata, date, dypir, max_bin, figut = False)
        axs.plot(index, templist, color='k', label='yvirmát fyri sjovarfallið')
        axs.set_ylim(0, max(mymax, maxcand))
    else:
        axs.set_ylim(0, mymax)

    axs.legend(ncol=int(np.ceil(len(stod)/2)))
    fig.subplots_adjust(left=0.1, bottom=0.15, right=0.99, top=0.99, wspace=0.0, hspace=0.2)
    fig.savefig(dest + 'myndir/%s' % navn, dpi=dpi)

    if caption is None:
        caption = 'Býti av streymferð niður gjøgnum dýpi. Dýpi er á x-ásini, '
        caption += 'og streymferð er á y-ásini. Hvør súla vísir býtið av '
        caption += 'streymferðini á einum ávísum dýpi. Tær óskavaðu súlurnar vísa máld virði, '
        caption += 'og tær skavaðu vísa sjóvarfalseffektina roknaða frá mátingunum. '
        caption += 'Litirnir vísa brøkpartin av mátingunum, '
        caption += 'har streymferðin er minni enn ferðin á y-ásini. '
        caption += 'T.d. vísir myndin, at á \\SI{%s}{m} dýpi er streymferðin í '\
                % str(int(-dypir[0]))
        caption += '75\\% av mátingunum minni enn '
        caption += '\\SI{%s}{mm/s}.' % str(int(bars[2][0]))

    label = '\\label{barstreym}'

    out = '\n\\FloatBarrier\n'
    out += '\\section{Býti av streymferð á ymsum dýpum}\n'
    out += '\\begin{figure}[h!]\n'
    out += '\\includegraphics[scale=1]{myndir/%s}\n' % navn
    out += '\\caption{%s}\n' % caption
    out += '%s\n' % label
    out += '\n\\end{figure}\n'
    out += '\\newpage\n'

    return out

#  TODO skriva framskriving ordiligt
#def tegnahovmuller(data, dypid, dato, mal='FO', ratning=0, nrplots=11, figwidth=6, figheight=7.1,
                   #font=7, vmax=None, dest='', navn='Hovmuller.pdf', caption='caption',
                   #dpi=200):


def frammskriva(tin, uin, vin, lat=62, nrplots=12, figwidth=6, figheight=7.1,
                navn='framskriving.pdf', dpi=200):
    ''''
    fyri tað fyrsta fari eg at skriva hettar til at framskriva eitt ár har framm frá sístu máting
    eg setið tað orginala dataði við har tey eru saman

    :param tin:     tíðin sum sum svarar til tíðina av mátinginum
    :param uin:     u dataði fyri mátingina
    :param vin:     v dataði fyri mátingina
    :param lat:     latetude
    :param navn:    navnið á figurinum
    '''
    tin = np.array(tin)
    uin = np.array(uin)
    vin = np.array(vin)

    coef = utide.solve(tin, uin, vin, lat=lat)

    #  finn hvar vit byrja og hvar vit enda
    start, stop = np.floor(tin[0]), np.ceil(tin[-1])
    start = mdate.num2date(start)
    stop = mdate.num2date(stop)

    fig, axs = plt.subplots(ncols=1, nrows=nrplots, figsize=(figwidth, figheight), dpi=dpi)


def tidal_analysis_for_depth(tin, uin, vin, lat=62,
              navn='tide.tex', caption='one layer', dest='LaTeX/', label=''):
    coef = utide.solve(tin, uin, vin, lat=lat)
    col = ['Const', 'Frequency', 'Perioda', 'Major', 'Minor', 'Theta', 'Graphl', 'R']
    supcol = ['', 'c/hr', '', 'mm/sec', 'mm/sec', 'deg', 'deg', '']
    a = list(coef.name)
    rekkjur = min(len(coef.name), 15)

    tabel = '\\begin{tabular}{|' + 'l|' +  (len(col) -1) * 'r|' + '}\n\\hline\n'
    tabel += col[0]
    for x in col[1:]:
        tabel += '&\t%s' % (x,)
    tabel += '\\\\'
    tabel += supcol[0]
    for x in supcol[1:]:
        tabel += '&\t%s' % (x,)
    tabel += '\\\\\\hline\n'

    for i in range(rekkjur):
        perioda = 1/coef.aux.frq[i]
        eind = ' t'
        if perioda > 24:
            perioda = perioda / 24
            eind = ' d'
        tabel += coef.name[i].rjust(4)
        tabel += '&\t%.8f' % (coef.aux.frq[i],)
        tabel += '&\t%4.1f' % (perioda,) + eind
        tabel += '&\t%4.2f' % (coef.Lsmaj[i],)
        tabel += '&\t%4.2f' % (abs(coef.Lsmin[i]),)
        tabel += '&\t%3.0f' % (coef.theta[i],)
        tabel += '&\t%3.0f' % (coef.g[i],)
        tabel += '&\t%s' % ('$\\circlearrowleft$' if coef.Lsmin[i]>0 else '$\\circlearrowright$',)
        tabel += '\\\\\n'
    tabel += '\\hline\n'
    tabel += '\\end{tabular}'
    texfil = open(dest + 'Talvur/%s' % (navn,), 'w')
    texfil.write(tabel)
    texfil.close()

    return '\n\\begin{subtable}{\\textwidth}' \
           '\n\\centering' \
           '\n\\input{Talvur/%s}' \
           '\n\\caption{%s}' \
           '\n%s' \
           '\n\\end{subtable}' % (navn, caption, label)


def tidal_analysis_for_depth_bins(bins, dato, datadf, dypir, mal='FO', lat=62,
                                  section=None,
                                  dest = 'LaTeX/'):
    if section == None:
        if mal == 'EN':
            section = 'Tidal analysis for selected depths'
        else:
            section = 'Sjóvarfalsanalysa fyri vald dýpi'

    #  geri out her
    out = '\n\\FloatBarrier\n'\
            '\\newpage\n'\
            '\\section{%s}\\label{sec:sjovarfall_vald_dypir}\n'\
            '\\begin{table}[h!]\n' % (section,)
    for i, mytempbin in enumerate([bins[0], bins[-1]]):
        if i == 0:
            prelabel = myprelabel(0)
        else:
            prelabel = myprelabel(3)
        u = datadf['mag' + str(mytempbin)].values * np.sin(np.deg2rad(datadf['dir' + str(mytempbin)].values))
        v = datadf['mag' + str(mytempbin)].values * np.cos(np.deg2rad(datadf['dir' + str(mytempbin)].values))

        if mytempbin == '10m':
            tempdypid = 10
        else:
            tempdypid = -dypir[mytempbin - 1]

        if mal == 'EN':
            caption = '%s, bin no: %s. at %2.0f m Depth' % (prelabel, mytempbin, tempdypid)
        else:
            caption = '%s - \\SI{%2.0f}{m}'\
                    % (prelabel.split(')')[-1].lower(), tempdypid)
        #  uppdateri hann her
        out += tidal_analysis_for_depth(np.array(dato), u, v, lat=lat,
                                     navn='tide%s.tex' % (mytempbin,), caption=caption, dest=dest,
                                     label='\\label{tidal_bin%s}' % (mytempbin,))
    forklarandi_tekstur = 'Sjóvarfalsanalysa av streyminum ovarliga og niðarliga í sjónum. '\
            'Sí frágreiðing um sjóvarfall í kapittul~\\ref{sec:sjovarfall}. '\
            'Talvurnar lýsa 15 teir sterkastu sjóvarfalslutirnar'

    out += '\n\\caption{%s}\n'\
            '\\label{tidal_bins}\n'\
            '\\end{table}\n'\
            '\\newpage\n' % (forklarandi_tekstur,)
    return out


def tital_oll_dypir(dato, bins, Frqs, datadf, dypir, mal='FO', lat=62, verbose = True,
                    Section=None, caption=None,
                    tabel_navn='tital_variation_with_depth',
                    dest='LaTeX/'):
    if Section == None:
        if mal == 'EN':
            Section = 'Tidal variation with depth'
        else:
            Section = 'Sjóvarfalsbroyting ígjøgnum dýpi'
    if caption == None:
        if mal == 'EN':
            caption='Harmonic constants for constituent '
        else:
            caption=''
    coefs = [None for _ in range(len(bins))]
    tin = np.array(dato)
    for i in range(len(coefs)):
        print(i)
        u = datadf['mag' + str(i + 1)].values * np.sin(np.deg2rad(datadf['dir' + str(i + 1)].values))
        v = datadf['mag' + str(i + 1)].values * np.cos(np.deg2rad(datadf['dir' + str(i + 1)].values))
        coefs[i] = utide.solve(tin, u, v, lat=lat, constit=Frqs, verbose=verbose)
    depts = [-dypir[x - 1] for x in bins]

    out = '\n\\FloatBarrier\n'\
            '\\newpage\n'\
            '\\section{%s}\\label{sec:sjovarfall_oll_dypir}' % (Section,)
    col = ['Bin', 'Depth', 'Major', 'Minor', 'Theta', 'Graphl', 'R']
    supcol = ['', 'm', 'mm/sec', 'mm/sec', 'deg', 'deg', '']

    time = coefs[0].aux.reftime
    print(time)
    time = mdate.num2date(time).strftime('%Y-%m-%dT%H:%M:%S')
    time = ', Reftime = ' + time
    for i, frq in enumerate(Frqs):
        if mal != 'EN':
            if frq == 'M2':
                caption = 'Sjóvarfalskonstantar fyri M2 á øllum dýpum. '\
                        'M2 er hálvdagligt sjóvarfall, ið kemur av, '\
                        'at Mánin dregur í vatnskorpuna, tá Jørðin snarar '\
                        'eitt umfar. M2 er á flestu støðum tann sterkasti sjóvarfalsluturin.'
            else:
                caption = 'Sjóvarfalskonstantar fyri %s á øllum dýpum.' % frq
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
        for j in range(len(bins)):
            tabel += str(bins[j])
            tabel += '&\t%s' % (int(depts[j]),)
            tabel += '&\t%4.2f' % (coefs[j].Lsmaj[master_index],)
            tabel += '&\t%4.2f' % (abs(coefs[j].Lsmin[master_index]),)
            tabel += '&\t%5.0f' % (coefs[j].theta[master_index],)
            tabel += '&\t%5.0f' % (coefs[j].g[master_index],)
            tabel += '&\t%s' % ('$\\circlearrowleft$' if coefs[j].Lsmin[master_index]>0 else '$\\circlearrowright$',)
            tabel += '\\\\\n'
        tabel += '\\hline\n\\end{tabular}'
        tabel_fil = open(dest + 'Talvur/%s_%s.tex' % (tabel_navn, frq), 'w')
        tabel_fil.write(tabel)
        tabel_fil.close()
        #  kanska skal hettar umarbeiðast vit finna útav tíð tá vit higgja eftir
        #  Úrslitinum
        if i % 2 == 0 and i != 0:
            out += '\n\\newpage'
        out += '\n\\begin{table}[!ht]'
        out += '\n\\centering'
        out += '\n\\input{Talvur/%s_%s.tex}' % (tabel_navn, frq)
        out += '\n\\caption{%s}' % (caption,)
        out += '\n\\label{Tidalvar_%s}' % (frq,)
        out += '\n\\end{table}'
    out += '\n\\newpage\n'
    return out

# tital_oll_dypir

def tidal_non_tidal_plot(dato, direct, mag, figwidth=6, figheight=7.1, dpi=200,
                         lat=62, verbose=True, figname='tidal_and_nontidal.pdf',
                         dest='LaTeX/', font=7):
    """
    plottar tíðar seriuna í Eystur og Norð, á einum dýpið (goymur eina mynd inni á myndir)
    :param dato: ein list like inniheldur mdate dato fyri tíðarseriuna
    :param datadf: eitt list like inniheldur mag í mm/s abs og dir
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
    #  mean verður fjerna fyri at tá vit hava tiki tingini frá hvørjum ørum
    #  so er munirin mitt í data settinum, tað er ikki heilt ratt men
    #  tað sar ratt ut tá tað skal síggja ratt út
    coef.umean = float(0)
    coef.vmean = float(0)
    reconstruckt = utide.reconstruct(tin, coef=coef, verbose=verbose)
    reconstruckt = utide.reconstruct(tin, coef=coef, verbose=verbose)

    fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(figwidth, figheight), dpi=dpi)
    mpl.rcParams['font.size'] = font

    date_fmt = mdate.DateFormatter('%d %b')
    axs[0].plot(tin, u, linewidth=.2, label='Original time series')
    axs[0].plot(tin, u - reconstruckt.u, linewidth=.2, label='Original time series minus prediction')
    axs[0].set_ylabel('Streymferð í eystan (mm/s)')
    axs[0].xaxis.set_major_formatter(date_fmt)
    axs[0].set_xlim([tin[0], tin[-1]])
    axs[1].plot(tin, v, linewidth=.2, label='Original time series')
    axs[1].plot(tin, v - reconstruckt.v, linewidth=.2, label='Original time series minus prediction')
    axs[1].xaxis.set_major_formatter(date_fmt)
    axs[1].set_ylabel('Streymferð í norðan (mm/s)')
    axs[1].set_xlim([tin[0], tin[-1]])
    mpl.rcParams['font.size'] = 7
    plt.subplots_adjust(left=0.15, bottom=0.05, right=0.95, top=0.95, wspace=0.1, hspace=0.1)
    fig.savefig(dest + 'myndir/' + figname)


def tidal_non_tidal_bins(bins, dato, datadf, dypir, mal='FO',
                         lat=62, verbose=True, section=None,
                         dest='LaTeX/'):
    if section == None:
        if mal == 'EN':
            section = 'Tidal and non-tidal currents'
        else:
            section = 'Streymur, sum ikki er sjóvarfalsdrivin'
    out = '\n\\FloatBarrier\n'\
            '\\newpage'
    out += '\n\\section{%s}' % (section,)
    for i, item in enumerate(bins):
        figname = 'tidal_and_nontidal_%s.pdf' % (item,)
        if i == 0:
            prelabel = 'Surface layer'
        elif i == 1:
            prelabel = 'Center layer'
        else:
            prelabel = 'Bottom layer'

        if item == '10m':
            tempdypid = 10
        else:
            tempdypid = -dypir[item - 1]

        if mal == 'EN':
            caption = '%s bin %s at %3.0f m' % (prelabel, item, tempdypid)
        else:
            caption = 'Bláu linjurnar vísa máldu streymferðirnar á \\SI{%2.0f}{m} dýpi í '\
                    'eysturættina (ovara myndin) og norðurættina (niðara myndin) undir '\
                    'mátitíðarskeiðinum. Gulu linjurnar vísa partin av rákinum, '\
                    'sum ikki er drivin av sjóvarfallinum.' % (tempdypid,)

        tidal_non_tidal_plot(dato, datadf['dir' + str(item)].values,
                             datadf['mag' + str(item)].values, lat=lat, verbose=verbose,
                             figname=figname, dest=dest)
        out += '\n\\begin{figure}[!ht]'
        out += '\n\\centering'
        out += '\n\\includegraphics[scale=1]{myndir/%s}' % (figname,)
        out += '\n\\caption{%s}' % (caption,)
        out += '\n\\label{tidal_non%s}' % (item,)
        out += '\n\\end{figure}'
        out += '\n\\newpage\n'
    return out


def tidaldominesrekkja(item, mag, direct, dato, dypid, lat=62, verbose=True,
                       trend=True, dataut=False):
    tin = np.array(dato)
    u = mag * np.sin(np.deg2rad(direct))
    v = mag * np.cos(np.deg2rad(direct))
    coef = utide.solve(tin, u, v, lat=lat, verbose=verbose, trend=trend)
    reconstruckt = utide.reconstruct(tin, coef=coef, verbose=verbose)
    orgmag = [x for x in mag if not np.isnan(x)]
    recmag = [np.sqrt(x**2+y**2) for x, y
              in zip(u - reconstruckt.u, v - reconstruckt.v) if not np.isnan(x)]
    if not dataut:
        out = ''
        out += str(item)
        out += '&\t%2.2f' % (dypid,)
        out += '&\t%2.2f\\%%' % (100 * np.var(recmag)/np.var(orgmag),)
        out += '&\t%6.0f' % (sum([coef.Lsmaj[i] for i in range(6)]),)
        out += '&\t%s' % ('Ja' if 100 * np.var(recmag)/np.var(orgmag) < 50
                          and sum([coef.Lsmaj[i] for i in range(6)]) > 150 else 'Nei',)
        out +='\\\\\n'
        return out
    else:
        part_av_var = 100 * np.var(recmag)/np.var(orgmag)
        sum_av_5 = sum([coef.Lsmaj[i] for i in range(6)])
        sjovarfallsdrivi = part_av_var < 50 and sum_av_5 > 150
        return part_av_var, sum_av_5, sjovarfallsdrivi


def tidaldomines(bins, dato, datadf, dypir, lat=62, verbose=True,
                 section='Sjovarfall', dest='LaTeX/'):
    colonnir = ['bin', 'dypid', 'varratio', 'sum', 'sjóvarfalsdrivin']
    tabel = '\\begin{tabular}{|r|r|r|r|c|}\n'
    tabel += '\\hline\n'
    tabel += colonnir[0]
    for col in colonnir[1:]:
        tabel += '&\t%s' % col
    tabel += '\\\\\\hline\n'
    for i in range(len(dypir)):
        item = i+1
        dypid = dypir[i]
        mag = datadf['mag' + str(i+1)].values
        direct = datadf['dir' + str(i+1)].values
        tabel += tidaldominesrekkja(item, mag, direct, dato, dypid, lat=62, verbose=False)
    tabel += '\\hline\n\\end{tabular}'
    tabel_fil = open(dest + 'Talvur/sjovarfalsdrivin.tex', 'w')
    tabel_fil.write(tabel)
    tabel_fil.close()
    caption = 'sjovarfalsdrivin'
    out = '\n\\FloatBarrier\n\\newpage'
    out += '\n\\section{sjovarfalsdrivin}'
    out += '\n\\begin{table}[!ht]'
    out += '\n\\centering'
    out += '\n\\resizebox{\\textwidth}{!}{'
    out += '\n\\input{Talvur/sjovarfalsdrivin.tex}'
    out += '\n}'
    out += '\n\\caption{%s}' % (caption,)
    out += '\n\\label{sjovarfalsdirvin}'
    out += '\n\\end{table}'
    out += '\n\\newpage\n'
    return out
