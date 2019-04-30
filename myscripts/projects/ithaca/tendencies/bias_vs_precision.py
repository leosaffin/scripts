import numpy as np
import matplotlib.pyplot as plt
from irise.plot.util import legend
from myscripts.statistics import mean_diff
from myscripts.models import speedy
from myscripts.projects.ithaca.tendencies import load_tendency


def main():
    sigma = speedy.sigma_levels[1]
    sbits = np.arange(5, 24)

    # Loop over physics schemes
    for scheme in speedy.physics_schemes:
        plp = speedy.physics_schemes[scheme]
        fp = load_tendency('Specific Humidity', sigma=sigma, precision=52)
        rp = load_tendency('Specific Humidity', rp_scheme=speedy.to_filename(scheme),
                           sigma=sigma, precision=sbits)

        # Calculate error of nonzero gridpoints
        rp.data = np.ma.masked_where([..., fp.data] == 0, rp.data - fp.data)
        mean_error = mean_diff(rp, 0)
        plp.plot(mean_error, label=scheme)

    plt.xlabel('Precision [sbits]')
    plt.ylabel('Mean relative error')
    legend(key=lambda x: speedy.physics_schemes[x[0]].idx)
    plt.show()

    return


if __name__ == '__main__':
    main()
