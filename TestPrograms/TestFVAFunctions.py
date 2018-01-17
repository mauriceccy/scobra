
# coding: utf-8

# In[2]:


import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
import get_all_functions as gaf
import re
n = scobra.Model("sample/Supplemental-Data-S1_Core-Leaf-Model.xml")
m = scobra.model(n)


# In[2]:


import scobra.classes.fva as fva
import scobra.classes.flux as flux
dic = m.ReactionsDegree()
f = fva.fva(dic)
f


# In[6]:


thefile = enumerate(open(gparentdir + "/scobra/classes/fva.py"))
flist = gaf.get_function_names_easy(thefile)


# In[4]:


f = fva.fva({'abc': [40,60], 'def': [20,50]})


# In[5]:


flist = ['Blocked', 'Allowed', 'Variable', 'Fixed', 'Essential', 'Substitutable', 'Unbounded',
         'Bounded', 'BothDirections', 'ForwardOnly', 'BackwardOnly', 'AsMtx', 'GetReacs', 'GetReacsMeanFlux',
         'MaxDiff', 'FluxRangeDiff', 'FluxDiffDirec', 'FluxRangeOverlap']

errors = []
for i in flist: 
    try:
        print('executing ' + i)
        exec("f." + i + "()")
    except TypeError: 
        errors.append(i)
#errors = errors +  []


# In[7]:


f.GetReacs(['abc'])
f.GetReacsMeanFlux(['abc'])
f2 = fva.fva({'abc': [20,100], 'jkl': [40,300]})
f.FluxDiffDirec(f2)
f.FluxRangeOverlap(f2)
f.FluxRangeDiff(f2)

