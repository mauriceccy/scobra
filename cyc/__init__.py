"""

ScrumPy -- Metabolic Modelling with Python

Copyright Mark Poolman 1995 - 2002

 This file was adopted from ScrumPy.

    ScrumPy is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    ScrumPy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

"""

from Organism import Organism
from AnnotatedOrganism import AnnotatedOrganism

import Base
import os

def Avail():

    rv = []

    for f in os.listdir(Base.DefaultPath):
        path = Base.DefaultPath + f
        if os.popen("ls -ld "+path).read()[0] == "d": # is a directory
            if "genes.dat" in os.listdir(path):
                rv.append(f)
    return rv
