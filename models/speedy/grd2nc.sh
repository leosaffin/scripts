#!/usr/bin/env bash

file=$1
filename=${file%.ctl}
cdo -f nc import_binary ${file} ${filename}.nc

# Make the NetCDF file CF Conventions conforming
ncatted -a standard_name,lev,c,c,atmosphere_sigma_coordinate ${filename}.nc
ncatted -a units,lev,d,c, ${filename}.nc

# Delete the history as the different dates don't allow merging forecasts
ncatted -hO -a history,global,d,, ${filename}.nc
