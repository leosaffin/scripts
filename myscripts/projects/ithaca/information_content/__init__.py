import numpy as np


def entropy(p_x):
    r"""
    ..math:: H(x) = \sum_i x \text{log}(x)

    Args:
        p_x: Probability distribution of x in discrete bins

    Returns:
        The entropy of x
    """
    p_x = np.ma.masked_where(p_x == 0, p_x)
    h = -np.ma.sum(p_x * np.log(p_x))

    return h


def conditional_entropy(predictor, predictand, condition, lag, bins):
    """

    Args:
        predictor:
        predictand:
        condition:
        lag:
        bins:

    Returns:

    """
    # Find the data in the predictand that corresponds to a chosen state in the
    # predictor a set amount of time ahead
    indices = np.where(condition(predictor))[0] + lag
    # Remove indices that are outside the data
    indices = indices[np.where(indices < len(predictand))]
    data = predictand[indices]

    # Calculate the conditional probability distribution
    p_x = np.histogram(data, bins=bins)[0] / len(data)

    return entropy(p_x)


def information_content(predictor, predictand, nbins, max_lag):
    r"""
    ..math:: I(\tau) = H - q_0 H_{b0} - q_1 H_{b1} \ldots

    Returns:

    """
    nt = len(predictand)
    quantiles_predictor = np.sort(predictor)[nt // nbins:-1:nt // nbins]
    bins_predictor = [-np.inf] + [x for x in quantiles_predictor] + [np.inf]

    quantiles_predictand = np.sort(predictand)[nt // nbins:-1:nt // nbins]
    bins_predictand = [-np.inf] + [x for x in quantiles_predictand] + [np.inf]

    # Climatological probability distribution and entropy
    p_x = np.histogram(predictand, bins=bins_predictand)[0] / nt
    h_x = entropy(p_x)

    I_b = []
    for n in range(max_lag):
        print(n)
        h_bn = np.zeros(nbins)
        for m in range(nbins):
            # Conditional p_x on being in each quantile
            h_bn[m] = conditional_entropy(
                predictor, predictand,
                lambda x: np.logical_and(x >= bins_predictor[m],
                                         x < bins_predictor[m+1]),
                n, bins_predictand)

        I_b.append(h_x - np.sum(p_x*h_bn))
    return I_b
