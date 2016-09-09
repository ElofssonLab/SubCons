#!/bin/bash

usage="
USAGE: $0 SEQFILE OUTDIR TMPDIR
"

domain=euka

rundir=`dirname $0`

cd $rundir

if [ $# -lt 3 ];then
	echo "$usage"
	exit 1
fi

SEQFILE=$1
OUTDIR=$2
TMPDIR=$3

RUNTOOL=TOOLS

#GetPSSMFile{
#	/bin/cp ../profile/*.pssm

	# or to be retrieved by the API script from the PSSM web-server
	# TO be done
#}

#exec_cmd{
#	echo "$*"
#	eval "$*"
#}

basename_seqfile=$(basename $SEQFILE)
rootname_seqfile=${basename_seqfile%.*}

pssmfile=$OUTDIR/$rootname_seqfile.pssm

#GetPSSMFile()

resfile_loctree2=$OUTDIR/prediction/${rootname_seqfile}.lc2.res

if [ ! -d "$OUTDIR/prediction" ]; then
	mkdir -p $OUTDIR/prediction
fi

echo "RUNNING LOCTREE2"
#exec_cmd "loctree2 --fasta $SEQFILE --blastmat $pssmfile --resfile $resfile_loctree2 --domain $domain"

success1=0
if [ -s $resfile_loctree2 ];then
	success1=1
else
	echo "Failed to run loctree2, resfile_loctree2 $resfile_loctree2 does not exist or empty" >&2
fi

resfile_sherloc2=$OUTDIR/prediction/${rootname_seqfile}.s2.res

echo "RUNNING SHERLOC2"
#exec_cmd "python ../TOOLS/SherLoc2/src/sherloc2_prediction.py -fasta=$SEQFILE -origin=animal -output=simple -result=$resfile_sherloc2"


success2=0
if [ -s $resfile_sherloc2 ];then
	success2=1
else
	echo "Failed to run sherloc2, resfile_loctree2 $resfile_sherloc2 does not exist or empty" >&2
fi

resfile_multiloc2=$OUTDIR/prediction/${rootname_seqfile}.m2.res

echo "RUNNING MULTILOC2"
#exec_cmd "python ../TOOLS/MultiLoc2/src/multiloc2_prediction.py -fasta=$SEQFILE -origin=animal -output=simple -result=$resfile_multiloc2"


success3=0
if [ -s $resfile_multiloc2 ];then
	success3=1
else
	echo "Failed to run multiloc2, resfile_multiloc2 $resfile_multiloc2 does not exist or empty" >&2
fi
	
resfile_yloc=$OUTDIR/prediction/${rootname_seqfile}.y.res

echo "RUNNING YLOC"
#exec_cmd "python ../TOOLS/YLocSOAPclient/yloc.py $SEQFILE YLoc-HighRes Animals No Simple > $resfile_yloc"

success4=0	
if [ -s $resfile_yloc ];then
	success4=1
else
	echo "Failed to run yloc, resfile_yloc $resfile_yloc does not exist or empty" >&2
	#exec "./$RUNTOOL/YLocSOAPclient/yloc.py $SEQFILE YLoc-HighRes Animals No Simple > $resfile_yloc"
fi

resfile_cello=$OUTDIR/prediction/${rootname_seqfile}.c.res

echo "RUNNING CELLO"
#exec_cmd "python ../TOOLS/cello.py $SEQFILE > $resfile_cello"


success5=0
if [ -s $resfile_cello ];then
	success5=1
else
	echo "Failed to run cello, resfile_cello $resfile_cello does not exist or empty" 	
fi


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
		mv $OUTDIR/prediction/${rootname_seqfile}.* $TMPDIR
	fi

fi
	
#sleep 1

echo "Parse prediction and obtain test file"

python src/parse_prediction_subcons.py $SEQFILE $OUTDIR $TMPDIR

#sleep 1

echo "Create dat file as input for SubCons"

python src/subcons-file-dat.py $OUTDIR

#sleep 1

echo "Obtain final prediction with SubCons"

python src/subcons-forest.py $OUTDIR

#REMOVE UNNECESSARY INTERMEDIATE FILES
#rm ../results/prediction/*.res 

#rm ../results/dat-files/*.dat

