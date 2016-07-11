from datetime import timedelta as dt
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, plot
from mymodule.detection.fronts import fronts
from scripts import case_studies


def main(cubes, p_level):
    # Load data
    theta = convert.calc('air_potential_temperature', cubes,
                         levels=('air_pressure', [p_level]))[0]

    # Calculate the fronts
    loc = fronts.main(theta)
    loc = theta.copy(data=loc)

    # Plot the output
    plot.pcolormesh(theta, vmin=280, vmax=320, cmap='plasma')
    plt.title(r'$\theta$ at ' + str(p_level) + ' Pa')
    iplt.contour(loc, [0], colors='k')
    plt.show()


if __name__ == '__main__':
    forecast = case_studies.iop8()
    cubes = forecast.set_lead_time(dt(hours=36))
    p_level = 65000
    main(cubes, p_level)
