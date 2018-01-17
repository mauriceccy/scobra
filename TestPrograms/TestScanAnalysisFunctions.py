
# coding: utf-8

# In[4]:


import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
import get_all_functions as gaf
import re
def fresh(): 
    new = scobra.Model("sample/Diel_Leaf_Model_cleaned.xls")
    #new = scobra.model(n)

    #new=scobra.Model('models/Diel_Leaf_Model_cleaned.xls')

    #Maximize Sucrose output (objective)
    #vary light (scan)
    #allow CO2 and O2, even Proton and Water
    #Output maintenance ATP and NADPHox
    tx_and_biomass = []
    for i in new.Reactions(): 
        if '_tx' in i:
            tx_and_biomass.append(re.search('(.*)_tx', i).group())
        elif '_biomass' in i: 
            tx_and_biomass.append(re.search('(.*)_biomass', i).group())
    #tx_and_biomass.append(re.search('(.*)_tx', 'slkdfjd_tx').group())
    tx_and_biomass

    necessary_rxn= ['ATPase_tx', 'CO2_tx', 'Photon_tx', 'O2_tx','H2O_tx', 'H_tx','NADPHoxc_tx','NADPHoxm_tx','NADPHoxp_tx','Sucrose_tx']
    unecessary_rxn= list(set(tx_and_biomass) - set(necessary_rxn))

    #blocking _tx and _biomass reactions that are not considered
    for i in unecessary_rxn: 
        new.GetReaction(i).lower_bound = 0.0
        new.GetReaction(i).upper_bound = 0.0

    #freeing _tx and _biomass reactions that are considered
    for i in necessary_rxn: 
        if new.GetReaction(i).lower_bound == 0.0:
            new.GetReaction(i).upper_bound == 1000.0
        else: 
            new.GetReaction(i).lower_bound == 1000.0
            new.GetReaction(i).upper_bound == 1000.0

    #setting constraints
    new.SetConstraint('ATPase_tx', 90, 90)
    new.SetConstraint('NADPHoxc_tx', 10, 10)
    #new.SetConstraint('NADPHoxm_tx', 10, 10)
    #new.SetConstraint('NADPHoxp_tx', 10, 10)
    #setting constraints for sucrose entering and exiting cytoplasm
    new.SetConstraint('Sucrose_ec', -1000, 1000)

    #setting objectives
    new.SetObjective('Sucrose_tx')
    new.SetObjDirec('Min')

    #setting constraint and running scan
    #result = {}
    #for i in range(0,1000,20):
    #    new.SetConstraint('Photon_tx', i, i)
    #    new.Solve()
    #    x = new.GetSol()['Sucrose_tx']
    #    result[i] = x

    #new.Solve() 
    #new.MinFluxSolve()

    new.Solve()
    return new
new = fresh()


# In[2]:


import scobra.analysis.Scan as scan


# In[ ]:


scan.ConstraintScan(new, {'NADPHoxm_tx': 10, 'NADPHoxp_tx': 10}, 0, 100, 20, MinFlux = False)


# In[21]:


scan.RatioScan(new, 'NADPHoxm_tx', 'NADPHoxp_tx', 20)


# In[26]:


new.Constraint2DScan({'NADPHoxm_tx': 10, 'NADPHoxp_tx': 10}, 0,500, {'2PGADEHYDRAT_RXN_c': 10, '2PGADEHYDRAT_RXN_p': 10}, 0, 1000, 10)



# In[16]:


new = fresh()
new.ConstraintRandomMinFluxScan({'NADPHoxm_tx': 10, 'NADPHoxp_tx': 10}, 0,500, 9, 1)
#doesn't work when the 4th argument is 10 for some reason...


# In[13]:


new = fresh()
new.SetSumReacsConstraint({'NADPHoxm_tx': 10, 'NADPHoxp_tx': 10}, 0, "this")
import scobra.analysis.RWFM as rwfm
rwfm.RandomMinFlux(new)
#import multiprocessing
#pool = multiprocessing.Pool(processes=None)
#results = [pool.apply_async(rwfm.RWFMSolveMinFlux, args=(new,)) for x in range(1)]
#pool.close()
#pool.join()


# In[12]:


results[0].__dict__


# In[15]:


new.GetReaction('this_sum_reaction').upper_bound


# In[4]:


new = fresh()
new.RatioRandomMinFluxScan('NADPHoxm_tx','NADPHoxp_tx', 10, 1)


# In[29]:


new.WeightingScan({'NADPHoxm_tx': 10, 'NADPHoxp_tx': 10}, 0, 500, 10)

