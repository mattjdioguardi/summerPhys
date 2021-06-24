import numpy as np
from matplotlib import pyplot as plt

x = [0,1,2,0,1,2,0,1,2,0,1,2]
y = [1,1,1,2,2,2,3,3,3,4,4,4]
z = [9,8,7,6,5,4,3,2,1,0,-1,-2]



max = max(z) if max(z) > abs(min(z)) else abs(min(z))


xx, yy = np.meshgrid(np.unique(x), np.unique(y))
zz = np.array(z).reshape(len(np.unique(y)), len(np.unique(x)))


fig1,ax=plt.subplots(1,1)
cx = ax.contourf(xx, yy, zz, levels = 20, cmap = "seismic",vmin = -max,vmax=max)
fig1.colorbar(cx)


plt.show()


