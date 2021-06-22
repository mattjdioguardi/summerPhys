import numpy as np
from matplotlib import pyplot as plt
x = np.array([1,2,3,4,5,6,7,8,9,10])
y = np.array([10,9,8,7,6,5,4,3,2,1]).reshape(-1,1)
h = y * x
print(x)
print(y)
# print (h)
fig,ax=plt.subplots(1,1)
ax.contourf(h)
ax.set_title("test")
plt.show()