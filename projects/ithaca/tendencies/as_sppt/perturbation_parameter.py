"""
:math:`T = (1+e) \cdot P`

Error in tendency should be proportional to tendency
The distribution of `e` due to rounding can be estimated from the tendencies
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sb
from myscripts.projects.ithaca.tendencies.as_sppt import load_tendency


def main():
    rp, fp = load_tendency(
        variable='Temperature',
        scheme='all physics processes',
        precision=10,
        forecast_period=2 / 3,
        sigma=0.95,
        total=True)

    error_distribution(rp, fp)

    return


def error_distribution(rp, fp):
    e, n_activated, n_deactivated, n_zeros = estimate_random_parameter(rp, fp)

    e = e.data.compressed()
    e, clipped = clip_outliers(e)

    ax = sb.distplot(e, kde=True, fit=norm, bins=100)
    y0, y1 = ax.get_ylim()
    sigma = overlay_gaussian(e, y1)

    textstr = '\n'.join([
        'Zero Tendency: {}'.format(n_zeros),
        'Activated: {}'.format(n_activated),
        'Deactivated: {}'.format(n_deactivated),
        'Clipped: {}'.format(clipped),
        r'$\sigma={:.4f}$'.format(sigma)])

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='lavender', alpha=1)

    # place a text box in upper left in axes coords
    ax.text(0.6, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    plt.show()
    return


def estimate_random_parameter(rp, fp):
    """
    :math: e = \frac{T}{P} - 1
    """
    # Exclude points where fp=0 or rp=0
    mask, n_activated, n_deactivated, n_zeros = filter_active_deactive(rp, fp)

    # Calculate the notional SPPT random parameter
    e = rp/fp - 1

    # Masked activated and deactived gridpoints
    e.data = np.ma.masked_where(mask, e.data)

    return e, n_activated, n_deactivated, n_zeros


def filter_active_deactive(rp, fp):
    # Ignore gridboxes where reduced precision has activated or deactivated the
    # physics scheme. Will give e=infinity or e=-1 respectively
    activated = np.logical_and(rp.data != 0, fp.data == 0)
    deactivated = np.logical_and(rp.data == 0, fp.data != 0)
    zeros = np.logical_and(rp.data == 0, fp.data == 0)
    mask = np.logical_or(np.logical_or(activated, deactivated), zeros)

    # Return the counts of these gridpoints
    n_activated = np.count_nonzero(activated)
    n_deactivated = np.count_nonzero(deactivated)
    n_zeros = np.count_nonzero(zeros)

    return mask, n_activated, n_deactivated, n_zeros


def clip_outliers(e):
    count = len(e)
    e = np.ma.masked_where(e < -1, e)
    e = np.ma.masked_where(e > 1, e)
    e = e.compressed()
    clipped = count - len(e)
    return e, clipped


def overlay_gaussian(e, magnitude):
    sigma = np.std(e)
    x = np.arange(e.min(), e.max(), 0.001)
    y = magnitude * gaussian(x, 0., sigma)

    plt.plot(x, y)

    return sigma


def gaussian(x, mu, sigma):
    return np.exp(-((x - mu) / sigma)**2 / 2.)


if __name__ == '__main__':
    main()
