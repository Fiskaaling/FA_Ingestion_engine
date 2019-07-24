import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.dates as mdate
import time
import os

#  umskriva dir til u og mag til v
path_to_data = '../orginal/navn/'
path_to_out = '../csv/navn/'

udf = pd.read_csv(path_to_data + 'u.txt', encoding='latin', skiprows=11, sep='\t', decimal=',').set_index('Ens').reset_index(drop=True)
vdf = pd.read_csv(path_to_data + 'v.txt', encoding='latin', skiprows=11, sep='\t', decimal=',').set_index('Ens').reset_index(drop=True)
verdf = pd.read_csv(path_to_data + 'w.txt', encoding='latin', skiprows=11, sep='\t', decimal=',').set_index('Ens').reset_index(drop=True)
metadf = pd.read_csv(path_to_data + 'anc.txt', encoding='latin', skiprows=16, sep='\t', decimal=',', header=None).reset_index(drop=True)
metacol = pd.read_csv(path_to_data + 'anc.txt', encoding='latin',skiprows=12, nrows=1, sep='\t', header=None).reset_index(drop=True).values
#  TODO kanska breit reglu omanfyri

maxbin = int(udf.keys()[-1])

metadf.columns = metacol[0]
metadf.set_index('Ens', inplace=True)
metacol = metadf.keys()[8::]

dato = []
for i in udf[['YR', 'MO', 'DA', 'HH', 'MM', 'SS']].values:
    i[0] += 2000
    dato.append(mdate.date2num(dt.datetime(*i)))

udf = udf[[str(i) for i in range(1, maxbin + 1)]]
vdf = vdf[[str(i) for i in range(1, maxbin + 1)]]
verdf = verdf[[str(i) for i in range(1, maxbin + 1)]]
metadf = metadf[metacol]

l = len(udf)
COL = ['dateTime']
out = {'dateTime': [mdate.num2date(x).strftime('%Y-%m-%dT%H:%M:%S') for x in dato]}

#  umskriva til [m/s]
c = 1e-3

for i in range(1, maxbin + 1):
    out['u' + str(i)] = udf[str(i)].values * c
    COL.append('u' + str(i))
    out['v' + str(i)] = vdf[str(i)].values * c
    COL.append('v' + str(i))

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

outdf.to_csv(path_to_out + 'uvdata.csv', sep=',', na_rep='NaN', index=False, encoding='utf-8', float_format='%6.3f')

