##################################################
# file: YLocSOAP_server.py
#
# skeleton generated by "ZSI.generate.wsdl2dispatch.ServiceModuleWriter"
#      /usr/bin/wsdl2py YLocSOAP?WSDL
#
##################################################

from ZSI.schema import GED, GTD
from ZSI.TCcompound import ComplexType, Struct
from YLocSOAP_types import *
from ZSI.ServiceContainer import ServiceSOAPBinding

# Messages  
class predictRequest:
    def __init__(self, **kw):
        """Keyword parameters:
        input -- part input
        """
        self._input =  kw.get("input")
predictRequest.typecode = Struct(pname=("urn:YLocSOAP.wsdl","predict"), ofwhat=[ns0.PredictionRequestType_Def(pname="input", aname="_input", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=predictRequest, encoded="urn:YLocSOAP.wsdl")

class predictResponse:
    def __init__(self, **kw):
        """Keyword parameters:
        predictions -- part predictions
        """
        self._predictions =  kw.get("predictions")
predictResponse.typecode = Struct(pname=("urn:YLocSOAP.wsdl","predictResponse"), ofwhat=[ns0.PredictionListType_Def(pname="predictions", aname="_predictions", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=predictResponse, encoded="urn:YLocSOAP.wsdl")


# Service Skeletons
class YLoc_Prediction_Web_Service(ServiceSOAPBinding):
    soapAction = {}
    root = {}

    def __init__(self, post='/Services/YLocSOAP', **kw):
        ServiceSOAPBinding.__init__(self, post)

    def soap_predict(self, ps, **kw):
        request = ps.Parse(predictRequest.typecode)
        return request,predictResponse()

    soapAction['urn:YLocSOAP.wsdl#predict'] = 'soap_predict'
    root[(predictRequest.typecode.nspname,predictRequest.typecode.pname)] = 'soap_predict'

