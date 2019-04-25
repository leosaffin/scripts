import numpy as np
import iris
from myscripts import statistics


def forecast_errors(forecast1, forecast2, cs):
    """Print summary differences between two forecasts

    Args:
        forecast1 (iris.cube.CubeList):
        forecast2 (iris.cube.CubeList):
        cs (iris.Constraint):
    """
    z1 = iris.load_cube(forecast1, cs)
    z2 = iris.load_cube(forecast2, cs)

    diff = z1 - z2

    rms_diff = statistics.rms_diff(z1, z2)
    mean_diff = statistics.mean_diff(z1, z2)

    print('\n'.join([
        'Forecast errors in {}'.format(z1.name()),
        'RMS Error: {}'.format(np.squeeze(rms_diff.data)),
        'Mean Error: {}'.format(np.squeeze(mean_diff.data)),
        'Max Error: {}'.format(diff.data.max()),
        'Min Error: {}'.format(diff.data.min())
    ]))

    return
