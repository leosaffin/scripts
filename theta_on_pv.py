import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.analysis.cartography as cart
from iris.analysis import Linear
from mymodule import files, convert, grid, interpolate


def main(filename, cscale):
    """
    """
    theta, u, v = load(filename)
    theta_pv2 = interpolate.to_level(theta,
                                     dimensionless_exner_function=[2.])[0]
    u_pv2 = interpolate.to_level(u, dimensionless_exner_function=[2.])[0]
    v_pv2 = interpolate.to_level(v, dimensionless_exner_function=[2.])[0]

    files.save([theta_pv2, u_pv2, v_pv2], '/home/lsaffi/data/iop5/thetapv2.nc')
    plotfig(theta_pv2, u_pv2, v_pv2, cscale)


def load(filename):
    """
    """
    cubelist = files.load(filename)
    cubelist.remove(cubelist.extract('air_pressure')[0])

    theta = convert.calc('air_potential_temperature', cubelist)
    u = convert.calc('x_wind', cubelist)
    v = convert.calc('y_wind', cubelist)
    u.regrid(theta, Linear())
    v.regrid(theta, Linear())

    pv = convert.calc('total_pv', cubelist)
    pv.rename('dimensionless_exner_function')
    coord = grid.make_coord(pv)
    theta.add_aux_coord(coord, [0, 1, 2])
    u.add_aux_coord(coord, [0, 1, 2])
    v.add_aux_coord(coord, [0, 1, 2])

    return theta, u, v


def plotfig(theta, u, v, cscale):
    n = 10
    x, y = cart.get_xy_grids(theta)
    plt.contourf(x, y, theta.data, cscale, cmap='cubehelix_r', extend='both')
    plt.colorbar()
    plt.quiver(x[::n, ::n], y[::n, ::n], u.data[::n, ::n], v.data[::n, ::n])
    plt.savefig('/home/lsaffi/plots/iop5/thetapv2.png')


def replot(cscale):
    cubes = files.load('/home/lsaffi/data/iop5/thetapv2.nc')
    theta = convert.calc('air_potential_temperature', cubes)
    u = convert.calc('x_wind', cubes)
    v = convert.calc('y_wind', cubes)
    plotfig(theta, u, v, cscale)


if __name__ == '__main__':
    filename = '/projects/diamet/lsaffi/xjjhq/*036.pp'
    cscale = np.linspace(270, 350, 17)
    #main(filename, cscale)
    replot(cscale)
