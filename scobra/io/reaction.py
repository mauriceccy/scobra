import builtins as exceptions
#many unsupported attribute of types lib in python 3
import types
import re, math 
from collections import defaultdict
import numpy
import scipy
#import metabolite

import cobra
from cobra import Metabolite, Reaction, Gene
from cobra.flux_analysis import deletion, moma, phenotype_phase_plane
from cobra.core.solution import get_solution
#from cobra.manipulation import modify

#from ..analysis import FCA, Pareto, RWFM, MOMA, ROOM, GeometricFBA, MinSolve
#from ..analysis import Graph, FluxSum, FVA, MinSolve, Scan
#from ..manipulation import Reversible
#from ..classes.flux import flux
#rom ..io import Network

class Reaction(cobra.Reaction):
	def __init__(self,id=None, name='', subsystem='', lower_bound=0.,upper_bound=1000., objective_coefficient=0.):
		super().__init__(id=id,name=name,subsystem=subsystem,lower_bound=lower_bound,upper_bound=upper_bound)
		#self.objective_coefficient = objective_coefficient
		return
	def __str__(self):
		return