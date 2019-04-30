#!/usr/bin/env bash

# Postprocess ECMWF spectral harmonic output to netCDF files
# Produces one file for each different vertical level in an output file

# Loop over wildcard files
for filename in "$@"
do
    # Split variables into separate files by vertical coordinate
    grib_copy ${filename} ${filename}_[typeOfLevel].grb

    # Loop over each new grib file
    for grib_file in ${filename}_*.grb
    do
        # Convert from spectral coefficient grib file to gridded netcdf file
        cdo -t ecmwf -f nc copy ${grib_file} ${grib_file/.grb/.nc}

        # Delete the history as the different dates don't allow merging forecasts
        ncatted -hO -a history,global,d,, ${grib_file/.grb/.nc}
    done
done