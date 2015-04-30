import numpy as np
import matplotlib.pyplot as plt
from mymodule import io, convert, grid, interpolate, plot


def main(filename, name, theta_value):
    cubes = io.load(filename)
    cubes.remove(cubes.extract('air_pressure')[0])
    x = convert.calc(name, cubes)

    pv = convert.calc('total_pv', cubes)
    theta = convert.calc('air_potential_temperature', cubes)
    thcoord = grid.make_coord(theta)
    pv.add_aux_coord(thcoord, [0, 1, 2])
    x.add_aux_coord(thcoord, [0, 1, 2])

    pv_on_theta = interpolate.to_level(pv, 'air_potential_temperature',
                                       theta_value)
    pv_on_theta = pv[0].copy(data=pv_on_theta)

    x_on_theta = interpolate.to_level(pv, 'air_potential_temperature',
                                      theta_value)
    x_on_theta = x[0].copy(data=x_on_theta)

    io.save(pv_on_theta, '/home/lsaffi/data/' + name + '_on_theta_' +
            str(theta_value) + '.nc')

    levs = np.linspace(-2.1, 2.1, 16)
    plot.level(x_on_theta, pv_on_theta, levs, cmap='cubehelix_r',
               extend='both')
    plt.savefig('/home/lsaffi/plots/' + name + '_on_theta.png')


if __name__ == '__main__':
    filename = '/projects/diamet/lsaffi/xjjhq/*030'
    name = 'advection_inconsistency_pv'
    theta_value = 330
    main(filename, name, theta_value)
