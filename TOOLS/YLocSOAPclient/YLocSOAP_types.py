##################################################
# file: YLocSOAP_types.py
#
# schema types generated by "ZSI.generate.wsdl2python.WriteServiceModule"
#    /usr/bin/wsdl2py YLocZSI.wsdl
#
##################################################

import ZSI
import ZSI.TCcompound
from ZSI.schema import LocalElementDeclaration, ElementDeclaration, TypeDefinition, GTD, GED

##############################
# targetNamespace
# YLocType_NS
##############################

class ns0:
    targetNamespace = "YLocType_NS"

    class DictType_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "YLocType_NS"
        type = (schema, "DictType")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.DictType_Def.schema
            TClist = [ZSI.TCnumbers.FPfloat(pname="value", aname="_value", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="name", aname="_name", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._value = None
                    self._name = None
                    return
            Holder.__name__ = "DictType_Holder"
            self.pyclass = Holder

    class ProteinType_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "YLocType_NS"
        type = (schema, "ProteinType")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.ProteinType_Def.schema
            TClist = [ZSI.TC.String(pname="sequence", aname="_sequence", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="name", aname="_name", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._sequence = None
                    self._name = None
                    return
            Holder.__name__ = "ProteinType_Holder"
            self.pyclass = Holder

    class PredictionRequestType_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "YLocType_NS"
        type = (schema, "PredictionRequestType")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.PredictionRequestType_Def.schema
            TClist = [GTD("YLocType_NS","ProteinType",lazy=False)(pname="proteins", aname="_proteins", minOccurs=1, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="model", aname="_model", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="origin", aname="_origin", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="homology", aname="_homology", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._proteins = []
                    self._model = None
                    self._origin = None
                    self._homology = None
                    return
            Holder.__name__ = "PredictionRequestType_Holder"
            self.pyclass = Holder

    class PredictionType_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "YLocType_NS"
        type = (schema, "PredictionType")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.PredictionType_Def.schema
            TClist = [ZSI.TC.String(pname="sequence_name", aname="_sequence_name", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="predicted_location", aname="_predicted_location", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="reasoning", aname="_reasoning", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TCnumbers.FPfloat(pname="confidence_score", aname="_confidence_score", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="most_similar_AC", aname="_most_similar_AC", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TCnumbers.FPfloat(pname="predicted_probability", aname="_predicted_probability", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), GTD("YLocType_NS","DictType",lazy=False)(pname="probabilties", aname="_probabilties", minOccurs=1, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded")), GTD("YLocType_NS","DictType",lazy=False)(pname="attributes", aname="_attributes", minOccurs=1, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._sequence_name = None
                    self._predicted_location = None
                    self._reasoning = None
                    self._confidence_score = None
                    self._most_similar_AC = None
                    self._predicted_probability = None
                    self._probabilties = []
                    self._attributes = []
                    return
            Holder.__name__ = "PredictionType_Holder"
            self.pyclass = Holder

    class PredictionListType_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "YLocType_NS"
        type = (schema, "PredictionListType")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.PredictionListType_Def.schema
            TClist = [GTD("YLocType_NS","PredictionType",lazy=False)(pname="prediction", aname="_prediction", minOccurs=1, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._prediction = []
                    return
            Holder.__name__ = "PredictionListType_Holder"
            self.pyclass = Holder

# end class ns0 (tns: YLocType_NS)
