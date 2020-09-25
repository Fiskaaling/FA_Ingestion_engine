import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
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


# Set variables for the run
tal = 31  # filenumber
filename = "/home/erna/Fiskaaling/projects/HVS/2020_skurd_fra_bati/Data/Export/" + str(tal)
figFolder = "/home/erna/Fiskaaling/projects/HVS/2020_skurd_fra_bati/figures/"
if tal > 35:
    colormap = 'PuOr'
    minmaxspd = 500  # used as min and max speed and color
    tickjump = 100
else:
    colormap = 'RdBu'
    minmaxspd = 100  # used as min and max speed and color
    tickjump = 25

nav = pd.read_csv(filename + "_nav.txt", skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15],
                  delim_whitespace=True, index_col=0, decimal=",")
# uppskot EO: df = pd.read_csv('{}{}'.format(folder, station), sep = '\t',
#             skiprows = [0,1,2,3,4,5,6,7,8,9,10,11,13,14,15],
#             decimal = ',',
#             usecols = list(range(7))+list(range(9,13)),
#             date_parser = lambda x: datetime.strptime(x, '%y %m %d %H %M %S'),
#             parse_dates={'DT': [1, 2, 3,4,5,6]})
u = pd.read_csv(filename + "_u.txt", skiprows=11, delim_whitespace=True, index_col=0, decimal=",")
v = pd.read_csv(filename + "_v.txt", skiprows=11, delim_whitespace=True, index_col=0, decimal=",")
bt = pd.read_csv(filename + "_bt.txt", skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15],
                 delim_whitespace=True, index_col=0, decimal=",")
print(nav)
etc = pd.read_csv(filename + "_etc.csv", index_col='key').T
print(etc)
skip_first = int(etc.skip_first)
skip_last = int(etc.skip_last)
print(skip_first)
print(skip_last)
print((nav["FLat"].iloc[skip_first], nav["FLon"].iloc[skip_first]))
print((nav["FLat"].iloc[skip_last], nav["FLon"].iloc[skip_last]))
direction = calculate_initial_compass_bearing((nav["FLat"].iloc[skip_first], nav["FLon"].iloc[skip_first]),
                                              (nav["FLat"].iloc[skip_last], nav["FLon"].iloc[skip_last]))
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

levels = np.linspace(-minmaxspd, minmaxspd, 256)
clevels = range(-minmaxspd, minmaxspd + 1, tickjump)
filtur = [1] * 5
z2 = []
for j in range(2, 25):
    for i in range(len(u.iloc[skip_first:])):
        if not np.isnan(v[str(1)].iloc[skip_first + i]):
            # if True:
            x.append(nav["FLat"].iloc[skip_first + i])
            y.append(-j * bin_size - blanking - recorder_waterlevel + bin_size / 2)
            # u.append(u[str(j)].iloc[skip_first + i])
            u_tmp = u[str(j)].iloc[skip_first + i]
            v_tmp = v[str(j)].iloc[skip_first + i]
            c_tmp = np.complex(u_tmp, v_tmp)
            z.append(np.real(c_tmp * np.exp(np.complex(0, 1) * np.deg2rad(direction))))
            z2.append(u_tmp)

# znew = np.append(z[0:len(filtur)-1], znew)

plt.figure(figsize=(14, 7))

resX = 500
resY = 500

meshgridy = np.linspace(min(y), max(y), resY)
meshgridx = np.linspace(min(x), max(x), resX)

meshgridx, meshgridy = [meshgridx, meshgridy]
meshgridx, meshgridy = np.meshgrid(meshgridx, meshgridy)
grid_z0 = griddata((x, y), z, (meshgridx, meshgridy), method='linear')
# plt.contourf(meshgridx, meshgridy, grid_z0, levels=levels, cmap='seismic', extend='both')

plt.contourf(meshgridx, meshgridy, grid_z0, levels=levels, cmap=colormap, extend='both')

# plt.scatter(x, y, c='k', marker=".")

cbar = plt.colorbar(pad=0.02)

# clevels = np.round(np.linspace(-20, 20, 15))*10
cbar.set_ticks(clevels)
cbar.set_ticklabels(clevels)
cbar.set_label('streymferð [mm/s]', labelpad=-1)

# plt.scatter(x,y, c='k', marker=".")
filtur = [1] * 10
botn = np.convolve(bt["BD2"].iloc[skip_first:skip_last] / 100, filtur, mode='valid') / len(filtur)
# plt.plot(nav["FLat"].iloc[skip_first:], -bt["BD2"].iloc[skip_first:]/100, c='g')
plt.plot(nav["FLat"].iloc[skip_first + len(filtur) - 1:skip_last], -botn, c='k')
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

plt.title(
    'HVS S' + str(tal - 30) + ', snarað ' + str(np.round(direction, 2)) + r'$^{\circ}$' + ' klokkan ' + HH + ':' + MM)

saveFilename = figFolder + str(tal) + '_rotated.png'
plt.savefig(saveFilename)
# plt.show()
