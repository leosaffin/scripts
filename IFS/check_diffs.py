"""Quick check of IFS run vs a reference run to check whether code changes have
broken the model.
"""

import iris
from scripts.IFS import datadir


def main():
    path = datadir + 't21test/output/'
    forecast1 = 'full_precision/ICMGG_prognostics.nc'
    forecast2 = 'rpe_new/ICMGG_prognostics.nc'
    variable = 'Geopotential'

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

    print(diff.data.min(), diff.data.max())

    return


if __name__ == '__main__':
    main()
