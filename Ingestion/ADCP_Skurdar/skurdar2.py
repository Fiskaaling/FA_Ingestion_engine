import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
import cmocean
from scipy.interpolate import griddata
def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

tal = 36
filename = "/home/johannus/Documents/Projektir/skur-ar-m-ta-ir-fr-b-ti/Export/" + str(tal)

nav = pd.read_csv(filename + "_nav.txt", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,13,14,15], delim_whitespace=True, index_col=0, decimal=",")
u = pd.read_csv(filename + "_u.txt", skiprows=11, delim_whitespace=True, index_col=0, decimal=",")
v = pd.read_csv(filename + "_v.txt", skiprows=11, delim_whitespace=True, index_col=0, decimal=",")
bt = pd.read_csv(filename + "_bt.txt", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,13,14,15], delim_whitespace=True, index_col=0, decimal=",")
print(nav)
etc = pd.read_csv(filename + "_etc.csv", delimiter=',')
print(etc)
skip_first = 0
skip_last = 0
for row in etc.iterrows():
    print('Row1: ' + str(row[1][0]))
    if row[1][0] == 'skip_first':
        print('???')
        skip_first = row[1][1]
    elif row[1][0] == 'skip_last':
        skip_last = row[1][1]
print(skip_first)
print(skip_last)
print((nav["FLat"].iloc[skip_first], nav["FLon"].iloc[skip_first]))
print((nav["FLat"].iloc[skip_last], nav["FLon"].iloc[skip_last]))
direction = calculate_initial_compass_bearing((nav["FLat"].iloc[skip_first], nav["FLon"].iloc[skip_first]), (nav["FLat"].iloc[skip_last], nav["FLon"].iloc[skip_last]))
if direction > 180:
    direction = np.mod(direction + 180, 360)
print('Direction of travel:' + str(direction))
x = []
y = []
z = []
xlast = []
ylast = []
zlast = []

if tal > 35:
    bin_size = 4
    blanking = 2
else:
    bin_size = 2
    blanking = 1
recorder_waterlevel = 0.5
levels = np.linspace(-100, 100, 256)
clevels = range(-100, 100, 25)
filtur = [1] * 5
for j in range(2, 25):
    for i in range(len(u.iloc[skip_first:])):
        if not np.isnan(v[str(1)].iloc[skip_first + i]):
        #if True:
            x.append(nav["FLat"].iloc[skip_first + i])
            y.append(-j * bin_size - blanking - recorder_waterlevel + bin_size/2)
            #u.append(u[str(j)].iloc[skip_first + i])
            u_tmp = u[str(j)].iloc[skip_first + i]
            v_tmp = v[str(j)].iloc[skip_first + i]
            c_tmp = np.complex(u_tmp, v_tmp)
            z.append(np.imag(c_tmp * np.exp(np.complex(0,1)*np.deg2rad(direction+90))))


#znew = np.append(z[0:len(filtur)-1], znew)

plt.figure(figsize=(14,7))


resX = 500
resY = 500

meshgridy = np.linspace(min(y), max(y), resY)
meshgridx = np.linspace(min(x), max(x), resX)

meshgridx, meshgridy = [meshgridx, meshgridy]
meshgridx, meshgridy = np.meshgrid(meshgridx, meshgridy)
grid_z0 = griddata((x, y), z, (meshgridx, meshgridy), method='linear')
plt.contourf(meshgridx, meshgridy, -grid_z0, levels=levels, cmap='seismic', extend='both')


#plt.scatter(x, y, c='k', marker=".")

cbar = plt.colorbar()

#clevels = np.round(np.linspace(-20, 20, 15))*10
cbar.set_ticks(clevels)
cbar.set_ticklabels(clevels)

#plt.scatter(x,y, c='k', marker=".")
filtur = [1] * 10
botn = np.convolve(bt["BD2"].iloc[skip_first:skip_last]/100, filtur, mode='valid')/len(filtur)
#plt.plot(nav["FLat"].iloc[skip_first:], -bt["BD2"].iloc[skip_first:]/100, c='g')
plt.plot(nav["FLat"].iloc[skip_first+len(filtur) - 1:skip_last], -botn, c='k')
plt.axhline(y=0, c='k')
plt.ticklabel_format(useOffset=False)

HH = str(nav['HH'].iloc[skip_first])
if len(HH) <= 1:
    HH = '0' + HH
MM = str(nav['MM'].iloc[skip_first])
print(MM)
print(len(MM))
if len(MM) <= 1:
    MM = '0' + MM
print(MM)

plt.title('Hvannasund S, S' + str(tal-30) + ', Rotera ' + str(np.round(direction, 2)) + '$^{\circ}$' + ', Klokkan: ' + HH + ':' + MM)

saveFilename = filename.split('/E')[0] + "/figs/" + str(tal) + '_rotated.png'
plt.savefig(saveFilename)
plt.show()
