"""
Compare a set of runs with reduced precision to a reference double precision
simulation. The forecasts use the same initial conditions and if SPPT is on each
forecast uses the same random-number seed in the SPPT forcing so all errors are
'deterministic'.
"""

import os
import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt
from iris.analysis import Linear
from myscripts.statistics import ensemble_std_dev, rms_diff
from myscripts.models.speedy import datadir


def main():
    filename = 'rp_prognostics_after'
    path = datadir + 'stochastic/'

    # Parameters to compare between forecasts
    name = 'Geopotential Height [m]'
    pressure = 500
    reference = 'fp'
    lead_time = 7*24

    # Load reference forecast
    cs = iris.Constraint(name=name, pressure=pressure, precision=23,
                         forecast_period=lead_time)
    fp = iris.load_cube(path + 'rp_convection.nc', cs)

    # Regrid other reference forecasts
    if reference == 't39':
        ref = iris.load_cube(datadir + 'output/exp_007/yyyymmddhh_p.nc', cs)
        ref = ref.regrid(fp, Linear())
        fp.data = ref.data

    elif reference == 'sppt':
        ref = iris.load_cube(datadir + 'output/exp_004/yyyymmddhh_p.nc', cs)
        fp.data = ref.data

    # Compare full precision with reduced precision forecasts
    cs = iris.Constraint(name=name, pressure=pressure,
                         forecast_period=lead_time)
    for filename in os.listdir(path):
        rp = iris.load_cube(path + filename, cs)
        plot_errors(fp, rp, marker='x', label=filename.split('.')[0])

    # Plot ensemble spread as upper limit
    ensemble = iris.load_cube(datadir + 'ensembles/yyyymmddhh_p52b.nc', cs)
    std_dev = ensemble_std_dev(ensemble)
    plt.axhline(std_dev.data, color='k', linestyle='--')

    plt.ylabel('RMS Error')
    plt.title(name)
    plt.legend()
    plt.show()

    return


def plot_errors(fp, rp, **kwargs):
    rmse = rms_diff(rp, fp)

    qplt.plot(rmse, **kwargs)

    return


if __name__ == '__main__':
    main()
