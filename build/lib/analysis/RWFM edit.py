
# coding: utf-8

# In[1]:


import os, sys, inspect
import pandas
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
import timeit
start = timeit.default_timer()

model_path = os.path.join(gparentdir,"scobra","TestPrograms", "sample","testmodel.xls")
n = scobra.Model(model_path)
m = scobra.model(n)


# In[14]:


import multiprocessing
from scobra.classes.matrix import matrix
from testprocess import RWFMSolveMinFlux #had to put function in diff .py because windows glitch
import time #added time for speed record


        
def RandomMinFlux(model,it=1,reacs=None,exc=[],processes=None):
    start_time= time.time()
    state = model.GetState()
    if reacs == None:
        reacs = model.Reactions()
        print ("1")
    else:
        reacs = model.GetReactionNames(reacs)
        print ("2")
    for reac in exc:
        reac = model.GetReactionName(exc)
        print ("3")
        if reac in reacs:
            reacs.remove(reac)
            print ("4")
       
    mtx = matrix()
    pool = multiprocessing.Pool(processes=processes)
    results = [pool.apply_async(RWFMSolveMinFlux, args=(model,)) for x in range(it)]    
    pool.close()
    print ("5")
    pool.join()
    print ("6")
    sols = [x.get() for x in results]
    #sols also hangs
    print ("7")
    for sol in sols:
        mtx = mtx.UpdateFromDic(sol)
    model.SetState(state)
    print ("8")
    end_time= time.time()- start_time
    
    print("Processing {} took {} seconds".format((model),end_time))
    return mtx
    

    






# In[1]:


x = RandomMinFlux(m)

