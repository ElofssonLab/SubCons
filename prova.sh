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
exec_cmd loctree2 " --fasta $SEQFILE --blastmat $pssmfile --resfile $resfile_loctree2 --domain $domain"

success1=0
if [ -s $resfile_loctree2 ];then
	success1=1
else
	echo "Failed to run loctree2, resfile_loctree2 $resfile_loctree2 does not exist or empty" >&2
fi

resfile_sherloc2=$OUTDIR/prediction/${rootname_seqfile}.s2.res
if [ $success -eq 1 ];then
	echo "RUNNING SHERLOC2"
	exec_cmd "python $TOOLS/SherLoc2/src/sherloc2_prediction.py -fasta=$SEQFILE -origin=animal -output=simple -result=$resfile_sherloc2"
fi


success2=0
if [ -s $resfile_loctree2 ];then
	success2=1
else
	echo "Failed to run loctree2, resfile_loctree2 $resfile_loctree2 does not exist or empty" >&2
fi
