import numpy as np
import matplotlib.pyplot as plt

Ri = np.linspace(0, 0.25, 26)

f_long = 1 / (1 + 10 * Ri)

f_sharp = (1 - 5 * Ri)**2
f_sharp[11:] = (1 / (20 * Ri[11:]))**2

print Ri[11]

plt.plot(Ri, f_long, '-g', label='Land')
plt.plot(Ri, f_sharp, '-b', label='Sea')
plt.xlabel('Ri')
plt.ylabel(r'$f(\mathrm{Ri})$')
plt.legend(loc='best')

plt.show()
