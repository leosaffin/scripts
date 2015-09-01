class Subset(object):
    """Class for describing a subset of a domain
    """

    def __init__(self, zmin, zmax, ymin, ymax, xmin, xmax):
        """
        Args:
            zmin (int): Index of lowest z-point
            zmax (int): Index of highest z-point
            ymin (int): Index of lowest y-point
            ymax (int): Index of highest y-point
            xmin (int): Index of lowest x-point
            xmax (int): Index of highest x-point
        """
        self.zmin = zmin
        self.zmax = zmax
        self.ymin = ymin
        self.ymax = ymax
        self.xmin = xmin
        self.xmax = xmax

    def slice(self, cube):
        """Slices the cube to only have the subset dimensions

        Args:
            cube (iris.cube.Cube, np.array):
        """
        if cube.ndim == 2:
            return cube[self.ymin:self.ymax, self.xmin:self.xmax]

        elif cube.ndim == 3:
            return cube[self.zmin:self.zmax, self.ymin:self.ymax,
                        self.xmin:self.xmax]

        else:
            raise IndexError


# Define subsets to be analysed
subsets = {'full': Subset(0, 50, 0, 330, 0, 570),
           'north': Subset(0, 50, 165, 300, 0, 570),
           'south': Subset(0, 50, 0, 165, 0, 570)
           }
