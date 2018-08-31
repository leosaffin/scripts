import numpy as np
import matplotlib.pyplot as plt
from mymodule import convert, plot
import iris.plot as iplt
from iris.analysis import SUM
from myscripts import case_studies


def main(cubes):
    mass = convert.calc('mass', cubes)
    water = convert.calc('mass_fraction_of_water', cubes)
    total_water = mass * water
    tcw = total_water.collapsed('atmosphere_hybrid_height_coordinate', SUM)

    mslp = convert.calc('air_pressure_at_sea_level', cubes)
    mslp.convert_units('hPa')

    plot.pcolormesh(tcw, vmin=0, vmax=5e9, cmap='Greys_r')
    iplt.contour(mslp, np.linspace(950, 1050, 11), colors='k', linewidths=2)

    plt.show()

    return


if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
