import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
from mymodule import files, convert, grid, interpolate, plot


def main(filename, names, theta_value, cscale):
    cubes, tot, adv = load(filename, names)

    # Interpolate two measure of pv to theta level
    tot_theta = interpolate.to_level(tot,
                        air_potential_temperature=[theta_value])[0]
    adv_theta = interpolate.to_level(adv,
                        air_potential_temperature=[theta_value])[0]

    theta_cubelist = iris.cube.CubeList()
    theta_cubelist.append(tot_theta)
    theta_cubelist.append(adv_theta)

    for name, cube in zip(names, cubes):
        # interpolate variable to theta level
        cube_theta = interpolate.to_level(cube,
                        air_potential_temperature=[theta_value])[0]

        # Plot variable
        plot.level(cube_theta, tot_theta, cscale, cmap='bwr', extend='both')
        iplt.contour(adv_theta, [2], colors='k',
                     linewidths='20', linestyles='--')
        plt.savefig('/home/lsaffi/plots/iop5/pv_on_theta/'
                    + str(theta_value) + 'k_' + name + '.png')
        plt.clf()

        # Add to cubelist
        theta_cubelist.append(cube_theta)

    files.save(theta_cubelist, ('/home/lsaffi/data/iop5/pv_on_theta/' +
                                str(theta_value) + 'k.nc'))


def load(filename, names):
    """
    """
    cubelist = files.load(filename)
    cubelist.remove(cubelist.extract('air_pressure')[0])

    # Create a potential temperature auxiliary coord
    theta = convert.calc('air_potential_temperature', cubelist)
    thcoord = grid.make_coord(theta)

    cubes = iris.cube.CubeList()
    for name in names:
        cube = convert.calc(name, cubelist)
        cube.add_aux_coord(thcoord, [0, 1, 2])
        cubes.append(cube)

    adv = convert.calc('advection_only_pv', cubelist)
    adv.add_aux_coord(thcoord, [0, 1, 2])
    tot = convert.calc('total_pv', cubelist)
    tot.add_aux_coord(thcoord, [0, 1, 2])

    return cubes, tot, adv


if __name__ == '__main__':
    filename = '/projects/diamet/lsaffi/xjjhq/*036.pp'
    names = ['residual_pv',
             'short_wave_radiation_pv',
             'long_wave_radiation_pv',
             'microphysics_pv',
             'gravity_wave_drag_pv',
             'convection_pv',
             'boundary_layer_pv',
             'cloud_rebalancing_pv',
             'advection_inconsistency_pv']

    theta_value = 320
    cscale = np.linspace(-2.1, 2.1, 16)
    main(filename, names, theta_value, cscale)
