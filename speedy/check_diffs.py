import datetime
import iris
from scripts.IFS.check_diffs import diffminmax
from scripts.speedy import datadir


def main():
    # Paths to reference and test forecasts
    reference = datadir + 'output/exp_000/prognostics_pressure_ref.nc'
    forecast = datadir + 'output/exp_000/prognostics_pressure_ref_rp2.nc'

    # Specify variable, level and lead time to compare forecasts
    name = 'Temperature [K]'
    pressure = 500
    time = datetime.datetime(1982, 1, 8)

    # Convert parameters to iris constraint and calculate statistics
    cs = iris.Constraint(name=name, pressure=pressure, time=time)
    diffminmax(reference, forecast, cs)

    return


if __name__ == '__main__':
    main()
