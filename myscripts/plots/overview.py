"""

Usage:
    overview.py <model_data> <yaml_file> [--output_path=<path>]

Arguments:
    <model_data>
        File containing variables to be plotted
    <yaml_file>
        Specification of variables and levels to plot
Options:
    --output_path=<path>
        Directory to save figures [default: "./"]
    -h --help
        Show help
"""

import docopt
import yaml

import iris
from iris.util import squeeze
import matplotlib.pyplot as plt

import irise
from irise import convert, plot


def main():
    arguments = docopt.docopt(__doc__)

    print(arguments)

    cubes = iris.cube.CubeList(
        [squeeze(cube) for cube in irise.load(arguments["<model_data>"])]
    )

    with open(arguments["<yaml_file>"]) as f:
        info = yaml.safe_load(f)

    generate_overview(cubes, info, path=arguments["--output_path"])


def generate_overview(cubes, info, path="./"):
    for field in info["single_level_fields"]:
        name = field.pop("name")
        cube = convert.calc(name, cubes)
        plot.pcolormesh(cube, **field)
        plt.savefig("{}{}.png".format(path, name))
        plt.clf()

    for levels in info["vertical_coordinates"]:
        for field in info["multi_level_fields"]:
            make_plots(field.copy(), cubes, levels, path)
        for field in info["vertical_coordinates"]:
            if field["name"] != levels["name"]:
                make_plots(field.copy(), cubes, levels, path)


def make_plots(field, cubes, levels, path):
    name = field.pop("name")
    cube = convert.calc(name, cubes, levels=(levels["name"], levels["values"]))
    for n, level in enumerate(levels["values"]):
        plot.pcolormesh(cube[n], **field)
        plt.savefig("{}{}_{}_{}.png".format(
            path, name, levels["name"], levels["values"][n])
        )
        plt.clf()


if __name__ == '__main__':
    main()
