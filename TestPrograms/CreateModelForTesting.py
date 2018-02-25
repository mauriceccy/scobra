
# coding: utf-8

# In[2]:


import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
import get_all_functions as gaf
import re

new=scobra.Model('sample/12018_0_supp_510122_p0t431.xls')
new= scobra.model(new)


# In[ ]:


new.Reactions()


# In[ ]:


for i in new.Reactions(): 
    if new.GetReaction(i).lower_bound == 0.0:
        new.GetReaction(i).upper_bound == 1000.0
    else: 
        new.GetReaction(i).lower_bound == 1000.0
        new.GetReaction(i).upper_bound == 1000.0
new.SetConstraint('O2_pc', -1, -1)
new.SetObjective('Photon_tx')
new.SetObjDirec('Max')
new.Solve()


# In[ ]:


len(new.GetSol())


# In[ ]:


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

necessary_rxn= ['CO2_tx', 'Photon_tx', 'O2_tx','H2O_tx','NADPHoxc_tx','NADPHoxm_tx','NADPHoxp_tx','Starch_tx']
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
new.SetConstraint('Starch_tx', -1, -1)

#setting objectives
new.SetObjective('Photon_tx')
new.SetObjDirec('Min')
#new.SetFixedFlux({'unlProtHYPO_c': 0})

#running scans
#new.MinFluxSolve() 
new.Solve()


# In[2]:


start = timeit.timeit()
new.MinFluxSolve()
end = timeit.timeit()
time_taken = end - start


# In[4]:


tx_and_biomass = []
for i in new.Reactions(): 
    if '_tx' in i:
        tx_and_biomass.append(re.search('(.*)_tx', i).group())
new.PrintReactions(tx_and_biomass)


# In[3]:


new.GenesToSubsystemsAssociations


# In[27]:


len(new.GetSol())


# In[29]:


len(new.Reactions())


# In[6]:


#new.WriteModel('/home/kristoforus/Desktop/model.xls')


# In[31]:


lst_submodel = [new.GetReaction(x) for x in new.GetSol()]
testm = new.SubModel(lst_submodel)

print( [ i for i in testm.Reactions() if 'ATP' in i])


# In[32]:


len(testm.Reactions())


# In[33]:


testm.SetObjective('Photon_tx')
testm.SetObjDirec('Min')


# In[35]:


testm.Solve()
testm.GetSol()
len(testm.GetSol())


# In[37]:


testm.WriteModel('/home/kristoforus/Desktop/testmodel.xls')

