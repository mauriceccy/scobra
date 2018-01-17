
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


# In[3]:


import scobra.classes.flux as flux
import scobra.classes.matrix as matrix
import scobra.classes.pareto as pareto


# In[4]:


f = flux.flux({'H2O_ec1':1, 'SUPEROX_DISMUT_RXN_c2': 0, 'RXN66_1_c1': 3})
mat = matrix.matrix({"Flux": f, "Obj": f, "Obj2": f})
par = pareto.pareto(mat)


# In[6]:


par.GetParetoPoints()


# In[12]:


rv = pareto.pareto()
dir(rv)

