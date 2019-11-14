import math

import numpy as np


def get_row_and_column_index(n, ncols):
    row = n // ncols
    column = n - row * ncols

    return row, column


def get_cscale_limit(data, old_limit):
    limit = np.abs(data).max()
    if limit > 0:
        # Round to one decimal place but always up
        order_of_magnitude = 10 ** math.floor(np.log10(limit))
        limit = math.ceil(limit / order_of_magnitude) * order_of_magnitude

    limit = max(limit, old_limit)

    return limit
