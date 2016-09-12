#!/bin/bash

usage="
USAGE: $0 SEQFILE OUTDIR 
"


rundir=`dirname $0`

cd $rundir

if [ $# -lt 2 ];then
	echo "$usage"
	exit 1
fi

SEQFILE=$1
OUTDIR=$2
TMPDIR=$3


for mfile in $SEQFILE/*
do
	filename=`basename "$mfile"`
	fname=$(echo $filename | cut -d'.' -f 1)
	echo "RUNNING run_subcons_sh"
	echo "bash run_subcons.sh $SEQFILE/$fname.fasta $OUTDIR $TMPDIR/$fname"
	bash run_subcons.sh $SEQFILE/$fname.fasta $OUTDIR $TMPDIR
done

resfile_loctree2=$OUTDIR/prediction/$fname.lc2.res
resfile_multiloc2=$OUTDIR/prediction/$fname.m2.res
resfile_sherloc2=$OUTDIR/prediction/$fname.s2.res

# WE NEED TO CHECK IF AT LEAST LOCTREE2,SHERLOC2 AND MULTILOC2 RESULTS ARE AVAILABLE, OTHERWISE WE NEED TO STOP THE PROCESS.
# MANY TIMES COULD HAPPEN THAT THE SEQUENCE ARE TOO SHORT SO WE DO NOT GET ANY PREDICTION.
echo "CHECK IF ALL THE FILES OF THE PREDICTORS ARE IN THE FOLDER RESULTS"


check_predicition_sherloc2="$(ls $resfile_sherloc2* | grep -c ".lc2.res" | awk '{print $1}')"

check_predicition_loctree2="$(ls $resfile_loctree2* | grep -c ".lc2.res" | awk '{print $1}')"

check_predicition_multiloc2="$(ls $resfile_multiloc2* | grep -c ".m2.res" | awk '{print $1}')"


count=$(find $SEQFILE -maxdepth 1 -name '*.fasta' | wc -l)




if (("$count" == 1));then

	if [[ -f "$resfile_loctree2" && "$resfile_sherloc2" && "$resfile_multiloc2" ]]
	then
		echo "The files of SherLoc2, LocTree2 and MultiLoc2 are here so continue"
	else
		echo "The files of SherLoc2, LocTree2 and MultiLoc2 are not here, so kill process "
		exit 1
	fi

	
elif (("$count" > 1));then

	if [[ -f "$resfile_loctree2" && "$resfile_sherloc2" && "$resfile_multiloc2" ]]
	then
		echo "For $fname the files of SherLoc2, LocTree2 and MultiLoc2 are here so continue"
	else
		echo "For $fname the files of SherLoc2, LocTree2 and MultiLoc2 are not here, so I put the file in the folder ../JUNK/"
		mv $OUTDIR/prediction/$fname.* $TMPDIR
	fi

fi
	
sleep 1

echo "Parse prediction and obtain test file"

python src/parse_prediction_subcons.py $SEQFILE $OUTDIR $TMPDIR

sleep 1

echo "Create dat file as input for SubCons"

python src/subcons-file-dat.py $OUTDIR

sleep 1

echo "Obtain final prediction with SubCons"

python src/subcons-prediction.py $OUTDIR

echo "REMOVE UNNECESSARY INTERMEDIATE FILES"
rm $OUTDIR/prediction/*.res 

rm $OUTDIR/dat-files/*.dat
