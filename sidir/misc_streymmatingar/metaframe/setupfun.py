import os
from tkinter import *

import pandas as pd
import numpy as np



def inset_feltir(meta):
    path = os.path.split(__file__)[0]
    path = os.path.split(path)[0]
    path = os.path.split(path)[0]
    temp = {}
    if 'setup.txt' in os.listdir(path):
        try:
            temp = dict(pd.read_csv(path + '/setup.txt', header=None).values)
        except:
            messagebox.showinfo('fekk ikki inlisi setup.txt')

    for key in temp:
        if key in meta.keys():
            meta[key].delete(0, END)
            if str(temp[key]) != 'nan':
                meta[key].insert(0, temp[key])
        else:
            print(key, 'fail')
