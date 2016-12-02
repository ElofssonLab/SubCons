import string, sys, os, getopt, smtplib, math
import cgi,re,time,posix

rundir=os.path.dirname(os.path.realpath(__file__))
basedir=os.path.realpath("%s/../"%(rundir))
src_path=rundir

sys.path.append(src_path)

def run_shell_command(cmd):
        stdout_handle = os.popen(cmd, "r")
        return re.sub("\n","",stdout_handle.read())   

import svm_target, svm_sa, motif_search, svm_aac, svm_sherloc2, svm_goloc, svm_phyloloc, epiloc, util

sherloc2_mode= "stand-alone"
#sherloc2_mode= "online-service"

sender_address = 'blum@informatik.uni-tuebingen.de'
email = ""

def create_prediction_id():
	return "sl" + str(time.time())
	
def mail(serverURL=None, sender='', to='', subject='', text=''):
	"""
	Usage:
	mail('somemailserver.com', 'me@example.com', 'someone@example.com', 'test', 'This is a test')
	"""
	headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, to, subject)
	message = headers + text
	mailServer = smtplib.SMTP(serverURL)
	mailServer.sendmail(sender, to, message)
	mailServer.quit()

class TimeOutError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def check_load():
	wait = 60.0
	max_load_avg = 4.0
	time_abort = 60.0 * 60.0 * 24.0 * 3.0
	cmd_pat = "hmmpfam|iprscan|svm-predict|blastall"
	start = time.time()
	end = time.time()
	load_avg = 0.0
	while 1:
		file = open("/proc/loadavg","r")
		line = file.readline()
		file.close()
		tokens = line.split(" ")
		load_avg = float(tokens[0])
		cmd ="top -b -n 1 > top_out"
		os.system(cmd)
		file = open("top_out","r")
		top_out = file.read()
		file.close()
		os.system("rm -f top_out")
		found_cmd=0
		if re.findall(cmd_pat,top_out):
			found_cmd=1
		if load_avg < max_load_avg and found_cmd == 0:
			break
		end = time.time()
		if (end - start) > time_abort:
			raise TimeOutError("Time out!")
		time.sleep(wait)

def sherloc2_create_feature_vector(origin, fastafile, go_file_names, model, prediction_id, epilocfile):
	global sherloc2_mode
	use_inter_pro_scan = 1
	if sherloc2_mode == "stand-alone":
		use_inter_pro_scan = 0
	feature_vector = []
	print "create feature vectors"
        libsvm_path=os.path.dirname(run_shell_command("which svm-predict"))+"/"
	inter_pro_scan_path=""
        blast_path=os.path.dirname(run_shell_command("which blastall"))+"/"
        genome_path="%s/data/NCBI/"%(basedir)
	svm_data_path="%s/data/svm_models/SherLoc2/"%(basedir)
	util.validate_not_empty([libsvm_path,blast_path,genome_path,svm_data_path])
	if use_inter_pro_scan == 1:
		util.validate_not_empty([inter_pro_scan_path])
	if origin == "animal":
		fastafile.seek(0)
		svm_model_path=svm_data_path+"/sherloc2_noplant_svm_target/" 
		print "run SVMTarget"
		result_svmtarget=svm_target.noplant_predict(fastafile,model,svm_model_path,libsvm_path, prediction_id)		
		fastafile.seek(0)
		print "run SVMSA"
		result_svm_sa = svm_sa.noplant_predict(fastafile,svm_data_path,libsvm_path,12345, prediction_id)			
		fastafile.seek(0)
		aac_type="aac"
		table="Benchmark80A"
		svm_model_path=svm_data_path+"/sherloc2_animal_svmaac/"
		print "run SVMaac"
		result_svm_aac = svm_aac.animal_predict(aac_type,table,svm_model_path,fastafile,model,libsvm_path,prediction_id)
		fastafile.seek(0)
		svm_model_path=svm_data_path+"/sherloc2_animal_goloc/"
		if use_inter_pro_scan == 0 and len(go_file_names) == 0:
			print "skip GOLoc"
		else:
			print "run GOLoc"
		result_svm_goloc = svm_goloc.animal_predict(table,svm_model_path,fastafile,model,libsvm_path,inter_pro_scan_path,use_inter_pro_scan,go_file_names,prediction_id)
		fastafile.seek(0)
		svm_model_path=svm_data_path+"/sherloc2_animal_phyloloc_G78BS/"
		print "run PhyloLoc"
		result_svm_phyloloc = svm_phyloloc.animal_predict(table,svm_model_path,fastafile,model,libsvm_path,blast_path,genome_path,prediction_id)
		fastafile.seek(0)
		print "run MotifSearch"
		result_motif_search=motif_search.search(fastafile)	
		fastafile.seek(0)
		print "run EpiLoc"
		result_epiloc = epiloc.animal_predict(fastafile, epilocfile) 
		for i in range(0,len(result_motif_search)):
			feature_vector.append({'id' : result_motif_search[i]['id'],
									'score_sp':result_svmtarget[i]['score_sp'],
									'score_mtp':result_svmtarget[i]['score_mtp'],
									'score_other': result_svmtarget[i]['score_other'],
									'score_sa' :result_svm_sa[i]['score_sa'],
									'score_nuc': result_svm_aac[i]['score_nuc'],
									'score_cyt': result_svm_aac[i]['score_cyt'],
									'score_nuc_vs_cyt': result_svm_aac[i]['score_nuc_vs_cyt'],
									'score_mit': result_svm_aac[i]['score_mit'],
									'score_per': result_svm_aac[i]['score_per'],
									'score_lys': result_svm_aac[i]['score_lys'],
									'score_er': result_svm_aac[i]['score_er'],
									'score_gol': result_svm_aac[i]['score_gol'],
									'score_ext': result_svm_aac[i]['score_ext'],
									'score_pm': result_svm_aac[i]['score_pm'],
									'phylo_score_nuc': result_svm_phyloloc[i]['score_nuc'],
									'phylo_score_cyt': result_svm_phyloloc[i]['score_cyt'],
									'phylo_score_mit': result_svm_phyloloc[i]['score_mit'],
									'phylo_score_ext': result_svm_phyloloc[i]['score_ext'],
									'phylo_score_pm': result_svm_phyloloc[i]['score_pm'],
									'phylo_score_per': result_svm_phyloloc[i]['score_per'],
									'phylo_score_er': result_svm_phyloloc[i]['score_er'],
									'phylo_score_gol': result_svm_phyloloc[i]['score_gol'],
									'phylo_score_lys': result_svm_phyloloc[i]['score_lys'],
									'go_score_nuc': result_svm_goloc[i]['score_nuc'],
									'go_score_cyt': result_svm_goloc[i]['score_cyt'],
									'go_score_mit': result_svm_goloc[i]['score_mit'],
									'go_score_ext': result_svm_goloc[i]['score_ext'],
									'go_score_pm': result_svm_goloc[i]['score_pm'],
									'go_score_per': result_svm_goloc[i]['score_per'],
									'go_score_er': result_svm_goloc[i]['score_er'],
									'go_score_gol': result_svm_goloc[i]['score_gol'],
									'go_score_lys': result_svm_goloc[i]['score_lys'],
									'epiloc_score_nuc': result_epiloc[i]['score_nuc'],
									'epiloc_score_cyt': result_epiloc[i]['score_cyt'],
									'epiloc_score_mit': result_epiloc[i]['score_mit'],
									'epiloc_score_ext': result_epiloc[i]['score_ext'],
									'epiloc_score_pm': result_epiloc[i]['score_pm'],
									'epiloc_score_per': result_epiloc[i]['score_per'],
									'epiloc_score_er': result_epiloc[i]['score_er'],
									'epiloc_score_gol': result_epiloc[i]['score_gol'],
									'epiloc_score_lys': result_epiloc[i]['score_lys'],
									'er_target' : result_motif_search[i]['er_target'],
									'peroxi_target' : result_motif_search[i]['peroxi_target'],
									'nuclear_bipartite' :result_motif_search[i]['nuclear_bipartite'],
									'dna_associated_domain' :  result_motif_search[i]['dna_associated_domain'],
									'pm_receptor_domain': result_motif_search[i]['pm_receptor_domain'],
									'dna_associated_domain_desc' :  result_motif_search[i]['dna_associated_domain_desc'],
									'pm_receptor_domain_desc' : result_motif_search[i]['pm_receptor_domain_desc'],	
									'predictNLS' : result_motif_search[i]['predictNLS'],
									'nls_mono' : result_motif_search[i]['nls_mono']})
	elif origin == "fungal":
		fastafile.seek(0)
		svm_model_path=svm_data_path+"/sherloc2_noplant_svm_target/"
		print "run SVMTarget" 
		result_svmtarget=svm_target.noplant_predict(fastafile,model,svm_model_path,libsvm_path, prediction_id)
		result_svm_sa = []
		fastafile.seek(0)
		print "run SVMSA"
		result_svm_sa = svm_sa.noplant_predict(fastafile,svm_data_path,libsvm_path,12345, prediction_id)
		fastafile.seek(0)
		aac_type="aac"
		table="Benchmark80F"
		svm_model_path=svm_data_path+"/sherloc2_fungi_svmaac/"
		print "run SVMaac"
		result_svm_aac = svm_aac.fungi_predict(aac_type,table,svm_model_path,fastafile,model,libsvm_path,prediction_id)
		fastafile.seek(0)
		svm_model_path=svm_data_path+"/sherloc2_fungi_goloc/"
		if use_inter_pro_scan == 0 and len(go_file_names) == 0:
			print "skip GOLoc"
		else:
			print "run GOLoc"
		result_svm_goloc = svm_goloc.fungi_predict(table,svm_model_path,fastafile,model,libsvm_path,inter_pro_scan_path,use_inter_pro_scan,go_file_names,prediction_id)
		fastafile.seek(0)
		svm_model_path=svm_data_path+"/sherloc2_fungi_phyloloc_G78BS/"
		print "run PhyloLoc"
		result_svm_phyloloc = svm_phyloloc.fungi_predict(table,svm_model_path,fastafile,model,libsvm_path,blast_path,genome_path,prediction_id)
		fastafile.seek(0)
		print "run MotifSearch"
		result_motif_search=motif_search.search(fastafile)
		fastafile.seek(0)
		print "run EpiLoc"
		result_epiloc = epiloc.fungi_predict(fastafile,epilocfile) 
		for i in range(0,len(result_motif_search)):
			feature_vector.append({'id' : result_motif_search[i]['id'],
									'score_sp':result_svmtarget[i]['score_sp'],
									'score_mtp':result_svmtarget[i]['score_mtp'],
									'score_other': result_svmtarget[i]['score_other'],
									'score_sa' :result_svm_sa[i]['score_sa'],
									'score_nuc': result_svm_aac[i]['score_nuc'],
									'score_cyt': result_svm_aac[i]['score_cyt'],
									'score_nuc_vs_cyt': result_svm_aac[i]['score_nuc_vs_cyt'],
									'score_mit': result_svm_aac[i]['score_mit'],
									'score_per': result_svm_aac[i]['score_per'],
									'score_vac': result_svm_aac[i]['score_vac'],
									'score_er': result_svm_aac[i]['score_er'],
									'score_gol': result_svm_aac[i]['score_gol'],
									'score_ext': result_svm_aac[i]['score_ext'],
									'score_pm': result_svm_aac[i]['score_pm'],
									'phylo_score_nuc': result_svm_phyloloc[i]['score_nuc'],
									'phylo_score_cyt': result_svm_phyloloc[i]['score_cyt'],
									'phylo_score_mit': result_svm_phyloloc[i]['score_mit'],
									'phylo_score_ext': result_svm_phyloloc[i]['score_ext'],
									'phylo_score_pm': result_svm_phyloloc[i]['score_pm'],
									'phylo_score_per': result_svm_phyloloc[i]['score_per'],
									'phylo_score_er': result_svm_phyloloc[i]['score_er'],
									'phylo_score_gol': result_svm_phyloloc[i]['score_gol'],
									'phylo_score_vac': result_svm_phyloloc[i]['score_vac'],
									'go_score_nuc': result_svm_goloc[i]['score_nuc'],
									'go_score_cyt': result_svm_goloc[i]['score_cyt'],
									'go_score_mit': result_svm_goloc[i]['score_mit'],
									'go_score_ext': result_svm_goloc[i]['score_ext'],
									'go_score_pm': result_svm_goloc[i]['score_pm'],
									'go_score_per': result_svm_goloc[i]['score_per'],
									'go_score_er': result_svm_goloc[i]['score_er'],
									'go_score_gol': result_svm_goloc[i]['score_gol'],
									'go_score_vac': result_svm_goloc[i]['score_vac'],
									'epiloc_score_nuc': result_epiloc[i]['score_nuc'],
									'epiloc_score_cyt': result_epiloc[i]['score_cyt'],
									'epiloc_score_mit': result_epiloc[i]['score_mit'],
									'epiloc_score_ext': result_epiloc[i]['score_ext'],
									'epiloc_score_pm': result_epiloc[i]['score_pm'],
									'epiloc_score_per': result_epiloc[i]['score_per'],
									'epiloc_score_er': result_epiloc[i]['score_er'],
									'epiloc_score_gol': result_epiloc[i]['score_gol'],
									'epiloc_score_vac': result_epiloc[i]['score_vac'],
									'er_target' : result_motif_search[i]['er_target'],
									'peroxi_target' : result_motif_search[i]['peroxi_target'],
									'nuclear_bipartite' :result_motif_search[i]['nuclear_bipartite'],
									'dna_associated_domain' :  result_motif_search[i]['dna_associated_domain'],
									'pm_receptor_domain': result_motif_search[i]['pm_receptor_domain'],
									'dna_associated_domain_desc' :  result_motif_search[i]['dna_associated_domain_desc'],
									'pm_receptor_domain_desc' : result_motif_search[i]['pm_receptor_domain_desc'],
									'predictNLS' : result_motif_search[i]['predictNLS'],
									'nls_mono' : result_motif_search[i]['nls_mono']})
	else:
		fastafile.seek(0)
		svm_model_path=svm_data_path+"/sherloc2_plant_svm_target/"
		print "run SVMTarget" 
		result_svmtarget=svm_target.plant_predict(fastafile,model,svm_model_path,libsvm_path, prediction_id)
		fastafile.seek(0)
		print "run SVMSA"
		result_svm_sa = svm_sa.plant_predict(fastafile,svm_data_path,libsvm_path,12345, prediction_id)
		fastafile.seek(0)
		aac_type="aac"
		table="Benchmark80P"
		svm_model_path=svm_data_path+"/sherloc2_plant_svmaac/"
		print "run SVMaac"
		result_svm_aac = svm_aac.plant_predict(aac_type,table,svm_model_path,fastafile,model,libsvm_path,prediction_id)
		fastafile.seek(0)
		svm_model_path=svm_data_path+"/sherloc2_plant_goloc/"
		if use_inter_pro_scan == 0 and len(go_file_names) == 0:
			print "skip GOLoc"
		else:
			print "run GOLoc"
		result_svm_goloc = svm_goloc.plant_predict(table,svm_model_path,fastafile,model,libsvm_path,inter_pro_scan_path,use_inter_pro_scan,go_file_names,prediction_id)
		fastafile.seek(0)
		svm_model_path=svm_data_path+"/sherloc2_plant_phyloloc_G78BS/"
		print "run PhyloLoc"
		result_svm_phyloloc = svm_phyloloc.plant_predict(table,svm_model_path,fastafile,model,libsvm_path,blast_path,genome_path,prediction_id)
		fastafile.seek(0)
		print "run MotifSearch"
		result_motif_search=motif_search.search(fastafile)
		fastafile.seek(0)
		print "run EpiLoc"
		result_epiloc = epiloc.plant_predict(fastafile, epilocfile)
		for i in range(0,len(result_motif_search)):
			feature_vector.append({'id' : result_motif_search[i]['id'],
									'score_sp':result_svmtarget[i]['score_sp'],
									'score_mtp':result_svmtarget[i]['score_mtp'],
									'score_ctp':result_svmtarget[i]['score_ctp'],
									'score_other': result_svmtarget[i]['score_other'],
									'score_sa' :result_svm_sa[i]['score_sa'],
									'score_nuc': result_svm_aac[i]['score_nuc'],
									'score_cyt': result_svm_aac[i]['score_cyt'],
									'score_nuc_vs_cyt': result_svm_aac[i]['score_nuc_vs_cyt'],
									'score_mtp_vs_ctp': result_svmtarget[i]['score_mtp_vs_ctp'],
									'score_mit': result_svm_aac[i]['score_mit'],
									'score_chl': result_svm_aac[i]['score_chl'],
									'score_per': result_svm_aac[i]['score_per'],
									'score_vac': result_svm_aac[i]['score_vac'],
									'score_er': result_svm_aac[i]['score_er'],
									'score_gol': result_svm_aac[i]['score_gol'],
									'score_ext': result_svm_aac[i]['score_ext'],
									'score_pm': result_svm_aac[i]['score_pm'],
									'phylo_score_nuc': result_svm_phyloloc[i]['score_nuc'],
									'phylo_score_cyt': result_svm_phyloloc[i]['score_cyt'],
									'phylo_score_mit': result_svm_phyloloc[i]['score_mit'],
									'phylo_score_chl': result_svm_phyloloc[i]['score_chl'],
									'phylo_score_ext': result_svm_phyloloc[i]['score_ext'],
									'phylo_score_pm': result_svm_phyloloc[i]['score_pm'],
									'phylo_score_per': result_svm_phyloloc[i]['score_per'],
									'phylo_score_er': result_svm_phyloloc[i]['score_er'],
									'phylo_score_gol': result_svm_phyloloc[i]['score_gol'],
									'phylo_score_vac': result_svm_phyloloc[i]['score_vac'],
									'go_score_nuc': result_svm_goloc[i]['score_nuc'],
									'go_score_cyt': result_svm_goloc[i]['score_cyt'],
									'go_score_mit': result_svm_goloc[i]['score_mit'],
									'go_score_chl': result_svm_goloc[i]['score_chl'],
									'go_score_ext': result_svm_goloc[i]['score_ext'],
									'go_score_pm': result_svm_goloc[i]['score_pm'],
									'go_score_per': result_svm_goloc[i]['score_per'],
									'go_score_er': result_svm_goloc[i]['score_er'],
									'go_score_gol': result_svm_goloc[i]['score_gol'],
									'go_score_vac': result_svm_goloc[i]['score_vac'],
									'epiloc_score_nuc': result_epiloc[i]['score_nuc'],
									'epiloc_score_cyt': result_epiloc[i]['score_cyt'],
									'epiloc_score_mit': result_epiloc[i]['score_mit'],
									'epiloc_score_chl': result_epiloc[i]['score_chl'],
									'epiloc_score_ext': result_epiloc[i]['score_ext'],
									'epiloc_score_pm': result_epiloc[i]['score_pm'],
									'epiloc_score_per': result_epiloc[i]['score_per'],
									'epiloc_score_er': result_epiloc[i]['score_er'],
									'epiloc_score_gol': result_epiloc[i]['score_gol'],
									'epiloc_score_vac': result_epiloc[i]['score_vac'],
									'er_target' : result_motif_search[i]['er_target'],
									'peroxi_target' : result_motif_search[i]['peroxi_target'],
									'nuclear_bipartite' :result_motif_search[i]['nuclear_bipartite'],
									'dna_associated_domain' :  result_motif_search[i]['dna_associated_domain'],
									'pm_receptor_domain': result_motif_search[i]['pm_receptor_domain'],
									'dna_associated_domain_desc' :  result_motif_search[i]['dna_associated_domain_desc'],
									'pm_receptor_domain_desc' : result_motif_search[i]['pm_receptor_domain_desc'],
									'predictNLS' : result_motif_search[i]['predictNLS'],
									'nls_mono' : result_motif_search[i]['nls_mono']})
	return feature_vector

def sherloc2_predict_location(origin, feature_vector, model, prediction_id):
	print "run SherLoc2"
	result = []
        libsvm_path=os.path.dirname(run_shell_command("which svm-predict"))+"/"
	svm_data_path="%s/data/svm_models/SherLoc2/"%(basedir)
	if origin == "animal":
		svm_model_path = svm_data_path+"/benchmark80_animal_sherloc2/"
		result = svm_sherloc2.animal_predict(feature_vector,svm_model_path,libsvm_path,model, prediction_id)
	elif origin == "fungal":
		svm_model_path = svm_data_path+"/benchmark80_fungi_sherloc2/"
		result = svm_sherloc2.fungi_predict(feature_vector,svm_model_path,libsvm_path,model, prediction_id)
	else:
		svm_model_path = svm_data_path+"/benchmark80_plant_sherloc2/"
		result = svm_sherloc2.plant_predict(feature_vector,svm_model_path,libsvm_path,model, prediction_id)
	return result

def advanced_output(vec,origin):
	line = "\n\n\n"
	line = line + "Detailed results of all subprediction methods:\n"
	line = line + "sequence_id\tsvm_target_score_sp\tsvm_target_score_mtp"
	if origin == "plant":
		line = line + "\tsvm_target_score_ctp\tsvm_target_score_mtp_vs_ctp"
	line = line + "\tsvm_target_score_oth"
	line = line + "\tsvm_sa_score"
	line = line + "\tsvm_aac_score_nuc\tsvm_aac_score_cyt\tsvm_aac_score_nuc_vs_cyt\tsvm_aac_score_mit"
	if origin == "plant":
		line = line + "\tsvm_aac_score_chl"
	line = line + "\tsvm_aac_score_ext"
	line = line + "\tsvm_aac_score_pm\tsvm_aac_score_per\tsvm_aac_score_er\tsvm_aac_score_gol"
	if origin == "animal":
		line = line + "\tsvm_aac_score_lys"
	else:
		line = line + "\tsvm_aac_score_vac"
	line = line + "\tgoloc_score_nuc\tgoloc_score_cyt\tgoloc_score_mit"
	if origin == "plant":
		line = line + "\tgoloc_score_chl"
	line = line + "\tgoloc_score_ext"
	line = line + "\tgoloc_score_pm\tgoloc_score_per\tgoloc_score_er\tgoloc_score_gol"
	if origin == "animal":
		line = line + "\tgoloc_score_lys"
	else:
		line = line + "\tgoloc_score_vac"
	line = line + "\tphyloloc_score_nuc\tphyloloc_score_cyt\tphyloloc_score_mit"
	if origin == "plant":
		line = line + "\tphyloloc_score_chl"
	line = line + "\tphyloloc_score_ext"
	line = line + "\tphyloloc_score_pm\tphyloloc_score_per\tphyloloc_score_er\tphyloloc_score_gol"
	if origin == "animal":
		line = line + "\tphyloloc_score_lys"
	else:
		line = line + "\tphyloloc_score_vac"
	line = line + "\tepiloc_score_nuc\tepiloc_score_cyt\tepiloc_score_mit"
	if origin == "plant":
		line = line + "\tepiloc_score_chl"
	line = line + "\tepiloc_score_ext"
	line = line + "\tepiloc_score_pm\tepiloc_score_per\tepiloc_score_er\tepiloc_score_gol"
	if origin == "animal":
		line = line + "\tepiloc_score_lys"
	else:
		line = line + "\tepiloc_score_vac"
	line = line + "\tmotif_search_er_target\tmotif_search_pm_receptor_domain\tmotif_search_pm_receptor_domain_desc\tmotif_search_peroxi_target\tmotif_search_nuclear_bipartite\tmotif_search_predictNLS\tmotif_search_nls_mono\tmotif_search_dna_associated_domain\tmotif_search_dna_associated_domain_desc\n"
	
	for i in range(0,len(vec)):
		line = line + vec[i]['id']
		line = line+"\t"+str(vec[i]['score_sp'])+"\t"+str(vec[i]['score_mtp'])
		if origin == "plant":
			line = line +"\t" + str(vec[i]['score_ctp'])+"\t"+str(vec[i]['score_mtp_vs_ctp'])
		line = line +"\t"+str(vec[i]['score_other'])
		line = line + "\t" + str(vec[i]['score_sa'])
		line = line + "\t" + str(vec[i]['score_nuc']) + "\t" + str(vec[i]['score_cyt']) + "\t" + str(vec[i]['score_nuc_vs_cyt']) + "\t" + str(vec[i]['score_mit'])
		if origin == "plant":
			line = line + "\t" + str(vec[i]['score_chl'])
		line = line + "\t" + str(vec[i]['score_ext'])
		line = line + "\t" + str(vec[i]['score_pm']) + "\t" + str(vec[i]['score_per']) + "\t" + str(vec[i]['score_er']) + "\t" + str(vec[i]['score_gol'])
		if origin == "animal":
			line = line + "\t" + str(vec[i]['score_lys'])
		else:
			line = line + "\t" + str(vec[i]['score_vac'])
		line = line + "\t" + str(vec[i]['go_score_nuc']) + "\t" + str(vec[i]['go_score_cyt']) + "\t" + str(vec[i]['go_score_mit'])
		if origin == "plant":
			line = line + "\t" + str(vec[i]['go_score_chl'])
		line = line + "\t" + str(vec[i]['go_score_ext'])
		line = line + "\t" + str(vec[i]['go_score_pm']) + "\t" + str(vec[i]['go_score_per']) + "\t" + str(vec[i]['go_score_er']) + "\t" + str(vec[i]['go_score_gol'])
		if origin == "animal":
			line = line + "\t" + str(vec[i]['go_score_lys'])
		else:
			line = line + "\t" + str(vec[i]['go_score_vac'])
		line = line + "\t" + str(vec[i]['phylo_score_nuc']) + "\t" + str(vec[i]['phylo_score_cyt']) + "\t" + str(vec[i]['phylo_score_mit'])
		if origin == "plant":
			line = line + "\t" + str(vec[i]['phylo_score_chl'])
		line = line + "\t" + str(vec[i]['phylo_score_ext'])
		line = line + "\t" + str(vec[i]['phylo_score_pm']) + "\t" + str(vec[i]['phylo_score_per']) + "\t" + str(vec[i]['phylo_score_er']) + "\t" + str(vec[i]['phylo_score_gol'])
		if origin == "animal":
			line = line + "\t" + str(vec[i]['phylo_score_lys'])
		else:
			line = line + "\t" + str(vec[i]['phylo_score_vac'])
		line = line + "\t" + str(vec[i]['epiloc_score_nuc']) + "\t" + str(vec[i]['epiloc_score_cyt']) + "\t" + str(vec[i]['epiloc_score_mit'])
		if origin == "plant":
			line = line + "\t" + str(vec[i]['epiloc_score_chl'])
		line = line + "\t" + str(vec[i]['epiloc_score_ext'])
		line = line + "\t" + str(vec[i]['epiloc_score_pm']) + "\t" + str(vec[i]['epiloc_score_per']) + "\t" + str(vec[i]['epiloc_score_er']) + "\t" + str(vec[i]['epiloc_score_gol'])
		if origin == "animal":
			line = line + "\t" + str(vec[i]['epiloc_score_lys'])
		else:
			line = line + "\t" + str(vec[i]['epiloc_score_vac'])
		line = line +"\t"+str(vec[i]['er_target'])
		line=line+"\t"+str(vec[i]['pm_receptor_domain'])+"\t"+str(vec[i]['pm_receptor_domain_desc'])+"\t"+str(vec[i]['peroxi_target'])
		line=line+"\t"+str(vec[i]['nuclear_bipartite'])+"\t"+str(vec[i]['predictNLS'])+"\t"+str(vec[i]['nls_mono'])
		line=line+"\t"+str(vec[i]['dna_associated_domain'])+"\t"+str(vec[i]['dna_associated_domain_desc']) 
		line = line + "\n"
	return line

#main
def main():
	origin = ""
	fastafile_name = ""
	global email
	prediction_id = create_prediction_id()
	output = "simple"
	rm_fasta = 0
	result_file_name = ""
	go_file_names = []
		
	global sherloc2_mode
	if len(sys.argv)<3:
		print "usage:"
		if sherloc2_mode == "stand-alone":
			print "python "+sys.argv[0]+" -fasta=<fasta file> -origin=<animal|plant|fungal> -result=<result file> [-output=<simple|advanced>] [[-go=<go file>] ... ]"
		else:
			print "python "+sys.argv[0]+" -fasta=<fasta file> -origin=<animal|plant|fungal> [-email=<email-address>] [-output=<simple|advanced>] [-rm_fasta=<0|1>]"
		sys.exit()
	param_error = 0
	for i in range(1,len(sys.argv)):
		param = sys.argv[i]
		match = 0
		if re.findall("^-fasta=",param):
			fastafile_name = re.sub("^-fasta=","",param)
			match=1
		if re.findall("^-result=",param):
			result_file_name = re.sub("^-result=","",param)
			match=1
		if re.findall("^-origin=",param):
			origin = re.sub("^-origin=","",param)
			match=1
		if re.findall("^-email=",param):
			email = re.sub("^-email=","",param)
			match=1
		if re.findall("^-output=",param):
			output = re.sub("^-output=","",param)
			match=1
		if re.findall("^-rm_fasta=",param):
			rm_fasta = int(re.sub("^-rm_fasta=","",param))
			match=1
		if re.findall("^-go=",param):
			go_file_names.append(re.sub("^-go=","",param))
			match=1
		if match == 0:
			print "Error: param %s not valid!" %(param)
			param_error = 1
	if param_error == 1 or (origin != "animal" and origin != "plant" and origin != "fungal") or fastafile_name == "" or (output != "simple" and output != "advanced") or (rm_fasta !=0 and rm_fasta !=1) or (sherloc2_mode == "stand-alone" and result_file_name == ""):
		print "Wrong parameter setting!\nusage:"
		if sherloc2_mode == "stand-alone":
			print "python "+sys.argv[0]+" -fasta=<fasta file> -origin=<animal|plant|fungal> -result=<result file> [-output=<simple|advanced>] [[-go=<go file>] ... ]"
		else:
			print "python "+sys.argv[0]+" -fasta=<fasta file> -origin=<animal|plant|fungal> [-email=<email-address>] [-output=<simple|advanced>] [-rm_fasta=<0|1>]"
		sys.exit()
	if sherloc2_mode == "online-service":
		check_load()

	file=open(fastafile_name,"r")
	epilocfile = None;
	vec = sherloc2_create_feature_vector(origin,file,go_file_names, 12345,prediction_id, epilocfile)
	file.close()
	if rm_fasta==1 and os.path.exists(fastafile_name):
		os.remove(fastafile_name)
	res = sherloc2_predict_location(origin, vec, 12345, prediction_id)

	line="Dear user,\nhere are the prediction results for your query.\n\n"
	if sherloc2_mode == "stand-alone":
		line = "SherLoc2 Prediction Result\n\n"
	line = line + "origin = "+origin+"\n\n"
	
	key_loc_dic={"score_chl":"chloroplast","score_cyt":"cytoplasmic","score_nuc":"nuclear","score_mit":"mitochondrial","score_ext":"extracellular","score_pm":"plasma membrane","score_per":"peroxisomal","score_gol":"Golgi apparatus","score_er":"ER","score_lys":"lysosomal","score_vac":"vacuolar"}
	for i in range(0,len(res)):
		sorted=[]
		for k in res[i].keys():
			max_score=0.0
			max_loc=""
			for k2 in res[i].keys():
				if k2 != 'id':
					if k2 in sorted:
						continue
					if res[i][k2] >= max_score:
						max_score = res[i][k2]
						max_loc=k2
			if max_loc != "":
				sorted.append(max_loc)
		line=line + res[i]['id'] 
		for j in range(0,len(sorted)):
			loc = sorted[j]
			score = round(res[i][loc],2)
			if sorted[j] in key_loc_dic.keys():
				loc = key_loc_dic[sorted[j]]
				line = line + "\t" + loc + ": " + str(score)
		line = line + "\n"
	if output == "advanced":
		line = line + advanced_output(vec,origin)
	if email != "":
		mail('smtp.informatik.uni-tuebingen.de', sender_address, email, 'SherLoc2 prediction results', str(line))
	if result_file_name != "":
		file = open(result_file_name,"w")
		file.write(line)
		file.close()

if sherloc2_mode == "online-service":
	try:
		main()
	except util.Error:
		mail('smtp.informatik.uni-tuebingen.de', sender_address, email, 'SherLoc2 error', "wrong fasta format!")
	except IOError, (errno, strerror):
		mail('smtp.informatik.uni-tuebingen.de', sender_address, sender_address, 'SherLoc2 error', "%s %s %s" %(errno, strerror, sys.stderr))
	except:
		mail('smtp.informatik.uni-tuebingen.de', sender_address, sender_address, 'SherLoc2 error', str(sys.exc_info()))
		mail('smtp.informatik.uni-tuebingen.de', sender_address, email, 'SherLoc2 error', "sorry, an error occured!")
else:
	main()
