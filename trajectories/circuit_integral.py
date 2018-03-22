import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import iris
import iris.plot as iplt
import iris.quickplot as qplt
from iris.analysis import SUM
from iris.analysis.cartography import unrotate_pole, rotate_winds
from iris.coords import AuxCoord
from iris.coord_systems import GeogCS
from iris.cube import Cube
from mymodule import convert, grid
from mymodule.user_variables import datadir, plotdir
from mymodule.constants import omega
from lagranto import trajectory
from scripts import case_studies

a = 6378100


def main(theta_level):
    # IOP5 (early start)
    forecast = case_studies.iop5_extended.copy()
    job = 'iop5_extended'
    name = 'isentropic_backward_trajectories_from_outflow_boundary'
    dtheta = 1

    # Load trajectories
    filename = datadir + job + '/' + name + '.pkl'
    trajectories = trajectory.load(filename)
    print len(trajectories)

    # Only include trajectories that stay in the domain
    # trajectories = trajectories.select('air_pressure', '>', 0)
    # print(len(trajectories))

    # Select an individual theta level
    trajectories = trajectories.select(
        'air_potential_temperature', '==', theta_level)
    print len(trajectories)
    levels = ('air_potential_temperature', [theta_level])

    results = iris.cube.CubeList()
    for n, cubes in enumerate(forecast):
        print n
        if n == 0:
            # Load grid parameters
            example_cube = convert.calc('upward_air_velocity', cubes,
                                        levels=levels)

            # Create a 1d array of points for determining which gridpoints are
            # contained in the trajectory circuit when performing volume
            # integrals
            glon, glat = grid.get_xy_grids(example_cube)
            gridpoints = np.array([glon.flatten(), glat.flatten()]).transpose()
            cs = example_cube.coord_system()

        # Load trajectory positions -(n+2) because the trajectories are
        # backwards in time. +2 to skip the analysis which is not in the
        # forecast object (i.e. n=0 corresponds to idx=-2 in the trajectories)
        x = trajectories.x[:, -(n + 2)]
        y = trajectories.y[:, -(n + 2)]
        z = trajectories['altitude'][:, -(n + 2)]
        u = trajectories['x_wind'][:, -(n + 2)]
        v = trajectories['y_wind'][:, -(n + 2)]
        w = trajectories['upward_air_velocity'][:, -(n + 2)]
        
        leftflag = (trajectories['air_pressure'][:, -(n+2)] < 0).astype(int)
        leftcount = np.count_nonzero(leftflag)
        
        print leftcount

        # Calculate enclosed area integrals
        integrals = mass_integrals(cubes, x, y, glat, gridpoints,
                                   theta_level, dtheta)
        for icube in integrals:
            if leftcount > 0:
                icube.data = 0.
            results.append(icube)

        # Convert to global coordinates in radians
        u, v, lon, lat = get_geographic_coordinates(u, v, x, y, cs)

        # Unrotated coordinates in radians
        lon = np.deg2rad(lon)
        lat = np.deg2rad(lat)

        # Calculate the velocity due to Earth's rotation
        u_abs = omega.data * (a+z) * np.cos(lat)
        u += u_abs

        # Integrate around the circuit
        if leftcount > 0:
            circulation = 0
        else:
            circulation = circuit_integral_rotated(u, v, w, lon, lat, z)
        ccube = icube.copy(data=circulation)
        ccube.rename('circulation')
        ccube.units = 's-1'
        results.append(ccube)

    iris.save(results.merge(),
              datadir + 'circulations_' + str(theta_level) + 'K.nc')

    return


def get_geographic_coordinates(u, v, x, y, cs):
    rlon = AuxCoord(x, standard_name='grid_longitude', units='degrees',
                    coord_system=cs)
    rlat = AuxCoord(y, standard_name='grid_latitude', units='degrees',
                    coord_system=cs)
    u_array, v_array = [], []
    for n in range(len(u)):
        u_array.append(u)
        v_array.append(v)
    u = np.array(u_array)
    v = np.array(v_array)
    u = Cube(u, standard_name='x_wind', units='m s-1',
             aux_coords_and_dims=[(rlon, 0), (rlat, 1)])
    v = Cube(v, standard_name='y_wind', units='m s-1',
             aux_coords_and_dims=[(rlon, 0), (rlat, 1)])
    u, v = rotate_winds(u, v, GeogCS(a))
    
    u_wind, v_wind, lon, lat = [], [], [], []
    lons = u.coord('projection_x_coordinate').points
    lats = u.coord('projection_y_coordinate').points
    for n in range(len(x)):
        u_wind.append(u.data[n,n])
        v_wind.append(v.data[n,n])
        lon.append(lons[n, n])
        lat.append(lats[n, n])
        
    u_wind = np.array(u_wind)
    v_wind = np.array(v_wind)
    lon = np.array(lon)
    lat = np.array(lat)

    return u_wind, v_wind, lon, lat


def circuit_integral_rotated(u, v, w, lon, lat, z):
    """

    Args:
        u: Zonal wind
        v: Meridional Wind
        w: Vertical wind
        lon: Longitude
        lat: Latitude
        z: Altitude

    Returns:
    """
    circ_u, circ_v, circ_w = (0, 0, 0)
    # Elements 0, -1 and -2 are identical
    for n in range(1, len(u)-1):
        # u.r.cos(phi).dlambda
        dx = (a+z[n]) * np.cos(lat[n]) * (lon[n+1] - lon[n-1])/2
        circ_u += u[n] * dx

        # v.r.dphi
        dy = (a + z[n]) * (lat[n+1] - lat[n-1])/2
        circ_v += v[n] * dy

        # w.dz
        dz = (z[n+1] - z[n-1])/2
        circ_w += w[n]*dz

    circulation = circ_u + circ_v + circ_w

    return circulation


def circuit_integrals(u_abs, u, v, w, lon, lat, glon, glat, z, r):
    # Integrate u.dl around the circuit of trajectories
    # 1st and last 2 trajectories are the same so don't double count
    dlambda, dx, dy, dz = [], [], [], []
    for n in range(1, len(u) - 1):
        # dlambda is length along true longitudes to match the direction of
        # the Earth rotation
        dlambda.append(r[n] * np.cos(lat[n]) * 0.5 * (lon[n + 1] - lon[n - 1]))

        # dx and dy are in the direction of the rotated grid which corresponds
        # to the wind fields in the forecast
        dx.append(r[n] * np.cos(glat[n]) * 0.5 * (glon[n + 1] - glon[n - 1]))
        dy.append(r[n] * 0.5 * (glat[n + 1] - glat[n - 1]))

        # dz is independent of grid rotation
        dz.append(0.5 * (z[n + 1] - z[n - 1]))

    dlambda = np.array(dlambda)
    dx = np.array(dx)
    dy = np.array(dy)
    dz = np.array(dz)

    # \int dl: Tracks the errors in each calculation (should be zero)
    dx_tot = np.sum(dx)
    dy_tot = np.sum(dy)
    dz_tot = np.sum(dz)
    dlambda_tot = np.sum(dlambda)

    # \int |dl|
    length = np.sum(np.sqrt(dx ** 2 + dy ** 2 + dz ** 2))

    # u * r cos(phi) dlambda
    circ_u = u[1:-1] * dx

    # v * r dphi
    circ_v = v[1:-1] * dy

    # w * dz
    circ_w = w[1:-1] * dz

    # u_abs * r cos(phi) dlambda
    circ_p = u_abs[1:-1] * dlambda
    """
    r_ave = 0.5 * (r[1:] + r[:-1])

    dlambda = r_ave * np.cos(0.5 * (lat[1:] + lat[:-1])) * (lon[1:] - lon[:-1])
    dx = r_ave * np.cos(0.5 * (glat[1:] + glat[:-1])) * (glon[1:] - glon[:-1])
    dy = r_ave * (glat[1:] - glat[:-1])
    dz = (z[1:] - z[:-1])

    # \int dl
    dx_tot = np.sum(dx)
    dy_tot = np.sum(dy)
    dz_tot = np.sum(dz)
    dlambda_tot = np.sum(dlambda)

    # \int |dl|
    length = np.sum(np.sqrt(dx ** 2 + dy ** 2 + dz ** 2))

    # u * r cos(phi) dlambda
    circ_u = 0.5 * (u[1:] + u[:-1]) * dx

    # v * r dphi
    circ_v = 0.5 * (v[1:] + v[:-1]) * dy

    # w * dz
    circ_w = 0.5 * (w[1:] + w[:-1]) * dz

    # u_abs * r cos(phi) dlambda
    circ_p = 0.5 * (u_abs[1:] + u_abs[:-1]) * dlambda
    """

    rel_circulation = np.sum(circ_u + circ_v + circ_w)
    planetary_circulation = np.sum(circ_p)
    abs_circulation = np.sum(circ_u + circ_v + circ_w + circ_p)

    return (dx_tot, dy_tot, dz_tot, dlambda_tot, length,
            rel_circulation, planetary_circulation, abs_circulation)


def mass_integrals(cubes, x, y, glat, gridpoints, theta_level, dtheta):
    """

    Args:
        cubes (iris.cube.CubeList):
        x (np.Array): Circuit longitudes
        y (np.Array): Circuit latitudes
        glat (np.array): Grid latitudes
        gridpoints(np.Array): Array of gridpoint longitudes and latitudes of
            shape (ngp, 2)
        theta_level:
        dtheta (int): Isentrope spacing used to calculate volume integrals

    Returns:

    """
    # Include points within circuit boundary
    points = np.array([x, y]).transpose()
    pth = Path(points)

    # Mask all points that are not contained in the circuit
    mask = np.logical_not(pth.contains_points(gridpoints).reshape(glat.shape))

    # Area = r**2 cos(phi) dlambda dphi
    levels = ('air_potential_temperature',
              [theta_level - dtheta / 2.0, theta_level,
               theta_level + dtheta / 2.0])
    zth = convert.calc('altitude', cubes, levels=levels)
    area = (a + zth[1]) ** 2 * np.cos(np.deg2rad(glat)) * np.deg2rad(0.11) ** 2
    area.units = 'm^2'
    area.rename('area')
    total_area = integrate(area, mask)

    # Volume = area * dz
    volume = area * (zth[2] - zth[0])
    volume.rename('volume')
    total_volume = integrate(volume, mask)

    # Mass = density * volume
    levels = ('air_potential_temperature', [theta_level])
    density = convert.calc('air_density', cubes, levels=levels)[0]
    mass = density * volume
    mass.rename('mass')
    total_mass = integrate(mass, mask)

    # Circulation = \int rho.pv.dv / dtheta
    pv = convert.calc('ertel_potential_vorticity', cubes, levels=levels)[0]
    pv.convert_units('m^2 K s-1 kg-1')
    pv_substance = pv * mass
    circulation = integrate(pv_substance, mask) / dtheta

    circulation.rename('mass_integrated_circulation')

    return total_area, total_volume, total_mass, circulation


def integrate(cube, mask):
    cube = cube.copy()
    cube.data = np.ma.masked_where(mask, cube.data)
    result = cube.collapsed(['grid_longitude', 'grid_latitude'], SUM)

    return result


def load_from_files(theta):
    cubes = iris.load(datadir + 'circulations_' + theta + 'K.nc')
    plot_timeseries(cubes, theta)
    return


def plot_timeseries(cubes, theta):
    for cube in cubes:
        if 'circulation' in cube.name():
            iplt.plot(cube, label=cube.name())

    plt.legend(ncol=2, loc='best')
    plt.savefig(plotdir + 'circulation_' + theta + 'K.png')

    for cube in cubes:
        if 'circulation' not in cube.name():
            plt.figure()
            qplt.plot(cube)
            plt.savefig(plotdir + cube.name() + '_' + theta + 'K.png')

    plt.show()

    return


if __name__ == '__main__':
    main(325)
    load_from_files('325')
