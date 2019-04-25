import parse
import numpy as np
import matplotlib.pyplot as plt
import iris
from irise.plot.util import legend
from myscripts.statistics import mean_diff, rms_diff
from myscripts.models.speedy import datadir, physics_schemes


def main():
    # Load cubes
    path = datadir + 'deterministic2/'
    cs = iris.Constraint(
        cube_func=lambda x: 'Temperature Tendency' in x.name(),
        forecast_period=2/3, pressure=0.95)
    rp_cubes = iris.load(path + 'rp_*_tendencies.nc', cs)
    fp_cubes = iris.load(path + 'fp_tendencies.nc', cs)

    # Show the reference machine epsilon
    sbits = np.arange(5, 24)
    error = 2.0 ** -(sbits + 1)
    #plt.plot(sbits, error, '--k')

    # Loop over physics schemes
    for rp in rp_cubes:
        scheme, units = parse.parse(
            'Temperature Tendency due to {} [{}]', rp.name())
        if scheme == 'Large-Scale Condensation':
            scheme = 'Condensation'
        plp = physics_schemes[scheme]
        fp = fp_cubes.extract(iris.Constraint(name=rp.name()))[0]

        # Calculate error of nonzero gridpoints
        rp.data = np.ma.masked_where(np.logical_or(rp.data == 0, fp.data == 0),
                                     np.abs(rp.data - fp.data))
        mean_error = mean_diff(rp, 0)
        plp.plot(mean_error, label=scheme)

        print('{}: {}'.format(scheme, np.mean(mean_error.data/error)))

    plt.xlabel('Precision [sbits]')
    plt.ylabel('Mean relative error')
    legend(key=lambda x: physics_schemes[x[0]].idx)
    plt.show()

    return


if __name__ == '__main__':
    main()
