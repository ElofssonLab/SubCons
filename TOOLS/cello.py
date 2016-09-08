import glob,os,sys
import webbrowser
import mechanize
import time
from bs4 import BeautifulSoup
import re
from mechanize import Browser


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




path = '../fasta/'
paths = glob.glob(path+'*.fasta')

   
for line in paths:
	identification = line.split('/')[2].split('.')[0]
	with open(os.path.join('../results/prediction/'+ identification + '.c.res'),'w') as files:
		saveout=sys.stdout
		sys.stdout=files
		cello()
		files.close()
		sys.stdout=saveout

