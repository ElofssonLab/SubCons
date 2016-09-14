import sys,os,glob
import pandas as pd

if not len(sys.argv) == 2:
  print "Usage:",sys.argv[0],"results_folder"
  sys.exit(-1)



def create_merged_dataframe(list_pred,a):
	global df_final1
	
	if len(list_pred)==5:
		predictor1 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[0])+".csv", sep='\t', encoding='utf-8')
		predictor2 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[1])+".csv", sep='\t', encoding='utf-8')
		predictor3 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[2])+".csv", sep='\t', encoding='utf-8')
		predictor4 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[3])+".csv", sep='\t', encoding='utf-8')
		predictor5 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[4])+".csv", sep='\t', encoding='utf-8')
		df_1 = pd.DataFrame(predictor1).merge(pd.DataFrame(predictor2),on='Unnamed: 0').merge(pd.DataFrame(predictor3),on='Unnamed: 0')
		df_2 = pd.DataFrame(predictor4).merge(pd.DataFrame(predictor5),on='Unnamed: 0')
		
		df_final = pd.merge(df_1,df_2,on='Unnamed: 0',how='inner')
		df_final1 = df_final.rename(columns={'Unnamed: 0': 'IDs'})
		df_final1.columns =['IDs','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40']
		return df_final1
	
	if len(list_pred)==4:
		predictor1 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[0])+".csv", sep='\t', encoding='utf-8')
		predictor2 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[1])+".csv", sep='\t', encoding='utf-8')
		predictor3 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[2])+".csv", sep='\t', encoding='utf-8')
		predictor4 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[3])+".csv", sep='\t', encoding='utf-8')
		df_1 = pd.DataFrame(predictor1).merge(pd.DataFrame(predictor2),on='Unnamed: 0')
		df_2 = pd.DataFrame(predictor3).merge(pd.DataFrame(predictor4),on='Unnamed: 0')
		df_final = pd.merge(df_1,df_2,on='Unnamed: 0',how='inner')
		df_final1 = df_final.rename(columns={'Unnamed: 0': 'IDs'})
		df_final1.columns =['IDs','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32']
		return df_final1
	
	elif len(list_pred) == 3:
		predictor1 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[0])+".csv", sep='\t', encoding='utf-8')
		predictor2 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[1])+".csv", sep='\t', encoding='utf-8')
		predictor3 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[2])+".csv", sep='\t', encoding='utf-8')
		
		df_1 = pd.DataFrame(predictor1).merge(pd.DataFrame(predictor2),on='Unnamed: 0').merge(pd.DataFrame(predictor3),on='Unnamed: 0')
		df_final1 = df_1.rename(columns={'Unnamed: 0': 'IDs'})
		df_final1.columns =['IDs','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
		return df_final1
	


predictor_list = []
all_list = []
dic_all = {}		
for el in os.listdir(sys.argv[1]+"/for-dat/"):
	name_file = el.split('.')[0]
	all_list.append(el)
	predictor_used = el.split('.')[1]
	predictor_list.append(predictor_used)
	predictor_list= sorted(set(predictor_list))
	if name_file in dic_all:
		dic_all[name_file].append(el)
	if not name_file in dic_all:
		dic_all[name_file]=[]
		dic_all[name_file].append(el)

print predictor_list
		
for k,v in dic_all.iteritems():
	create_merged_dataframe(predictor_list,k)
	saveout = sys.stdout
	ff1 = open(sys.argv[1]+'/dat-files/'+str(k)+'.dat','w+')
	sys.stdout=ff1
	for row in create_merged_dataframe(predictor_list,k).iterrows():
		data = row[1][1:]
		alist = []
		for k, v in data.iteritems():
			alist.append(str(k)+' '+str(v))
		print "0 "+' '.join(alist)+' #'+str(row[1][0])
		
	
	sys.stdout=saveout
	ff1.close()

