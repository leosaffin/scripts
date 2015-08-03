from math import atan2
import numpy as np
import ffronts


k1 = 0.4
k2 = 1.45
tol = 0.1
m = 1 / np.sqrt(2)


def main(tau, dx):
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
    abs_grad_tau = np.sqrt(grad_tau[:, :, 0]**2 + grad_tau[:, :, 1]**2)
    grad_abs_grad_tau = ffronts.grad2d(abs_grad_tau, dx)

    # Calculate the locating variable
    loc = locating_variable(grad_abs_grad_tau)

    # Calculate the two masking variables
    mask = np.logical_and(m1(tau, grad_tau, grad_abs_grad_tau, dx),
                          m2(tau, grad_tau, grad_abs_grad_tau, dx))

    # Find where the locating variable is zero
    fronts = np.logical_and(loc > tol, mask)

    return fronts


def locating_variable(grad_abs_grad_tau):
    """
    'At each gridpoint \(\hat{s}\) is evaluated by computing a mean of five
    values of \(\nabla \nabla \tau \), treating each as an axis as opposed to a
    vector
    """
    # Derive a five point mean axis
    beta, D = ffronts.mean_axis(grad_abs_grad_tau)
    # Resolve the four outer vectors into the positive \(\hat{s}\) direction
    # and compute the total divergence of the resolved vectors using simple
    # first order finite differencing
    loc = ffronts.div2d(beta, D)

    return loc


def m1(tau, grad_tau, grad_abs_grad_tau, dx):
    # Calculate \(\nabla \tau \cdot \nabla |\nabla \tau |\))
    y = grad_tau * grad_abs_grad_tau
    y = y[:, :, 0] + y[:, :, 1]
    # Average over 5 gridpoint array
    y = ffronts.fivepointave(y)
    # Use sign
    y = grad_abs_grad_tau * np.sign(y)

    mask = y > k1

    return mask


def m2(tau, abs_grad_tau, grad_abs_grad_tau, dx):

    abs_grad_abs_grad_tau = np.sqrt(grad_abs_grad_tau**2[:, :, 0] +
                                    grad_abs_grad_tau[:, :, 1]**2)
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
    D_mean = (1 / len(x)) * np.sqrt(P**2 + Q**2)
    return beta_mean, D_mean
