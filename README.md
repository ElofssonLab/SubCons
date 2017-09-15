SubCons

This is the standalone version of web-server http://subcons.bioinfo.se.
This software package is supposed to be run on Ubuntu x64 system. 
It might also work on other Linux boxes but have not been tested.

If you are interested in running SubCons on other systems, please contact Arne Elofsson (arne@bioinfo.se)

Description of the method:

SubCon is a new ensemble method for improved subcellular localization prediction in Human.
SubCons combines up to five predictors methods, SherLoc2, LocTree2, MultiLoc2, 
CELLO2.5 and YLoc (the latest two if available) using a random forest classifier.
LocTree2 requires PSSM. To speed up the creation of PSSM file,
we use our tool PRODRES (more info at https://github.com/ElofssonLab/PRODRES).
PRODRES is faster in creating PSSM profile and it has the same accuracy as Psi-Blast.
It is recommended to read carefully the instruction and install it!
However, SubCons runs Psi-Blast as alternative to PRODRES (THIS MAKE SUBCONS MUCH SLOWER)
 
The software is open source and licensed under the GPL license.

Reference

Salvatore M., Warholm P., Shu N., Basile W. and Elofsson A. (Epub 2017) SubCons: a new ensemble method for improved human subcellular localization predictions. Bioinformatics (Epub ahead of print)

Installation and usage:

Check out the software from bitbucket by:

	git clone https://bitbucket.org/salvatore_marco/subcons-web-server



Install dependencies if not installed:
	
	numpy
	scipy
	scikit-learn 0.17.1 (https://pypi.python.org/pypi/scikit-learn/0.17.1)
	python-mechanize
	pandas
	matplotlib
	itertools
	time
	collections
	pickle
	ncbi-blast+ or blast2
	libsvm 
	pp-popularity-contest
	
NOTE:
	It is strongly recommended to have this version of sklearn "scikit-learn 0.17.1 (https://pypi.python.org/pypi/scikit-learn/0.17.1)".
	We experienced some problem with the latest version of sklearn in using the package pickle.

INSTALL libsvm 

	git clone https://github.com/cjlin1/libsvm.git # then open cd libsvm/ and type : make all

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

INSTALL MultiLoc2: 

	python TOOLS/MultiLoc2/configureML2.py

INSTALL SherLoc2:

	python TOOLS/SherLoc2/configureSL2.py


NO INSTALLATION NEEDED FOR CELLO2.5 since runs through the script in /TOOLS/cello.py

We provide MultiLoc2, SherLoc2, and CELLO2.5. 
For LocTree2 follow the instruction (if something goes wrong refer to https://rostlab.org/owiki/index.php/Packages)

INSTALL LocTree2 (https://rostlab.org/owiki/index.php/Debian_repository):

	sudo apt-get install python-software-properties
	sudo apt-add-repository "deb http://rostlab.org/debian/ stable main contrib non-free"
	sudo apt-get update (ignore GPG error)
	sudo apt-get install rostlab-debian-keyring (without verification)
	sudo apt-get update
	sudo apt-get install loctree2

INSTALL loctree2-data:

	1-) wget ftp://rostlab.org/free/loctree2-data-1.0.2.tar.gz

	2-) it is recommended to untar the folder in the same path of LocTree2

NOTE: IF YOU GOT AN ERROR LIKE THIS WHEN INSTALLING 

	"LocTree2: Cannot set LC_CTYPE to default locale: No such file or directory"

You maybe need to type in the terminal this command:
	
	1-) export LC_ALL="en_US.UTF-8"

NOTE:
   
	1-) it is recommended to have libsvm, blast, loctree2-data and loctree2 in the same path
	2-) keep the tools in the folder /SubCons-web-server/TOOLS
	3-) the folder "src" is the folder containing the SubCons scripts.

To run SubCons after the installation type:
	
	$ bash master_subcons.sh SEQFILE/test.fasta OUTDIR
	

NOTE:

	The final prediction(s) of SubCons can be found in '/SubCons-web-server/OUTDIR/plot'. 
	The Latest contains both a stacked-barplot and a csv file with the score for each single predictor and SubCons.


##Docker version
A docker image of SubCons is also available at `nanjiang/subcons` for easier
running SubCons locally on multiple platforms

First install docker on your system according to the instructions
Then your can run the following command in the terminal to get the docker image

    docker pull nanjiang/subcons

Next, you need to download the following two databases for SubCons and saved them to e.g. /data, and then extracted the zipped files there

* http://subcons.bioinfo.se/static/download/db\_subcons.zip (3.5 GB)
* http://subcons.bioinfo.se/static/download/db\_prodres.zip (60 GB)

After that, you can start the docker container by the following command, suppose your working directory is /home/user/workdir

    docker run -v /data:/data -v /home/user/workdir:/workdir -u $(id -u):$(id -g) -it --name subcons -restart=unless-stopped -d nanjiang/subcons


Finally, copy your sequence file, e.g. `query.fa` to `/home/user/workdir` and you can run SubCons docker container using the following command

    docker exec subcons script /dev/null -c "cd /home/user/workdir ; /home/app/subcons/master_subcons.sh /home/usr/workdir/query.fa /home/usr/workdir/out1"

The result will be available at `/home/user/workdir/out1` after successful run.

