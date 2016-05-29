import pygame
import matplotlib
from matplotlib import cm
from mymodule import convert
from scripts import case_studies


def main(cube, vmin=None, vmax=None, cmap='cubehelix', k=0):
    """
    Args:
        cube (np.array): array(z,y,x)

        vmin, vmax (int or float): Maximum and minimum

        cmap (str): Name of a matplotlib colormap (default is cubehelix)

        k (int): Vertical level to show first (default is 0)
    """
    # Reverse the y-axis to work in pygame coordinates
    data = cube.data.transpose()[:, ::-1, :]
    nx, ny, nz = data.shape

    # Set up a matplotlib colormap
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    mapping = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap(cmap))

    # Start a pygame window
    pygame.init()
    surface = pygame.display.set_mode([nx, ny])
    copy_array_to_pixels(data[:, :, k], surface, mapping)

    clock = pygame.time.Clock()
    running = True
    # Main loop
    while(running):
        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Use up and down keys to change vertical level plotted
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    k = (k + 1) % nz
                elif event.key == pygame.K_DOWN:
                    k = (k - 1) % nz

                # Update the display pixels with the new level
                copy_array_to_pixels(data[:, :, k], surface, mapping)
        clock.tick(30)
        pygame.display.update()

    pygame.quit()


def make_mapping(vmin, vmax, cmap):
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    mapping = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap(cmap))

    return mapping


def copy_array_to_pixels(array, surface, mapping):
    pixelarray = pygame.surfarray.pixels3d(surface)
    pixelarray[:, :] = mapping.to_rgba(array)[:, :, 0:3] * 255
    surface.unlock()

    return

if __name__ == '__main__':
    forecast = case_studies.iop5()
    cubes = forecast.set_lead_time(hours=36)
    cube = convert.calc('ertel_potential_vorticity', cubes)
    main(cube, vmin=0, vmax=10, cmap='plasma')
