#!/usr/bin/env bash

COLLECTION_NAME="old_tweets"
UNIQUE_USERS="data/24Legacy_20/24Legacy_lda_20/unique_users.csv"
OUTPUT_DIR="data_preprocessed"

python read_data.py $COLLECTION_NAME $UNIQUE_USERS $OUTPUT_DIR

