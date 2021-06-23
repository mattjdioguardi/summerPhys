import numpy as np
from matplotlib import pyplot as plt
x = np.array([1,1,1,1,2,2,2,2,3,3,3,3])
y = np.array([1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12])
print(np.unique(x))
print(np.unique(y))
xx, yy = np.meshgrid(np.unique(x),np.unique(y))
print(xx)
print(yy)




# h = y * x
# print(x)
# print(y)
# # print (h)
# fig,ax=plt.subplots(1,1)
# ax.contourf(h)
# ax.set_title("test")
# plt.show()