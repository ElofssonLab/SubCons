import sys, time, re
from YLocSOAP_services import *

# YLoc interface script, 2009 Sebastian Briesemeister
# The script uses SOAP via port 8020, so make sure the connection
# is not blocked and ZSI installed.

# Error class
class Error(Exception):
	def __init__(self, value):
		self.value = value;
	def __str__(self):
		return repr(self.value);

# definition of a protein type used via SOAP
class ProteinType(object):
	def __init__(self, name, sequence):
		self._name = name;
		self._sequence = sequence;
			
# definition of a prediction request consisting of a protein and the predictor options
class PredictionRequestType(object):
	def __init__(self, protein_list, model_name, origin, homology):
		self._proteins = protein_list;
		self._model = model_name;
		self._origin = origin;
		self._homology = homology;


# connect to YLoc Webservice
loc = YLoc_Prediction_Web_ServiceLocator();
f = open('debug.out','w');
yloc = loc.getYLoc_PortType( tracefile=f)
		

# start prediction via SOAP using the protein list, the model name, origin and the use of homology
def __startPrediction(protein_list, model_name, origin, homology, advanced = True):
	#prepare input
	predictionRequest = predictRequest()
	predictionRequest._input = PredictionRequestType( protein_list , model_name, origin, homology);
	
	# predict and retrieve result
	predictionResponse = yloc.predict(predictionRequest);
	
	
	if not predictionResponse._predictions:
		raise Error("YLoc returned and error. Contact the adminstrator of the Webserver.");
	
	# create return type
	result_list = [];
	for pred in predictionResponse._predictions._prediction:
	
		#create probability dictionary
		probs = {};
		for p in pred._probabilties:
			probs[p._name] = 100*p._value;
			
		#create attribute dictionary
		attr = {};
		for a in pred._attributes:
			attr[re.sub("<.{1,60}>","", a._name)] = a._value;
			
		reasoning = re.sub("<.{1,20}>","", pred._reasoning);			
			
		if advanced:
			result_list.append( (pred._sequence_name, pred._predicted_location, pred._predicted_probability*100, probs, pred._confidence_score, pred._most_similar_AC, reasoning, attr) );
		else:
			result_list.append( (pred._sequence_name, pred._predicted_location, pred._predicted_probability*100, pred._confidence_score, reasoning) );

		
	return result_list;	


# predict the locations of all given sequences in the list using the given model, origin and the defined use homology
def predict(sequence_list, model_name, origin, homology, advanced=False):
	# split sequences in packs of 20 since the webserver allows at most 20 protein sequences
	i = 0;
	results = [];
	while i < len(sequence_list):
		protein_list = [];
		k = 0;
		while i < len(sequence_list) and k < 20:
			# add protein to list with id and sequence
			protein_list.append( ProteinType(  str(sequence_list[i]['id']), sequence_list[i]['sequence']  ) );
			k += 1;
			i += 1;
		
		# start prediction
		results += __startPrediction(protein_list, model_name, origin, homology, advanced);
	
	return results;
