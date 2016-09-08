"""Read in John's equivalent latitude data and output as netcdf
"""
import datetime
import numpy as np
import iris
from mymodule import convert, interpolate, grid

directory = "/home/lsaffin/Documents/meteorology/data/"
infile = "eqlats/emuseries_2013120100"
outfile = "eqlats/2013_eqlats.nc"


def main():
    """
    Equivalent Latitude (PV Level, Theta Level, Time)

    Surface Equivalent Latitude (Theta Level, Time)
    """
    with open(directory + infile) as data:
        # Top line has the start date
        date = data.readline().split()[-1]
        date = datetime.datetime(
            int(date[0:4]), int(date[4:6]), int(date[6:8]), int(date[8:10]))

        # Second line says how many times there are
        ntimes = int(data.readline().split()[0])

        # Third line gives the time interval
        dt = int(data.readline().split()[0])
        time = iris.coords.DimCoord(
            np.arange(ntimes) * dt, long_name='time', units='hours')

        # Next block states the number of latitudes and their values
        nlats = int(data.readline().split()[0])
        latitude = readlines(data, nlats)
        latitude = iris.coords.DimCoord(latitude, standard_name='latitude')

        # Next block states the number of isentropic levels and their values
        ntheta = int(data.readline().split()[0])
        theta = readlines(data, ntheta)
        theta = iris.coords.DimCoord(
            theta, long_name='potential_temperature')

        # The next line states the top boundary of isentropic levels
        theta_max = float(data.readline().split()[0])

        # The next line states the max/min values of theta at the surface
        surf_theta = data.readline().split()
        surf_theta_max = float(surf_theta[0])
        surf_theta_min = float(surf_theta[1])

        # The next block states the number of PV levels and their values
        npv = int(data.readline().split()[0])
        pv = readlines(data, npv) * 1e6
        pv = iris.coords.DimCoord(
            pv, long_name='ertel_potential_vorticity', units='PVU')

        # The next block is the max PV on theta values
        data.readline()
        pv_max = readlines(data, ntheta)

        # The next block is the minimum PV on theta values
        data.readline()
        pv_min = readlines(data, ntheta)

        # The next block is equivalent latitudes at the surface
        data.readline()
        eqlat_s = np.arcsin(readlines(data, ntheta * ntimes)) * 180 / np.pi
        eqlat_s = iris.cube.Cube(
            np.reshape(eqlat_s, (ntimes, ntheta)),
            long_name="surface_equivalent_latitude",
            units='degrees',
            dim_coords_and_dims=[(time, 0), (theta, 1)])

        # The next block is equivalent latitudes of PV values
        data.readline()
        eqlat = np.arcsin(readlines(data, npv * ntheta * ntimes)) * 180 / np.pi
        eqlat = iris.cube.Cube(
            np.reshape(eqlat, (ntimes, ntheta, npv)),
            long_name="equivalent_latitude",
            units='degrees',
            dim_coords_and_dims=[(time, 0), (theta, 1), (pv, 2)])

        iris.save(iris.cube.CubeList([eqlat, eqlat_s]), directory + outfile)


def readlines(data, npoints):
    values = []
    while len(values) < npoints:
        for value in data.readline().split():
            values.append(float(value))

    return np.array(values)


def theta_pv2(start_time):
    # Load the equivalent latitude data on PV2
    cubes = iris.load(directory + 'eqlats/eqlats_' + start_time + '.nc')

    # phi(t, theta, q)
    eqlats_cube = convert.calc('equivalent_latitude', cubes)

    # theta coordinate
    theta = eqlats_cube.coord('potential_temperature').points

    # phi(t, theta, q=2PVU)
    eqlats = interpolate.main(
        eqlats_cube, ertel_potential_vorticity=[2])[:, :, 0].data

    return eqlats_cube, theta, eqlats


def thetapv2_hemisphere(start_time):
    """Re-arrange the data as theta(time, grid_lat, grid_lon)
    """
    # Load the equivalent latitude data on PV2
    eqlats_cube, theta, eqlats = theta_pv2(start_time)

    # Create a coordinate for latitude
    nlats = 91
    lat = np.linspace(0, 90, nlats)

    # Initialise the output
    ntimes, ntheta = eqlats.shape
    output = np.zeros([ntimes, nlats])

    for n in range(ntimes):
        print(n)
        for j in range(nlats):
            # Search upward for the equivalent latitude value
            k = ntheta - 2
            while eqlats[n, k] > lat[j] and k > 0:
                k -= 1

            if k > 0:
                # Linearly interpolate to find theta
                alpha = ((lat[j] - eqlats[n, k]) /
                         (eqlats[n, k + 1] - eqlats[n, k]))

                output[n, j] = (alpha * theta[k + 1] + (1 - alpha) * theta[k])

            else:
                output[n, j] = theta[k]

    output = iris.cube.Cube(
        output, long_name='potential_temperature', units='K',
        dim_coords_and_dims=[(eqlats_cube.coord('time'), 0),
                             (iris.coords.DimCoord(lat, long_name='latitude',
                                                   units='degrees'), 1)])

    iris.save(output, directory + 'eqlats/theta_2pvu_' + start_time + '.nc')


def thetapv2_nae(start_time):
    """Re-arrange the data as theta(time, grid_lat, grid_lon)
    """
    # Load the equivalent latitude data on PV2
    eqlats_cube, theta, eqlats = theta_pv2(start_time)

    # Load the NAE grid
    cubes = iris.load(directory + 'xjjhq/xjjhqa_036.pp')
    lat = grid.true_coords(cubes[0])[1]

    # Initialise the output
    nt, ntheta = eqlats.shape
    ny, nx = lat.shape
    output = np.zeros([nt, ny, nx])

    for n in range(nt):
        print(n)
        for j in range(ny):
            for i in range(nx):
                # Search upward for the equivalent latitude value
                k = ntheta - 2
                while eqlats[n, k] > lat[j, i]:
                    k -= 1

                if k > 0:
                    # Linearly interpolate to find theta
                    alpha = ((lat[j, i] - eqlats[n, k]) /
                             (eqlats[n, k + 1] - eqlats[n, k]))
                    output[n, j, i] = (alpha * theta[k + 1] +
                                       (1 - alpha) * theta[k])
                else:
                    output[n, j, i] = theta[k]

    output = iris.cube.Cube(
        output, long_name='potential_temperature', units='K',
        dim_coords_and_dims=[(eqlats_cube.coord('time'), 0),
                             (cubes[0].coord('grid_latitude'), 1),
                             (cubes[0].coord('grid_longitude'), 2)])

    iris.save(output,
              directory + 'eqlats/theta_2pvu_nae_' + start_time + '.nc')

if __name__ == '__main__':
    start_time = '2011_11'
    thetapv2_hemisphere(start_time)
    thetapv2_nae(start_time)
