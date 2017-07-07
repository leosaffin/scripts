import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt
from mymodule import convert
from systematic_forecasts import second_analysis


def main(variable):
    # RMS errors
    cubes = second_analysis.get_data('rms_error_24_air_pressure', 'full')
    plot_errors(cubes, variable, '-kx')

    cubes = second_analysis.get_data('mean_error_24_air_pressure', 'full')
    plot_errors(cubes, variable, '--kx')


def plot_errors(cubes, variable, *args):
    # 500 hPa height
    z500 = convert.calc(variable, cubes)
    z500 = z500.extract(
        iris.Constraint(air_pressure=20000, forecast_lead_time=24))

    qplt.plot(z500, *args)

    return


if __name__ == '__main__':
    for variable in ['ertel_potential_vorticity']:
        plt.figure()
        main(variable)

    plt.show()
