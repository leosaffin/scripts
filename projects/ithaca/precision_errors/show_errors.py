"""Calculate the forecast error as a function of precision
"""
import matplotlib.pyplot as plt
import iris
from mymodule import plot
from myscripts.models.speedy import datadir, physics_schemes
from myscripts.projects.ithaca.precision_errors import decode_name


def main():
    # Specify which files and variable to compare
    path = datadir + 'output/'
    filename = 'precision_errors_temperature_500hpa.nc'
    lead_time = 24

    cs = iris.Constraint(forecast_period=lead_time)
    cubes = iris.load(path + filename, cs)

    for cube in cubes:
        print(cube.name())
        variable, units, scheme = decode_name(cube.name())
        plp = physics_schemes[scheme]
        plp.plot(cube, label=scheme)

    variable, units, scheme = decode_name(cubes[0].name())
    pressure = int(cubes[0].coord('pressure').points[0])

    plt.xlabel('Precision (sbits)')
    plt.ylabel('RMSE ({})'.format(units))
    plt.title('{} at {}hPa at T+{}h'.format(variable, pressure, lead_time))
    plot.legend(key=lambda x: physics_schemes[x[0]].idx)
    plt.show()

    return


if __name__ == '__main__':
    main()
