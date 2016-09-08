#!/bin/bash

DIR_JUNK='../JUNK'
DIR_PROFILE='../profile'
DIR_OUT='../results'
DIR_DATA="../fasta"


echo "Checking to see if pssm is in the folder:"
sleep 1


OUTPUT="$(ls ../fasta | cut -d'.' -f1)"


# THIS IS THE PART THAT EITHER RUN PSIBLAST/FASTPSSM (NANJIANG TAKE CARE OF THIS PART) OR CHECK IF THERE IS/ARE PSSM/s AVAILABLE SOMEWHERE

if [ 'ls -A DIR_PROFILE/${OUTPUT}.profile' ]

then 
	echo "PSSM OK"
else
	echo "WE NEED TO RUN EITHER FASTPSSM OR PSIBLAST "
fi

for mfile in $DIR_DATA/*
do
	filename=`basename "$mfile"`
	fname=$(echo $filename | cut -d'.' -f 1)
	echo "RUNNING LOCTREE2"
	#loctree2 --fasta $DIR_DATA/$fname.fasta --blastmat $DIR_PROFILE/$fname.pssm --resfile $DIR_OUT/prediction/$fname.lc2.res --domain euka
done

for mfile in $DIR_DATA/*
do
	filename=`basename "$mfile"`
	fname=$(echo $filename | cut -d'.' -f 1)
	echo "RUNNING SHERLOC2"
	python ../TOOLS/SherLoc2/src/sherloc2_prediction.py -fasta=$DIR_DATA/$fname.fasta -origin=animal -output=simple -result=$DIR_OUT/prediction/$fname.s2.res
done

for mfile in $DIR_DATA/*
do
	filename=`basename "$mfile"`
	fname=$(echo $filename | cut -d'.' -f 1)
	echo "RUNNING MULTILOC2"
	python ../TOOLS/MultiLoc2/src/multiloc2_prediction.py -fasta=$DIR_DATA/$fname.fasta -origin=animal -output=simple -result=$DIR_OUT/prediction/$fname.m2.res
done

for mfile in $DIR_DATA/*
do
	filename=`basename "$mfile"`
	fname=$(echo $filename | cut -d'.' -f 1)
	echo "RUNNING YLOC"
	#python ../TOOLS/YLocSOAPclient/yloc.py $DIR_DATA/$fname.fasta YLoc-HighRes Animals No Simple > $DIR_OUT/prediction/$fname.yloc.res
done

echo "RUNNING CELLO2.5"
python ../TOOLS/cello.py




# WE NEED TO CHECK IF AT LEAST LOCTREE2,SHERLOC2 AND MULTILOC2 RESULTS ARE AVAILABLE, OTHERWISE WE NEED TO STOP THE PROCESS.
# MANY TIMES COULD HAPPEN THAT THE SEQUENCE ARE TOO SHORT SO WE DO NOT GET ANY PREDICTION.
echo "CHECK IF ALL THE FILES OF THE PREDICTORS ARE IN THE FOLDER RESULTS"


check_predicition_sherloc2="$(ls ../results/prediction/*lc2.res | grep -c ".lc2.res" | awk '{print $1}')"

check_predicition_loctree2="$(ls ../results/prediction/*lc2.res | grep -c ".lc2.res" | awk '{print $1}')"

check_predicition_multiloc2="$(ls ../results/prediction/*m2.res | grep -c ".m2.res" | awk '{print $1}')"


count=$(find ../fasta -maxdepth 1 -name '*.fasta' | wc -l)

#echo $count


if (("$count" == 1));then
	for mfile in $DIR_DATA/*
	do
		filename=`basename "$mfile"`
		fname=$(echo $filename | cut -d'.' -f 1)
	if [[ -f "$DIR_OUT/prediction/$fname.lc2.res" && "$DIR_OUT/prediction/$fname.s2.res" && "$DIR_OUT/prediction/$fname.m2.res" ]]
	then
		echo "The files of SherLoc2, LocTree2 and MultiLoc2 are here so continue"
	else
		echo "The files of SherLoc2, LocTree2 and MultiLoc2 are not here, so kill process "
		exit 1
	fi
	done
	
elif (("$count" > 1));then
	for mfile in $DIR_DATA/*
	do
		filename=`basename "$mfile"`
		fname=$(echo $filename | cut -d'.' -f 1)
	if [[ -f "$DIR_OUT/prediction/$fname.lc2.res" && "$DIR_OUT/prediction/$fname.s2.res" && "$DIR_OUT/prediction/$fname.m2.res" ]]
	then
		echo "For $fname the files of SherLoc2, LocTree2 and MultiLoc2 are here so continue"
	else
		echo "For $fname the files of SherLoc2, LocTree2 and MultiLoc2 are not here, so I put the file in the folder ../JUNK/"
		mv $DIR_OUT/prediction/$fname.* $DIR_JUNK/
	fi
	done
fi
	
sleep 1

echo "Parse prediction and obtain test file"

python parse_prediction_subcons.py

sleep 1

echo "Create dat file as input for SubCons"

python subcons-file-dat.py

sleep 1

echo "Obtain final prediction with SubCons"

python subcons-forest.py $DIR_OUT/dat-files/prediction.dat

#REMOVE UNNECESSARY INTERMEDIATE FILES
#rm ../results/prediction/*.res 

#rm ../results/dat-files/*.dat
