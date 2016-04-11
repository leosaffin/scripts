from datetime import timedelta as dt
from mymodule import convert, grid
from scripts import case_studies


def create_startf(cubes, theta_level, output_file):
    """Creates a startfile for lagranto for the whole grid on a single
    isentropic surface

    Reference date 20111129_2300 / Time range       0 min

      time      lon     lat     p     level
    ---------------------------------------

       0.00   -10.000   50.000   258   320.000

    """
    # Find pressure on theta level
    P = convert.calc('air_pressure', cubes,
                     levels=('air_potential_temperature', theta_level))[0].data

    # Get longitude and latitude
    lon, lat = grid.true_coords(P)

    # Create startfile
    with open(output_file, 'w') as output:
        output.write('Reference date 20111129_2300 / Time range       0 min\n')
        output.write('\n')
        output.write('  time      lon     lat     p     level\n')
        output.write('---------------------------------------\n')
        output.write('\n')
        ny, nx = P.shape
        for j in xrange(ny):
            for i in xrange(nx):
                output.write('   0.00   ' + str(round(lon[j, i], 3)) +
                             '   ' + str(round(lat[j, i], 3)) +
                             '   ' + str(round(P[j, i] / 100.0, 0)) +
                             '   ' + str(theta_level) + '\n\n')


if __name__ == '__main__':
    forecast = case_studies.iop5()
    cubes = forecast.set_lead_time(dt(hours=36))
    output_file = '/home/lsaffi/data/iop5/trajectories/start_320k_35h.1'
    create_startf(cubes, 320, output_file)
