import numpy as np
import matplotlib.pyplot as plt
from mymodule import convert, interpolate, plot
from myscripts.models.um import case_studies
import tropopause


def main(cubes, dz, name, **kwargs):
    """Produces cross section plots above and below the tropopause
    """
    # Extract cube to be plotted
    cube = convert.calc(name, cubes)

    # Find the height of the tropopause
    ztrop, fold_t, fold_b = tropopause.height(cubes)

    # Produce a new co-ordinate above and below the tropopause
    ny, nx = ztrop.shape
    new_coord = np.zeros([3, ny, nx])
    new_coord[0, :, :] = ztrop.data - dz
    new_coord[1, :, :] = ztrop.data
    new_coord[2, :, :] = ztrop.data + dz

    # Interpolate the cubes to be plotted to the coordinate above and below the
    # tropopause
    plotcube = interpolate.to_level(cube, altitude=new_coord)

    # Plot the cross sections
    for n in xrange(3):
        plt.figure()
        plot.pcolormesh(plotcube[n], **kwargs)
    plt.show()


if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    dz = 1000
    name = 'sum_of_physics_pv_tracers'
    main(cubes, dz, name, vmin=-2, vmax=2, cmap='bwr')
