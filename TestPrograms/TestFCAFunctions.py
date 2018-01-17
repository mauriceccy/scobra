
# coding: utf-8

# In[1]:


import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
import get_all_functions as gaf
import re
n = scobra.Model("sample/Supplemental-Data-S1_Core-Leaf-Model.xml")
m = scobra.model(n)


# In[20]:


import scobra.classes.flux as flux
import scobra.classes.matrix as matrix
import scobra.classes.fca as fca
f = flux.flux({'H2O_ec1':1, 'SUPEROX_DISMUT_RXN_c2': 0, 'RXN66_1_c1': 3})
mat = matrix.matrix({"Flux": f, "Obj": f, "Obj2": f})
path = "sample/model4a(1).xls"
mat = mat.FromFile(path)
fc = fca.fca(mat)


# In[14]:


fc.Copy()
fc.DirectionallyCoupled()
fc.PartiallyCoupled()
fc.FullyCoupled()
fc.SwapSign('+')
fc.ReacCoupling('Proteins')


# In[51]:


fc.RangeType(10, 5, 0.00001, 100)
fc.RangeType(1, 100, 1, 1000)

