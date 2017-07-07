import numpy as np
from mymodule import grid, variable
import pvi

omega = 7.2921e-5  # Coriolis Term
gravity = 9.81     # Gravitational Acceleration
f_0 = 1.e-4        # Typical Coriolis Parameter
ll = 12000         # dy in m
tho = f_0 * f_0 * ll * ll


def pv_invert(pv, boundary_theta, thrs1=0.1, relaxation_parameter=0.4,
              max_iterations=1999, max_cycles=999, omega_s=1.7, omega_h=1.4):
    """Inverts pv to find balanced geopotential and streamfunction

    Args:
        pv (iris.cube.Cube):

        boundary_theta (iris.cube.Cube):
    """

    threshold = gravity * thrs1 / tho

    lon, lat = grid.true_coords(pv)

    laplacian_coefficients = coefficients(len(lat))
    coriolis_parameter = 2 * omega * np.sin(lat)
    cos_latitude = np.cos(lat)
    geopotential_height, streamfunction = first_guess(pv)

    # Extract the vertical coordinate from the cube
    pressure = grid.make_cube(pv, 'air_pressure')
    exner = variable.exner(pressure)

    # Perform the PV inversion
    geopotential_height, streamfunction, pv_out, boundary_theta = \
        pvi.balnc(coriolis_parameter, cos_latitude, laplacian_coefficients,
                  geopotential_height, streamfunction, pv.data,
                  boundary_theta.data, exner, relaxation_parameter, threshold,
                  max_iterations, max_cycles, omega_s, omega_h)

    return pv_out, geopotential_height, streamfunction


def coefficients(N):
    laplacian_coefficients = np.zeros([N, 5])
    laplacian_coefficients[:, 0] = 1.0
    laplacian_coefficients[:, 1] = 1.0
    laplacian_coefficients[:, 2] = -4.0
    laplacian_coefficients[:, 3] = 1.0
    laplacian_coefficients[:, 4] = 1.0

    return laplacian_coefficients


def first_guess(pv):
    """Gives a first guess for streamfunction and geopotential height
    """
    geopotential_height = np.ones_like(pv.data)
    streamfunction = geopotential_height
    return geopotential_height, streamfunction
