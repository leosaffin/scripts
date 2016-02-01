import numpy as np
import matplotlib.pyplot as plt
from mymodule import files, convert, grid, interpolate, plot


def main(filename, dz, names, titles):
    """Produces cross section plots above and below the tropopause
    """
    cubes = files.load(filename)
    pv = convert.calc('advection_only_pv', cubes)
    z = grid.make_cube(pv, 'altitude')
    plotcubes = [convert.calc(name, cubes) for name in names]

    # Add PV as a coordinate to altitude
    pv.rename('ertel_potential_vorticity')
    pv = grid.make_coord(pv)
    z.add_aux_coord(pv, [0, 1, 2])

    # Find the height of the tropopause
    zpv2 = interpolate.to_level(z, ertel_potential_vorticity=[2])[0]

    # Produce a new co-ordinate above and below the tropopause
    ny, nx = zpv2.shape
    new_coord = np.zeros([3, ny, nx])
    new_coord[0, :, :] = zpv2.data - dz
    new_coord[1, :, :] = zpv2.data
    new_coord[2, :, :] = zpv2.data + dz

    # Interpolate the cubes to be plotted to the coordinate above and below the
    # tropopause
    plotcubes = [interpolate.to_level(cube, altitude=new_coord)
                 for cube in plotcubes]

    # Plot the cross sections
    extension = [r' - 1$ km', r'$', r' + 1$ km']
    for i, cube in enumerate(plotcubes):
        for n in xrange(3):
            plt.figure()
            plot.contourf(cube[n], plot.even_cscale(2), cmap='bwr',
                          extend='both')
            plt.title(titles[i] + r' at $z(q_{adv}=2 PVU)' + extension[n])
    plt.show()


if __name__ == '__main__':
    filename = '../iop5_36h.pp'
    dz = 1000
    names = ['total_minus_advection_only_pv', 'sum_of_physics_pv_tracers']
    titles = [r'$q-q_{adv}$', r'$\sum q_{phys}$']
    main(filename, dz, names, titles)
