#!/usr/bin/env bash
for var in "$@"
do
#    grib_set -s editionNumber=1 ${var} tmp.g1
    grib_copy ${var} ${var}_[typeOfLevel].grb
#    cdo -t ecmwf -f nc copy ${var}_isobaricInhPa.grb ${var}_isobaricInhPa.nc
    cdo -t ecmwf -f nc copy -sp2gpl -dv2uvl -sellevel,85000 ${var}_isobaricInhPa.grb ${var}_uv_pl850.nc
    rm -f *.grb
done
