import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#  TODO skriva hettar uppá ein fornuftigan máta
def met(u, v , phi):
    '''
    eitt met yvir hvuus kraftigur rattningurin er har u og v eru bara í ovarau hálvplan

    :param u:       streymur í u ratningin
    :param v:       streymur í v ratningin
    :param phi:     ein vinkur í gradum
    '''
    N = np.cos(np.deg2rad(phi))
    E = np.sin(np.deg2rad(phi))
    return sum([abs(N*myv + E*myu) for (myu, myv) in zip(u, v)])

def hovusratningur(uvdatadf, max_bin):
    '''
    okkurt sum kann minna um ein høvus ratning hettar skal sikkurt broytast

    :param uvdatadf:    ein pandas dataframe við dataðinum um uv dataði
    :param max_bin:     hvat er nr á tíð stóstu bin
    :høvusratning:      eitt gradutal sum sigur hvat høvus ratningurin er
    '''
    u = uvdatadf[['u'+str(i) for i in range(1, max_bin+1)]].values
    v = uvdatadf[['v'+str(i) for i in range(1, max_bin+1)]].values
    #  sortera nan vekk
    temp = []
    for row in u:
        mysum = 0
        count = 0
        for x in row:
            if not np.isnan(x):
                mysum += x
                count += 1
        if count > 0:
            temp.append(mysum/count)
    u = temp
    temp = []
    for row in v:
        mysum = 0
        count = 0
        for x in row:
            if not np.isnan(x):
                mysum += x
                count += 1
        if count > 0:
            temp.append(mysum/count)
    v = temp

    # skriva hettar ordiligt
    theta = np.arange(180)
    values = [met(u, v, phi) for phi in theta]

    out = theta[np.argmax(values)]

    if out > 90:
        out +=180
    return out


#def old_hovusratningur(uvdatadf, max_bin):
#    '''
#    okkurt sum kann minna um ein høvus ratning hettar skal sikkurt broytast
#
#    :param uvdatadf:    ein pandas dataframe við dataðinum um uv dataði
#    :param max_bin:     hvat er nr á tíð stóstu bin
#    :høvusratning:      eitt gradutal sum sigur hvat høvus ratningurin er
#    '''
#    u = uvdatadf[['u'+str(i) for i in range(1, max_bin+1)]].values
#    v = uvdatadf[['v'+str(i) for i in range(1, max_bin+1)]].values
#    temp = []
#    for row in u:
#        mysum = 0
#        count = 0
#        for x in row:
#            if not np.isnan(x):
#                mysum += x
#                count += 1
#        if count > 0:
#            temp.append(mysum/count)
#    u = temp
#    temp = []
#    for row in v:
#        mysum = 0
#        count = 0
#        for x in row:
#            if not np.isnan(x):
#                mysum += x
#                count += 1
#        if count > 0:
#            temp.append(count)
#    v = temp
#
#    # skriva hettar ordiligt
#    theta = [0, 60, 120]
#    temp = []
#    for phi in theta:
#        temp.append(met(u, v, phi))
#
#    minsti = np.argmin(temp)
#    vinklar = [theta[(minsti + 1) % 3], theta[(minsti - 1) % 3]]
#    values = [met(u, v, phi) for phi in vinklar]
#    #  bara ein greedy algurytma til at finna min
#    for i in range(10):
#        minsti = np.argmin(values)
#        vinklar[minsti] = (vinklar[0] + ((vinklar[1] - vinklar[0]) % 180)/2) % 180
#        values[minsti] = met(u, v, vinklar[minsti])
#    out = vinklar[0]
#    if out > 90:
#        out +=180
#    return out
