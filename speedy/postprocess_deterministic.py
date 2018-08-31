import os
import datetime as dt
import pandas as pd
import iris
from iris.coords import AuxCoord, DimCoord
from cf_units import Unit
from myscripts.speedy import datadir


def main():
    path = os.path.expanduser('~/temp/')
    prefix = 'output'
    t0 = dt.datetime(1982, 1, 1)
    t1 = dt.datetime(1982, 1, 1)
    pmin, pmax = 5, 23
    nt = 32

    cubes = gather_data(path, prefix, t0, t1, pmin, pmax, nt)
    print(cubes)
    path = datadir
    iris.save(cubes, path + str(t0.year) + '-' + str(t1.year) + '_' +
              str(pmin) + '-' + str(pmax) + '.nc')

    return


def gather_data(path, prefix, t0, t1, pmin, pmax, nt):
    """
    Filenames follow the structure '{prefix}_{precision}.nc' where prefix is a
    generic prefix or the date in the format '{YYYYMMDDHH}'.

    Args:
        path (str): Directory containing forecast output
        prefix (str): Start of filename
        t0 (datetime.datetime): Start time of earliest forecast
        t1 (datetime.datetime): Start time of latest forecast
        pmin (int): Lowest precision forecast (sbits)
        pmax (int): Highest precision forecast (sbits)
        nt (int): Expected number of timesteps in each forecast

    Returns:
        cubes (iris.cube.CubeList): A cubelist containing all forecasts with
            cubes merged over new coordinates of start time and precision
    """
    all_cubes = iris.cube.CubeList()
    for time in pd.date_range(t0, t1, freq='MS'):
        print(time)

        if prefix == 'yyyymmddhh':
            filename = path + time.strftime('%Y%m%d%H')
        else:
            filename = path + prefix

        for n in range(pmin, pmax+1):
            cubes = iris.load(filename + '_' + str(n) + '.nc')
            coord = iris.coords.AuxCoord(points=n, long_name='precision')
            for cube in cubes:
                cube.add_aux_coord(coord)

            t0_dt(cubes)

            for cube in cubes:
                if len(cube.coord('forecast_period').points) == nt:
                    all_cubes.append(cube)

    cubes = all_cubes.merge()

    return cubes


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
