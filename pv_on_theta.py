import matplotlib.pyplot as plt
import iris.plot as iplt
from iris.time import PartialDateTime as PDT
from mymodule import files, convert, grid, interpolate, plot
from mymodule.detection import rossby_waves


def main(cubes, theta_value, **kwargs):
    pv = convert.calc('ertel_potential_vorticity', cubes)
    theta = convert.calc('air_potential_temperature', cubes)

    pv.add_aux_coord(grid.make_coord(theta), [0, 1, 2])

    # Interpolate pv to theta level
    pv = interpolate.to_level(pv, air_potential_temperature=[theta_value])[0]

    # Add equivalent latitude
    lon, lat = grid.true_coords(theta)
    lat = pv.copy(data=lat)
    time = grid.get_datetime(theta)[0]
    time = PDT(month=time.month, day=time.day, hour=time.hour)
    eqlat = rossby_waves.equivalent_latitude(time, theta_value, 2)

    # Plot PV on theta
    plot.pcolormesh(pv, pv=pv, **kwargs)
    iplt.contour(lat, [eqlat.data], colors='r', linewidths=3)
    plt.show()

if __name__ == '__main__':
    cubes = files.load('datadir/xjjhq/xjjhq_036.pp')
    theta_value = 320
    main(cubes, theta_value, vmin=0, vmax=10, cmap='plasma')
