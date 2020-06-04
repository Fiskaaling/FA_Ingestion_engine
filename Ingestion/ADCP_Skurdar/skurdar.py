import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

tal = 30

filename = "/home/johannus/Documents/Projektir/skur-ar-m-ta-ir-fr-b-ti/Export/" + str(tal)

nav = pd.read_csv(filename + "_nav.txt", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,13,14,15], delim_whitespace=True, index_col=0, decimal=",")
u = pd.read_csv(filename + "_u.txt", skiprows=11, delim_whitespace=True, index_col=0, decimal=",")
v = pd.read_csv(filename + "_v.txt", skiprows=11, delim_whitespace=True, index_col=0, decimal=",")
bt = pd.read_csv(filename + "_bt.txt", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,13,14,15], delim_whitespace=True, index_col=0, decimal=",")
print(len(nav))
print(len(u))
print(len(v))
print(len(bt))


print(u)
print(nav)
skip_first = 0

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
filtur = [1] * 5

for i in range(len(u.iloc[skip_first:])):
    if not np.isnan(v[str(1)].iloc[skip_first + i]):
        x.append(nav["FLat"].iloc[skip_first + i])
        y.append(-1 * bin_size - blanking - recorder_waterlevel + bin_size/2)
        z.append(v[str(1)].iloc[skip_first + i])
print(len(z))
znew = np.convolve(z, filtur, mode='valid')/len(filtur)
#znew = np.append(z[0:len(filtur)-1], znew)
print(len(znew))
print(len(x))
z = znew
y = y[len(filtur) - 1:]
x = x[len(filtur) - 1:]
plt.figure(figsize=(14,7))
for j in range(2, 25):
    print(j)
    xlast = x.copy()
    ylast = y.copy()
    zlast = z.copy()
    x = []
    y = []
    z = []
    for i in range(len(u.iloc[skip_first:])):
        if not np.isnan(v[str(j)].iloc[skip_first + i]):
            x.append(nav["FLat"].iloc[skip_first + i])
            y.append(-j*bin_size-blanking - recorder_waterlevel + bin_size/2)
            z.append(v[str(j)].iloc[skip_first + i])
    try:
        znew = np.convolve(z, filtur, mode='valid')/len(filtur)
        #znew = np.append(z[0:len(filtur) - 1], znew)
        z = znew
        y = y[len(filtur) - 1:]
        x = x[len(filtur) - 1:]
        plt.tricontourf(x+xlast, y+ylast, np.append(z,zlast), cmap='seismic', levels=levels, extend='both')
        #plt.scatter(x, y, c='k', marker=".")
    except Exception as e:
        print(e)
plt.colorbar()
#plt.scatter(x,y, c='k', marker=".")
filtur = [1] * 10
botn = np.convolve(bt["BD2"].iloc[skip_first:]/100, filtur, mode='valid')/len(filtur)
#plt.plot(nav["FLat"].iloc[skip_first:], -bt["BD2"].iloc[skip_first:]/100, c='g')
plt.plot(nav["FLat"].iloc[skip_first+len(filtur) - 1:], -botn, c='k')
plt.axhline(y=0, c='k')

saveFilename = filename.split('/E')[0] + "/figs/" + str(tal) + '.png'
plt.savefig(saveFilename)

exit()



















for i in range(len(u.iloc[skip_first:])):
    for j in range(25):
        if not np.isnan(v[str(j+1)].iloc[skip_first + i]):
            x.append(nav["FLat"].iloc[skip_first + i])
            y.append(-j*bin_size-blanking)
            z.append(v[str(j+1)].iloc[skip_first + i])

print(z)

ax = plt.axes()
# Setting the background color
ax.set_facecolor("lightgrey")

plt.tricontourf(x, y, z, cmap='seismic', levels=levels, extend='both')
plt.colorbar()
#plt.scatter(x,y, c='k', marker=".")

plt.axhline(y=0, c='k')

#
plt.show()