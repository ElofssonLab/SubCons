YLoc - Interpretable Subcellular Localization Prediction - SOAP client
######################################################################

Usage: python yloc.py <fastafile.fasta> <model_name> <origin> <use of homology(Yes/No)> <output(Advanced/Simple)>

Available models: YLoc-LowRes, YLow-HighRes, YLoc+ 
YLoc-LowRes	predicts into 4 locations (nucleus, cytoplasm, mitochodrion, secretory pathway for the animal and fungi version) or 5 locations (in addition chloroplast for the plant version), respectively.
YLoc-HighRes	predicts into 9 or 10 locations, respectively. These are nucleus, cytoplasm, mitochodrion, plasma membrane, extracellular space, endoplasmic reticulum, peroxisome, and Golgi apparatus for all models. In addition, lysosome for the animal model, vacuole for the fungi model, and vacuole and chloroplast for the plant model.
YLoc+	predicts into 9 or 10 locations, as described above. In addition, it allows to predict multiple locations. It was trained, in addition to the 11 main eukaryotic location classes, on 7 multi-location classes. 
Available origins: Animals, Fungi, Plants

Example:
--------
python yloc.py test.fasta YLoc-LowRes Animals Yes Simple

Debug information is written in "debug.out".

If you use the SOAP client to call YLoc, make sure that you have Python ZSI 2.0 installed and your internet connection is not blocked.

If you face any troubles, please contact us. Information can be found on the YLoc website: www.multiloc.org/YLoc.

If you like to create your own ZSI client follow the following steps:
1.) Install ZSI 2.0 on your computer.
2.) Download the YLoc WSDL from http://abi.inf.uni-tuebingen.de/Services/YLocSOAP?WSDL
3.) Use "wsdl2py" to create YLocSOAP_services.py and YLocSOAP_services_types.py
4.) Create your own client by importing "from YLocSOAP_services import *". Its probably best if you follow a ZSI tutorial to know how to use a ZSI SOAP service or have close look at "YLocSOAPclient.py".


