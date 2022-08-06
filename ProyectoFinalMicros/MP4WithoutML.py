from tkinter import N
import numpy as np
import numpy
import random
import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FFMpegWriter, FuncAnimation
import time
import serial
import matplotlib.animation as animation
import sklearn.cluster as skl_cluster
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
print(beats, beatsVal)

bb = beats
bVal = beatsVal
beats = [0]
beatsVal = [bVal[-1]]

beats.extend(bb)
beatsVal.extend(bVal)
beats.append(sec)
beatsVal.append(beatsVal[0])

beats = numpy.array(beats)
#beatsVal = numpy.array(beatsVal)

print(beats)
print(beatsVal)





cant = 100
x_plot_vals = np.array(x_vals[:cant])
y_plot_vals = np.array(y_vals[:cant])
it_graph = cant


fig = plt.figure()
ax = plt.axes(xlim=(0, 2),  ylim=(-1.2, 1.2))
line, = ax.plot([], [], lw=3)
#line2, = ax.plot([], [], color = (1,0,0), lw = 2, linestyle='dotted')
def init():
    line.set_data([], [])
    #line2.set_data([], [])
    return line,
def animate(frame_number):
    global x_vals
    global y_vals
    global x_plot_vals
    global y_plot_vals
    global it_graph
    global cant
    global prev
    global beatsVal
    global beats
    
    
    x_plot_vals = np.array(x_vals[:cant])
    y_plot_vals = np.array(y_vals[it_graph-cant:it_graph])
    mini= np.argmin(y_plot_vals)

    nZero = x_vals[it_graph-cant]
    values_to_plot_pp = beats-nZero
    values_to_plot_p2 = beatsVal
    

    mini = y_plot_vals[mini]
    maxi = np.argmax(y_plot_vals)
    maxi = y_plot_vals[maxi]

    y_plot_vals -= mini
    y_plot_vals /= (maxi-mini)
    y_plot_vals *= 2
    y_plot_vals -= 1

    values_to_plot_p2 -= mini
    values_to_plot_p2 /= (maxi-mini)
    values_to_plot_p2 *= 2
    values_to_plot_p2 -= 1

    #print(y_plot_vals)
    #print(x_plot_vals)
    #print(" perro")
    #print(values_to_plot_pp)
    #print(values_to_plot_p2)
    it_graph += 1
    line.set_data(x_plot_vals, y_plot_vals)
    #line2.set_data(values_to_plot_pp, values_to_plot_p2)


    #p = x_plot_vals[0]
    #p2 = x_plot_vals[-1]
    #aa = numpy.searchsorted(beats,p)
    #bb = numpy.searchsorted(beats,p2, side= 'right')
    #print(aa)
    #print(bb)
    #line2.set_data(beats[aa:bb], beatsVal[aa:bb])
    #plt.scatter(beats[aa:bb], beatsVal[aa:bb], color = (1,0,0), zorder = 3)
    return line,
print(it)
lin_ani = FuncAnimation(fig, animate, interval=20,  init_func=init,  frames = it-cant-1, repeat = False, blit=True)




writer = animation.PillowWriter(fps=50)





lin_ani.save('leadIIECG_NoLearningPaciente.gif', writer = writer)
plt.close()
print(it)