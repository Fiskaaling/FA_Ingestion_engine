import numpy as np

def round(lat1,lon1,lat2,lon2):
    r = 6371000
    a = np.cos(np.deg2rad(lat1))
    b = np.cos(np.deg2rad(lat2))
    return r*np.arccos(a*b*(np.cos(np.deg2rad(lon1-lon2))) + np.sin(np.deg2rad(lat1))*np.sin(np.deg2rad(lat2)))

def flat(lat1,lon1,lat2,lon2):
    '''wrong use round plz'''
    r = 6371000
    c = 0.46947156278589086
    return r*np.sqrt(np.square(np.deg2rad(lat1-lat2))+np.square(np.deg2rad(c*(lon1-lon2))))
