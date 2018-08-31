import matplotlib.pyplot as plt
import iris.plot as iplt
from iris.time import PartialDateTime as PDT
from mymodule import convert, grid, plot
from mymodule.detection import rossby_waves
from myscripts.models.um import case_studies


def main(cubes, theta_value, **kwargs):
    """Plot PV on theta and the equivalent latitude circle

    Args:
        cubes (iris.cube.CubeList): Contains variables to calculate PV and
            potential temperature
    """
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
    plt.title('')
    plt.show()

if __name__ == '__main__':
    forecast = case_studies.iop5()
    cubes = forecast.set_lead_time(hours=36)
    theta_value = 330
    main(cubes, theta_value, vmin=0, vmax=10, cmap='cubehelix_r')
