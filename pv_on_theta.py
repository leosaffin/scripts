from datetime import timedelta as dt
import matplotlib.pyplot as plt
import iris.plot as iplt
from iris.time import PartialDateTime as PDT
from mymodule import convert, grid, plot
from mymodule.detection import rossby_waves
from scripts import case_studies


def main(cubes, theta_value, **kwargs):
    pv = convert.calc('ertel_potential_vorticity', cubes,
                      levels=('air_potential_temperature', [theta_value]))[0]

    # Add equivalent latitude
    lon, lat = grid.true_coords(pv)
    lat = pv.copy(data=lat)
    time = grid.get_datetime(pv)[0]
    time = PDT(month=time.month, day=time.day, hour=time.hour)
    eqlat = rossby_waves.equivalent_latitude(time, theta_value, 2)

    # Plot PV on theta
    plot.pcolormesh(pv, pv=pv, **kwargs)
    iplt.contour(lat, [eqlat.data], colors='r', linewidths=2)
    plt.show()

if __name__ == '__main__':
    forecast = case_studies.iop8()
    forecast.set_lead_time(dt(hours=36))
    cubes = forecast.cubelist
    theta_value = 310
    main(cubes, theta_value, vmin=0, vmax=10, cmap='plasma')
