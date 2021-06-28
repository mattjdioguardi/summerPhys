import numpy as np
from matplotlib import pyplot as plt

x = [0,1,2,0,1,2,0,1,2,0,1,2]
y = [1,1,1,2,2,2,3,3,3,4,4,4]
Bz = [1,1,1,1,1,1,1,1,1,1,1,1]
Bx = [12,11,10,9,8,7,6,5,4,3,2,1]




max = max(Bz) if max(Bz) > abs(min(Bz)) else abs(min(Bz))


xx, yy = np.meshgrid(np.unique(x), np.unique(y))
Bzz = np.array(Bz).reshape(len(np.unique(y)), len(np.unique(x)))
Bxx = np.array(Bx).reshape(len(np.unique(y)), len(np.unique(x)))



fig1,ax=plt.subplots(1,1)
cx = ax.plot(x)



plt.show()


