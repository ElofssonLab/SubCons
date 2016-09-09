import glob,os,sys
import mechanize
import time
import re
from mechanize import Browser

if not len(sys.argv) == 2:
  print "Usage:",sys.argv[0],"fasta file"
  sys.exit(-1)

def cello():
	url = "http://cello.life.nctu.edu.tw/" #for Cello
	br = mechanize.Browser()
	br.set_handle_robots(False) # ignore robots
	br.open(url)
	br.form = list(br.forms())[0] # Detect the form of the page to fill 
	br.form.find_control("species").items[2].selected=True # choose the box of Eukaryotic Species
	br.form.add_file(open(line), 'text/plain', line) # add the file to submit in this case we have 500 sequences in each file
	br.form.set_all_readonly(False)
	res = br.submit()
	content = res.read()
	print content




path = sys.argv[1]
paths = glob.glob(path+'*.fasta')

   
for line in paths:
	identification = line.split('/')[2].split('.')[0]
	cello()

