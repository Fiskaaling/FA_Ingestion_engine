import pandas as pd
import numpy as np


def Seaguardcut(df):
    '''
    hettar er bara fyrsta utkast skal higgja narri uppá hvussu hettar skal implementerast
    :param df:
    :return: m, M start og enda indexini har Seaguardirin er farin á sjógv
    '''
    l = int(len(df) / 2)
    a = df['Temperature'][0:l].rolling(10, center=True).var().dropna().values
    b = np.max(a) / 2
    m = 0
    for i in range(len(a)):
        if a[i] > b:
            m = i
    a = df['Temperature'][l::].rolling(10, center=True).var().dropna().values
    b = np.max(a) / 2
    M = len(a)
    for i in range(len(a) - 1, -1, -1):
        if a[i] > b:
            M = i
    return m, M + l