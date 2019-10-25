
# coding: utf-8

# In[1]:


import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
import timeit
start = timeit.default_timer()
model_path = os.path.join(currentdir, "sample","testmodel.xls")
n = scobra.Model(model_path)
m = scobra.model(n)


# In[2]:


m.FCA() 


# In[3]:


end = timeit.default_timer()
end - start

