import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation
import time
import serial





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
cant = 100
x_plot_vals = x_vals[:cant]
y_plot_vals = y_vals[:cant]
it_graph = cant
def animate(i):
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
print(it)
aniFunction = FuncAnimation(plt.gcf(), animate, interval=20, frames = it-cant-1, repeat = False)



plt.tight_layout()
#plt.plot(x_vals[10:110], y_vals[10:110])
plt.show()

print(it)