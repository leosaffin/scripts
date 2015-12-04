from iris.analysis.cartography import get_xy_grids, unrotate_pole
from mymodule import files, convert, grid, interpolate


def create_startf(theta, P, theta_level, output_file):
    """Creates a startfile for lagranto for the whole grid on a single
    isentropic surface

    Reference date 20111129_2300 / Time range       0 min

      time      lon     lat     p     level
    ---------------------------------------

       0.00   -10.000   50.000   258   320.000

    """
    # Get longitude and latitude
    rlon, rlat = get_xy_grids(theta)
    lon, lat = unrotate_pole(rlon, rlat, 177.5, 37.5)

    # Find pressure on theta level
    thcoord = grid.make_coord(theta)
    P.add_aux_coord(thcoord, [0, 1, 2])
    P_theta = interpolate.to_level(P, air_potential_temperature=[theta_level])
    P_theta = P_theta[0].data

    # Create startfile
    with open(output_file, 'w') as output:
        output.write('Reference date 20111129_2300 / Time range       0 min\n')
        output.write('\n')
        output.write('  time      lon     lat     p     level\n')
        output.write('---------------------------------------\n')
        output.write('\n')
        ny, nx = P_theta.shape
        for j in xrange(ny):
            for i in xrange(nx):
                output.write('   0.00   ' + str(round(lon[j, i], 3)) +
                             '   ' + str(round(lat[j, i], 3)) +
                             '   ' + str(round(P_theta[j, i] / 100.0, 0)) +
                             '   ' + str(theta_level) + '\n\n')


if __name__ == '__main__':
    cubes = files.load('/projects/diamet/lsaffi/xjjhq/xjjhqa_035.pp')
    cubes.remove(cubes.extract('air_pressure')[0])
    theta = convert.calc('air_potential_temperature', cubes)
    P = convert.calc('air_pressure', cubes)
    create_startf(theta, P, 320,
                  '/home/lsaffi/data/iop5/trajectories/start_320k_35h.1')
