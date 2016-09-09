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
  


# test data provided as argument to the script
Xt, Yt = readXY(open(sys.argv[1]+"/dat-files/prediction.dat"))

# test data provided as argument to the script to extract the protein id
id_protein = take_ids(open(sys.argv[1]+"/dat-files/prediction.dat"))

list_result = []
for files in os.listdir(sys.argv[1]+"/for-dat/"):
	list_result.append(files)


def peak_correct_forest(list_pred):
	global f
	
	if len(list_pred)==5:
		f = pickle.load(open('forests/forest-slycm.dat',"rb"))
		return f
		
	elif len(list_pred)==4:					
		f = pickle.load(open('forests/forest-slm'+str(list_pred[3][0])+'.dat',"rb"))	
		return f
	
	elif len(list_pred) == 3:
		f = pickle.load(open('forests/forest-slm.dat',"rb"))
		return f



peak_correct_forest(list_result)
predictions = f.predict(Xt)
probs = f.predict_proba(Xt)

# SAVE THE FILE WITH THE RESULTS
# YOU NEED TO CHANGE THE PATH TO PRINT THE FILE

saveout = sys.stdout
ff1 = open(sys.argv[1]+'/final-prediction/subcons-final.pred','w+')
sys.stdout=ff1
for i in range(len(Xt)):
	if predictions[i] in loc_types_1.keys():
		id_protein[i] = id_protein[i].split("#")[1]
		subcons_prediction = str(predictions[i]).replace(str(predictions[i]),loc_types_2[str(predictions[i])])
		#PRINT ALL THE PROBABILITIES FOR ALL THE LOCALIZATIONS
		
		print id_protein[i]+"\t"+"LOC_DEF:"+str(subcons_prediction)+"\t"+'CYT:'+str(probs[i][0])+"\t"+'ERE:'+str(probs[i][1])+"\t"+'EXC:'+str(probs[i][2])+"\t"+'GLG:'+str(probs[i][3])+"\t"+'MEM:'+str(probs[i][4])+"\t"+'MIT:'+str(probs[i][5])+"\t"+'NUC:'+str(probs[i][6])+"\t"+'VES:'+str(probs[i][7])
		#PRINT ONLY THE FINAL LOCALIZATION DECIDED BY SUBCONS
		#print id_protein[i],subcons_prediction
		
sys.stdout=saveout
ff1.close()


