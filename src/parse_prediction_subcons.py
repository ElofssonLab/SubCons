import glob,os,sys
import itertools
import pandas as pd
import time
from collections import Counter

if not len(sys.argv) == 2:
  print "Usage:",sys.argv[0],"results_folder"
  sys.exit(-1)
  
dic_loc = {'nuclear':'NUC','plasma membrane':'MEM','extracellular':'EXE','cytoplasmic':'CYT','mitochondrial':'MIT','ER':'ERE','peroxisomal':'VES','lysosomal':'VES','Golgi apparatus':'GLG'}
dic_sherloc2_loc = {'VES':'VES','cytoplasmic':'CYT','ER':'ERE','Golgi apparatus':'GLG','lysosomal':'VES','mitochondrial':'MIT','nuclear':'NUC','peroxisomal':'VES','plasma membrane':'MEM','extracellular':'EXC'}
dic_loctree2_loc = {'chloroplast':'MIT','chloroplast membrane':'MIT','cytosol':'CYT','endoplasmic reticulum':'ERE','endoplasmic reticulum membrane':'ERE','golgi apparatus':'GLG','golgi apparatus membrane':'GLG','mitochondria':'MIT','mitochondria membrane':'MIT','nucleus':'NUC','nucleus membrane':'NUC','peroxisome':'VES','peroxisome membrane':'VES','plasma membrane':'MEM','plastid':'MIT','vacuole':'MIT','vacuole membrane':'MIT','secreted':'EXC'}
dic_cello_loc ={'Cytoplasmic':'CYT','Cytoskeletal':'CYT','ER':'ERE','Golgi':'GLG','Lysosomal':'VES','Mitochondrial':'MIT','Nuclear':'NUC','Peroxisomal':'VES','PlasmaMembrane':'MEM','Extracellular':'EXC'}
dic_yloc_loc = {'cytoplasm':'CYT','ER':'ERE','Golgi':'GLG','lysosome':'VES','mitochondrion':'MIT','nucleus':'NUC','peroxisome':'VES','plasma':'MEM','extracellular':'EXC'}
dic_multiloc2_loc = {'VES':'VES','cytoplasmic':'CYT','ER':'ERE','Golgi apparatus':'GLG','lysosomal':'VES','mitochondrial':'MIT','nuclear':'NUC','peroxisomal':'VES','plasma membrane':'MEM','extracellular':'EXC'} 	



def parse_cello(cello,filename):
	dic_pred = {}
	dic_cello = {}
	try:
		for line in cello:
			line = line.split('\t') 
			if 'SeqID' in line[0] :
				id_sp1 =  line[0].split(':')[1].split(' ')[1]
			elif len(line)>=7 :#and 'Combined SVM classifier:' in line[1]:
				if id_sp1 == id_sp1 and len(line) == 7:
		
					if line[-2] in dic_cello_loc.keys():
						score = line[-1].split(' ')[0]
						loc = line[-2].replace(line[-2],dic_cello_loc[line[-2]])
						if not id_sp1 in dic_pred:
							dic_pred[id_sp1]={}
						
							if not loc in dic_pred[id_sp1]:
								dic_pred[id_sp1][loc]=[]
								dic_pred[id_sp1][loc].append(float(score))
							if loc in dic_pred[id_sp1]:
								dic_pred[id_sp1][loc].append(float(score))
	
						if id_sp1 in dic_pred:
							loc = line[-2].replace(line[-2],dic_cello_loc[line[-2]])
						
							if not loc in dic_pred[id_sp1]:
								dic_pred[id_sp1][loc]=[]
								dic_pred[id_sp1][loc].append(float(score))
							#dic_pred[id_sp1][loc]=round(float(line[-1].split(' ')[0])/7,2)
							if loc in dic_pred[id_sp1]:
								dic_pred[id_sp1][loc].append(float((score)))
								
				if id_sp1 != id_sp1 and len(line) == 7:
					if line[-2]  in dic_cello_loc.keys():
						score = line[-1].split(' ')[0]
						loc = line[-2].replace(line[-2],dic_cello_loc[line[-2]])
						if not id_sp1 in dic_pred:
							dic_pred[id_sp1]={}
							
							if not loc in dic_pred[id_sp1]:	
								dic_pred[id_sp1][loc]=[]			
								dic_pred[id_sp1][loc].append(float(score))
							if loc in dic_pred:
								dic_pred[id_sp1][loc].append(float(score))
	
						if id_sp1 in dic_pred:
							loc = line[-2].replace(line[-2],dic_cello_loc[line[-2]])
						
							if not loc in dic_pred[id_sp1]:
								dic_pred[id_sp1][loc]=[]
								dic_pred[id_sp1][loc].append(float(score))
							#dic_pred[id_sp1][loc]=round(float(score)
							if loc in dic_pred[id_sp1]:
								dic_pred[id_sp1][loc].append(float(score))
	
				if line[-4] == '':
					if id_sp1 == id_sp1 and len(line) == 8:
						if line[-3]  in dic_cello_loc.keys():
							loc = line[-3].replace(line[-3],dic_cello_loc[line[-3]])
							score = line[-1].split(' ')[0]
							if not id_sp1 in dic_pred:
								dic_pred[id_sp1]={}
							
								if not loc in dic_pred[id_sp1]:
									dic_pred[id_sp1][loc]=[]
									dic_pred[id_sp1][loc].append(float(score))
								if loc in dic_pred[id_sp1]:
									dic_pred[id_sp1][loc].append(float(score))
							if id_sp1 in dic_pred:
							
								if not loc in dic_pred[id_sp1]:
									dic_pred[id_sp1][loc]=[]
									dic_pred[id_sp1][loc].append(float(score))
								if loc in dic_pred[id_sp1]:
									dic_pred[id_sp1][loc].append(float(score))
					if id_sp1 != id_sp1 and len(line) == 8:
						if line[-3]  in dic_cello_loc.keys():
							loc = line[-3].replace(line[-3],dic_cello_loc[line[-3]])
							score = line[-1].split(' ')[0]
							if not id_sp1 in dic_pred:
								dic_pred[id_sp1]={}
							
								if not loc in dic_pred[id_sp1]:
									dic_pred[id_sp1][loc]=[]							
									dic_pred[id_sp1][loc].append(float(score))
								if loc in dic_pred[id_sp1]:
									dic_pred[id_sp1][loc].append(float(score))
							if id_sp1 in dic_pred:
							
								if not loc in dic_pred[id_sp1]:	
									dic_pred[id_sp1][loc]=[]						
									dic_pred[id_sp1][loc].append(float(score))
								if loc in dic_pred[id_sp1]:
									dic_pred[id_sp1][loc].append(float(score))
	
		for k,v in dic_pred.iteritems():
			k =  k.strip('\n')
			for loc1,s in v.iteritems():
				score = round(sum(set(s))/8,3)
				if not k in dic_cello:
					dic_cello[k]={}
					dic_cello[k][loc1]=score
				if k in dic_cello:
					dic_cello[k][loc1]=score
		cello_df = pd.DataFrame(dic_cello).T
		#print cello_df
		cello_df.to_csv(sys.argv[1]+'/for-dat/'+str(filename)+'.cello.csv', sep='\t', encoding='utf-8')
	except:
		pass

def parse_loctree2(loctree2,filename):
	dic_loctree2 = {}
	for line in loctree2:
		if line.startswith('sp'):
			sp_id1 = line.split('\t')[0].strip('\n')
			loc = line.split('\t')[1].strip('\n')
			score = line.split('\t')[2].strip('\n')
			score = float(score)/100
			if loc in dic_loctree2_loc.keys():
				loc = loc.replace(loc,dic_loctree2_loc[loc])
				if not sp_id1 in dic_loctree2:
					dic_loctree2[sp_id1]={}
					dic_loctree2[sp_id1][loc]=score
				if sp_id1 in dic_loctree2:
					dic_loctree2[sp_id1][loc]=score
	
	
	loctree2_df = pd.DataFrame(dic_loctree2).T
	
	## CHECK THE SINGLE LOCALIZATION FROM LOCTREE2 AND THEN
	## ADD COLUMNS WITH VALUE = 0 BECAUSE LOCTREE2 GIVE SINGLE LOCALIZATION
	loc_not_present_in_loctree2 = []
	for k,v in dic_loctree2_loc.iteritems():
		loc_not_present_in_loctree2.append(v)
	
	
	loc_df_in_loctree2 = list(loctree2_df.columns.values)#[0]
	
	
	if loc_df_in_loctree2[0] in set(loc_not_present_in_loctree2):
		to_add_in_loctree2 = list(set(loc_not_present_in_loctree2)-set(loc_df_in_loctree2))
	
	lack_loc_in_loctree2 = sorted(to_add_in_loctree2)
	
	for col_in_loctree2 in lack_loc_in_loctree2:
	    loctree2_df[col_in_loctree2] = 0.0
	
	loctree2_df = loctree2_df.fillna(0.0)
	loctree2_df = loctree2_df.sort_index(axis=1)
	loctree2_df.to_csv(sys.argv[1]+'/for-dat/'+str(filename)+'.loctree2.csv', sep='\t', encoding='utf-8')


def parse_multiloc2(multiloc2,filename):
	dic_multiloc2 = {}
	for line in multiloc2:
		if line.startswith('sp'):
			line = line.replace(':',',').replace('\t',',').replace(', ',',').strip('\n')
			ids = line.split(',')[0].strip('\n')
			#loc = line.split(',')[1].split(':')[0]
			d = dict(itertools.izip_longest(*[iter(line.split(',')[1:])] * 2, fillvalue=""))
			x = list(''.join(value) for key, value in d.items() if 'lysosomal' in key or "peroxisomal" in key)
			d.pop('lysosomal')
			d.pop('peroxisomal')
			a = float(x[0])
			b = float(x[1])
			x1 = round(float(a+b),3)
			d['VES']=x1
			d3 = {v2:v for k2,v2 in dic_multiloc2_loc.iteritems() for k,v in d.iteritems() if k==k2}
			dic_multiloc2[ids]=d3
	
	multiloc2_df = pd.DataFrame(dic_multiloc2).T
	multiloc2_df.to_csv(sys.argv[1]+'/for-dat/'+str(filename)+'.multiloc2.csv', sep='\t', encoding='utf-8')

def parse_sherloc2(sherloc2,filename):
	dic_sherloc2 = {}
	for line in sherloc2:
		if line.startswith('sp'):
			line = line.replace(':',',').replace('\t',',').replace(', ',',').strip('\n')
			ids = line.split(',')[0].strip('\n')
			#loc = line.split(',')[1].split(':')[0]
			d4 = dict(itertools.izip_longest(*[iter(line.split(',')[1:])] * 2, fillvalue=""))
			x = list(''.join(value) for key, value in d4.items() if 'lysosomal' in key or "peroxisomal" in key)
			d4.pop('lysosomal')
			d4.pop('peroxisomal')
			a = float(x[0])
			b = float(x[1])
			x1 = round(float(a+b),3)
			d4['VES']=x1
			d5 = {v2:v for k2,v2 in dic_sherloc2_loc.iteritems() for k,v in d4.iteritems() if k==k2}
			dic_sherloc2[ids]=d5
	
	sherloc2_df = pd.DataFrame(dic_sherloc2).T
	sherloc2_df.to_csv(sys.argv[1]+'/for-dat/'+str(filename)+'.sherloc2.csv', sep='\t', encoding='utf-8')

def parse_yloc(yloc,filename):
	dic_yloc = {}
	try:
		for line in yloc:
			sp_id1 = line.split(',')[0].strip('\n')
			loc = line.split(',')[1].split(' ')[0].strip('\n')
			score = line.split(',')[1].split('(')[1].replace(')','').replace('%','')
			score = round(float(score)/100,3)
			if loc in dic_yloc_loc.keys():
				loc = loc.replace(loc,dic_yloc_loc[loc])
				if not sp_id1 in dic_yloc:
					dic_yloc[sp_id1]={}
					dic_yloc[sp_id1][loc]=score
				if sp_id1 in dic_yloc:
					dic_yloc[sp_id1][loc]=score
	
		yloc_df = pd.DataFrame(dic_yloc).T
		
		## CHECK THE ONLY LOCALIZATION FROM YLOC AND THEN
		## ADD COLUMNS WITH VALUE = 0 BECAUSE YLOC GIVE SINGLE LOCALIZATION
		loc_not_present_in_yloc = []
	
		for k,v in dic_yloc_loc.iteritems():
			loc_not_present_in_yloc.append(v)
		
		loc_df_in_yloc = list(yloc_df.columns.values)
	
	
		if loc_df_in_yloc[0] in set(loc_not_present_in_yloc):
			to_add_in_yloc = list(set(loc_not_present_in_yloc)-set(loc_df_in_yloc))
	
		lack_loc_in_yloc = sorted(to_add_in_yloc)
	
		for col_in_yloc in lack_loc_in_yloc:
	    		yloc_df[col_in_yloc] = 0.0
		yloc_df = yloc_df.fillna(0.0)
		yloc_df = yloc_df.sort_index(axis=1)
		yloc_df.to_csv(sys.argv[1]+'/for-dat/'+str(filename)+'.yloc.csv', sep='\t', encoding='utf-8')
	
	except:
		pass
	
			
	
path_results = sys.argv[1]+'/prediction/'
paths_results = glob.glob(path_results+'*.*.res')


for el in paths_results:
	name_file = el.split('/')[2].split('.')[0]
	predictor_used = el.split('/')[2]
	if predictor_used.endswith(".lc2.res"):
		file_pred = open(sys.argv[1]+'/prediction/'+str(predictor_used))
		parse_loctree2(file_pred,name_file)	
			
	if predictor_used.endswith(".s2.res"):
		file_pred = open(sys.argv[1]+'/prediction/'+str(predictor_used))
		parse_sherloc2(file_pred,name_file)	
		
	if predictor_used.endswith(".m2.res"):
		file_pred = open(sys.argv[1]+'/prediction/'+str(predictor_used))
		parse_multiloc2(file_pred,name_file)
		
	if predictor_used.endswith(".c.res"):
		file_pred = open(sys.argv[1]+'/prediction/'+str(predictor_used))
		parse_cello(file_pred,name_file)
	
	if predictor_used.endswith(".y.res"):
		file_pred = open(sys.argv[1]+'/prediction/'+str(predictor_used))
		parse_yloc(file_pred,name_file)
		




	




	
	
	
	
	
	
