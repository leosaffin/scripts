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
    abs_grad_tau = np.sqrt(grad_tau[:, :, 0] ** 2 + grad_tau[:, :, 1] ** 2)
    grad_abs_grad_tau = ffronts.grad2d(abs_grad_tau, dx)

    # Calculate the locating variable
    loc = locating_variable(grad_abs_grad_tau, dx)
    mask = np.logical_and(m1(tau, grad_tau, grad_abs_grad_tau, dx),
                          m2(tau, abs_grad_tau, grad_abs_grad_tau, dx))

    # Find where the locating variable is zero
    fronts = np.logical_and(loc < tol, loc > -tol)
    fronts = np.logical_and(fronts, mask)

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


def m1(tau, grad_tau, grad_abs_grad_tau, dx):
    # Calculate \(\nabla \tau \cdot \nabla |\nabla \tau |\))
    y = grad_tau * grad_abs_grad_tau
    y = y[:, :, 0] + y[:, :, 1]
    # Average over 5 gridpoint array
    y = ffronts.fivepointave(y, dx)
    # Use sign
    z = np.sqrt(grad_abs_grad_tau[:, :, 0] ** 2 +
                grad_abs_grad_tau[:, :, 1] ** 2)
    y = z * np.sign(y)

    mask = y > k1
    return mask


def m2(tau, abs_grad_tau, grad_abs_grad_tau, dx):

    abs_grad_abs_grad_tau = np.sqrt(grad_abs_grad_tau[:, :, 0] ** 2 +
                                    grad_abs_grad_tau[:, :, 1] ** 2)
    y = abs_grad_tau + m * dx * abs_grad_abs_grad_tau

    mask = y > k2
    return mask


def mean_axis(x):
    """ Calculate the mean axis as described in appendix 2 of Hewson 1998

    Args:
        x (list): A list of tuples containing size and angle of the axis to be
            averaged over
    """
    P = sum([D * np.cos(2 * beta) for D, beta in x])
    Q = sum([D * np.sin(2 * beta) for D, beta in x])
    beta_mean = 0.5 * atan2(Q, P)
    D_mean = (1 / len(x)) * np.sqrt(P ** 2 + Q ** 2)
    return beta_mean, D_mean


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
