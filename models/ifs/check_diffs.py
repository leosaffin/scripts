"""Quick check of IFS run vs a reference run to check whether code changes have
broken the model.
"""

import iris
from myscripts.models import forecast_errors
from myscripts.models.ifs import datadir


def main():
    path = datadir + 't21test/'
    forecast1 = 'prognostics_pressure_ref_rp.nc'
    forecast2 = 'prognostics_pressure_ref.nc'
    variable = 'geopotential'

    cs = iris.Constraint(name=variable)
    forecast_errors(path+forecast1, path+forecast2, cs)

    return


if __name__ == '__main__':
    main()
