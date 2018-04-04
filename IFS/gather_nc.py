"""Collapse output of IFS over multiple timesteps into single output file

"""

import iris
from iris.util import unify_time_units


def main():
    path = '/home/saffin/cirrus/openifs/t21test/output/rpe_new/'
    files_in = 'ICMGGepc8+0000??_isobaricInhPa.nc'
    file_out = 'ICMGG_prognostics.nc'

    gather_files(path + files_in, path + file_out)

    return


def gather_files(files_in, file_out):
    """
    Args:
        files_in (str):
        file_out (str):
    """
    cubes = iris.load(files_in)
    unify_time_units(cubes)
    for cube in cubes:
        cube.attributes = {}

    newcubes = cubes.concatenate()
    print newcubes

    iris.save(newcubes, file_out)

    return


if __name__ == '__main__':
    main()
