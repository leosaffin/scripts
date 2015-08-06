from math import atan2
import numpy as np
import matplotlib.pyplot as plt
import iris
from mymodule import convert, grid, interpolate
import ffronts


k1 = 0.4 * (12 ** 2 / 100 ** 2)
k2 = 1.45 * (12 / 100)
dx = 1.0
tol = 1
m = 1 / np.sqrt(2)


def main(tau):
    """
    Args:
        tau (iris.cube.Cube): A 2d iris cube of an appropriate variable for
            locating fronts

    Returns:
        fronts (list):
    """
    # Calculate grad(tau)
    grad_tau = ffronts.grad2d(tau, dx)

    # Calculate grad_abs_grad_tau
    grad_abs_grad_tau = ffronts.grad2d(abs2d(grad_tau), dx)

    # Calculate the locating variable
    loc = locating_variable(grad_abs_grad_tau, dx)
    mask1 = m1(grad_tau, grad_abs_grad_tau, dx)
    mask2 = m2(grad_tau, grad_abs_grad_tau, dx)

    # Find where the locating variable is zero
    fronts = np.logical_and(loc < tol, loc > -tol)
    fronts = np.logical_and(fronts, np.logical_and(mask1, mask2))

    return fronts


def locating_variable(grad_abs_grad_tau, dx):
    """
    'At each gridpoint \(\hat{s}\) is evaluated by computing a mean of five
    values of \(\nabla \nabla \tau \), treating each as an axis as opposed to a
    vector
    """
    # Derive a five point mean axis
    means = ffronts.mean_axis(grad_abs_grad_tau, dx)
    beta = means[0, :, :]
    D = means[1, :, :]
    # Resolve the four outer vectors into the positive \(\hat{s}\) direction
    # and compute the total divergence of the resolved vectors using simple
    # first order finite differencing
    loc = ffronts.div2d(beta, D, dx)

    return loc


def m1(grad_tau, grad_abs_grad_tau, dx):
    """Calculate the first masking variable
    """
    # Calculate grad(tau).grad(|grad(tau|)
    y = grad_tau * grad_abs_grad_tau
    y = y[:, :, 0] + y[:, :, 1]
    # Average over 5 gridpoint array
    y = ffronts.fivepointave(y, dx)
    # Use sign
    z = abs2d(grad_abs_grad_tau)
    y = z * np.sign(y)
    return y
    mask = y > k1
    return mask


def m2(grad_tau, grad_abs_grad_tau, dx):
    """
    """
    y = abs2d(grad_tau) + m * dx * abs2d(grad_abs_grad_tau)
    return y
    mask = y > k2
    return mask


def abs2d(x):
    """Calculate the absolute value of a 2D array of vectors
    """
    y = np.sqrt(x[:, :, 0] ** 2 + x[:, :, 1] ** 2)
    return y


if __name__ == '__main__':
    filename = '/projects/diamet/lsaffi/xjjhq/*24.pp'
    cubes = iris.load(filename)
    cubes.remove(cubes.extract('air_pressure')[0])
    p = cubes.extract('air_pressure')[0]
    p.convert_units('hPa')
    theta = convert.calc('air_potential_temperature', cubes)
    newcoord = grid.make_coord(p)
    theta.add_aux_coord(newcoord, [0, 1, 2])
    theta850 = interpolate.to_level(theta, air_pressure=[850])
    fronts = main(theta850[0].data)
    plt.contourf(fronts)
    plt.savefig('/home/lsaffi/plots/IOP5/24h_fronts.png')
