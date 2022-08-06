import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation
import time
import serial

import matplotlib
import numpy
import os
import pandas
import sklearn.linear_model as skl_linear
import sklearn.cluster as skl_cluster
import wfdb

#from biosppy.signals import ecg
from matplotlib import pyplot as plt
from scipy.fft import fft, ifft





x_vals = []
y_vals = []
ser = serial.Serial("COM8", 9600)
it = 0
start = time.time()
sec = 11
while(time.time() < start + sec):

    y = ser.readline()
    x = time.time() - start
    
    it+= 1
    x_vals.append(x)
    y_vals.append(y)
plt.style.use('fivethirtyeight')
freq = len(x_vals)/sec
#print(y)
for i,y in enumerate(y_vals):
    y = y.replace(b'\n', b'')
    #print(y)   
    y = int.from_bytes(y, 'big', signed=False)
    
    y/= 6116.69333333 
    y-=  685.71
    if(y < -600):
        if(i == 0):
            y_vals[i] = 0
            continue
        y_vals[i] = y_vals[i-1]
        continue
    y_vals[i] = y
    #print(y)

kek = dict()
for i in range(len(x_vals)):
    kek[x_vals[i]] = y_vals[i]

y_vals_copy = y_vals
x_vals_copy = x_vals
print(len(y_vals))
#print(y_vals)
y_fourier = fft(y_vals_copy)
y_fourier[:int(sec*5)] = 0
y_fourier[int(sec*-5):] = 0
plt.plot(y_fourier)
plt.plot()
leadIIExample = ifft(y_fourier).real


leadIITuple = []
startTrim = 50
for i,x in zip(x_vals_copy[startTrim:], leadIIExample[startTrim:]):
    leadIITuple.append((x,i))
leadIITuple.sort()
leadIITuple = leadIITuple[::-1]

valid = set()

leadIIMaxPoints = []
for (val, itt) in leadIITuple:
    if(itt in valid):
        continue
    for (val2, itt2) in leadIITuple:
        if(itt - .05 < itt2 and itt + .05 > itt2):
            valid.add(itt2)
    leadIIMaxPoints.append((itt, val))
leadIIMaxPoints.sort()
leadIIMaxPoints = numpy.array(leadIIMaxPoints)

plt.scatter(leadIIMaxPoints[:,0], leadIIMaxPoints[:,1])
plt.show()



#print(leadIIMaxPoints[:,1])
YPred = numpy.zeros(leadIIMaxPoints[:,0].size)
leadIINewSpace = leadIIMaxPoints[:,1]- YPred.reshape((-1))

hierechyCluster = skl_cluster.AgglomerativeClustering(n_clusters = 2, linkage='ward')
fittedClusters = hierechyCluster.fit(leadIINewSpace.reshape((-1,1)))
cc = [(1,0,0), (0,1,0)]
ax = plt.subplot()
cc2 = [cc[x] for x in fittedClusters.labels_]
ax.scatter(leadIINewSpace, numpy.zeros(leadIINewSpace.shape), color = cc2)
plt.show()

maxPoint = numpy.argmax(leadIIMaxPoints[:,1])
if(fittedClusters.labels_[maxPoint] == 0):
    fittedClusters.labels_ += 1
    fittedClusters.labels_ %= 2

pit_des = int(.21*freq)
leadIIMaxPointsPrueba = leadIIMaxPoints[pit_des:]
lTemp = len(leadIIMaxPointsPrueba)
aaaa = list(leadIIMaxPointsPrueba)
aaaa.extend(leadIIMaxPoints[:pit_des])
leadIIMaxPointsPrueba = np.array(aaaa)


beats = leadIIMaxPoints[fittedClusters.labels_ == 1,0]
beatsVal = [kek[x] for x in beats]


cant = 100
x_plot_vals = x_vals[:cant]
y_plot_vals = y_vals[:cant]
it_graph = cant
print(beats)
print(beatsVal)
def animate(i):
    global beats
    global beatsVal
    global x_vals
    global y_vals
    global x_plot_vals
    global y_plot_vals
    global it_graph
    global cant
    
    x_plot_vals.append(x_vals[it_graph])
    y_plot_vals.append(y_vals[it_graph])
    x_plot_vals = x_plot_vals[-1*cant:]
    y_plot_vals = y_plot_vals[-1*cant:]
    it_graph += 1
    plt.cla()
    plt.plot(x_plot_vals, y_plot_vals)
    p = x_plot_vals[0]
    p2 = x_plot_vals[-1]
    aa = numpy.searchsorted(beats,p)
    bb = numpy.searchsorted(beats,p2, side= 'right')
    #print(aa)
    #print(bb)
    plt.scatter(beats[aa:bb], beatsVal[aa:bb], color = (1,0,0), zorder = 3)
    print(aa,bb)


print(it)
aniFunction = FuncAnimation(plt.gcf(), animate, interval=20, frames = it-cant-1, repeat = False)



plt.tight_layout()
#plt.plot(x_vals[10:110], y_vals[10:110])
plt.show()

print(it)