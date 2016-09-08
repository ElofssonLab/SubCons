import sys,os
import pandas as pd



loctree2 = pd.read_csv("../results/for-dat/loctree2.csv", sep='\t', encoding='utf-8')
multiloc2 = pd.read_csv("../results/for-dat/multiloc2.csv", sep='\t', encoding='utf-8')
sherloc2 = pd.read_csv("../results/for-dat/sherloc2.csv", sep='\t', encoding='utf-8')


list_available_pred = ["sherloc2","loctree2","multiloc2"]

try:
	cello = pd.read_csv("../results/for-dat/cello.csv", sep='\t', encoding='utf-8')
	list_available_pred.append('cello')
	
except:
	
	pass

try:
	yloc = pd.read_csv("../results/for-dat/yloc.csv", sep='\t', encoding='utf-8')
	list_available_pred.append('yloc')
	
except:
	pass



list_result = []
for files in os.listdir("../results/for-dat/"):
	files = files.split('.')[0]
	list_result.append(files)


print list_result

def create_merged_dataframe(list_pred):
	global df_final1
	if len(list_pred)==5:
		df_1 = pd.DataFrame(eval(list_pred[0])).merge(pd.DataFrame(eval(list_pred[1])),on='Unnamed: 0').merge(pd.DataFrame(eval(list_pred[2])),on='Unnamed: 0')
		df_2 = pd.DataFrame(eval(list_pred[3])).merge(pd.DataFrame(eval(list_pred[4])),on='Unnamed: 0')
		df_final = pd.merge(df_1,df_2,on='Unnamed: 0',how='inner')
		df_final1 = df_final.rename(columns={'Unnamed: 0': 'IDs'})
		df_final1.columns =['IDs','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',16,'17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40']
		#print df_final1
		return df_final1
	elif len(list_pred)==4:
		df_1 = pd.DataFrame(eval(list_pred[0])).merge(pd.DataFrame(eval(list_pred[1])),on='Unnamed: 0')
		df_2 = pd.DataFrame(eval(list_pred[2])).merge(pd.DataFrame(eval(list_pred[3])),on='Unnamed: 0')
		df_final = pd.merge(df_1,df_2,on='Unnamed: 0',how='inner')
		df_final1 = df_final.rename(columns={'Unnamed: 0': 'IDs'})
		df_final1.columns =['IDs','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',16,'17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32']
		#print df_final1		
		return df_final1
	
	elif len(list_pred) == 3:
		df_1 = pd.DataFrame(eval(list_pred[0])).merge(pd.DataFrame(eval(list_pred[1])),on='Unnamed: 0').merge(pd.DataFrame(eval(list_pred[2])),on='Unnamed: 0')
		df_final1 = df_1.rename(columns={'Unnamed: 0': 'IDs'})
		df_final1.columns =['IDs','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',16,'17','18','19','20','21','22','23','24']
		#print df_final1
		return df_final1



		
	
create_merged_dataframe(list_result)


saveout = sys.stdout
ff1 = open('../results/dat-files/prediction.dat','w+')
sys.stdout=ff1
for row in create_merged_dataframe(list_result).iterrows():
	data = row[1][1:]
	alist = []
	for k, v in data.iteritems():
		alist.append(str(k)+' '+str(v))
	print "0 "+' '.join(alist)+' #'+str(row[1][0])
		
	
sys.stdout=saveout
ff1.close()


