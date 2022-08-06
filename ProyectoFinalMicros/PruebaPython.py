import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation
import time
import serial


# plt.style.use('fivethirtyeight')

# x_vals = []
# y_vals = []

# index = count()
# it = 0
# ser = serial.Serial("COM8", 9600,timeout=0)
# adc_max = 	8388608
# vref = 2.4
# time.sleep(3)
# def animate(i):
#     global x_vals
#     global y_vals
#     global it
#     global ser
#     global adc_max
#     xs = bytearray()
#     ser.write(b'x\01')
#     s1 = ser.read()
#     xs.append(int.from_bytes(s1, 'big', signed=False))
#     ser.write(b'x\01')
#     s1 = ser.read()
#     xs.append(int.from_bytes(s1, 'big', signed=False))
#     ser.write(b'x\01')
#     s1 = ser.read()
#     xs.append(int.from_bytes(s1, 'big', signed=False))
#     y = bytes(xs)
#     print(y)
#     y = int.from_bytes(y, 'big', signed=True)
    
#     y/= adc_max
#     y-= .5
#     y *= 2*2.4/3.5
#     it+= .200
#     x_vals.append(it)
#     y_vals.append(y)
    

#     x_vals = x_vals[-60:]
#     y_vals = y_vals[-60:]
    

#     plt.cla()
#     plt.plot(x_vals, y_vals)

# aniFunction = FuncAnimation(plt.gcf(), animate, interval=200, frames = 100, repeat = False)

# plt.tight_layout()
# plt.show()


x_vals = []
y_vals = []
ser = serial.Serial("COM8", 9600)
adc_max = 	8388608
vref = 2.4
it = 0
time.sleep(3)
freq =  60
per = 1/freq
sec = 11
for i in range(freq*sec):
    time.sleep(per)
    xs = bytearray()
    ser.write(b'x\01')
    s2 = ser.read()
    #print(s2)
    ser.write(b'x\01')
    s44 = ser.read()
    #print(s44)
    ser.write(b'x\01')
    s3 = ser.read()
    #print(s3)
    ser.write(b'x\01')
    s1 = ser.read()
    #print(s1)
    xs.append(int.from_bytes(s1, 'big', signed=False))
    ser.write(b'x\01')
    s1 = ser.read()
    #print(s1)
    xs.append(int.from_bytes(s1, 'big', signed=False))
    ser.write(b'x\01')
    s1 = ser.read()
    #print(s1)
    xs.append(int.from_bytes(s1, 'big', signed=False))
    ser.write(b'x\01')
    y = bytes(xs)
    #print(y)    
    y = int.from_bytes(y, 'big', signed=False)
    #print(y)
    y/= 6116.69333333 
    #print(y)
    y-=  685.71
    #print(y)
    it+= per
    x_vals.append(it)
    y_vals.append(y)
    if(s3 != b'\x00'):
        print(s1)
        print(s44)
        print(s3)
        print(y)


plt.tight_layout()
plt.plot(x_vals[10:(freq)*3 + 10], y_vals[10:(freq)*3 + 10])
plt.show()
plt.style.use('fivethirtyeight')