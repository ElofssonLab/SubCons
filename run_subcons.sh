#!/bin/bash

usage="
USAGE: $0 SEQFILE OUTDIR TMPDIR
"

VERBOSE=1

domain=euka

rundir=`dirname $0`
rundir=$(readlink -f $rundir)

#cd $rundir

if [ $# -lt 3 ];then
	echo "$usage"
	exit 1
fi

SEQFILE=$1
OUTDIR=$2
TMPDIR=$3


SEQFILE=$(readlink -f $SEQFILE)
OUTDIR=$(readlink -f $OUTDIR)
TMPDIR=$(readlink -f $TMPDIR)


RUNTOOL=$rundir/TOOLS

exec_cmd(){
    case $VERBOSE in 
        yes|1)
        echo -e "\n$*\n"
    esac
    eval "$*"
}

#GetPSSMFile{
#	/bin/cp $OUTDIR/*.pssm

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

#CREATE FOLDER:
if [ ! -d "$OUTDIR/prediction" ]; then
	mkdir -p $OUTDIR/prediction
fi

if [ ! -d "$OUTDIR/for-dat" ]; then
	mkdir -p $OUTDIR/for-dat
fi
if [ ! -d "$OUTDIR/dat-files" ]; then
	mkdir -p $OUTDIR/dat-files
fi
if [ ! -d "$OUTDIR/final-prediction" ]; then
	mkdir -p $OUTDIR/final-prediction
fi

if [ ! -d "$OUTDIR/plot" ]; then
	mkdir -p $OUTDIR/plot
fi

if [ ! -d "$TMPDIR" ]; then
	mkdir -p $TMPDIR
fi

resfile_loctree2=$OUTDIR/prediction/${rootname_seqfile}.lc2.res

echo "RUNNING LOCTREE2"
exec_cmd "loctree2 --fasta $SEQFILE --blastmat $pssmfile --resfile $resfile_loctree2 --domain $domain"

success1=0
if [ -s $resfile_loctree2 ];then
	success1=1
else
	echo "Failed to run loctree2, resfile_loctree2 $resfile_loctree2 does not exist or empty" >&2
	exec_cmd "mv $resfile_loctree2 $TMPDIR/"
fi

resfile_sherloc2=$OUTDIR/prediction/${rootname_seqfile}.s2.res

if [ $success1 -eq 1 ];then
	echo "RUNNING SHERLOC2"
	exec_cmd "python $RUNTOOL/SherLoc2/src/sherloc2_prediction.py -fasta=$SEQFILE -origin=animal -output=simple -result=$resfile_sherloc2"
fi


success2=0
if [ -s $resfile_sherloc2 ];then
	success2=1
else
	echo "Failed to run Sherloc2, resfile_sherloc2 $resfile_sherloc2 does not exist or empty" >&2
	exec_cmd "mv $resfile_sherloc2 $TMPDIR/"
fi

resfile_multiloc2=$OUTDIR/prediction/${rootname_seqfile}.m2.res

if [ $success2 -eq 1 ];then
	echo "RUNNING MULTILOC2"
	exec_cmd "python $RUNTOOL/MultiLoc2/src/multiloc2_prediction.py -fasta=$SEQFILE -origin=animal -output=simple -result=$resfile_multiloc2"
fi


success3=0
if [ -s $resfile_multiLoc2 ];then
	success3=1
else
	echo "Failed to run multiLoc2, resfile_multiLoc2 $resfile_multiLoc2 does not exist or empty" >&2
	exec_cmd "mv $resfile_multiloc2 $TMPDIR/"
fi


resfile_yloc=$OUTDIR/prediction/${rootname_seqfile}.y.res

if [ $success3 -eq 1 ];then
	echo "RUNNING YLOC"
	exec_cmd "python $RUNTOOL/YLocSOAPclient/yloc.py $SEQFILE YLoc-HighRes Animals No Simple > $resfile_yloc"

fi


success4=0
if [ -s $resfile_yloc ];then
	success4=1
else
	echo "Failed to run yloc, resfile_yloc $resfile_yloc does not exist or empty" >&2
	exec_cmd "mv $resfile_yloc $TMPDIR/"
fi

resfile_cello=$OUTDIR/prediction/${rootname_seqfile}.c.res

if [ $success3 -eq 1 ];then
	echo "RUNNING CELLO"
	exec_cmd "python $RUNTOOL/cello.py $SEQFILE > $resfile_cello"

fi


success5=0
if [ -s $resfile_cello ];then
	success5=1
else
	echo "Failed to run cello, resfile_cello $resfile_cello does not exist or empty" >&2
	exec_cmd "mv $resfile_cello $TMPDIR/"
fi




