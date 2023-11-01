import builtins as exceptions
#many unsupported attribute of types lib in python 3
import types
import re, math
from collections import defaultdict
import numpy
import scipy

import cobra
from cobra import Metabolite, Reaction, Gene
from cobra.flux_analysis import deletion, moma, phenotype_phase_plane
from cobra.core.solution import get_solution
#from cobra.manipulation import modify

#from ..analysis import FCA, Pareto, RWFM, MOMA, ROOM, GeometricFBA, MinSolve
#from ..analysis import Graph, FluxSum, FVA, MinSolve, Scan
#from ..manipulation import Reversible
#from ..classes.flux import flux
#from ..io import Network

class Metabolite(cobra.Metabolite):
    """
    Metabolite is a class inherited from the cobra Metabolite class that holds information
	that can be used in the scobra reaction class.  It differs forom the original cobra
	Metabolite class with 3 new states:

	Parameters
	----------
	inchi : str
	smiles : str
	molecular_weights : float
		the combined weight of the molecules in the metabolite
    """
    def __init__(self, id=None, formula=None, name="",charge=None, compartment=None,inchi=None,smiles=None,molecular_weights=None,comments="", concentration=None):
        super().__init__(id=id, formula=formula, name=name,charge=charge, compartment=compartment)
        self.inchi_id = inchi
        self.smiles = smiles
        self.molecular_weights = molecular_weights
        self.comments = comments
        self.concentration = concentration
