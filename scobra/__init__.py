__verison__ = '1.0.0'

from .io.IO import ReadModel as Model
from .classes.model import model
from .classes.fva import fva
from .classes.fca import fca
from .classes.matrix import matrix
from .classes.pareto import pareto
from .classes.flux import flux
#from .classes.reaction import reaction
#from .classes.metabolite import metabolite
#from .classes.db import db
##import sys
##import os
##p = os.path.abspath(__file__)
##location = p[:p.rindex(os.sep)]
##sys.path.append(location)
