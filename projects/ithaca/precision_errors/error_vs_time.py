"""Calculate the forecast error as a function of lead time
"""
import matplotlib.pyplot as plt
import iris
from mymodule.plot.util import legend
from myscripts.models.speedy import datadir, physics_schemes
from myscripts.projects.ithaca.precision_errors import decode_name


def main():
    # Specify which files and variable to compare
    path = datadir + 'output/'
    filename = 'precision_errors_temperature_500hpa_stochastic.nc'
    cs = iris.Constraint(pressure=500, precision=23)
    cubes = iris.load(path + filename, cs)

    for cube in cubes:
        print(cube.name())
        cube.coord('forecast_period').convert_units('days')
        variable, scheme = decode_name(cube.name())
        plp = physics_schemes[scheme]
        plp.plot(cube, label=scheme)

    variable, scheme = decode_name(cubes[0].name())
    units = cubes[0].units
    pressure = int(cubes[0].coord('pressure').points[0])
    precision = cubes[0].coord('precision').points[0]

    plt.xlabel('Time (days)')
    plt.ylabel('RMSE ({})'.format(units))
    plt.title('{} at {}hPa at {} sbits'.format(variable, pressure, precision))
    legend(key=lambda x: physics_schemes[x[0]].idx)
    plt.show()

    return


if __name__ == '__main__':
    main()
