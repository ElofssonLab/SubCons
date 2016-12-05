SubCons

This is the standalone version of web-server http://subcons.bioinfo.se. This software package is supposed to be run on Ubuntu x64 system. It might also work on other Linux boxes but have not been tested.

If you are interested in running SubCons on other systems, please contact Arne Elofsson (arne@bioinfo.se)

SubCon is a new ensemble method for improved subcellular localization prediction in Human.

The software is open source and licensed under the GPL license.

Reference

Salvatore, M., Warholm, P., Shu, N., Basile, W., Elofsson, A., 2015. SubCons: a new ensemble method for improved subcellular localization predictions.

NOTE: SubCons runs PRODRES our new programm that generatares PSSM profile very fast and with the same accuracy of Psi-Blast
      We suggest to read carefully the instruction and install it!
      However, SubCons runs Psi-Blast as alternative to PRODRES (THIS MAKE SUBCONS MUCH SLOWER)

Description

Installation and usage:

Check out the software from the github by

  $ git clone https://bitbucket.org/salvatore_marco/subcons-web-server (I THINK WE SHOULD MOVE FROM HERE)


Install dependencies if not installed
	numpy
	scipy
	sklearn
	python-ZSI
	python-mechanize
	pandas
	matplotlib
	itertools
	time
	collections
	pickle
	R library ggplot2
	R library reshape
	ncbi-blast+ or blast2
	libsvm 
	pp-popularity-contest

INSTALL libsvm FOR SherLoc2 & MultiLoc2

	git clone https://github.com/cjlin1/libsvm.git # then open cd libsvm/ and type : make all
	
 	NOTE: after download and install svm-predict & co must be moved in /usr/bin on your local machine

INSTALL BLAST PACKAGE 

	sudo apt-get install ncbi-blast+ 
	sudo apt-get install blast2

INSTALL PRODRES 
	
	Download (or clone) the PRODRES Git repository ("https://github.com/ElofssonLab/PRODRES")
	Follow the instruction written in the README.md in the PRODRES REPOSITORY at "https://github.com/ElofssonLab/PRODRES"	
	After installation of of PRODRES, make a symlink to the location of PRODRES in the subfolder `apps`

	```
	ln -s PATH-TO-PRODRES PATH-TO-SUBCONS/apps/PRODRES
	```

    The database of PRODRES should be installed in the folder
    `PATH-TO-PRODRES/databases`. The blastdb uniprot90.fasta should be
    installed at `PATH-TO-PRODRES/databases/blastdb`.

INSTALL MUltiLoc2: 

	python TOOLS/MultiLoc2/configureML2.py

INSTALL SherLoc2:

	python TOOLS/MultiLoc2/ configureSL2.py

INSTALL YLoc: (NOT WORKING)
	
	Use "wsdl2py" to create YLocSOAP_services.py and YLocSOAP_services_types.py

NO INSTALLATION NEEDED FOR CELLO2.5 since runs through the script in /TOOLS/cello.py

WE PROVIDE MultiLoc2, SherLoc2, YLoc, CELLO2.5 insted for LocTree2 follow the instruction (if something goes wrong refer to https://rostlab.org/owiki/index.php/Packages)

INSTALL LocTree2 TYPE FROM THE COMMAND LINE THE FOLLOWING:

 	sudo apt-get install python-software-properties
 	sudo apt-add-repository "deb http://rostlab.org/debian/ stable main contrib non-free"
	sudo apt-get update (ignore GPG error)
	sudo apt-get install rostlab-debian-keyring (without verification)
	sudo apt-get update
	sudo apt-get install loctree2

YOU ALSO NEED loctree2-data so download using:

	1-) wget ftp://rostlab.org/free/loctree2-data-1.0.2.tar.gz

	2-) untar this file in /usr/share using "sudo tar -C /usr/share/ -zxvf loctree2-data-1.0.2.tar.gz"

NOTE: IF YOU GOT AN ERROR LIKE THIS WHEN INSTALLING LocTree2: Cannot set LC_CTYPE to default locale: No such file or directory
You maybe need to type in the terminal this command:
	
	A-) export LC_ALL="en_US.UTF-8"

NOTE:
   
	1-) make sure you have libsvm, blast, loctree2-data and loctree2 in the folder /usr/share in your local machine 
 	2-) keep the tools in the folder /SubCons-web-server/TOOL
 	3-) the folder "src" is the folder containing the SubCons scripts.
 	4-) run_subcons.sh is a script that create necessary folder and run each predictor (IT IS INCLUDED IN THE FINAL SCRIPT batch_subcons.sh)

To run SubCons after the installation type:
	
	$ bash master_subcons.sh SEQFILE/test.fasta OUTDIR/ JUNK
	

NOTE:

	The final prediction(s) of SubCons can be found in the folders '/SubCons-web-server/RESULTS/final-prediction' & in '/SubCons-web-server/RESULTS/plot'. 
	The Latest contains both a stacked-barplot and a csv file with the score for each single predictor and SubCons




