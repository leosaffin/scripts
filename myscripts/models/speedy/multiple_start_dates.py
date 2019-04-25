"""
Compare a set of runs with reduced precision to a reference double precision
simulation. Each forecast uses the same random-number seed in the SPPT forcing
so all errors are 'deterministic'.
"""

import numpy as np
import matplotlib.pyplot as plt
import iris
from iris.time import PartialDateTime
from iris.analysis import STD_DEV, MEAN
from irise import plot
from myscripts import datadir
from myscripts.statistics import rms_diff
from myscripts.models.speedy import plotdir


def main():
    # Parameters to compare between forecasts
    name = 'Temperature [K]'
    pressure = 500
    path = datadir + 'cirrus/'
    cs = iris.Constraint(
        name=name, pressure=pressure, forecast_reference_time=(
            lambda cell: (PartialDateTime(year=1982) < cell <
                          PartialDateTime(year=1992))))

    # Load full precision reference forecast
    with iris.FUTURE.context(cell_datetime_objects=True):
        fp = iris.load_cube(path + '1982-1991_p52.nc', cs)

        # Compare with reduced precision forecasts
        rp = iris.load(path + '*_10-30.nc', cs)
        rp = rp.concatenate_cube()

    # Calculate the global RMS error at each forecast lead time
    diff = rms_diff(rp, fp)

    # Calculate the mean error as a function of precision and the standard error
    # of the mean for each lead time
    mean = diff.collapsed('forecast_reference_time', MEAN)
    std_dev = diff.collapsed('forecast_reference_time', STD_DEV)
    std_err = (std_dev /
               np.sqrt(len(diff.coord('forecast_reference_time').points)))

    for mean_slice, std_slice in zip(mean.slices(['precision']),
                                     std_err.slices(['precision'])):
        plot.errorbar(mean_slice, yerr=std_slice, marker='x')

    plt.savefig(plotdir + 'average_errors' + '_' + name.split()[0].lower() +
                '_' + str(pressure) + 'hpa.png')
    plt.show()

    return


if __name__ == '__main__':
    print('Executing ' + __name__ + ' as script.')
    main()
