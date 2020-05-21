data="/home/lsaffin/Documents/meteorology/data"
flight_data="${data}/eurec4a/twin-otter"
goes_data="${data}/eurec4a/goes/2km_10min/2020/"
output="/home/lsaffin/Documents/meteorology/output/eurec4a/twin-otter"

for n in {330..354}
do
    echo ${n}
    #python -m twinotter.plots.flight_track_frames "${flight_data}/flight${n}" ${goes_data} "${output}/flight${n}/flight_track_frames"
    python -m twinotter.plots.heights_and_legs "${flight_data}/flight${n}" "${flight_data}/flight${n}/flight${n}-legs.csv"
done
