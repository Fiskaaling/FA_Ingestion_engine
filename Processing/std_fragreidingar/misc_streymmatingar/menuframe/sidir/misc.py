import numpy as np

def minmaxvika(df, max_bin, longd = 6*12*7):
    '''
    ein simpul algurytma til at finna miðuna á einum strekkji uppá 2 * longd,
    har tað rekur mest og minst
    defolt longd er basera uppá at 2*longd er 1 vika (har vit hava 10 min ímillum mátingar)

    :param df:      dataði sum skal plottast
    :param max_bin: tann ovasta binnin vit higgja eftir
    :param longd:   Hvussu nógv datapunktir vit higgja í báar ratningarnir
    :return:        (max_v, min_v) har max_v er miðan av hvar tað rekur mest
    '''
    #  TODO skriva hettar betur
    mylist = []
    for mating in range(len(df)):
        mysum = 0
        mycount = 0
        for my_bin in range(max_bin):
            item = df['mag%s' % int(my_bin + 1)][mating]
            if not np.isnan(item):
                mysum += item
                mycount += 1
        if mycount > 0:
            mylist.append(mysum/mycount)
        else:
            mylist.append(np.NaN)

    max_v = np.argmax([np.average(mylist[x:x+longd]) for x in
                      range(100, len(mylist) - longd + 1 - 100)]) + longd
    min_v = np.argmin([np.average(mylist[x:x+longd]) for x in
                      range(100, len(mylist) - longd + 1 - 100)]) + longd
    return max_v, min_v


def myprelabel(i, mal='FO'):
    if i == 0:
        if mal=='EN':
            prelabel = 'a) Surface layer'
        else:
            prelabel = 'a) Ovara lag'
    elif i == 1:
        if mal=='EN':
            prelabel = 'b) Center layer'
        else:
            prelabel = 'b) Miðlag'
    else:
        if mal=='EN':
            prelabel = 'c) Bottom layer'
        else:
            prelabel = 'c) Niðasta lag'
    return prelabel
