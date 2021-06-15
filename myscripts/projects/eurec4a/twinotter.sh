#!/usr/bin/env bash

met="/home/lsaffin/Documents/meteorology"
data="${met}/data/eurec4a"
flight_data="${data}/twin-otter"
flight_segments=${met}/programming/flight-phase-separation/flight_phase_files/TO
goes_data="${data}/goes/2km_10min/2020"
output="${met}/output/eurec4a/twin-otter"

declare -A flight_segments_fnames

flight_segments_fnames[330]="EUREC4A_TO_Flight-Segments_20200124a_0.1.yaml"
flight_segments_fnames[331]="EUREC4A_TO_Flight-Segments_20200124b_0.1.yaml"
flight_segments_fnames[332]="EUREC4A_TO_Flight-Segments_20200126a_0.1.yaml"
flight_segments_fnames[333]="EUREC4A_TO_Flight-Segments_20200126b_0.1.yaml"
flight_segments_fnames[334]="EUREC4A_TO_Flight-Segments_20200128a_0.1.yaml"
flight_segments_fnames[335]="EUREC4A_TO_Flight-Segments_20200128b_0.1.yaml"
flight_segments_fnames[336]="EUREC4A_TO_Flight-Segments_20200130a_0.1.yaml"
flight_segments_fnames[337]="EUREC4A_TO_Flight-Segments_20200131a_0.1.yaml"
flight_segments_fnames[338]="EUREC4A_TO_Flight-Segments_20200131b_0.1.yaml"
flight_segments_fnames[339]="EUREC4A_TO_Flight-Segments_20200202a_0.1.yaml"
flight_segments_fnames[340]="EUREC4A_TO_Flight-Segments_20200205a_0.1.yaml"
flight_segments_fnames[341]="EUREC4A_TO_Flight-Segments_20200205b_0.1.yaml"
flight_segments_fnames[342]="EUREC4A_TO_Flight-Segments_20200206a_0.1.yaml"
flight_segments_fnames[343]="EUREC4A_TO_Flight-Segments_20200207a_0.1.yaml"
flight_segments_fnames[344]="EUREC4A_TO_Flight-Segments_20200207b_0.1.yaml"
flight_segments_fnames[345]="EUREC4A_TO_Flight-Segments_20200209a_0.1.yaml"
flight_segments_fnames[346]="EUREC4A_TO_Flight-Segments_20200209b_0.1.yaml"
flight_segments_fnames[347]="EUREC4A_TO_Flight-Segments_20200210a_0.1.yaml"
flight_segments_fnames[348]="EUREC4A_TO_Flight-Segments_20200211a_0.1.yaml"
flight_segments_fnames[349]="EUREC4A_TO_Flight-Segments_20200211b_0.1.yaml"
flight_segments_fnames[350]="EUREC4A_TO_Flight-Segments_20200213a_0.1.yaml"
flight_segments_fnames[351]="EUREC4A_TO_Flight-Segments_20200213b_0.1.yaml"
flight_segments_fnames[352]="EUREC4A_TO_Flight-Segments_20200214a_0.1.yaml"
flight_segments_fnames[353]="EUREC4A_TO_Flight-Segments_20200215a_0.1.yaml"
flight_segments_fnames[354]="EUREC4A_TO_Flight-Segments_20200215b_0.1.yaml"

#python -m twinotter.summary ${flight_data} ${data}/summary.csv

for n in {330..354}
do
    fname=`ls ${flight_data}/EUREC4A_TO-${n}_MASIN-1Hz_2020*_v0.5.nc`
    echo ${fname}
    python -m twinotter.plots.basic_flight_track "${fname}" --show-gui

    # Generate flight segment files
    python -m twinotter.plots.interactive_flight_track "${fname}"

    # Flight phase separation report
    python ~/Documents/meteorology/programming/flight-phase-separation/scripts/report.py \
        ${flight_segments}/${flight_segments_fnames[${n}]} \
        ${output}/flight${n}/${flight_segments_fnames[${n}]%.*}.html \
        -n ${fname}

    # Flight phase separation verification script
    python ~/Documents/meteorology/programming/flight-phase-separation/scripts/verify.py \
        ${flight_segments}/${flight_segments_fnames[${n}]} \
        -n ${fname}

    # Flight track animation
    python -m twinotter.plots.flight_track_frames "${fname}" \
        --goes_path=${goes_data} \
        --output_path="${output}/flight${n}/flight_track_frames"
    convert -delay 5 "${output}/flight${n}/flight_track_frames/*.png" \
         "${output}/flight${n}/TO-${n}_flight-track.gif"

    python -m twinotter.plots.heights_and_legs "${fname}" \
        ${flight_segments}/${flight_segments_fnames[${n}]} \
        --output_path="${output}/flight${n}/TO-${n}_flight-phases.png"

    python -m twinotter.quicklook "${fname}" \
        ${flight_segments}/${flight_segments_fnames[${n}]}

    python -m twinotter.quicklook_microphysics ${flight_data}/flight${n}/ \
        ${flight_segments}/${flight_segments_fnames[${n}]}

    mv *.png ${output}/flight${n}
done
