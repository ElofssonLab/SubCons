#!/bin/bash

exec_cmd(){ #{{{
    case $VERBOSE in
        yes|1)
        echo -e "\n$*\n"
    esac
    eval "$*"
}
#}}}

usage="
USAGE: $0 SEQFILE OUTDIR

OPTIONS:
  SEQFILE  A file containing a single amino acid sequence in FASTA format
  OUTDIR   Path where the result will be output
"

VERBOSE=1

domain=euka

#yloc is not run in this versino of subcons, might be implemented in the future versions
is_run_yloc=0

rundir=`dirname $0`
rundir=$(readlink -f $rundir)
echo $rundir
#cd $rundir

if [ $# -lt 2 ];then
	echo "$usage"
	exit 1
fi

SEQFILE=$1
OUTDIR=$2

SEQFILE=$(readlink -f $SEQFILE)
OUTDIR=$(readlink -f $OUTDIR)


TMPDIR=$OUTDIR/tmp/
TMP_MULTILOC=$OUTDIR/tmp/tmp_MULTILOC/
TMP_SHERLOC=$OUTDIR/tmp/tmp_SHERLOC/

export TMP_MULTILOC
export TMP_SHERLOC

RUNTOOL=$rundir/TOOLS

PRODRES_PATH=$rundir/apps/PRODRES
PfamScan_PATH=$rundir/apps/PfamScan

export PERL5LIB=$PERL5LIB:$PfamScan_PATH

PRODRES_PATH=$(readlink -f $PRODRES_PATH)

exec_PRODRES=$PRODRES_PATH/PRODRES/PRODRES.py

if [  ! -e $exec_PRODRES ];then
	echo "PRODRES script '$exec_PRODRES' does not exist. Aborting." >&2
	exit 1
fi




basename_seqfile=$(basename $SEQFILE)
rootname_seqfile=${basename_seqfile%.*}



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
if [ ! -d "$TMP_SHERLOC" ]; then
	mkdir -p $TMP_SHERLOC
fi
if [ ! -d "$TMP_MULTILOC" ]; then
	mkdir -p $TMP_MULTILOC
fi


echo "CREATE PSSM File"
outpath_PRODRES=$TMPDIR/rst_prodres
mkdir -p $outpath_PRODRES
exec_cmd "python $exec_PRODRES --input $SEQFILE --output $outpath_PRODRES --pfam-dir $PRODRES_PATH/databases/ --pfamscan-script $PfamScan_PATH/pfam_scan.pl --pfamscan_bitscore 2 --uniprot-db-fasta $PRODRES_PATH/databases/blastdb/uniref90.fasta --second-search psiblast --psiblast_e-val 0.001 --psiblast_iter 3"

resfile_pssm=$outpath_PRODRES/$rootname_seqfile/outputs/psiPSSM.txt

success1=0
if [ -s $resfile_pssm ];then
        success1=1
else
        echo "Failed to run PRODRES, resfile_pssm $resfile_pssm does not exist or empty" >&2
        exec_cmd "mv $resfile_pssm $TMPDIR/"
fi


resfile_loctree2=$OUTDIR/prediction/${rootname_seqfile}.lc2.res

echo "RUNNING LOCTREE2"
#exec_cmd "loctree2 --fasta $SEQFILE --blastmat $OUTDIR --resfile $resfile_loctree2 --domain $domain"
exec_cmd "loctree2 --fasta $SEQFILE --blastmat $outpath_PRODRES/$rootname_seqfile/outputs/psiPSSM.txt --resfile $resfile_loctree2 --domain $domain"

success2=0
if [ -s $resfile_loctree2 ];then
	success2=1
else
	echo "Failed to run loctree2, resfile_loctree2 $resfile_loctree2 does not exist or empty" >&2
	exec_cmd "mv $resfile_loctree2 $TMPDIR/"
fi

resfile_sherloc2=$OUTDIR/prediction/${rootname_seqfile}.s2.res

if [ $success2 -eq 1 ];then
	echo "RUNNING SHERLOC2"
	exec_cmd "python $RUNTOOL/SherLoc2/src/sherloc2_prediction.py -fasta=$SEQFILE -origin=animal -output=simple -result=$resfile_sherloc2"
fi


success3=0
if [ -s $resfile_sherloc2 ];then
	success3=1
else
	echo "Failed to run Sherloc2, resfile_sherloc2 $resfile_sherloc2 does not exist or empty" >&2
	exec_cmd "mv $resfile_sherloc2 $TMPDIR/"
fi

resfile_multiloc2=$OUTDIR/prediction/${rootname_seqfile}.m2.res

if [ $success3 -eq 1 ];then
	echo "RUNNING MULTILOC2"
	exec_cmd "python $RUNTOOL/MultiLoc2/src/multiloc2_prediction.py -fasta=$SEQFILE -origin=animal -output=simple -result=$resfile_multiloc2"
fi


success4=0
if [ -s $resfile_multiLoc2 ];then
	success4=1
else
	echo "Failed to run multiLoc2, resfile_multiLoc2 $resfile_multiLoc2 does not exist or empty" >&2
	exec_cmd "mv $resfile_multiloc2 $TMPDIR/"
fi


if [ $is_run_yloc -eq 1 ];then
    resfile_yloc=$OUTDIR/prediction/${rootname_seqfile}.y.res

    if [ $success4 -eq 1 ];then
        echo "RUNNING YLOC"
        #exec_cmd "python $RUNTOOL/YLocSOAPclient/yloc.py $SEQFILE YLoc-HighRes Animals No Simple > $resfile_yloc"

    fi

    success4=0
    if [ -s $resfile_yloc ];then
        success4=1
    else
        echo "Failed to run yloc, resfile_yloc $resfile_yloc does not exist or empty" >&2
        exec_cmd "mv $resfile_yloc $TMPDIR/"
    fi
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



exec_cmd "mv $outpath_PRODRES/${rootname_seqfile}/outputs/psiPSSM.txt $OUTDIR/${rootname_seqfile}.pssm"

exec_cmd "sleep 1s"



#resfile_loctree2=$OUTDIR/prediction/${rootname_seqfile}.lc2.res
#resfile_multiloc2=$OUTDIR/prediction/${rootname_seqfile}m2.res
#resfile_sherloc2=$OUTDIR/prediction/${rootname_seqfile}.s2.res

# WE NEED TO CHECK IF AT LEAST LOCTREE2,SHERLOC2 AND MULTILOC2 RESULTS ARE AVAILABLE, OTHERWISE WE NEED TO STOP THE PROCESS.
# MANY TIMES COULD HAPPEN THAT THE SEQUENCE ARE TOO SHORT SO WE DO NOT GET ANY PREDICTION.



success6=0
if [ -e $resfile_loctree2 -a -e $resfile_sherloc2 -a -e $resfile_loctree2 ];then
        success6=1
	echo "files here proceed"

	echo "Parse prediction and obtain test file"
	echo "$OUTDIR"
	exec_cmd "python $rundir/src/parse_prediction_subcons.py $OUTDIR/"

	sleep 1

	echo "Create dat file as input for SubCons"

	exec_cmd "python $rundir/src/subcons-file-dat.py $OUTDIR/"

	sleep 1

	echo "Obtain final prediction with SubCons"

	exec_cmd "python $rundir/src/subcons-prediction.py $OUTDIR/"

	sleep 1

	echo "Plot Results"

	exec_cmd "python $rundir/src/create_dataframe_plot.py $OUTDIR/"
	exec_cmd "Rscript $rundir/src/plot.R $OUTDIR/plot"


else
        echo "Failed to run LocTree2, MultiLoc2 & SherLoc2" >&2
	exec_cmd "mv  $OUTDIR/* $TMPDIR/"

fi

echo "REMOVE UNNECESSARY INTERMEDIATE FILES"

rm $OUTDIR/prediction/*.res

rm $OUTDIR/dat-files/*.dat
