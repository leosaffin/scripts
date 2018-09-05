"""Calculate the error of a forecast of each precision with respect to each
other precision.
"""
import matplotlib.pyplot as plt
import iris
from iris.cube import CubeList
from iris.coords import AuxCoord
import iris.quickplot as qplt
from myscripts.statistics import rms_diff
from myscripts.models.speedy import datadir


def main():
    # Parameters to compare between forecasts
    path = datadir + 'deterministic/'
    filename = 'rp_physics.nc'
    name = 'Temperature [K]'
    pressure = 500
    lead_time = 7*24

    cs = iris.Constraint(
        name=name, pressure=pressure, forecast_period=lead_time)

    # Load full precision reference forecast
    cube = iris.load_cube(path + filename, cs)

    # Calculate the errors with each different precision used as the `truth`
    diffs = CubeList()
    for pseudo_truth in cube.slices_over('precision'):
        # Add the precision of the `truth` cube as another coordinate
        p = pseudo_truth.coord('precision').points[0]
        p = AuxCoord(p, long_name='reference_precision')

        # Calculate the errors
        diff = rms_diff(cube, pseudo_truth)
        diff.add_aux_coord(p)

        # Store the errors in the cubelist
        diffs.append(diff)

    # Combine all the errors into a single cube with dimensions of
    # precision vs reference_precision
    diffs = diffs.merge_cube()

    # Plot the errors
    qplt.pcolor(diffs, vmin=0, cmap='cubehelix_r')
    precisions = cube.coord('precision').points
    plt.xticks(precisions)
    plt.yticks(precisions)

    plt.show()
    return


if __name__ == '__main__':
    main()
