import pygame
import numpy as np
import matplotlib
from matplotlib import cm

frames_per_second = 60


def pcolor(data, vmin=None, vmax=None, cmap='cubehelix', k=0, t=0):
    """Quickly navigate a 4d array using arrow keys

    When run a window will pop up showing a plot of an x-y cross section of the
    given data at a specified height and time index. Pressing the up and down
    arrows will modify the height index and pressing left and right will modify
    the time index. The window will be updated with the new cross section.

    Produces a pcolormesh like plot by directly modifying pixels on the screen.
    Uses matplotlib colourscales to define the mapping to RGB values.

    Args:
        data (np.array): 4d array with shape (t,z,y,x). Can also be input with
            a 3d array which will be copied into a 4d array with t-dimension 1.

        vmin, vmax (scalar): Maximum and minimum for the colorscale

        cmap (str): Name of a matplotlib colormap (default is cubehelix)

        k (int): Vertical level to show first (default is 0)

        t (int): Time index to show first (default is 0)
    """
    # Check the array is the correct dimension
    if data.ndim != 4:
        if data.ndim == 3:
            data = np.expand_dims(data, axis=0)
        else:
            raise ValueError('Input array must have 3 or 4 dimensions')

    # Transpose and reverse the y-axis to work in pygame coordinates
    data = data.transpose()[:, ::-1, :, :]
    nx, ny, nz, nt = data.shape

    # Set up a matplotlib colourscale mapping between values and colours
    mapping = make_mapping(vmin, vmax, cmap)

    # Start a pygame window
    pygame.init()
    surface = pygame.display.set_mode([nx, ny])

    # Show the initial array
    copy_array_to_pixels(data[:, :, k, t], surface, mapping)
    pygame.display.update()

    # Main loop
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(frames_per_second)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Use up and down keys to change vertical level plotted
                if event.key == pygame.K_UP:
                    k = (k + 1) % nz
                elif event.key == pygame.K_DOWN:
                    k = (k - 1) % nz

                # Use left and right keys to change time
                elif event.key == pygame.K_LEFT:
                    t = (t - 1) % nt
                elif event.key == pygame.K_RIGHT:
                    t = (t + 1) % nt

                # Update the display pixels with the new level
                copy_array_to_pixels(data[:, :, k, t], surface, mapping)
                pygame.display.update()

    pygame.quit()


def make_mapping(vmin, vmax, cmap):
    """Create an object for mapping from values to colours
    """
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    mapping = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap(cmap))

    return mapping


def copy_array_to_pixels(array, surface, mapping):
    pixelarray = pygame.surfarray.pixels3d(surface)
    pixelarray[:, :] = mapping.to_rgba(array)[:, :, 0:3] * 255
    surface.unlock()

    return


if __name__ == '__main__':
    from mymodule import convert
    from scripts import case_studies
    forecast = case_studies.iop5()
    cubes = forecast.set_lead_time(hours=36)
    cube = convert.calc('ertel_potential_vorticity', cubes)
    pcolor(cube.data, vmin=0, vmax=10, cmap='plasma')
