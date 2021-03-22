#!/bin/bash

sr_k=8
minmax='min'
mix_dir="../../dataset/wsj0-mix"

mixed_n_sources='2+3'

. ./parse_options.sh || exit 1

to_dir="${mix_dir}/${mixed_n_sources}speakers/wav${sr_k}k/${minmax}"
mkdir -p "${to_dir}"

n_sources_set=`echo ${mixed_n_sources} | tr '+' '\n'`

for n_sources in ${n_sources_set} ; do
    from="${mix_dir}/${n_sources}speakers/wav${sr_k}k/${minmax}/*"
    cp "${from}" "${to_dir}"

    for data_type in 'tr' 'cv' 'tt' ; do
        cat "${mix_dir}/${n_sources}speakers/mix_${n_sources}_spk_${minmax}_${data_type}_mix" >> "${mix_dir}/${mixed_n_sources}speakers/mix_${mixed_n_sources}_spk_${minmax}_${data_type}_mix"
    done
done