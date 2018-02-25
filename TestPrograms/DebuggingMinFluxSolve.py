
# coding: utf-8

# In[1]:


import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
import get_all_functions as gaf
import re

new=scobra.Model('sample/Diel_Leaf_Model_cleaned.xls')
new= scobra.model(new)
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
#new.SetConstraint('ATPase_tx', 90, 90)
#new.SetConstraint('NADPHoxc_tx', 10, 10)
#new.SetConstraint('NADPHoxm_tx', 10, 10)
#new.SetConstraint('NADPHoxp_tx', 10, 10)
#setting constraints for sucrose entering and exiting cytoplasm
new.SetConstraint('Sucrose_ec', -1, -1)

#setting objectives
new.SetObjective('Photon_tx')
new.SetObjDirec('Min')
#new.SetFixedFlux({'unlProtHYPO_c': 0})

#running scans
#new.MinFluxSolve() 
#new.Solve()


# In[2]:


new.MinFluxSolve()


# In[3]:


new.GetSol()


# In[5]:


new.solution.x_dict


# In[14]:


this = new.GetSol()
this


# In[ ]:


that = new.GetSol()


# In[25]:


new.GetConstraints()


# In[17]:


new.Solve()


# In[23]:


new.GetState()['solution'].x_dict
new.GetSol()


# In[5]:


new.MinFluxSolve()


# In[15]:


new.solution.x_dict

