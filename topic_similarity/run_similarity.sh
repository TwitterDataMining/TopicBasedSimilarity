#!/usr/bin/env bash

TOPIC_VECTOR="data/24Legacy1000_topic_vector.p"
SIM_DIR="Social"

declare -a pairfiles=("data/sim_no_relations.csv" "data/sim_one_way_pairs.csv" "data/sim_reciprocal_pairs.csv")

cd "path to similarity script"
for pairfile in "${pairfiles[@]}"
do
    python pair_similarity.py $TOPIC_VECTOR $pairfile $SIM_DIR
done
