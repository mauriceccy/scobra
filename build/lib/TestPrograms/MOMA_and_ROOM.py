
# coding: utf-8

# In[27]:


import timeit 
start = timeit.default_timer()
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
gparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, gparentdir)
import scobra
import get_all_functions as gaf
import re
new = scobra.Model(os.path.join(currentdir, "sample", "Diel_Leaf_Model_cleaned.xls"))
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
new.SetConstraint('NADPHoxm_tx', 10, 10)
new.SetConstraint('NADPHoxp_tx', 10, 10)
#setting constraints for sucrose entering and exiting cytoplasm
new.SetConstraint('Sucrose_ec', -1000, 1000)

#setting objectives
new.SetObjective('Sucrose_tx')
new.SetObjDirec('Min')

#setting constraint and running scan
"""
result = {}
for i in range(0,1000,20):
    new.SetConstraint('Photon_tx', i, i)
    new.Solve()
    x = new.GetSol()['Sucrose_tx']
    result[i] = x
"""
#new.Solve() 
#new.MinFluxSolve()

new.Solve()


# In[28]:


refflux = {'1TRANSKETO_RXN_p': 31.979030144167627,
 '1_PERIOD_10_PERIOD_2_PERIOD_2_RXN_mi': 28.12581913499394,
 '1_PERIOD_18_PERIOD_1_PERIOD_2_RXN_p': 250.00000000000009,
 '2KG_ISOCITRATE_mc': 9.999999999999966,
 '2TRANSKETO_RXN_p': -31.979030144167627,
 'ADENYL_KIN_RXN_c': -42.188728702489634,
 'ADENYL_KIN_RXN_m': 42.18872870248983,
 'ATP_ADP_Pi_pc': 13.617300131062754}


# In[29]:


import scobra.analysis.MOMA as moma
moma.LinearMOMA(new, refflux)
moma.MOMA(new, refflux)


# In[30]:


new.ROOM(refflux)


# In[31]:


start = timeit.default_timer()
new.MinReactionsSolve()
end = timeit.default_timer()
end - start


# In[32]:


end = timeit.default_timer()
print(end - start)
#print('Test Completed')

