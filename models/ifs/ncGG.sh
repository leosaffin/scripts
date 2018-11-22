#!/usr/bin/env bash

# Postprocess ECMWF gridded output to gridded netCDF files
# Produces one file for each different vertical level in an output file

# Loop over wildcard files
for filename in "$@"
do
    # Force outdated cdo installed at Oxford to work with v2 grib files
    grib_set -s editionNumber=1 ${filename} tmp.grb

    # Copy to netcdf and interpolate to a regular lat/lon grid
    cdo -t ecmwf -f nc -R copy tmp.grb ${filename}.nc

    # Delete the history as the different dates don't allow merging forecasts
    ncatted -hO -a history,global,d,, ${filename}.nc
done

# Delete temporary file created by script
rm tmp.grb
