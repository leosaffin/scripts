#!/usr/bin/env bash

file=$1
filename=${file%.ctl}
cdo -f nc import_binary ${file} ${filename}.nc

# Make the NetCDF file CF Conventions conforming
ncatted -a long_name,lev,o,c,sigma ${filename}.nc
ncatted -a units,lev,d,, ${filename}.nc

# Delete the history as the different dates don't allow merging forecasts
ncatted -hO -a history,global,d,, ${filename}.nc
