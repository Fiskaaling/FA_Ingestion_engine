import datetime as dt

import pandas as pd
import numpy as np
from matplotlib import dates as mdate


#  TODO skriva hettar til at kunna taka fleiri input inn
def inles(path_to_data, dictionary=False):
    '''
    Innlesur streym frá 'path_to_data', sorterar tað vánaliga dataði
    vekk og gevur aftur eitt set av variablum (date, dypir, max_bin, datadf, uvdatadf)

    :param dictionary: skal hetta returna í einari dict

    returns:
    date:   tíðspunkti á mátingunum við formati frá matplotlib.dates
    dypir:  dýpi á teimun forskelligu bins "dypir[n]" er dýpið á bin nr n+1
    max_bin:    størsta bin sum er við í datasettinum
    datadf:     mag, dir og w av dataðinum á øllum dýpinum
    datadf:     u, v og w av dataðinum á øllum dýpinum
    --------------------------------------------------------------------------------
    vánaligt data er definera til quali > 2
    fyrsta bin er altíð nr 1
    '''
    qualidf = pd.read_csv(path_to_data + 'quali.csv')
    #  finn hvar mátarin er farin á skjógv og har dataði er markera vánaligt
    keys = list(qualidf.keys())
    keys.remove('dateTime')
    mask = qualidf[keys].min(axis=1).values
    mask = np.argwhere(mask > 2).flatten()

    # inless dataði og fjerna dataði har mátarin ikki er komin á skjógv
    qualidf = qualidf.drop(mask).reset_index(drop=True)
    datadf = pd.read_csv(path_to_data + 'magdirdata.csv').drop(mask).reset_index(drop=True)
    uvdatadf = pd.read_csv(path_to_data + 'uvdata.csv').drop(mask).reset_index(drop=True)

    #  ger ein var til dato
    date = [mdate.date2num(dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S')) for x in datadf['dateTime']]

    #  metadata ting
    metadf = pd.read_csv(path_to_data + 'meta.csv', index_col='key')['value']
    Bin_Size = float(metadf['bin_size'])
    firstbinrange = float(metadf['firstbinrange'])
    max_bin = int(metadf['maxbin'])
    dypid = float(metadf['median_dypid'])

    #  skriva ein variabil til brúka sum ref til hvat dýpi allar mátingarnar eru gjørdar á
    dypir = [float(metadf['bin' + str(x)]) - dypid for x in range(1, max_bin+1)]

    ##  finn hvat fyri bins skullu droppast
    #droppa_meg = [ i+1 for i in range(len(dypir)) if dypir[i] >= -dypid/10]
    #if len(droppa_meg) != 0:
    #    max_bin = droppa_meg[0] - 1

    #dypir = [dypir[i] for i in range(len(dypir)-len(droppa_meg))]

    ##  tak ting úr datadf
    #datadf.drop([ '%s%s' % (typa, int(tal)) for typa in ['mag', 'dir', 'w'] for tal in droppa_meg],
    #            axis=1, inplace=True)
    ##  tak ting úr uvdatadf
    #uvdatadf.drop([ '%s%s' % (typa, int(tal)) for typa in ['u', 'v', 'w'] for tal in droppa_meg],
    #              axis=1, inplace=True)

    #  ger datði til [mm/s] ístaðinfyri [m/s]
    for key in datadf.keys():
        if 'mag' in key or key[1:].isdigit():
            datadf[key] = np.round(datadf[key].values*1000)
        elif 'w' in key or key[1:].isdigit():
            datadf[key] = np.round(datadf[key].values*1000)
    for key in uvdatadf.keys():
        if key[1:].isdigit():
            uvdatadf[key] = np.round(uvdatadf[key].values*1000)
    ##################################################
    #                Gerirera 10m data               #
    ##################################################
    #  men eg fari at generera eina colonnu í bæði datadf og uvdatadf
    #  har eg havi interpolera fyri at hava data 10 m undir vatnskorpini
    #  uvdataði verður interpolera so rokni eg út hvat magdir eiður at vera
    tiggju_m = uvdatadf['d']
    tiggju_u = []
    tiggju_v = []
    tiggju_mag = []
    tiggju_dir = []
    for i, item in enumerate(tiggju_m):
        #  ger hettar seint fyri first
        #  finn ein vector har vit hava dypi allastani
        tempdypir = [float(metadf['bin' + str(x)]) - item for x in range(1, max_bin+1)]

        #  finn hvar 10m er ímillum
        j = np.searchsorted(tempdypir, -10)

        #  finn s og t
        s = (-10 - tempdypir[j]) / (tempdypir[j-1] - tempdypir[j])

        #  rokna og set inn í tiggju_u og tiggju_v
        if j > 0:
            tempu = s * uvdatadf['u%s' % str(j)][i] + (1-s) * uvdatadf['u%s' % str(j+1)][i]
            tempv = s * uvdatadf['v%s' % str(j)][i] + (1-s) * uvdatadf['v%s' % str(j+1)][i]
        else:
            tempu = uvdatadf['u%s' % str(1)][i]
            tempv = uvdatadf['v%s' % str(1)][i]
        tiggju_u.append(tempu)
        tiggju_v.append(tempv)
        #  rokna og set inn í tiggju_mag og tiggju_dir
        tiggju_mag.append(np.sqrt(tempu**2+tempv**2))
        tiggju_dir.append(np.rad2deg(np.arctan2(tempu, tempv)))
    #  set col inní DataFrame
    uvdatadf.insert(loc=0, column='u10m', value=tiggju_u)
    uvdatadf.insert(loc=0, column='v10m', value=tiggju_v)
    datadf.insert(loc=0, column='mag10m', value=tiggju_mag)
    datadf.insert(loc=0, column='dir10m', value=tiggju_dir)
    ##################################################
    #                  enda 10 m data                #
    ##################################################

    #  finn hvat fyri bins skullu droppast
    droppa_meg = [ i+1 for i in range(len(dypir)) if dypir[i] >= -dypid/10]
    if len(droppa_meg) != 0:
        max_bin = droppa_meg[0] - 1

    dypir = [dypir[i] for i in range(len(dypir)-len(droppa_meg))]

    #  tak ting úr datadf
    datadf.drop([ '%s%s' % (typa, int(tal)) for typa in ['mag', 'dir', 'w'] for tal in droppa_meg],
                axis=1, inplace=True)
    #  tak ting úr uvdatadf
    uvdatadf.drop([ '%s%s' % (typa, int(tal)) for typa in ['u', 'v', 'w'] for tal in droppa_meg],
                  axis=1, inplace=True)

    if dictionary:
        return {'data':date, 'dypir':dypir, 'max_bin':max_bin,
                'datadf':datadf, 'uvdatadf':uvdatadf
               }
    return date, dypir, max_bin, datadf, uvdatadf

