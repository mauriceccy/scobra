
# coding: utf-8

# In[ ]:


import timeit 
start = timeit.default_timer()


# In[3]:


import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
model_path = os.path.join(currentdir, "sample","testmodel.xls")
n = scobra.Model(model_path)
m = scobra.model(n)

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

blockPrint()

# In[4]:


m.AllFluxRange()


# In[5]:


m.FluxRange({'O2_tx': 1})


# In[6]:


m.InternalCycles()


# In[8]:


end = timeit.default_timer()
print(end - start)

