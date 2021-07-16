import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.cbook as cbook
import matplotlib.colors as colors
import pandas as pd
import numpy as np
import time
from datetime import datetime


def TD_plot(X,Y,Z,title):
    """given two coordinate matricies X and Y, intensity data for every point Z
    and a title, a contour plot with adjustable color gradient and number of
    contour levels will be produced"""
    fig1,ax=plt.subplots(1,1)

    fig1.suptitle(title)
    contour_axis = fig1.gca()
    ax = contour_axis.contourf(X, Y, Z,100,cmap = "seismic")
    cb = fig1.colorbar(ax)
    fig1.subplots_adjust(bottom=0.25)

    axlev = plt.axes([0.25, 0.1, 0.65, 0.03])  #slider location and size
    slev = Slider(axlev, 'contour levels',0, 100, 100, valstep = 1)     #slider properties
    axmid = plt.axes([0.25, 0.15, 0.65, 0.03])  #slider location and size
    smid = Slider(axmid, 'color map center',np.amin(Z),np.amax(Z), 0)     #slider properties
    def update(x):
        offset = colors.TwoSlopeNorm(vcenter=smid.val)
        contour_axis.clear()
        ax = contour_axis.contourf(X,Y,Z,slev.val,norm=offset,cmap = "seismic")
        cb.update_normal(ax)
        plt.draw()

    slev.on_changed(update)
    smid.on_changed(update)

    return slev, smid

def plot_Bfield(data):
    """take data in the form [[z coordonates], [y coordonates], [Bx], [By], [Bz]]
    and plots the field intensity for all three axises over the change in x and
    in z"""

    fig, (xBxBy,xBz) = plt.subplots(nrows=1, ncols=2, sharex=True,figsize=(12, 6))

    xBxBy.plot(data[0],data[2], color='tab:blue')
    xBxBy.plot(data[0],data[4],  color='tab:orange')
    xBz.plot(data[0],data[6],  color='tab:red')

    xBxBy.set_xlabel('mm displacement z')
    xBxBy.set_ylabel('B field (Gauss)')
    xBxBy.legend(('x direction','y direction'))

    xBz.set_xlabel('mm displacement z')
    xBz.set_ylabel('B field (Gauss)')
    xBz.legend(('z direction'))

    fig.tight_layout(pad=3.0)

    fig2, (yBxBy,yBz) = plt.subplots(nrows=1, ncols=2, sharex=True,figsize=(12, 6))

    yBxBy.plot(data[1],data[2], color='tab:blue')
    yBxBy.plot(data[1],data[4],  color='tab:orange')
    yBz.plot(data[1],data[6],  color='tab:red')

    yBxBy.set_xlabel('mm displacement y')
    yBxBy.set_ylabel('B field (Gauss)')
    yBxBy.legend(('x direction','y direction'))

    yBz.set_xlabel('mm displacement y')
    yBz.set_ylabel('B field (Gauss)')
    yBz.legend(('z direction'))

    fig.tight_layout(pad=3.0)

    plt.savefig('Bfield.png')

    plt.show()

def saveData(data,save_dir):
    """saves passed data in the form
    [[z coordonates], [y coordonates], [Bx], [By], [Bz]] to a spreadsheet that
    is timestamped"""
    now = datetime.now()
    dateString = now.strftime("%d-%m-%Y %H:%M:%S")

    df = pd.DataFrame({'z':data[0], 'y': data[1], 'Bx':data[2], "Bx std":data[3],
                       'By':data[4],"By std":data[5],'Bz':data[6],"Bz std":data[7],})
    writer = pd.ExcelWriter(save_dir + "Bfield_at_"+dateString+ '.xlsx')
    df.to_excel(writer,index=False)
    writer.save()
