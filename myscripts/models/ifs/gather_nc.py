"""Collapse output of IFS over multiple timesteps into single output file

"""
import iris
from iris.coords import AuxCoord
from iris.util import unify_time_units
from iris.exceptions import ConstraintMismatchError
from irise import grid
from myscripts.models.ifs import datadir, replace_names


def main():
    path = datadir + 't159/'
    exp_id = 'b221'
    files_in = 'ICMGG' + exp_id + '+0000??.nc'
    file_out = 'ICMGG_prognostics.nc'

    #cubes = gather_files(path + files_in)
    cubes = multiple_precisions(path, files_in, range(9, 24))

    print(cubes)
    iris.save(cubes, path+file_out)

    return


def multiple_precisions(path, files_in, precisions):
    all_forecasts = iris.cube.CubeList()
    for precision in precisions:
        pcoord = AuxCoord(points=precision, long_name='precision')

        cubes = gather_files(path + 'p' + str(precision) + '/' + files_in)
        for cube in cubes:
            cube.attributes = {}
            cube.add_aux_coord(pcoord)

        newcubes = cubes.concatenate()

        for cube in newcubes:
            all_forecasts.append(cube)

    all_forecasts = all_forecasts.merge()
    print(all_forecasts)

    return all_forecasts


def gather_files(files_in):
    """
    Args:
        files_in (str):
    """
    cubes = iris.load(files_in)
    cubes.sort(key=lambda x: x.name())

    unify_time_units(cubes)

    # Add the names of custom output fields
    replace_names(cubes)

    # Remove hybrid height cubes and add as coordinates instead
    replace_hybrid_heights(cubes)

    return cubes


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
            # If the cubelist doesn't have hybrid height just return
            return

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
