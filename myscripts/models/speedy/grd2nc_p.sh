#!/usr/bin/env bash

# Convert a .ctl mapping of GrADS files (.grd) to netCDF
# Input argument is the name of the .ctl file
# Resulting netCDF has the same name with .ctl replaced by .nc
file=$1
filename=${file%.ctl}

# Copy the file to netCDF
cdo -f nc import_binary ${file} ${filename}.nc

# Make the NetCDF file CF Conventions conforming
ncatted -a long_name,lev,o,c,pressure ${filename}.nc
ncatted -a units,lev,o,c,hPa ${filename}.nc

# Delete the history as the different dates don't allow merging forecasts
ncatted -hO -a history,global,d,, ${filename}.nc
