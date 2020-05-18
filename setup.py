#!/usr/bin/env python

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['scitools-iris', 'numpy', 'scipy', 'matplotlib', 'metpy']

setup_requirements = []

test_requirements = []



setup(
    author="Leo Saffin",
    author_email='string_buster@hotmail.com',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Atmospheric Science'],
    description="Scripts for work.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='',
    name='myscripts',
    packages=find_packages(include=['myscripts']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/LSaffin/myscripts',
    version='0.2',
)
