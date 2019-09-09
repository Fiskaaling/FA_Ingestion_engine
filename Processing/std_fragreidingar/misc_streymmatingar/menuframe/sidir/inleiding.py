import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def testgraph(datadf, max_bin, dypir):
    print(max_bin)
    print(datadf.keys())
    print(dypir, len(dypir))
    dypir = [dypir[x] for x in range(max_bin)]
    stod = [25, 50, 75, 95, 99.5]
    bars = [[] for _ in stod]
    for i in range(1, max_bin + 1):
        temp = [x for x in datadf['mag' + str(i)].values if not np.isnan(x)]
        temp = np.sort(temp)
        l = len(temp)
        for j, brok in enumerate(stod):
            if brok > 100:
                raise ValueError('brok er ov stort')
            elif brok == 100:
                bars[j].append(temp[-1])
            elif brok<=0:
                raise ValueError('brok er ov litið')
            else:
                bars[j].append(temp[int(brok*l/100)])

    print(bars)
    index = np.arange(max_bin)
    plots = []
    plots.append(plt.bar(index, bars[0], 0.5, label=str(stod[0])+'%'))
    for i in range(1, len(stod)):
        plots.append(plt.bar(index, [x - y for x, y in zip(bars[i], bars[i-1])],
                                     .5, bottom=bars[i-1], label=str(stod[i])+'%'))
    plt.xticks(index, [int(-x) for x in dypir])
    plt.ylabel('Streymferð [mm/s]')
    plt.xlabel('Dýpið [m]')
    temp = bars[-1]
    temp = np.sort(temp)
    M = min(2 * temp[int(.5*len(temp))], temp[-1])
    plt.ylim(0, M)
    plt.legend(ncol=int(np.ceil(len(stod)/2)))
    plt.show()
