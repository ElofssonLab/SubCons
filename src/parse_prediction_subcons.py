import glob,os,sys
import itertools
import pandas as pd
import time
from collections import Counter

if not len(sys.argv) == 2:
  print "Usage:",sys.argv[0],"results_folder"
  sys.exit(-1)

dic_loc = {'nuclear':'NUC','plasma membrane':'MEM','extracellular':'EXE','cytoplasmic':'CYT','mitochondrial':'MIT','ER':'ERE','peroxisomal':'PEX','lysosomal':'LYS','Golgi apparatus':'GLG'}
dic_sherloc2_loc = {'cytoplasmic':'CYT','ER':'ERE','Golgi apparatus':'GLG','lysosomal':'LYS','mitochondrial':'MIT','nuclear':'NUC','peroxisomal':'PEX','plasma membrane':'MEM','extracellular':'EXC'}
dic_loctree2_loc = {'chloroplast':'MIT','chloroplast membrane':'MIT','cytosol':'CYT','endoplasmic reticulum':'ERE','endoplasmic reticulum membrane':'ERE','golgi apparatus':'GLG','golgi apparatus membrane':'GLG','mitochondria':'MIT','mitochondria membrane':'MIT','nucleus':'NUC','nucleus membrane':'NUC','peroxisome':'PEX','peroxisome membrane':'PEX','plasma membrane':'MEM','plastid':'MIT','vacuole':'MIT','vacuole membrane':'MIT','secreted':'EXC','LYS':'LYS'}
dic_cello_loc ={'Chloroplast':'MIT','Cytoplasmic':'CYT','Cytoskeletal':'CYT','ER':'ERE','Golgi':'GLG','Lysosomal':'LYS','Mitochondrial':'MIT','Nuclear':'NUC','Peroxisomal':'PEX','PlasmaMembrane':'MEM',"Vacuole":"MIT",'Extracellular':'EXC'}
dic_multiloc2_loc = {'cytoplasmic':'CYT','ER':'ERE','Golgi apparatus':'GLG','lysosomal':'LYS','mitochondrial':'MIT','nuclear':'NUC','peroxisomal':'PEX','plasma membrane':'MEM','extracellular':'EXC'} 




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
				score = round(sum(set(s))/10,2)
				if not k in dic_cello:
					dic_cello[k]={}
					dic_cello[k][loc1]=score
				if k in dic_cello:
					dic_cello[k][loc1]=score
		cello_df = pd.DataFrame(dic_cello).T
		cello_df.to_csv(sys.argv[1]+'for-dat/'+str(filename)+'.cello.csv', sep='\t', encoding='utf-8')
	except:
		pass


def parse_loctree2(loctree2,filename):
	dic_loctree2 = {}
	for line in loctree2:
		if not line.startswith('#'):
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
		line = line.replace('MultiLoc2 Prediction Result','')
		line = line.rstrip('\n\n')
		if line != '':
			if not line.startswith('predictor'):
				if not line.startswith('origin'):
					line = line.rstrip()
					line = line.replace(':',',').replace('\t',',').replace(', ',',').strip('\n')
					ids = line.split(',')[0].strip('\n')
					d = dict(itertools.izip_longest(*[iter(line.split(',')[1:])] * 2, fillvalue=""))			
					d3 = {v2:v for k2,v2 in dic_multiloc2_loc.iteritems() for k,v in d.iteritems() if k==k2}
					dic_multiloc2[ids]=d3
	
	multiloc2_df = pd.DataFrame(dic_multiloc2).T
	multiloc2_df.to_csv(sys.argv[1]+'for-dat/'+str(filename)+'.multiloc2.csv', sep='\t', encoding='utf-8')

def parse_sherloc2(sherloc2,filename):
	dic_sherloc2 = {}
	for line in sherloc2:
		line = line.replace('SherLoc2 Prediction Result','')
		line = line.rstrip('\n\n')
		if line != '':
			if not line.startswith('origin'):
				line = line.rstrip()
				line = line.replace(':',',').replace('\t',',').replace(', ',',').strip('\n')
				ids = line.split(',')[0].strip('\n')
				d4 = dict(itertools.izip_longest(*[iter(line.split(',')[1:])] * 2, fillvalue=""))
				d5 = {v2:v for k2,v2 in dic_sherloc2_loc.iteritems() for k,v in d4.iteritems() if k==k2}
				dic_sherloc2[ids]=d5
	
	sherloc2_df = pd.DataFrame(dic_sherloc2).T
	sherloc2_df.to_csv(sys.argv[1]+'for-dat/'+str(filename)+'.sherloc2.csv', sep='\t', encoding='utf-8')
	
			
	
path_results = sys.argv[1]+'prediction/'
paths_results = glob.glob(path_results+'*.*.res')
print paths_results

for el in paths_results:
	name_file = el.split('/')[-1].split('.')[0]
	predictor_used = el.split('/')[-1]
	if predictor_used.endswith(".lc2.res"):
		file_pred = open(sys.argv[1]+'prediction/'+str(predictor_used))
		parse_loctree2(file_pred,name_file)	
			
	if predictor_used.endswith(".s2.res"):
		file_pred = open(sys.argv[1]+'prediction/'+str(predictor_used))
		parse_sherloc2(file_pred,name_file)	
		
	if predictor_used.endswith(".m2.res"):
		file_pred = open(sys.argv[1]+'prediction/'+str(predictor_used))
		parse_multiloc2(file_pred,name_file)
		
	if predictor_used.endswith(".c.res"):
		file_pred = open(sys.argv[1]+'prediction/'+str(predictor_used))
		parse_cello(file_pred,name_file)
	

		

