import pandas as pd
import numpy as np

path_to_out = '../csv/navn/'

inddf = pd.read_csv(path_to_out + 'magdirdata.csv')
metadf = pd.read_csv(path_to_out + 'meta.csv', index_col='key')['value']

greinsa_un = 5

out = {'dateTime': inddf.dateTime.values}
inddf.drop(['dateTime'], axis=1, inplace=True)

d = inddf['d'].values
d_greinsa = float(metadf['median_dypid']) - 5

komin_a_botn = False
tikin_upp = False

for i in range(1, int(metadf.maxbin) + 1):
    komin_oman = False
    komin_upp = False
    upp_cnt = 0
    down_cnt = 0
    temp = []
    data = inddf['mag' + str(i)].values
    inddf.drop(['mag' + str(i), 'dir' + str(i), 'w' + str(i)], axis=1, inplace=True)
    for j in range(len(data)):
        if np.isnan(data[j]):
            temp.append(9)
            if komin_oman and not komin_upp and upp_cnt > greinsa_un:
                komin_upp = j
            upp_cnt += 1
        elif d[j] < d_greinsa:
            down_cnt = 0
            temp.append(3)
            if komin_oman and not komin_upp:
                if upp_cnt < greinsa_un:
                    upp_cnt += 1
                else:
                    komin_upp = j
        else:
            upp_cnt = 0
            if komin_oman:
                temp.append(2)
            else:
                temp.append(3)
                down_cnt += 1
                if down_cnt > greinsa_un:
                    komin_oman = j
    if not komin_a_botn:
        komin_a_botn = komin_oman
    if not tikin_upp:
        tikin_upp = komin_upp - 2 * greinsa_un

    for j in range(tikin_upp, len(data)):
        temp[j] = max(temp[j], 3)
    out[str(i)] = np.array(temp)

for key in inddf.keys():
    temp = []
    data = inddf[key].values
    for j in range(len(data)):
        if komin_a_botn < j < tikin_upp:
            temp.append(2)
        else:
            temp.append(3)
    out[key] = np.array(temp)


outdf = pd.DataFrame.from_dict(out)

outdf.to_csv(path_to_out + 'quali.csv', sep=',', na_rep='NaN', index=False, encoding='utf-8', float_format='%6.3f')

