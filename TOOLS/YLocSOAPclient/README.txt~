YLoc - Interpretable Subcellular Localization Prediction - SOAP client
######################################################################

Usage: python yloc.py <fastafile.fasta> <model_name> <origin> <use of homology(Yes/No)> <output(Advanced/Simple)>

Available models: YLoc-LowRes, YLow-HighRes, YLoc+
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


