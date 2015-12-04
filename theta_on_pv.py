import numpy as np
import matplotlib.pyplot as plt
from mymodule import files, convert, grid, interpolate, plot


def main(filename, cscale):
    """
    """
    theta = load(filename)
    theta_pv2 = interpolate.to_level(theta, ertel_potential_vorticity=[2.])[0]
    plot.contourf(theta_pv2, cscale, cmap='cubehelix_r', extend='both')
    plt.show()


def load(filename):
    """
    """
    cubelist = files.load(filename)
    theta = convert.calc('air_potential_temperature', cubelist)

    # Add PV as a coordinate
    pv = convert.calc('ertel_potential_vorticity', cubelist)
    coord = grid.make_coord(pv)
    theta.add_aux_coord(coord, [0, 1, 2])

    return theta

if __name__ == '__main__':
    filename = '../iop5_36h.pp'
    cscale = np.linspace(270, 350, 17)
    main(filename, cscale)
