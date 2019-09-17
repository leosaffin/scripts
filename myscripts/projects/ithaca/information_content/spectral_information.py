import numpy as np
import matplotlib.pyplot as plt

import iris
import iris.coord_categorisation
from iris.analysis import MEAN

from myscripts.models import speedy
from myscripts.projects.ithaca.information_content import information_content


def main():
    path = '/media/saffin/TOSHIBA EXT/lsaffin/meteorology/data/speedy/'
    filename = 'spectral_prognostics.nc'

    name = 'Real Part of Geopotential'

    cs = iris.Constraint(name=name, sigma=speedy.sigma_levels[3])
    cube = iris.load_cube(path + filename, cs)

    # Remove first year of data for spin up
    iris.coord_categorisation.add_year(cube, 'time')
    cube = cube.extract(iris.Constraint(year=lambda x: x > 1980))

    # Calculate a daily climatology
    iris.coord_categorisation.add_month_number(cube, 'time')
    iris.coord_categorisation.add_day_of_month(cube, 'time')
    climatology = cube.aggregated_by(['day_of_month', 'month_number'], MEAN)

    # Extract climatology without the leap year
    climatology_no_leap = climatology[list(range(59)) + list(range(60, 366))]

    # Calculate anomaly with respect to climatology taking into account
    # leap years
    anomalies = iris.cube.CubeList()
    for year in set(cube.coord('year').points):
        subcube = cube.extract(iris.Constraint(year=year))
        if len(subcube.coord('time').points) == 366:
            anomalies.append(subcube-climatology.data)
        else:
            anomalies.append(subcube-climatology_no_leap.data)
    anomalies = anomalies.concatenate_cube()

    # Information content from on spectral mode at predicting another
    predictor = anomalies.data[:, 1, 0]
    predictand = anomalies.data[:, 0, 0]
    I_b = information_content(predictor, predictand, 3, 30)

    plt.plot(I_b)
    plt.show()

    return


if __name__ == '__main__':
    main()
