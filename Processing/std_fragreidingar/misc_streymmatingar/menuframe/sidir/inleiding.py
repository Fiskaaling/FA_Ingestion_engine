import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import utide


def gersamadratt(datadf, uvdatadf, dypir, max_bin, date, dest='LaTeX/', lat=62,
                 dpi=200, font=7, figwidth=6, figheight=3):

    #  TODO finn hattar 27 tali
    caption = 'Býti av streymferð niður gjøgnum dýpi.' \
            ' Dýpi er á x-ásini og streymferð er á y-ásini.'\
            ' Hvør súla vísir býtið av streymferðini á einum dýpi.'\
            ' Tær óskavaðu súlurnar vísa máld virði og'\
            ' tær skavaðu vísa sjóvarfallseffektina roknaða frá mátingunum.'\
            ' Litirnir vísa brøkpartin av mátingunum har streymferðin'\
            ' er minni enn ferðina á y-ásini.'\
            ' T.d. vísir myndin, at á 27 m dýpi er streymferðin'\
            ' í 75\\% av mátingunum minni enn \\SI{300}{mm/s}.'
    out = ''
    out += intro_bar(datadf, max_bin, dypir, dest=dest, figheight=figheight,
                    max_sj=True, uvdata=uvdatadf, date=date)
    return out


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
              caption='fordeiling av streymi gjøgnum dypid', max_sj=False,
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
    axs.set_ylabel('Streymferð [mm/s]')
    axs.set_xlabel('Dýpi [m]')
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

    label = '\\label{barstreym}'

    out = ''
    out += '\n\\FloatBarrier\n'
    out += '\\begin{figure}[h!]%s\n' % label
    out += '\\includegraphics[scale=1]{myndir/%s}\n' % navn
    out += '\\caption{%s}' % caption
    out += '\n\\end{figure}\n'
    out += '\\newpage\n'

    return out
