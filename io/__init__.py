import iris
from mymodule import files


def ff2nc(infile, outfile, stash_maps=[]):
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

    iris.save(cubes, outfile + '.nc')
