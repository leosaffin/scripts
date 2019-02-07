import matplotlib.pyplot as plt
import iris.plot as iplt
from irise import convert, plot
from myscripts.models.um import case_studies


def main(cubes):
    pv = convert.calc('air_potential_temperature', cubes,
                      levels=('ertel_potential_vorticity', [2]))[0]

    theta = convert.calc('air_potential_temperature', cubes,
                         levels=('air_pressure', [85000]))[0]

    plot.pcolormesh(theta, vmin=250, vmax=300)
    iplt.contour(pv, [300, 320], colors='k')

    plt.show()

    return


if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
