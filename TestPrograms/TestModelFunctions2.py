
# coding: utf-8

# In[3]:


import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
import get_all_functions as gaf
import re
n = scobra.Model("sample/Diel_Leaf_Model_cleaned.xls")
m = scobra.model(n)


# In[4]:


m.SingleDeletion()
m.EssentialGenes() 
m.EssentialReactions() 
m.DoubleDeletion()

