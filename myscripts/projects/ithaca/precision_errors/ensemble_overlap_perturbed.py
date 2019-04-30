import warnings
import random

import numpy as np
import iris

from myscripts.models.speedy import datadir
from myscripts.projects.ithaca.precision_errors import ensemble_overlap, ensemble_pdf


warnings.filterwarnings('ignore')


def main():
    path = datadir + 'stochastic/ensembles/'
    filenames = path + 'rp_physics_52b.nc', path + 'rp_physics_52b_v2.nc'
    bins = np.arange(4000, 6500)
    cs = iris.Constraint('Geopotential Height', pressure=500)
    ensembles = iris.load(filenames, cs)

    # Join the two ensembles together
    ensembles[1].coord('ensemble_member').points = np.array(range(21, 41))
    ensembles = ensembles.concatenate_cube()[:, 1:]
    members = list(ensembles.coord('ensemble_member').points)

    for n in range(43, 100):
        # Randomly split the ensemble members into to groups
        e1, e2 = shuffle_ensembles(members)

        print(e1, e2)

        # Calculate the overlapping coefficient for these two groups
        pdf1 = get_pdf(ensembles, e1, bins)
        pdf2 = get_pdf(ensembles, e2, bins)
        ovl = ensemble_overlap.overlapping_coefficient(pdf1, pdf2)

        iris.save(ovl, path + 'ovl_perturbed_{:02d}.nc'.format(n))

    return


def shuffle_ensembles(members):
    n = len(members)
    random.shuffle(members)

    return members[:n//2], members[n//2:]


def get_pdf(ensembles, members, bins):
    cs = iris.Constraint(ensemble_member=members)
    pdf = ensemble_pdf.pdf_aggregator_function(bins, ensembles.extract(cs).data, 0)
    pdf = ensemble_pdf.repackage_as_cube(pdf, bins, ensembles, 'ensemble_member')

    return pdf


if __name__ == '__main__':
    main()
