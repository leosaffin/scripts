from datetime import timedelta as dt
import numpy as np
import matplotlib.pyplot as plt
from mymodule import convert, grid, interpolate, plot
from scripts import case_studies


def main(cubes, dz, name, title):
    """Produces cross section plots above and below the tropopause
    """
    pv = convert.calc('advection_only_pv', cubes)
    z = grid.make_cube(pv, 'altitude')
    cube = convert.calc(name, cubes)

    # Add PV as a coordinate to altitude
    pv = grid.make_coord(pv)
    z.add_aux_coord(pv, [0, 1, 2])

    # Find the height of the tropopause
    zpv2 = interpolate.to_level(z, advection_only_pv=[2])[0]

    # Produce a new co-ordinate above and below the tropopause
    ny, nx = zpv2.shape
    new_coord = np.zeros([3, ny, nx])
    new_coord[0, :, :] = zpv2.data - dz
    new_coord[1, :, :] = zpv2.data
    new_coord[2, :, :] = zpv2.data + dz

    # Interpolate the cubes to be plotted to the coordinate above and below the
    # tropopause
    plotcube = interpolate.to_level(cube, altitude=new_coord)

    # Plot the cross sections
    extension = [r' - 1$ km', r'$', r' + 1$ km']
    for n in xrange(3):
        plt.figure()
        plot.pcolormesh(plotcube[n], vmin=-2, vmax=2, cmap='bwr')
        plt.title(title + r' at $z(q_{adv}=2 PVU)' + extension[n])
    plt.show()


if __name__ == '__main__':
    forecast = case_studies.iop8()
    forecast.set_lead_time(dt(hours=36))
    cubes = forecast.cubelist
    dz = 1000
    name = 'sum_of_physics_pv_tracers'
    title = r'IOP8: $\sum q_{phys}$'
    main(cubes, dz, name, title)
