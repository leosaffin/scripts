from datetime import timedelta as dt
import matplotlib.pyplot as plt
from irise import convert, plot
from myscripts.models.um import case_studies


def main(cubes, **kwargs):
    theta = convert.calc('air_potential_temperature', cubes,
                         levels=('ertel_potential_vorticity', [2]))

    plot.pcolormesh(theta[0], **kwargs)
    plt.show()

if __name__ == '__main__':
    forecast = case_studies.iop5()
    cubes = forecast.set_lead_time(dt(hours=36))
    main(cubes, vmin=285, vmax=350, cmap='plasma')
