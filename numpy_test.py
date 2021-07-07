import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.cbook as cbook
import matplotlib.colors as colors
import tkinter as tk
import pandas as pd
x = [-1,0,1,-1,0,1,-1,0,1,-1,0,1]
y = [-1,-1,-1,-2,-2,-2,-3,-3,-3,-4,-4,-4]
Bz = [1,1,1,1,1,1,1,1,1,1,1,1]
Bx = [12,11,10,9,8,7,6,5,4,3,2,1]




max = max(Bz) if max(Bz) > abs(min(Bz)) else abs(min(Bz))


xx, yy = np.meshgrid(pd.unique(x), pd.unique(y))

print(pd.unique(x))
print(pd.unique(y))
print(xx)
print(yy)

Bzz = np.array(Bz).reshape(len(pd.unique(y)), len(pd.unique(x)))
Bxx = np.array(Bx).reshape(len(pd.unique(y)), len(pd.unique(x)))
print(Bxx)

feature_x = np.arange(0, 50, 2)
feature_y = np.arange(0, 50, 3)

# Creating 2-D grid of features
[X, Y] = np.meshgrid(feature_x, feature_y)

Z = np.cos(X / 2) + np.sin(Y / 4)

#
# l=plt.contourf(X,Y,Z,100)
# contour_axis = plt.gca()
# plt.subplots_adjust(bottom=0.25)
# xcb = fig.colorbar(l)
#
#
# axlev = plt.axes([0.25, 0.1, 0.65, 0.03])  #slider location and size
# slev = Slider(axlev, 'contour levels',0, 100, 100, valstep = 1)     #slider properties
# axmid = plt.axes([0.25, 0.15, 0.65, 0.03])  #slider location and size
# smid = Slider(axmid, 'color map center',-100, 100, 0)     #slider properties
#
#
# def update(val):
#     offset = colors.TwoSlopeNorm(vcenter=smid.val)
#     contour_axis.clear()
#     ax = contour_axis.contourf(X,Y,Z,slev.val,norm=offset,cmap = "seismic")
#     xcb.update_normal(ax)
#     plt.draw()
# slev.on_changed(update)
# smid.on_changed(update)
#
#
#)


def TD_plot(X,Y,Z,title):
    fig1,ax=plt.subplots(1,1)

    fig1.suptitle(title)
    contour_axis = fig1.gca()
    ax = plt.contourf(X, Y, Z,100,cmap = "seismic")
    cb = fig1.colorbar(ax)
    fig1.subplots_adjust(bottom=0.25)

    axlev = plt.axes([0.25, 0.1, 0.65, 0.03])  #slider location and size
    slev = Slider(axlev, 'contour levels',0, 100, 100, valstep = 1)     #slider properties
    axmid = plt.axes([0.25, 0.15, 0.65, 0.03])  #slider location and size
    smid = Slider(axmid, 'color map center',np.amin(Z), np.amax(Z), 0)     #slider properties
    def update(x):
        offset = colors.TwoSlopeNorm(vcenter=smid.val)
        contour_axis.clear()
        ax = contour_axis.contourf(X,Y,Z,slev.val,norm=offset,cmap = "seismic")
        cb.update_normal(ax)
        plt.draw()

    slev.on_changed(update)
    smid.on_changed(update)

    return slev, smid

levels1, center1 = TD_plot(xx,yy,Bxx,"testw")
#levels2, center2 = TD_plot(X,Y,Z,"test")
#levels3, center3 = TD_plot(X,X,Z,"test")
#
#
figt,ac=plt.subplots(1,1)
ac.streamplot(xx,yy,Bxx,Bzz)

plt.show()
print("testing testin")



