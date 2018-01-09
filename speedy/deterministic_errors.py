"""
Compare a set of runs with reduced precision to a reference double precision
simulation. Each forecast uses the same random-number seed in the SPPT forcing
so all errors are 'deterministic'.
"""

import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt
from iris.analysis import STD_DEV, MEAN
from iris.analysis.cartography import cosine_latitude_weights
from scripts.speedy import datadir, plotdir, rms_diff


def main():
    filename = 'rp_prognostics_after'

    # Parameters to compare between forecasts
    name = 'Geopotential Height [m]'
    pressure = 500
    cs = iris.Constraint(name=name, pressure=pressure)

    # Load full precision reference forecast
    with iris.FUTURE.context(cell_datetime_objects=True):
        # Load full precision reference forecast
        rp = iris.load_cube(datadir + 'deterministic/' +
                            filename + '.nc', cs)
        fp = rp.extract(iris.Constraint(precision=52))

    for fps, rps in zip(fp.slices_over('forecast_period'),
                        rp.slices_over('forecast_period')):
        plot_errors(fps, rps)

    # Plot ensemble spread as upper limit
    fp = iris.load_cube(datadir + 'ensembles/yyyymmddhh_p52b.nc', cs)
    std_dev = fp.collapsed('ensemble_member', STD_DEV)
    weights = cosine_latitude_weights(std_dev)
    std_dev = std_dev.collapsed(['longitude', 'latitude'],
                                MEAN, weights=weights)

    for n in range(0, 4*7*4+1, 4*7):
        plt.axhline(2*std_dev.data[n], color='k', linestyle='--')

    plt.ylabel('RMS Error')
    plt.title(name)
    plt.savefig(plotdir + filename + '_' + name.split()[0].lower() +
                '_' + str(pressure) + 'hpa.png')
    plt.show()

    return


def plot_errors(fp, rp, **kwargs):
    weights = cosine_latitude_weights(rp)
    rmse = rms_diff(rp, fp, weights=weights)

    qplt.plot(rmse, **kwargs)

    return


if __name__ == '__main__':
    main()
