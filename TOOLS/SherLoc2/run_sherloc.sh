#!/bin/bash -l

id=$1

DIR_OUT='/home/marco/Desktop/TOOL_PREDICTION/SherLoc2/results/animal'
DIR_DATA="/home/marco/Desktop/fasta/animal"


python src/sherloc2_prediction.py -fasta=$DIR_DATA/${id}.fasta -origin=animal -output=simple -result=$DIR_OUT/${id}.res 
