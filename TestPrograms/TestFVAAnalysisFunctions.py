
# coding: utf-8

# In[1]:


import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
import get_all_functions as gaf
import re
n = scobra.Model("sample/Diel_Leaf_Model_cleaned.xls")
new = scobra.model(n)


# In[2]:


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
new.SetConstraint('NADPHoxm_tx', 10, 10)
new.SetConstraint('NADPHoxp_tx', 10, 10)
#setting constraints for sucrose entering and exiting cytoplasm
new.SetConstraint('Sucrose_ec', -1000, 1000)

#setting objectives
new.SetObjective('Sucrose_tx')
new.SetObjDirec('Min')


# In[3]:


import scobra.analysis.FVA as FVA 


# In[4]:


FVA.FVA(new, reaclist = new.reactions, cobra = True)


# In[4]:


FVA.AllFluxRange(new)


# In[ ]:


FVA.FVA(new, reaclist = new.reactions, cobra = True)
FVA.FluxVariability(new, fva=fva)


# In[ ]:


FVA.FluxRange(new, 'Sucrose_tx')
FVA.InternalCycles(new)

