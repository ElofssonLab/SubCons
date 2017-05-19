import numpy as np
import sys,glob,os
import pandas as pd
import matplotlib as mpl
import matplotlib.gridspec as gridspec
mpl.use('Agg')
import matplotlib.pyplot as plt
 
rundir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.realpath("%s/../"%(rundir))


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
		list_pred.append("SubCons-RF-Score")
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
		list_pred.append("SubCons-RF-Score")
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
	others = pd.read_csv('%s/precision-score/others.csv'%(basedir),sep = ',')
	results = pd.read_csv(sys.argv[1]+"/plot/"+str(files_csv), sep='\t', encoding='utf-8')
	cyt = pd.read_csv('%s/precision-score/cyt-precision-score.csv'%(basedir),sep = ',')
	nuc = pd.read_csv('%s/precision-score/nuc-precision-score.csv'%(basedir),sep = ',')
	loc_subcons = round(float(results.iloc[4][1]),1)
	results.set_index('Unnamed: 0', inplace=True)
	decimals = pd.Series([2, 2], index=['Average','Unnamed: 6'])
	cyt = cyt.round(decimals)
	nuc = nuc.round(decimals)
	others = others.round(decimals)
	cyt_score = cyt.loc[cyt['Average'] == (round(results.iloc[4]['CYT'],2))]
	nuc_score = nuc.loc[nuc['Average'] == (round(results.iloc[4]['NUC'],2))]
	mit_score = others.loc[others['Average'] == (round(results.iloc[4]['MIT'],2))]
	pex_score = others.loc[others['Average'] == (round(results.iloc[4]['PEX'],2))]
	mem_score = others.loc[others['Average'] == (round(results.iloc[4]['MEM'],2))]
	lys_score = others.loc[others['Average'] == (round(results.iloc[4]['LYS'],2))]
	ere_score = others.loc[others['Average'] == (round(results.iloc[4]['ERE'],2))]
	glg_score = others.loc[others['Average'] == (round(results.iloc[4]['GLG'],2))]
	exc_score = others.loc[others['Average'] == (round(results.iloc[4]['EXC'],2))]
	dic_cyt = cyt_score.set_index('Average').to_dict() 
	dic_ere = ere_score.set_index('Average').to_dict() 
	dic_glg = glg_score.set_index('Average').to_dict() 
	dic_lys = lys_score.set_index('Average').to_dict() 
	dic_mem = mem_score.set_index('Average').to_dict() 
	dic_mit = mit_score.set_index('Average').to_dict() 
	dic_nuc = nuc_score.set_index('Average').to_dict() 
	dic_pex = pex_score.set_index('Average').to_dict()
	dic_exc = exc_score.set_index('Average').to_dict() 
	final_cyt = round(dic_cyt['Unnamed: 6'][(round(results.iloc[4]['CYT'],2))],2)
	final_ere = round(dic_ere['Unnamed: 6'][(round(results.iloc[4]['ERE'],2))],2)
	final_glg = round(dic_glg['Unnamed: 6'][(round(results.iloc[4]['GLG'],2))],2)
	final_lys = round(dic_lys['Unnamed: 6'][(round(results.iloc[4]['LYS'],2))],2)
	final_mem = round(dic_mem['Unnamed: 6'][(round(results.iloc[4]['MEM'],2))],2)
	final_mit = round(dic_mit['Unnamed: 6'][(round(results.iloc[4]['MIT'],2))],2)
	final_nuc = round(dic_nuc['Unnamed: 6'][(round(results.iloc[4]['NUC'],2))],2)
	final_pex = round(dic_pex['Unnamed: 6'][(round(results.iloc[4]['PEX'],2))],2)
	final_exc = round(dic_exc['Unnamed: 6'][(round(results.iloc[4]['EXC'],2))],2)
	new_dataframe = [final_cyt,final_ere,final_glg,final_lys,final_mem,final_mit,final_nuc,final_pex,final_exc]
	loc_plot = results.axes[1].tolist()
	correct = {"NUC":final_nuc,"CYT":final_cyt,"ERE":final_ere,"GLG":final_glg,"LYS":final_lys,"MEM":final_mem,"MIT":final_mit,"PEX":final_pex,"EXC":final_exc}
	df_average_score = pd.DataFrame(correct,index=['SubCons-Reliability'], columns=loc_plot)
	loc_def_subcons = round(df_average_score.ix[:,0][0],2)
	frames = [results,df_average_score]
	final_df = pd.concat(frames)
	
	plt.figure(1,figsize=(8,5),frameon=False)
	gs = gridspec.GridSpec(2, 2,width_ratios=[12, 1],height_ratios=[1, 2])
	ax2 = plt.subplot(gs[0])
	ind = np.arange(len(final_df[final_df.columns[0]]))  
	colors = {"GLG":'#1f77b4',"NUC":'#ff7f0e',"EXC":'#7f7f7f',"MIT":'#d62728',"PEX":'#9467bd',"CYT":'#bcbd22',"MEM":'#98df8a',"LYS":'#17becf',"ERE":'#393b79'}
	localizations = final_df.columns.values[0:]
	localizations = localizations.tolist()
	final_df.iloc[4:].plot(ax=plt.gca(),kind="barh", stacked=True,color=[colors[i] for i in final_df[localizations]], width=0.9)#,linewidth=2.0)
	ax2.annotate(loc_def_subcons, (0.01, 0.85),fontsize=18)
	ax2.spines['bottom'].set_visible(False)
	ax2.yaxis.set_ticks_position('left')
	ax2.spines['right'].set_visible(False)
	ax2.spines['top'].set_visible(False)
	plt.yticks(fontsize = 13,fontweight='bold')
	plt.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') 
	plt.legend().set_visible(False)
	plt.xlim(0,1.05)
	
	ax4 = plt.subplot(gs[2])
	ind = np.arange(len(final_df[final_df.columns[0]]))  
	colors = {"GLG":'#1f77b4',"NUC":'#ff7f0e',"EXC":'#7f7f7f',"MIT":'#d62728',"PEX":'#9467bd',"CYT":'#bcbd22',"MEM":'#98df8a',"LYS":'#17becf',"ERE":'#393b79'}
	localizations = final_df.columns.values[0:]
	localizations = localizations.tolist()
	final_df.iloc[0:4].plot(ax=plt.gca(),kind="barh", stacked=True,color=[colors[i] for i in final_df[localizations]],width=0.75)
	plt.yticks(fontsize = 13)
	plt.legend(fontsize = 18,loc="best", ncol=1,bbox_to_anchor=(1.,1.14),handletextpad=0.2, frameon=False)
	plt.gca().yaxis.grid(False)
	plt.gca().xaxis.grid(False)
	ax4.xaxis.set_ticks_position('bottom')
	ax4.set_ylim(0,5)
	ax4.spines['right'].set_visible(False)
	ax4.spines['top'].set_visible(False)
	ax4.xaxis.set_ticks_position('bottom')
	ax4.yaxis.set_ticks_position('left')
	ax4.autoscale(enable=True, axis='both', tight=None)
	plt.ylim(-1,4.00)
	plt.xlim(0,1.05)
	plt.tight_layout(h_pad=-0.65)
	final_df.to_csv(sys.argv[1]+'/plot/'+str(name_plot)+'_final.csv', sep='\t', encoding='utf-8')
	plt.savefig(sys.argv[1]+"/plot/"+str(name_plot)+".pdf",transparent=True,bbox_inches="tight",pad_inches=0,dpi = 600)
	plt.savefig(sys.argv[1]+"/plot/"+str(name_plot)+".png",transparent=False,bbox_inches="tight",pad_inches=0,dpi = 600)
