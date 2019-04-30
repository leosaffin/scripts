"""Check the correlation between PV tracers and full PV
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from irise import convert
from myscripts.models.um import case_studies


def main(cubes):
    # Load the data
    res = convert.calc('residual_pv', cubes)
    pv = convert.calc('ertel_potential_vorticity', cubes)
    expected_pv = pv - res

    stats = []
    # Calculation correlation on each model level
    for n in range(pv.shape[0]):
        stats.append(linregress(pv[n].data.flatten(),
                                expected_pv[n].data.flatten()))

    stats = np.array(stats)
    print(stats.shape)

    fig = plt.figure(figsize=(18, 20))
    ax = plt.subplot2grid((2, 2), (0, 0))
    plt.plot(stats[:, 2])
    plt.title('Correlation Coefficient')

    ax = plt.subplot2grid((2, 2), (1, 0))
    plt.plot(stats[:, 0])
    plt.title('Gradient')

    ax = plt.subplot2grid((2, 2), (1, 1))
    plt.plot(stats[:, 1])
    plt.title('Intercept')

    plt.show()

if __name__ == '__main__':
    forecast = case_studies.iop5b.copy()
    cubes = forecast.set_lead_time(hours=12)

    main(cubes)
