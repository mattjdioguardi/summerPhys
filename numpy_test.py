import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.cbook as cbook
import matplotlib.colors as colors

x = [0,1,2,0,1,2,0,1,2,0,1,2]
y = [1,1,1,2,2,2,3,3,3,4,4,4]
Bz = [1,1,1,1,1,1,1,1,1,1,1,1]
Bx = [12,11,10,9,8,7,6,5,4,3,2,1]




max = max(Bz) if max(Bz) > abs(min(Bz)) else abs(min(Bz))


xx, yy = np.meshgrid(np.unique(x), np.unique(y))
Bzz = np.array(Bz).reshape(len(np.unique(y)), len(np.unique(x)))
Bxx = np.array(Bx).reshape(len(np.unique(y)), len(np.unique(x)))


feature_x = np.arange(0, 50, 2)
feature_y = np.arange(0, 50, 3)

# Creating 2-D grid of features
[X, Y] = np.meshgrid(feature_x, feature_y)

fig, ax = plt.subplots(1, 1)

Z = np.cos(X / 2) + np.sin(Y / 4)


l=plt.contourf(X,Y,Z,100)
contour_axis = plt.gca()
plt.subplots_adjust(bottom=0.25)



axlev = plt.axes([0.25, 0.1, 0.65, 0.03])  #slider location and size
slev = Slider(axlev, 'contour levels',0, 100, 100, valstep = 1)     #slider properties

axmid = plt.axes([0.25, 0.15, 0.65, 0.03])  #slider location and size
smid = Slider(axmid, 'color map center',-100, 100, 0)     #slider properties


def update(val):
    offset = colors.TwoSlopeNorm(vcenter=smid.val)
    contour_axis.clear()
    contour_axis.contourf(X,Y,Z,slev.val,norm=offset,cmap = "seismic")
    plt.draw()
slev.on_changed(update)
smid.on_changed(update)




plt.show()


