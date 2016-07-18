import iris
from iris.cube import CubeList


slices = [slice(0, 50), slice(15, 345), slice(15, 585)]


def ff2nc(infile, outfile, stash_maps=[], orography=None, slices=slices):
    cubes = iris.load(infile)

    # Define attributes of custom variables by stash mapping
    for stash_map in stash_maps:
        stash_map.remap_cubelist(cubes)

    for cube in cubes:
        # Remove unneeded attributes
        cube.attributes = {}

        # Remove all aux factories
        for factory in cube.aux_factories:
            cube.remove_aux_factory(factory)

        try:
            # Use the hybrid height coordinate as the main vertical coordinate
            cube.remove_coord('model_level_number')
            iris.util.promote_aux_coord_to_dim_coord(cube, 'level_height')
        except iris.exceptions.CoordinateNotFoundError:
            pass

        if orography is not None:
            cube.add_aux_coord(orography, [1, 2])

    cubes = CubeList([cube[slices] for cube in cubes])

    iris.save(cubes, outfile + '.nc')
