import numpy as np

def round(lat1,lon1,lat2,lon2):
    r = 6371000
    a = np.cos(np.deg2rad(lat1))
    b = np.cos(np.deg2rad(lat2))
    return r*np.arccos(a*b*(np.cos(np.deg2rad(lon1-lon2))) + np.sin(np.deg2rad(lat1))*np.sin(np.deg2rad(lat2)))

a=[62.2666563333333,62.2712193333333,62.2707601666667,62.2661471666667,62.2666563333333]
b=[6.71907616666667,6.72514866666667,6.7267795,6.72081416666667,6.71907616666667]

for i in range(len(a)-1):
    print(round(a[i], b[i], a[i+1], b[i+1]))