##########################################################################
#                                                                        #
# Created by Marco Salvatore:						                     #
# This is the code of SubCons 						                     #
# To run SubCons you need to use something like this: 			         #
#									                                     #
# python src/subcons.py files/file-prediction.dat              		     #
#									                                     #					
##########################################################################

import sys,os
import pickle

# in case the pickle library does not work use:
#from sklearn.externals import joblib
#EXAMPLE : f = joblib.load(open('forests/forest-slycm.dat',"rb")

if not len(sys.argv) == 2:
  print "Usage:",sys.argv[0],"test_file"
  sys.exit(-1)


# THESE ARE THE DICTIONARIES USED TO CONVERT THE CORRESPONDENT VALUES OF THE LOCALIZATIONS TO THE ACTUAL NAME OF THE LOCALIZATIONS
# CYT = cytoplasm (cytoskeleton)
# ERE = endoplasmic reticulum
# EXC = extracellular or secreted
# GLG = Golgi apparatus
# MEM = membrane protein
# MIT = mitochondrion
# NUC = nucleus  
# VES = vesicles (lysosome & peroxisome)
 
loc_types_1 = {1.0:'CYT',2.0:'ERE',3.0:'EXC',4.0:'GLG',5.0:'MEM',6.0:'MIT',7.0:'NUC',8.0:'VES'}
loc_types_2 = {'1.0':'CYT','2.0':'ERE','3.0':'EXC','4.0':'GLG','5.0':'MEM','6.0':'MIT','7.0':'NUC','8.0':'VES'}


# FUNCTION USED TO READ THE TRAIN AND TEST FILE:
def readXY(handle):
  X = []
  Y = []
  for line in handle.readlines():
    #print line
    line = line.split()
    X.append([float(x) for x in line[1:-1]])
    Y.append(float(line[0]))
  return X, Y

# FUNCTION USED TO EXTRACT THE ID OF THE PROTEIN: 
def take_ids(handle):
  Z = []
  for line in handle.readlines():
    line = line.split()
    Z.append(line[-1])
  return Z
  

def peak_correct_forest(list_pred):
	global f
	if len(list_pred)==5:
		f = pickle.load(open('forests/forest-slycm.dat',"rb"))
		#f = joblib.load(open('forests/forest-slycm.dat',"rb") 
		return f
		
	elif len(list_pred)== 4 :
		try :
			if str("cello") in list_pred:					
				f = pickle.load(open('forests/forest-slmc.dat',"rb"))
				#f = joblib.load(open('forests/forest-slycm.dat',"rb") 
				return f
			else:
				f = pickle.load(open('forests/forest-slmy.dat',"rb"))
				#f = joblib.load(open('forests/forest-slycm.dat',"rb") 
				return f				
		except:
			pass
			
	elif len(list_pred) == 3:
		f = pickle.load(open('forests/forest-slm.dat',"rb"))
		#f = joblib.load(open('forests/forest-slycm.dat',"rb") 
		return f


predictor_list = []

for files in os.listdir(sys.argv[1]+"/for-dat/"):
	predictor_used = files.split('.')[1]
	predictor_list.append(predictor_used)
	predictor_list= sorted(set(predictor_list))

		
for el in os.listdir(sys.argv[1]+"/dat-files/"):
	name_file = el.split('.')[0]
	# test data provided as argument to the script
	Xt, Yt = readXY(open(sys.argv[1]+"/dat-files/"+str(name_file)+".dat"))

	# test data provided as argument to the script to extract the protein id
	id_protein = take_ids(open(sys.argv[1]+"/dat-files/"+str(name_file)+".dat"))
	peak_correct_forest(predictor_list)
	predictions = f.predict(Xt)
	probs = f.predict_proba(Xt)

	# SAVE THE FILE WITH THE RESULTS
	# YOU NEED TO CHANGE THE PATH TO PRINT THE FILE

	saveout = sys.stdout
	ff1 = open(sys.argv[1]+'/final-prediction/'+str(name_file)+'.subcons-final-pred.csv','w+')
	sys.stdout=ff1
	for i in range(len(Xt)):
		if predictions[i] in loc_types_1.keys():
			id_protein[i] = id_protein[i].split("#")[1]
			subcons_prediction = str(predictions[i]).replace(str(predictions[i]),loc_types_2[str(predictions[i])])
			#PRINT ALL THE PROBABILITIES FOR ALL THE LOCALIZATIONS
			print "id_protein"+"\t"+"LOC_DEF"+"\t"+"CYT"+"\t"+"ERE"+"\t"+"EXC"+"\t"+"GLG"+"\t"+"MEM"+"\t"+"MIT"+"\t"+"NUC"+"\t"+"VES"
			print id_protein[i]+"\t"+str(subcons_prediction)+"\t"+str(round(float(probs[i][0]),2))+"\t"+str(round(float(probs[i][1]),2))+"\t"+str(round(float(probs[i][2]),2))+"\t"+str(round(float(probs[i][3]),2))+"\t"+str(round(float(probs[i][4]),2))+"\t"+str(round(float(probs[i][5]),2))+"\t"+str(round(float(probs[i][6]),2))+"\t"+str(round(float(probs[i][7]),2))
			#PRINT ONLY THE FINAL LOCALIZATION DECIDED BY SUBCONS
			#print id_protein[i],subcons_prediction
		
	sys.stdout=saveout
	ff1.close()
print predictor_list










