from math import atan2


def main(tau):
    """
    Args:
        tau (iris.cube.Cube): A 2d iris cube of an appropriate variable for
            locating fronts

    Returns:
        fronts (list):
    """
    # Calculate axis at each gridpoint
    pass


def locating_variable():
    """
    'At each gridpoint \(\hat{s}\) is evaluated by computing a mean  of five
    values of \(\nabla \nabla \tau \), treating each as an axis as opposed to a
    vector
    """

    # Derive a five point mean Axis
    mean_axis()
    # Resolve the four outer vectors into the positive \(\hat{s}\) direction

    # Compute the total divergence of the resolved vectors using simple first
    # order finite differencing


def mean_axis(x):
    """
    """
    P = sum([D * cos(2 * beta) for D, beta in x])
    Q = sum([D * sin(2 * beta) for D, beta in x])
    beta_mean = 0.5 * atan2(Q, P)
    D_mean = (1 / n) * sqrt(P**2 + Q**2)
    return beta_mean, D_mean
