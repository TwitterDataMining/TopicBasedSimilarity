#!/usr/bin/env bash
# This script runs all the steps of LDA
# step 1 : Create corpus , takes the processed tweets as input,
#          arguments :
#           PREFIX= prefix of the date files used while preprocessing data
#           INPUT_DIR = directory where preprocessed files are stored
#           OUTPUT_DIR = here the lda output files will be stored
# STEP 2 : run lda output lda model and dict and html visualization.
# STEP 3 : create topic vector


PREFIX="24Legacy1000"
TOPICS=40
PASSES=10
INPUT_DIR="../data_gathering/24Legacy1000"
OUTPUT_DIR="data/24Legacy1000/40Topics"

echo "make corpus starting"
python lda_gensim_make_corpus.py $PREFIX $INPUT_DIR $OUTPUT_DIR
echo "make corpus done"
python run_lda.py $PREFIX $OUTPUT_DIR $TOPICS $PASSES
echo "run lda done"
python create_topic_vectors.py $PREFIX $OUTPUT_DIR $INPUT_DIR
echo "topic vectors done and html pyLDAvis written"





