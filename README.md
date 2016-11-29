SubCons

This is the standalone version of web-server http://subcons.net. This software package is supposed to be run on Ubuntu x64 system. It might also work on other Linux boxes but have not been tested.

If you are interested in running SubCons on other systems, please contact Arne Elofsson (arne@bioinfo.se)
Description

SubCon is a new ensemble method for improved subcellular localization prediction in Human.

The software is open source and licensed under the GPL license.

Reference

Salvatore, M., Warholm, P., Shu, N., Basile, W., Elofsson, A., 2015. SubCons: a new ensemble method for improved subcellular localization predictions.
Installation and usage:

Check out the software from the github by

  $ git clone https://bitbucket.org/salvatore_marco/subcons-web-server (I THINK WE SHOULD MOVE FROM HERE)


Install dependencies if not installed
	numpy
	scipy
	sklearn
	ZSI
	mechanize
	pandas
	matplotlib
	itertools
	pd
	time
	collections
	pickle
	R library ggplot2
	R library reshape
	ncbi-blast+ or blast2
	libsvm 

INSTALL libsvm FOR SherLoc2 & MultiLoc2

	git clone https://github.com/cjlin1/libsvm.git # then open cd libsvm/ and type : make all
	
  NOTE: after download and install svm-predict & co must be move in /usr/bin on your local machine

INSTALL BLAST PACKAGE 

	sudo apt-get install ncbi-blast+ 
	sudo apt-get install blast2

INSTALL FastPSSM (Nanjiang could you add this?)

INSTALL MUltiLoc2: 

	python TOOLS/MultiLoc2/configureML2.py

INSTALL SherLoc2:

	python TOOLS/MultiLoc2/ configureSL2.py

INSTALL YLoc: (NOT WORKING)
	
	Use "wsdl2py" to create YLocSOAP_services.py and YLocSOAP_services_types.py

NO INSTALLATION NEEDED FOR CELLO2.5 since runs through the script in /TOOLS/cello.py 	

WE PROVIDE MultiLoc2, SherLoc2, YLoc and CELLO2.5 but follow the instruction to install LocTree2

INSTALL LocTree2 TYPE FROM THE COMMAND LINE THE FOLLOWING:

 	sudo apt-get install python-software-properties
 	sudo apt-add-repository "deb http://rostlab.org/debian/ stable main contrib non-free"
	sudo apt-get update (ignore GPG error)
	sudo apt-get install rostlab-debian-keyring (without verification)
	sudo apt-get update
	sudo apt-get install loctree2

YOU ALSO NEED loctree2-data so download using:

	1-) wget ftp://rostlab.org/free/loctree2-data-1.0.2.tar.gz

	2-) untar this file in /usr/share 

NOTE: IF YOU GOT AN ERROR LIKE THIS WHEN INSTALLING LocTree2: Cannot set LC_CTYPE to default locale: No such file or directory
You maybe need to type in the terminal this command:
	
	A-) export LC_ALL="en_US.UTF-8"

NOTE:
   
	1-) make sure you have libsvm, blast, loctree2-data and loctree2 in the folder /usr/share in your local machine 
 	2-) keep the tools in the folder /SubCons-web-server/TOOL
 	3-) the folder "src" is the folder containing the SubCons scripts.
 	4-) run_subcons.sh is a script that create necessary folder and run each predictor (IT IS INCLUDED IN THE FINAL SCRIPT batch_subcons.sh)

To run SubCons after the installation type:
	
	$ bash batch_subcons.sh SEQFILE OUTDIR TMPDIR
	NOTE:  You do not need to specify tha fasta name/seq; SubCons will automatically take the sequence(s) in the folder SEQFILE

NOTE:

	The results can be found in the folders '/SubCons-web-server/RESULTS/final-prediction' in which you have the only the final prediction of SubCons  and    in '/SubCons-web-server/RESULTS/plot' in which 		you have both graphically and as csv file with the score for each single predictor and SubCons




