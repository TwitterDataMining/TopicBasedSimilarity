#!/usr/bin/env bash

COLLECTION_NAME="24Legacy1000"
UNIQUE_USERS="data/24Legacy_20/24Legacy_lda_20"
OUTPUT_DIR="Social"

python read_data.py $COLLECTION_NAME $UNIQUE_USERS $OUTPUT_DIR

