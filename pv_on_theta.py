import numpy as np
import matplotlib.pyplot as plt
from mymodule import files, convert, grid, interpolate, plot


def main(filename, name, theta_value):
    cubes = files.load(filename)
    cubes.remove(cubes.extract('air_pressure')[0])
    x = convert.calc(name, cubes)

    pv = convert.calc('advection_only_pv', cubes)
    theta = convert.calc('air_potential_temperature', cubes)
    thcoord = grid.make_coord(theta)
    pv.add_aux_coord(thcoord, [0, 1, 2])
    x.add_aux_coord(thcoord, [0, 1, 2])

    pv_on_theta = interpolate.to_level(pv,
                                       air_potential_temperature=[theta_value])

    x_on_theta = interpolate.to_level(x,
                                      air_potential_temperature=[theta_value])

    files.save([pv_on_theta, x_on_theta],
               ('/home/lsaffi/data/' + name + '_on_theta_' +
                str(theta_value) + '.nc'))

    levs = np.linspace(-2.1, 2.1, 16)
    plot.level(x_on_theta[0], pv_on_theta[0], levs, cmap='bwr', extend='both')
    plt.savefig('/home/lsaffi/plots/' + name + '_on_theta.png')


if __name__ == '__main__':
    filename = '/projects/diamet/lsaffi/xjjhq/*036.pp'
    name = 'final_residual_pv'
    theta_value = 320
    main(filename, name, theta_value)
