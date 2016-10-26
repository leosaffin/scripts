import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, plot


def wind_speed(u, v, w, vmin=0, vmax=70, cmap='BuPu', factor=20):
    wind_speed = (u**2 + v**2 + w**2)**0.5
    plot.pcolormesh(wind_speed[0], vmin=vmin, vmax=vmax, cmap=cmap)

    ny, nx = u.shape[1:]
    plot.overlay_winds(u[0], v[0], int(nx / factor), int(ny / factor))

    plt.title('Wind Speed')

    return


def pv_tracer(cubes, name, vmin=-2, vmax=2, cmap='coolwarm'):
    cube = convert.calc(name, cubes)
    epv = convert.calc('ertel_potential_vorticity', cubes)
    adv = convert.calc('advection_only_pv', cubes)

    plot.pcolormesh(cube, pv=epv, vmin=vmin, vmax=vmax, cmap=cmap)

    adv.data = np.abs(adv.data)
    iplt.contour(adv, [2], colors='k', linestyle='--')

    return
