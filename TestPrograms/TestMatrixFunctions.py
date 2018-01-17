
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


# In[2]:


m.Reactions() 


# In[3]:


import scobra.classes.flux as flux
import scobra.classes.matrix as matrix


# In[4]:


f = flux.flux({'H2O_ec1':100, 'SUPEROX_DISMUT_RXN_c2': 200, 'RXN66_1_c1': 300})
mat = matrix.matrix({"Flux": f})


# In[2]:


thefile = enumerate(open(gparentdir + "/scobra/classes/matrix.py"))
flist = gaf.get_function_names_easy(thefile)


# In[6]:


flist = ['__init__', 'Copy', 'FromFile', 'ToFile', 'Plot', 'VaryReacs', 'FixedReacs', 'NonZeroes', 'ZeroReac', 'AverageFlux',
         'DicUpdate', 'UpdateFromDic', 'FluxCorrCoefMtx', 'FluxCorrCoef',
         'PrintFluxCorrCoef', 'StDev', 'PrintSD', 'RelStDev', 'PrintRSD', 'AverageDev', 'PrintAD', 'RelAverageDev',
         'PrintRAD', 'AsDic', 'PrintSorted']

errors = []
for i in flist: 
    try:
        print('executing ' + i)
        exec("mat." + i + "()")
    except TypeError: 
        errors.append(i)
errors = errors +  ['FluxRange', 'ResponseCoef', 'PrintResponseCoef']


# In[7]:


mat = matrix.matrix({"Flux": f})
mat.DicUpdate({"Flux2": 'test'})
mat.UpdateFromDic({"Flux2": 'test'})


# In[8]:


mat = matrix.matrix({"Flux": f})
mat2 = mat
mat.FluxCorrCoef('Flux')
mat.PrintFluxCorrCoef('Flux')
mat.StDev('Flux')
mat.RelStDev('Flux')
mat.AverageDev('Flux')
mat.RelAverageDev('Flux')
mat.PrintSorted({'H2O_ec1':100})


# In[3]:


path = "sample/sample_chloroplast.xls"
mat = mat.FromFile(path)
#mat.ToFile("/home/kristoforus/Desktop/test.xls")
mat.Plot('Objective')


# In[10]:


# mat.FluxRange() doesn't work due to the incompatible data structure demanded by fva functions
mat.columns


# In[12]:


mat = matrix.matrix({"Flux": f})
mat.ResponseCoef()
mat.PrintResponseCoef()

