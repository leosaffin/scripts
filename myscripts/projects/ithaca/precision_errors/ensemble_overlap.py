import numpy as np
import iris
from myscripts.statistics import global_mean
from myscripts.models.speedy import datadir


def main():
    path = datadir + 'stochastic/ensembles/'

    pdf1 = iris.load_cube(path + 'rp_physics_52b_pdf.nc')
    pdf2 = iris.load_cube(path + 'rp_surface_fluxes_9b_pdf.nc')

    ovl = overlapping_coefficient(pdf1, pdf2)

    iris.save(ovl, path + 'overlap_52_sflx9.nc')

    return


def overlapping_coefficient(pdf1, pdf2):
    overlap = np.sum(np.minimum(pdf1.data, pdf2.data), axis=0)
    overlap = pdf1[0].copy(data=overlap)
    mean_overlap = global_mean(overlap)
    return mean_overlap


if __name__ == '__main__':
    main()
