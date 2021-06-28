import tkinter as tk
import u6
from functools import partial
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np

# #############################u6 setup##########################################
d = u6.U6()
d.getCalibrationData()
print("Configuring U6 stream")
d.streamConfig(NumChannels=3, ChannelNumbers=[0, 1, 2], ChannelOptions=[0, 0, 0],
                SettlingFactor=1, ResolutionIndex=1, ScanFrequency=10000)



data = [[],[],[]]

def scan():
    DESIRED_SAMPLES = 3000
    samples_collected = 0
    packets_collected = 0
    Bfield = [0, 0, 0]
    d.streamStart()
    while(samples_collected < 3*DESIRED_SAMPLES):
        Bcur = next(d.streamData())
        Bfield[0] += sum(Bcur["AIN0"])/len(Bcur["AIN0"])
        Bfield[1] += sum(Bcur["AIN1"])/len(Bcur["AIN1"])
        Bfield[2] += sum(Bcur["AIN2"])/len(Bcur["AIN2"])
        samples_collected += len(Bcur["AIN0"]) + len(Bcur["AIN1"])+ len(Bcur["AIN2"])
        packets_collected += 1
    for i in range(3):
        Bfield[i] /= packets_collected
        data[i].append(Bfield[i])
    d.streamStop()

def plot_scan():
    fig1,ax=plt.subplots(1,1)
    fig2,ay=plt.subplots(1,1)
    fig3,az=plt.subplots(1,1)

    ax.plot(data[0])
    ay.plot(data[1])
    az.plot(data[2])

    plt.show()



win = tk.Tk()
win.title("3D Mapper")
win.geometry("2000x500")


tk.Button(win, text="scan point",command=scan).grid(column=1, row=1)
tk.Button(win, text="plot scan",command=plot_scan).grid(column=1, row=2)
#tk.Button(win, text="save scan",command=save_scan).grid(column=1, row=3)

win.mainloop()