
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


# In[6]:


m.SetFixedFlux({'H2O_ec1':100, 'SUPEROX_DISMUT_RXN_c2': 200, 'RXN66_1_c1': 300})


# In[12]:


import scobra.classes.flux as flux


# In[21]:


f = flux.flux({'H2O_ec1':100, 'SUPEROX_DISMUT_RXN_c2': 200, 'RXN66_1_c1': 300})


# In[23]:


f.__call__()
f.Filter()
f.Print()
f.Diff({'H2O_ec1':100, 'SUPEROX_DISMUT_RXN_c2': 200})
f.AsMtx()
f.Copy()

