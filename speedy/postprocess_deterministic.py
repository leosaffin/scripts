import datetime as dt
import pandas as pd
import iris
from iris.coords import AuxCoord, DimCoord
from iris.unit import Unit
from scripts.speedy import datadir

datadir = datadir + 'exp_000/'
#datadir = '/home/saffin/cirrus/speedy/'


def main():
    t0 = dt.datetime(1982, 1, 1)
    t1 = dt.datetime(1982, 1, 1)
    pmin, pmax = 5, 52
    all_cubes = iris.cube.CubeList()

    for time in pd.date_range(t0, t1, freq='MS'):
        print time

        yyyymmddhh = time.strftime('%Y%m%d%H')

        for n in range(pmin, pmax+1):
            cubes = iris.load(datadir + 'yyyymmddhh' + '_p' + str(n) + '.nc')
            coord = iris.coords.AuxCoord(points=n, long_name='precision')
            for cube in cubes:
                cube.add_aux_coord(coord)

            t0_dt(cubes)

            for cube in cubes:
                all_cubes.append(cube)

    cubes = all_cubes.merge()
    print cubes
    iris.save(cubes, datadir + str(t0.year) + '-' + str(t1.year) + '_' +
              str(pmin) + '-' + str(pmax) + '.nc')
    return


def t0_dt(cubes):
    """Change time units from time to start time and lead time
    """
    time = cubes[0].coord('time')
    time.convert_units(Unit('hours since 1982-01-01 00:00:00',
                            calendar='standard'))
    start_time = AuxCoord(
        points=time.points[0], standard_name='forecast_reference_time',
        units=time.units)
    lead_time = DimCoord(
        points=time.points-time.points[0], standard_name='forecast_period',
        units='hours')

    for cube in cubes:
        cube.remove_coord('time')
        cube.add_dim_coord(lead_time, [0])
        cube.add_aux_coord(start_time)

    return


if __name__ == '__main__':
    main()
