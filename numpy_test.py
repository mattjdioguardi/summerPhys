import numpy as np
from matplotlib import pyplot as plt
x = np.arange(-5, 5, 1)

y = np.arange(-5, 5, 1)

xx, yy = np.meshgrid(x, y)

z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)

print(xx)
print(yy)


h = plt.contourf(x,y,z)

plt.show()


