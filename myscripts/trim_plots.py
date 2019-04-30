#!/usr/bin/env python

import glob
import os


def main():
    """Run this to trim every png plot in a directory
    """
    for filename in glob.glob('*.png'):
        os.system('convert -trim ' + filename + ' ' + filename)

if __name__ == '__main__':
    main()
