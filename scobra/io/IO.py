import re
import sys
import os
sys.path.append(os.path.split(os.path.abspath(__file__))[0][:-3])
import cobra
from ..classes.model import model
from .Excel import ReadExcel, WriteExcel
#from .Cyc import ReadCyc
from .ScrumPy import ReadScrumPyModel, WriteScrumPyModel
from past.builtins import basestring

def ReadModel(model_file=None, model_format=None, excel_parse="cobra_string",
          variable_name=None, Print=False, compartment_dic={}, bounds=1000000, **kwargs):
    """ model_format = "sbml" | "sbml_legacy" | "excel" | "matlab" | "json" | "scrumpy | "yaml"
        excel_parse = "cobra_string" | "cobra_position" "cyc" """
    if not model_file:
        pass
    elif model_format == "sbml" or model_format == "xml" or (
        model_format == None and model_file.endswith(".sbml")) or (
        model_format == None and model_file.endswith(".xml")):
        model_file = cobra.io.read_sbml_model(model_file, **kwargs)
    elif model_format == "sbml_legacy":
        model_file = cobra.io.read_legacy_sbml(model_file, **kwargs)
#        model_file = cobra.io.read_sbml_model(model_file,
#            old_sbml=old_sbml, legacy_metabolite=legacy_metabolite,
#            print_time=False, use_hyphens=use_hyphens)
    elif model_format == "matlab" or (model_format == None and
        model_file.endswith(".mat")):
        model_file = cobra.io.load_matlab_model(model_file,
                                                variable_name=variable_name, **kwargs)
    elif model_format == "json" or (model_format == None and
                                            model_file.endswith(".json")):
        model_file = cobra.io.load_json_model(model_file, **kwargs)
    elif model_format == "excel" or model_format == "xls" or \
        model_format == "cobra" or (model_format == None and
        model_file.endswith(".xls")) or (model_format == None
                                    and model_file.endswith(".xlsx")):
        model_file = ReadExcel(model_file,
                                       parse=excel_parse, Print=Print, **kwargs)
    elif model_format == "scrumpy" or model_format == "spy" or (
        model_format == None and model_file.endswith(".spy")):
        model_file = ReadScrumPyModel(model_file,
                    compartment_dic=compartment_dic, Print=Print, **kwargs)
    elif model_format == "yaml" or model_file.endswith(".yaml") or model_file.endswith(".yml"):
        model_file = cobra.io.load_yaml_model(model_file, **kwargs)
    """
    elif model_format == "dat" or model_file.endswith(".dat"):
        model_file = ReadCyc(model_file, Print=Print,**kwargs)
    """
    m = model(model_file)
    if isinstance(model_file, basestring):
        m.description = m.id = model_file.rsplit(".",1)[0]
    m.SetBounds(bounds=bounds)
    return m

def WriteModel(model, filename, model_format=None, excel_format="cobra", ExtReacs=[], **kwargs):
    """ model_format = "sbml" | "sbml_legacy" | "excel" | "matlab" | "json" | "cobra" | "cobra_old" | "scrumpy" | "yaml" | "cyc" """
    if model_format == "sbml" or model_format == "xml"or (
        model_format == None and filename.endswith(".sbml")) or (
        model_format == None and filename.endswith(".xml")):
        cobra.io.write_sbml_model(model, filename, **kwargs)
    elif model_format == "sbml_legacy":
        description = model.description
        model.description = str(description)
        m_id = model.id
        model.id = str(m_id)
        compartments = model.compartments
        if not model.compartments:
            model.compartments = {'':''}
        original_met_id = {}
        original_met_compartment = {}
        for met in model.metabolites:    # changes metabolites in the model
            original_met_id[met] = met.id
            original_met_compartment[met] = met.compartment
            met.id = re.sub('[-/().,\[\]+]','_',met.id)
            if not met.compartment:
                met.compartment = ''
        original_reac_id = {}
        for reac in model.reactions:
            original_reac_id[reac] = reac.id
            reac.id = re.sub('[-/().,\[\]+]','_',reac.id)
        # cobra.io.write_sbml_model(model, filename=filename,
        #     sbml_level=sbml_level, sbml_version=sbml_version,
        #     print_time=False, use_fbc_package=fbc)
        cobra.io.write_legacy_sbml(model, filename=filename, **kwargs)
        model.description = description
        model.id = m_id
        model.compartments = compartments
        for met in model.metabolites:    # revert changes to metabolites
            met.id = original_met_id[met]
            met.compartment = original_met_compartment[met]
        for reac in model.reactions:
            reac.id = original_reac_id[reac]
    elif model_format == "matlab" or (
                model_format == None and filename.endswith(".mat")):
        cobra.io.save_matlab_model(model, filename, **kwargs)
    elif model_format == "json" or (
                model_format == None and filename.endswith(".json")):
        cobra.io.save_json_model(model, filename, **kwargs)
    elif model_format == "excel" or model_format == "xls" or (
        model_format == None and filename.endswith(".xls")) or (
        model_format == None and filename.endswith(".xlsx")):
        WriteExcel(model, filename, excel_format=excel_format)
    elif model_format == "cobra":
        WriteExcel(model, filename, excel_format="cobra")
    elif model_format == "cobra_old":
        WriteExcel(model, filename, excel_format="cobra_old")
    elif model_format == "scrumpy" or model_format == "spy" or (
                model_format == None and filename.endswith(".spy")):
        WriteScrumPyModel(model, filename, ExtReacs=ExtReacs)
    elif model_format == "yaml" or filename.endswith(".yaml") or filename.endswith(".yml"):
        cobra.io.save_yaml_model(model, filename, **kwargs)
    elif model_format== "cyc":
        print("INFO: writing Cyc model is only supported to excel format for now.")
        if excel_format == None:
            raise Exception("No excel format is given")
        #print(kwargs["usable_reactions"])
        if "usable_reactions" in kwargs and kwargs["usable_reactions"]:
            delete_metabolites=False
            if "delete_metabolites" in kwargs:
                delete_metabolites = kwargs["delete_metabolites"]
            model_copy = model.Copy()
            #print("this runs...")
            for v in model.unusable_reactions:
                #print(v)
                model_copy.DelReaction(v,delete_metabolites=delete_metabolites)
            WriteExcel(model_copy, filename, excel_format=excel_format)
        else:
            WriteExcel(model, filename, excel_format=excel_format)
    else:
        print('Please specify model_format')
