import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.dates as mdate
import os

path_to_data = '../orginal/navn/'
path_to_out = '../csv/VIK2019/'

dirdf = pd.read_csv(path_to_data + 'dir.txt', encoding='latin', skiprows=11, sep='\t', decimal=',').set_index('Ens').reset_index(drop=True)
magdf = pd.read_csv(path_to_data + 'mag.txt', encoding='latin', skiprows=11, sep='\t', decimal=',').set_index('Ens').reset_index(drop=True)
verdf = pd.read_csv(path_to_data + 'w.txt', encoding='latin', skiprows=11, sep='\t', decimal=',').set_index('Ens').reset_index(drop=True)
metadf = pd.read_csv(path_to_data + 'anc.txt', encoding='latin', skiprows=16, sep='\t', decimal=',', header=None).reset_index(drop=True)
metacol = pd.read_csv(path_to_data + 'anc.txt', encoding='latin',skiprows=12, nrows=1, sep='\t', header=None).reset_index(drop=True).values
#  TODO kanska breit reglu omanfyri

maxbin = int(dirdf.keys()[-1])

metadf.columns = metacol[0]
metadf.set_index('Ens', inplace=True)
metacol = metadf.keys()[8::]

dato = []
for i in magdf[['YR', 'MO', 'DA', 'HH', 'MM', 'SS']].values:
    i[0] += 2000
    dato.append(mdate.date2num(dt.datetime(*i)))

dirdf = dirdf[[str(i) for i in range(1, maxbin + 1)]]
magdf = magdf[[str(i) for i in range(1, maxbin + 1)]]
verdf = verdf[[str(i) for i in range(1, maxbin + 1)]]
metadf = metadf[metacol]
#dirdf['dato'] = dato
#magdf['dato'] = dato

# TODO skriva mag sum [m/s]

#  at umskriva eindina
c = 1e-3

l = len(dirdf)
COL = ['dateTime']
out = {'dateTime': [mdate.num2date(x).strftime('%Y-%m-%dT%H:%M:%S') for x in dato]}

#  TODO skal hettar verða [m/s]
for i in range(1, maxbin + 1):
    out['mag' + str(i)] = magdf[str(i)].values * c
    COL.append('mag' + str(i))
    out['dir' + str(i)] = dirdf[str(i)].values
    COL.append('dir' + str(i))

for i in range(1, maxbin + 1):
    out['w' + str(i)] = [verdf[str(i)].values[j] * c for j in range(l)]
    COL.append('w' + str(i))
for i in metacol:
    j = i
    if i == 'Pit':
        j = 'pitch'
    elif i == 'Rol':
        j = 'roll'
    elif i == 'Hea':
        j = 'hedding'
    elif i == 'Tem':
        j = 'temp'
    elif i == 'Dep':
        j = 'd'
    elif i == 'Ori':
        j = 'ori'
    elif i == 'BIT':
        j = 'bit'
    elif i == 'Bat':
        j = 'bat'
    out[j] = metadf[i].values
    COL.append(j)

outdf = pd.DataFrame(out)
outdf = outdf[COL]

outdf.to_csv(path_to_out + 'magdirdata.csv', sep=',', na_rep='NaN', index=False, encoding='utf-8', float_format='%6.3f')

