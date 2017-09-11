FROM ubuntu:16.04
LABEL maintainer "Nanjiang Shu (nanjiang.shu@nbis.se)"
LABEL version "1.0"

#================================
# Install basics
#===============================
RUN apt-get  update -y
RUN apt-get install -y apt-utils 
RUN apt-get install -y curl wget vim tree bc git
RUN apt-get install -y python python-dev python-pip
RUN apt-get install -y build-essential 
RUN apt-get install -y libxml2-dev libxslt1-dev libsqlite3-dev zlib1g-dev  
RUN apt-get install -y r-base
RUN apt-get install -y cmake 
RUN apt-get install -y qt4-qmake

#================================
#  Add subcons source code
#===============================
WORKDIR /home/app
# add the source code to WORKDIR/home/app
ADD . ./subcons 


RUN mkdir /home/download
#================================
# Install libsvm
#===============================
RUN cd /home/download && \
	git clone https://github.com/cjlin1/libsvm.git && \
	cd libsvm && \
	make all && \
	/bin/cp -f svm-predict svm-scale svm-train /usr/local/bin/

#================================
# Install HMMER 
#===============================
RUN cd /home/download && \
	wget http://eddylab.org/software/hmmer3/3.1b2/hmmer-3.1b2-linux-intel-x86_64.tar.gz -O  hmmer-3.1b2-linux-intel-x86_64.tar.gz && \
	tar -xvzf  hmmer-3.1b2-linux-intel-x86_64.tar.gz  && \
	cd hmmer-3.1b2-linux-intel-x86_64 && \
	./configure && \
	make	&& \
	make install

#================================
# Install blast  
#===============================
RUN apt-get install -y ncbi-blast+ 
RUN apt-get install -y blast2


#================================
# Install PRODRES  
#===============================
RUN cd /home/app &&\
	git clone https://github.com/ElofssonLab/PRODRES &&\
	cd PRODRES &&\
	ln -s /data/db_prodres databases

#================================
# Install loctree2  
#===============================
RUN apt-get install -y pp-popularity-contest
RUN apt-get install -y software-properties-common
RUN apt-get install -y python-software-properties
RUN apt-add-repository "deb http://rostlab.org/debian/ stable main contrib non-free"
RUN apt-get update -y
RUN apt-get install -y  --allow-unauthenticated rostlab-debian-keyring
RUN apt-get update -y
RUN apt-get install -y loctree2  
# link data
RUN cd /usr/share &&\
	ln -s /data/db_subcons/loctree2-data-1.0.2 loctree2-data

#================================
# Install R packages 
#===============================
RUN R -e "install.packages(c('ggplot2', 'reshape'), repos='http://ftp.acc.umu.se/mirror/CRAN/')"

#================================
# Install python package 
#===============================
RUN pip install --upgrade pip
RUN pip install biopython==1.70
RUN pip install matplotlib==1.5.3
RUN pip install html5lib==0.999
RUN pip install mechanize==0.2.5
RUN pip install pandas==0.19.1
RUN pip install numpy==1.11.2
RUN pip install scipy==0.18.1
RUN pip install scikit-learn==0.17.1
RUN pip install bokeh==0.12.5

#================================
# Install perl packages
#===============================
RUN apt-get install -y perlbrew
RUN perlbrew install-cpanm
RUN /root/perl5/perlbrew/bin/cpanm Bio::Perl Moose IPC::Run

#================================
# Install MultiLoc2 
#===============================
RUN cd /home/app/subcons && \
	python TOOLS/MultiLoc2/configureML2.py

#================================
# Install SherLoc2
#===============================
RUN cd /home/app/subcons && \
	python TOOLS/SherLoc2/configureSL2.py

RUN export LC_ALL="en_US.UTF-8"
