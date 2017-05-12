import numpy as np
import sys,glob,os
import pandas as pd
import matplotlib.pyplot as plt
 


if not len(sys.argv) == 2:
  print "Usage:",sys.argv[0],"results_folder "
  sys.exit(-1)



def predictors_merged_dataframe(list_pred,a):
	global df_final1

		
	if len(list_pred)==4:
		list_pred = sorted(list_pred)
		predictor1 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[0])+".csv", sep='\t', encoding='utf-8')
		predictor2 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[1])+".csv", sep='\t', encoding='utf-8')
		predictor3 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[2])+".csv", sep='\t', encoding='utf-8')
		predictor4 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[3])+".csv", sep='\t', encoding='utf-8')
		df_subcons = pd.read_csv(sys.argv[1]+"/final-prediction/"+str(k)+".subcons-final-pred.csv",sep = '\t', encoding='utf-8')
		df_1 = [predictor1,predictor2,predictor3,predictor4]
		df_final = pd.concat(df_1)
		df_final1 = df_final.rename(columns={'Unnamed: 0': 'id_protein'})	
		df_final1 = df_final1.drop('id_protein',1)
		#print df_final1
		df_subcons_1 = df_subcons.drop('LOC_DEF',1)
		df_subcons_1 = df_subcons_1.drop('id_protein',1)
		new_columns = df_subcons_1.columns[df_subcons_1.ix[df_subcons_1.last_valid_index()].argsort()]
		df_subcons_1 =  df_subcons_1[new_columns]
		df_final1 = df_final1[new_columns]
		df_all = df_final1.append(df_subcons_1,ignore_index=True)
		list_pred.append("SubCons")
		se = pd.Series(list_pred)
		df_all['Tools'] = se.values
		cols = df_all.columns.tolist()
		cols = cols[-1:] + cols[:-1]
		df_all = df_all[cols]
		df_all.set_index("Tools", drop=True, inplace=True)
		dictionary = df_all.to_dict(orient = "index")
		dictionary['LocTree2'] = dictionary.pop('loctree2')
		dictionary['MultiLoc2'] = dictionary.pop('multiloc2')
		dictionary['SherLoc2'] = dictionary.pop('sherloc2')
		dictionary['CELLO2.5'] = dictionary.pop('cello')
		df_finished= pd.DataFrame(dictionary)
		df_finished =  df_finished.T
		final_columns = df_finished.columns[df_finished.ix[df_finished.last_valid_index()].argsort()]
		df_finished = df_finished[final_columns]
		df_finished = df_finished[df_finished.columns[::-1]]
		df_finished.to_csv(sys.argv[1]+'/plot/'+str(predictor1["Unnamed: 0"][0])+'.csv', sep='\t', encoding='utf-8')
		
	elif len(list_pred) == 3:
		list_pred = sorted(list_pred)
		predictor1 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[0])+".csv", sep='\t', encoding='utf-8')
		predictor2 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[1])+".csv", sep='\t', encoding='utf-8')
		predictor3 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[2])+".csv", sep='\t', encoding='utf-8')
		df_subcons = pd.read_csv(sys.argv[1]+"/final-prediction/"+str(k)+".subcons-final-pred.csv",sep = '\t', encoding='utf-8')
		df_1 = [predictor1,predictor2,predictor3]
		df_final = pd.concat(df_1)
		df_final1 = df_final.rename(columns={'Unnamed: 0': 'id_protein'})
		df_final1 = df_final1.drop('id_protein',1)
		df_subcons_1 = df_subcons.drop('LOC_DEF',1)
		df_subcons_1 = df_subcons_1.drop('id_protein',1)
		new_columns = df_subcons_1.columns[df_subcons_1.ix[df_subcons_1.last_valid_index()].argsort()]
		df_subcons_1 =  df_subcons_1[new_columns]
		df_final1 = df_final1[new_columns]
		df_all = df_final1.append(df_subcons_1,ignore_index=True)
		list_pred.append("SubCons")
		se = pd.Series(list_pred)
		df_all['Tools'] = se.values
		cols = df_all.columns.tolist()
		cols = cols[-1:] + cols[:-1]
		df_all = df_all[cols]
                df_all.set_index("Tools", drop=True, inplace=True)
                dictionary = df_all.to_dict(orient = "index")
                dictionary['LocTree2'] = dictionary.pop('loctree2')
                dictionary['MultiLoc2'] = dictionary.pop('multiloc2')
                dictionary['SherLoc2'] = dictionary.pop('sherloc2')
                df_finished= pd.DataFrame(dictionary)
                df_finished =  df_finished.T
                final_columns = df_finished.columns[df_finished.ix[df_finished.last_valid_index()].argsort()]
                df_finished = df_finished[final_columns]
		df_finished = df_finished[df_finished.columns[::-1]]
		df_finished.to_csv(sys.argv[1]+'/plot/'+str(predictor1["Unnamed: 0"][0])+'.csv', sep='\t', encoding='utf-8')



	
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
	predictors_merged_dataframe(predictor_list,k)

for files_csv in os.listdir(sys.argv[1]+"/plot/"):
	print files_csv
	name_plot = files_csv.split('.')[0]

	data = pd.read_csv(sys.argv[1]+"/plot/"+str(files_csv), sep='\t', encoding='utf-8')
	plt.figure(figsize=(20,10))
	ind = np.arange(len(data[data.columns[0]]))  
	colors = {"GLG":'#1f77b4',"NUC":'#ff7f0e',"EXC":'#7f7f7f',"MIT":'#d62728',"PEX":'#9467bd',"CYT":'#bcbd22',"MEM":'#98df8a',"LYS":'#17becf',"ERE":'#393b79'}
	localizations = data.columns.values[1:]
	localizations = localizations.tolist()
	data.plot(kind="barh", stacked=True, color=[colors[i] for i in data[localizations]])
	plt.yticks(ind, data[data.columns[0]],fontsize = 11)
	plt.legend(loc="best", bbox_to_anchor=(1.0, 1.00))
	plt.subplots_adjust(right=0.75)
	plt.gca().yaxis.grid(False)
	plt.gca().xaxis.grid(True)
	plt.autoscale(tight=True)
	plt.savefig(sys.argv[1]+"/plot/"+str(name_plot)+".pdf",transparent=True,dpi = 500)


		
