"""Quick check of IFS run vs a reference run to check whether code changes have
broken the model.
"""

import numpy as np
import iris
from myscripts import statistics
from myscripts.models.ifs import datadir


def main():
    path = datadir + 't21test/'
    forecast1 = 'prognostics_pressure_ref_rp.nc'
    forecast2 = 'prognostics_pressure_ref.nc'
    variable = 'geopotential'

    cs = iris.Constraint(name=variable)
    diffminmax(path+forecast1, path+forecast2, cs)

    return


def diffminmax(forecast1, forecast2, cs):
    """ Print the minimum and maximum differences between two forecasts

    Args:
        forecast1 (iris.cube.CubeList):
        forecast2 (iris.cube.CubeList):
        cs (iris.Constraint):
    """
    z1 = iris.load_cube(forecast1, cs)
    z2 = iris.load_cube(forecast2, cs)

    diff = z1 - z2

    rms_diff = statistics.rms_diff(z1, z2)
    mean_diff = statistics.mean_diff(z1, z2)

    print(diff.data.min(), diff.data.max(),
          np.squeeze(mean_diff.data), np.squeeze(rms_diff.data))

    return


if __name__ == '__main__':
    main()
