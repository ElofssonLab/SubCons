import numpy as np
import matplotlib.pyplot as plt
import sys,glob,os
import pandas as pd


if not len(sys.argv) == 2:
  print "Usage:",sys.argv[0],"results_folder "
  sys.exit(-1)






def predictors_merged_dataframe(list_pred,a):
	global df_final1
	if len(list_pred)==5:
		list_pred = sorted(list_pred)
		predictor1 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[0])+".csv", sep='\t', encoding='utf-8')
		predictor2 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[1])+".csv", sep='\t', encoding='utf-8')
		predictor3 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[2])+".csv", sep='\t', encoding='utf-8')
		predictor4 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[3])+".csv", sep='\t', encoding='utf-8')
		predictor5 = pd.read_csv(sys.argv[1]+"/for-dat/"+str(k)+"."+str(list_pred[4])+".csv", sep='\t', encoding='utf-8')
		df_subcons = pd.read_csv(sys.argv[1]+"/final-prediction/"+str(k)+".subcons-final-pred.csv",sep = '\t', encoding='utf-8')
		df_1 = [predictor1,predictor2,predictor3,predictor4,predictor5]
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
		df_all.Tools[df_all.Tools=='cello']='CELLO2.5'
		df_all.Tools[df_all.Tools=='sherloc2']='SherLoc2'
		df_all.Tools[df_all.Tools=='multiloc2']='MultiLoc2'
		df_all.Tools[df_all.Tools=='loctree2']='LocTree2'
		df_all.Tools[df_all.Tools=='yloc']='YLoc'
		df_all.to_csv(sys.argv[1]+'/plot/'+str(predictor1["Unnamed: 0"][0])+'.csv', sep='\t', encoding='utf-8')
		
	elif len(list_pred)==4:
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
		df_all.Tools[df_all.Tools=='sherloc2']='SherLoc2'
		df_all.Tools[df_all.Tools=='multiloc2']='MultiLoc2'
		df_all.Tools[df_all.Tools=='loctree2']='LocTree2'
		df_all.Tools[df_all.Tools=='cello']='CELLO2.5'
		df_all.Tools[df_all.Tools=='yloc']='YLoc'
		df_all.to_csv(sys.argv[1]+'/plot/'+str(predictor1["Unnamed: 0"][0])+'.csv', sep='\t', encoding='utf-8')
		
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
		df_all.Tools[df_all.Tools=='sherloc2']='SherLoc2'
		df_all.Tools[df_all.Tools=='multiloc2']='MultiLoc2'
		df_all.Tools[df_all.Tools=='loctree2']='LocTree2'
		df_all.to_csv(sys.argv[1]+'/plot/'+str(predictor1["Unnamed: 0"][0])+'.csv', sep='\t', encoding='utf-8')


	
predictor_list = []
all_list = []
dic_all = {}		
for el in os.listdir(sys.argv[1]+"/for-dat/"):
	
	name_file = el.split('.')[0]
	all_list.append(el)
	predictor_used = el.split('.')[1]
	predictor_list.append(predictor_used)
	predictor_list= sorted(set(predictor_list),reverse= True)
	if name_file in dic_all:
		dic_all[name_file].append(el)
	if not name_file in dic_all:
		dic_all[name_file]=[]
		dic_all[name_file].append(el)

print predictor_list	
for k,v in dic_all.iteritems():
	predictors_merged_dataframe(predictor_list,k)

# I PLOT WITH GGPLOTW IN R BECAUSE 
# IF YOU LIKE MORE THE MATPLOTLIB LIBRARY DECOMMET THIS
'''	
for files_csv in os.listdir(sys.argv[1]+"/plot/"):
	print files_csv
	name_plot = files_csv.split('.')[0]

	
	q = pd.read_csv(sys.argv[1]+"/plot/"+str(files_csv), sep='\t', encoding='utf-8')

	plt.figure(figsize=(10,5))
	if len(predictor_list) == 5: 
		N = 6
		ind = np.arange(N)    # the x locations for the groups
		width = 0.3       # the width of the bars: can also be len(x) sequence
		p1 = plt.barh(ind+0.05, q[q.columns[9]], width,color='#ed3747')
		p2 = plt.barh(ind+0.05, q[q.columns[8]], width,color='#33499a',left=q[q.columns[9]])
		p3 = plt.barh(ind+0.05, q[q.columns[7]], width,color='orange',left=q[q.columns[9]] +q[q.columns[8]])
		p4 = plt.barh(ind+0.05, q[q.columns[6]], width,color='#008000',left=q[q.columns[9]] +q[q.columns[8]]+q[q.columns[7]])
		p5 = plt.barh(ind+0.05, q[q.columns[5]], width,color='#ffff66',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]])
		p6 = plt.barh(ind+0.05, q[q.columns[4]], width,color='#a04c97',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]]+q[q.columns[5]])
		p7 = plt.barh(ind+0.05, q[q.columns[3]], width,color='#12CFF5',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]]+q[q.columns[5]]+q[q.columns[4]])
		p8 = plt.barh(ind+0.05, q[q.columns[2]], width,color='#FF33CC',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]]+q[q.columns[5]]+q[q.columns[4]]+q[q.columns[3]])

		plt.xlabel('Predicted Score per Localization',fontsize = 10)
		plt.title('PREDICTION RESULTS FOR: '+str(name_plot),fontsize = 13)
		plt.yticks(ind+0.05 + width/2., q[q.columns[1]],fontsize = 11)#,rotation=20)
		plt.xticks([0,0.2,0.4,0.6,0.8,1])
		plt.legend((p1[0], p2[0],p3[0], p4[0],p5[0], p6[0],p7[0],p8[0]), (q.columns[9],q.columns[8],q.columns[7],q.columns[6],q.columns[5],q.columns[4],q.columns[3],q.columns[2]),fontsize = 12, bbox_to_anchor=(1, .98), fancybox=True, shadow=True)
		plt.grid(b=False,color='grey', linestyle='--')
		plt.savefig(sys.argv[1]+"/plot/"+str(name_plot)+".pdf",transparent=True,dpi = 300)


	elif len(predictor_list) == 4: 
		N = 5
		ind = np.arange(N)    # the x locations for the groups
		width = 0.3       # the width of the bars: can also be len(x) sequence
		p1 = plt.barh(ind+0.05, q[q.columns[9]], width,color='#ed3747')
		p2 = plt.barh(ind+0.05, q[q.columns[8]], width,color='#33499a',left=q[q.columns[9]])
		p3 = plt.barh(ind+0.05, q[q.columns[7]], width,color='orange',left=q[q.columns[9]] +q[q.columns[8]])
		p4 = plt.barh(ind+0.05, q[q.columns[6]], width,color='#008000',left=q[q.columns[9]] +q[q.columns[8]]+q[q.columns[7]])
		p5 = plt.barh(ind+0.05, q[q.columns[5]], width,color='#ffff66',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]])
		p6 = plt.barh(ind+0.05, q[q.columns[4]], width,color='#a04c97',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]]+q[q.columns[5]])
		p7 = plt.barh(ind+0.05, q[q.columns[3]], width,color='#12CFF5',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]]+q[q.columns[5]]+q[q.columns[4]])
		p8 = plt.barh(ind+0.05, q[q.columns[2]], width,color='#FF33CC',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]]+q[q.columns[5]]+q[q.columns[4]]+q[q.columns[3]])

		plt.xlabel('Predicted Score per Localization',fontsize = 10)
		plt.title('PREDICTION RESULTS FOR: '+str(name_plot),fontsize = 13)
		plt.yticks(ind+0.05 + width/2., q[q.columns[1]],fontsize = 11)#,rotation=20)
		plt.xticks([0,0.2,0.4,0.6,0.8,1])
		plt.legend((p1[0], p2[0],p3[0], p4[0],p5[0], p6[0],p7[0],p8[0]), (q.columns[9],q.columns[8],q.columns[7],q.columns[6],q.columns[5],q.columns[4],q.columns[3],q.columns[2]),fontsize = 12, bbox_to_anchor=(1, .98), fancybox=True, shadow=True)
		plt.grid(b=False,color='grey', linestyle='--')
		plt.savefig(sys.argv[1]+"/plot/"+str(name_plot)+".pdf",transparent=True,dpi = 300)

	elif len(predictor_list) == 3: 
		N = 4
		ind = np.arange(N)    # the x locations for the groups
		width = 0.3       # the width of the bars: can also be len(x) sequence
		p1 = plt.barh(ind+0.05, q[q.columns[9]], width,color='#ed3747')
		p2 = plt.barh(ind+0.05, q[q.columns[8]], width,color='#33499a',left=q[q.columns[9]])
		p3 = plt.barh(ind+0.05, q[q.columns[7]], width,color='orange',left=q[q.columns[9]] +q[q.columns[8]])
		p4 = plt.barh(ind+0.05, q[q.columns[6]], width,color='#008000',left=q[q.columns[9]] +q[q.columns[8]]+q[q.columns[7]])
		p5 = plt.barh(ind+0.05, q[q.columns[5]], width,color='#ffff66',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]])
		p6 = plt.barh(ind+0.05, q[q.columns[4]], width,color='#a04c97',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]]+q[q.columns[5]])
		p7 = plt.barh(ind+0.05, q[q.columns[3]], width,color='#12CFF5',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]]+q[q.columns[5]]+q[q.columns[4]])
		p8 = plt.barh(ind+0.05, q[q.columns[2]], width,color='#FF33CC',left=q[q.columns[9]]+q[q.columns[8]]+q[q.columns[7]]+q[q.columns[6]]+q[q.columns[5]]+q[q.columns[4]]+q[q.columns[3]])

		plt.xlabel('Predicted Score per Localization',fontsize = 10)
		plt.title('PREDICTION RESULTS FOR: '+str(name_plot),fontsize = 13)
		plt.yticks(ind+0.05 + width/2., q[q.columns[1]],fontsize = 11)#,rotation=20)
		plt.xticks([0,0.2,0.4,0.6,0.8,1])
		plt.legend((p1[0], p2[0],p3[0], p4[0],p5[0], p6[0],p7[0],p8[0]), (q.columns[9],q.columns[8],q.columns[7],q.columns[6],q.columns[5],q.columns[4],q.columns[3],q.columns[2]),fontsize = 12, bbox_to_anchor=(1, .98), fancybox=True, shadow=True)
		plt.grid(b=False,color='grey', linestyle='--')
		plt.savefig(sys.argv[1]+"/plot/"+str(name_plot)+".pdf",transparent=True,dpi = 300)

'''
