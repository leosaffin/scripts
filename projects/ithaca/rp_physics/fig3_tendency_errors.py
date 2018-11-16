"""
Show the errors in physics tendencies as a function of precision. Show both
relative and absolute errors (haven't decided on mean_diff or rms_diff). For
relative errors, this can be directly compared to the machine epsilon so add
this line also. Also print out errors as a function of machine epsilon to be
shown in a table.
"""

import parse
import numpy as np
import matplotlib.pyplot as plt
import iris
from mymodule.plot.util import legend, multilabel
from myscripts.statistics import mean_diff, rms_diff
from myscripts.models.speedy import datadir, physics_schemes


def main():
    # Load cubes
    path = datadir + 'deterministic/'
    cs = iris.Constraint(
        cube_func=lambda x: 'Temperature Tendency' in x.name(),
        forecast_period=2/3, pressure=0.95)
    rp_cubes = iris.load(path + 'rp_*_tendencies.nc', cs)
    fp_cubes = iris.load(path + 'fp_tendencies.nc', cs)

    # Create a two by one grid
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=[14.4, 5.4])

    plt.axes(axes[0])

    plt.yscale('log')
    plt.xlabel('Precision [sbits]')
    plt.ylabel('Temperature tendency error')
    plt.title('Absolute Error')

    plt.axes(axes[1])
    plt.yscale('log')
    plt.xlabel('Precision [sbits]')
    plt.title('Relative Error')

    # Show the reference machine epsilon
    sbits = np.arange(5, 24)
    error = 2.0 ** -(sbits + 1)
    plt.plot(sbits, error, '--k', label='Machine Epsilon')

    # Loop over physics schemes
    for rp in rp_cubes:
        scheme, units = parse.parse('Temperature Tendency due to {} [{}]', rp.name())
        if scheme == 'Large-Scale Condensation':
            scheme = 'Condensation'
        plp = physics_schemes[scheme]
        fp = fp_cubes.extract(iris.Constraint(name=rp.name()))[0]

        # Ignore where tendencies are zero
        rp.data = np.ma.masked_where(
            np.logical_or(rp.data == 0, fp.data == 0), rp.data)

        # Calculate absolute error
        plt.axes(axes[0])
        abs_error = rp.copy(data=np.abs(rp.data - fp.data))
        abs_error = mean_diff(abs_error, 0)
        plp.plot(abs_error, label=scheme)

        # Calculate relative error
        plt.axes(axes[1])
        rel_error = rp.copy(data=np.abs((rp.data - fp.data)/fp.data))
        rel_error = mean_diff(rel_error, 0.0)
        plp.plot(rel_error)

        # Print values
        print('{} & {} & {}'.format(scheme, abs_error.data[5], (rel_error.data/error).mean()))

    plt.axes(axes[0])
    legend(key=lambda x: physics_schemes[x[0]].idx, ncol=2,
           title='Physics Schemes')
    multilabel(axes[0], 0, factor=0.01)
    multilabel(axes[1], 1, factor=0.01)
    plt.show()

    return


if __name__ == '__main__':
    main()
