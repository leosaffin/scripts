from mymodule import forecast, interpolate, convert, grid, io, plot
from mymodule.trajectory import load
from iris.analysis.cartography import rotate_pole
import numpy as np
import matplotlib.pyplot as plt
import datetime


def main(filename, start_time, mapping, pole_lon, pole_lat):
    # Load the trajectories
    trajectories = load.raw(filename)
    # Load the forecast data
    forecast = forecast.Forecast(start_time, mapping)

    rlons = []
    rlats = []
    values = []
    for trajectory in trajectories:
        # Find the variable at the last trajectory point
        time, lon, lat, p = trajectory.data[-1]
        rlon, rlat = rotate_pole(np.array(lon), np.array(lat),
                                 pole_lon, pole_lat)
        forecast.set_time(time)
        cube = convert.calc(name, forecast.cubelist)

        # Add pressure as an Auxiliary coordinate
        pressure = forecast.cubelist.extract('air_pressure')[1]
        pcoord = grid.make_coord(pressure)
        cube.add_aux_coord(pcoord)

        # Interpolate to the trajectory point
        column = interpolate.main(cube, grid_longitude=rlon,
                                  grid_latitude=rlat)
        value = interpolate.main(column, air_pressure=p)

        # Save the values for plotting
        rlons.append(rlon)
        rlats.append(rlat)
        values.append(value)

    # Put the values on the normal grid
    lons = cube.coord('grid_longitude').points()
    lats = cube.coord('grid_latitude').points()
    field = regular_grid(values, rlons, rlats, lons, lats)
    cube = cube.copy(data=field)
    cube.rename('name')

    # Save the field
    io.save(cube, '/home/lsaffi/data/rdf_pv.nc')
    # Plot the field
    levs = np.linspace(0, 5, 21)
    plot.level(cube, cube, levs, cmap=cubehelix_r, extend='both')


def regular_grid(field, lons, lats, grid_lon, grid_lat):
    """
    Args:
        field (list):
        lons (list):
        lats (list):
        grid_lon (numpy.ndarray): 1d array
        grid_lat (numpy.ndarray): 1d array
    """
    points = [x_points, y_points]
    points = np.transpose(np.array(points))
    return griddata(points, field, (x_grid, y_grid), method='linear')

if __name__ == '__main__':
    pole_lon = 177.5
    pole_lat = 37.5
    filename = '/home/lsaffi/data/out_1h.1'
    start_time = datetime.datetime(2011, 11, 28, 12)
    dt = datetime.timedelta(hours=6)
    mapping = {start_time + (n + 1) * dt: '*' +
               str(int((n * dt).total_seconds() / 3600)).zfill(3)
               for n in range(6)}
    main(filename, start_time, mapping, pole_lon, pole_lat)
