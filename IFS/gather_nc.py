"""Collapse output of IFS over multiple timesteps into single output file

"""
import iris
from iris.util import unify_time_units
from iris.exceptions import ConstraintMismatchError
from mymodule import grid
from myscripts.IFS import datadir, replace_names


def main():
    path = datadir + 't159/'
    exp_id = 'b221'
    files_in = 'ICMGG' + exp_id + '+0000??.nc'
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
    cubes.sort(key=lambda x: x.name())

    unify_time_units(cubes)

    # Add the names of custom output fields
    replace_names(cubes)

    # Remove hybrid height cubes and add as coordinates instead
    replace_hybrid_heights(cubes)

    print(cubes)
    iris.save(cubes, file_out)

    return


def replace_hybrid_heights(cubes):
    hybrid_coords = iris.cube.CubeList()
    for letter in ['A', 'B']:
        try:
            points = cubes.extract_strict(
                'hybrid {0} coefficient at layer midpoints'.format(letter))
            cubes.remove(points)

            bounds = cubes.extract_strict(
                'hybrid {0} coefficient at layer interfaces'.format(letter))
            cubes.remove(bounds)

            hybrid_coords.append(grid.make_coord(points, bounds=bounds))
        except ConstraintMismatchError:
            pass

    for cube in cubes:
        cube_coords = [coord.name() for coord in cube.dim_coords]
        # Add hybrid height coordinate only to cubes on model levels
        if 'hybrid level at layer midpoints' in cube_coords:
            idx = cube_coords.index('hybrid level at layer midpoints')
            for coord in hybrid_coords:
                cube.add_aux_coord(coord, idx)
    return


if __name__ == '__main__':
    main()
