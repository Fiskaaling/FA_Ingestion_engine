import pandas as pd
import numpy as np

path_to_data = '../orginal/navn/'
path_to_out = '../csv/navn/'

metadf = pd.read_csv(path_to_data + 'anc.txt', encoding='latin', skiprows=16, sep='\t', decimal=',', header=None).reset_index(drop=True)
metacol = pd.read_csv(path_to_data + 'anc.txt', encoding='latin',skiprows=12, nrows=1, sep='\t', header=None).reset_index(drop=True).values
metadf.columns = metacol[0]
out={}

with open(path_to_data + 'dir.txt', 'r') as file:
    file.readline()
    file.readline()
    a = file.readline().split()
    out[a[0][1:]] = float(a[1])
    a = file.readline()

    while '=' in a:
        a = a.split('=')
        a[0] = a[0][1:-1]
        a[1] = a[1].replace('"', '').replace(',', '.').strip()
        if ':' not in a[1] and '/' not in a[1]:
            a[1] = float(a[1])
        out[a[0]] = a[1]
        a = file.readline()
    maxbin = int(file.readline().split()[-1])


for key in out.keys():
    if '1st' in key.lower():
        first = out[key]
        break
for key in out.keys():
    if 'Bin Size'.lower() in key.lower():
        Bin_Size = out[key]
        break

bins = [first + Bin_Size * x for x in range(maxbin)]


temp = {}
for i in range(maxbin):
    temp['bin' + str(i+1)] = first + Bin_Size * i

temp['maxbin'] = maxbin

for key in out.keys():
    newkey = key.replace('(m)','').replace('(s)','').strip().lower().replace(' ','_')
    if '1st' in newkey:
        newkey = 'firstbinrange'
    temp[newkey] = out[key]
out = temp.copy()
out['median_dypid'] = np.median(metadf['Dep'].astype(float).values)   #median

df = pd.DataFrame.from_dict(out, orient='index', columns=['value'])

df.index.name = 'key'
df.to_csv(path_to_out + 'meta.csv')

