
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


#from model.py
thefile = enumerate(open(gparentdir + "/scobra/classes/model.py"))
flist = gaf.get_function_names(thefile)


# In[4]:


def filter_f(lower, upper=100):
    for i in flist: 
        count = 0 
        for j in open(gparentdir + "/scobra/classes/model.py"): 
            if i in j: 
                count += 1
        if count > lower and count < upper: 
            print("%s: %d" % (i, count))
filter_f(20)


# In[5]:


m.Metabolites()
m.Reactions()
m.GetReaction('Pi_PROTON_mc2')
m.GetMetabolite('pALA_b2')
m.GetReactionName('Pi_PROTON_mc2')
m.Solve()
m.solution


# In[6]:


m.Genes()
m.GetGene('SOLYC03G062890.2')
m.GetMetaboliteName('pALA_b2')
m.InvolvedWith('Pi_PROTON_mc2')
m.SetConstraint('Pi_PROTON_mc2', 0, 10)
m.SetMetBounds('3_DEHYDRO_SHIKIMATE_p2', 100)


# In[7]:


m.Degree('CYTOCHROME_C_OXIDASE_RXN_mi1')


# In[8]:


m.WriteModel(currentdir + "/misc/TestSBML", model_format="sbml")
## works for sbml, xml, and json 
## writing to xls, matlab, scrumpy requires more modules 
## writing to cobra and cobra old is problematic
m.WriteFile(currentdir + "/misc/TestSBML", model_format="sbml")
m.ToFile(currentdir + "/misc/TestXML", model_format="xml")


# In[9]:


m.Copy()
m.SubModel({'CYTOCHROME_C_OXIDASE_RXN_mi1': 10, 'NADPPHOSPHAT_RXN_c1': 20})
n = m.DuplicateModel(['_c'])
m.MergeWithModel(n)


# In[10]:


m.GetReactions(['CYTOCHROME_C_OXIDASE_RXN_mi1', 'NADPPHOSPHAT_RXN_c1'])
m.GetMetabolites(['Beta_3_hydroxybutyryl_ACPs_p1','NAD_x1','Beta_3_hydroxybutyryl_ACPs_p2',
 'NAD_x2',])
m.GetGenes(['SOLYC11G066390.1',
 'SOLYC06G048420.1',
 'SOLYC02G021140.2',
 'SOLYC08G079830.2',
 'SOLYC03G062890.2',
 'SOLYC06G048410.2'])
m.GetGeneName('SOLYC11G066390.1')
m.GetMetaboliteNames(['Beta_3_hydroxybutyryl_ACPs_p1','NAD_x1','Beta_3_hydroxybutyryl_ACPs_p2',
 'NAD_x2'])
m.GetGeneNames(['SOLYC11G066390.1',
 'SOLYC06G048420.1',
 'SOLYC02G021140.2',
 'SOLYC08G079830.2',
 'SOLYC03G062890.2',
 'SOLYC06G048410.2'])
m.PrintReaction('CYTOCHROME_C_OXIDASE_RXN_mi1')
m.PrintReactions(['CYTOCHROME_C_OXIDASE_RXN_mi1', 'NADPPHOSPHAT_RXN_c1'])


# In[11]:


#from model.py
thefile = enumerate(open(gparentdir + "/scobra/classes/model.py"))
flist_self_only = gaf.get_functions_self_only(thefile)[0]
flist_more = gaf.get_functions_self_only(thefile)[1]
for i in flist_self_only: 
    count = 0 
    for j in open(gparentdir + "/scobra/classes/model.py"): 
        if i in j: 
            count += 1
    if count < 5: 
        print("%s: %d" % (i, count)) 


# In[12]:


flist_self_only.remove('NoDeadEndModel')
flist_self_only.remove('ChokepointReactions')
for i in flist_self_only: 
    print("executing " + i)
    try:
        exec("m." + i + "()")
    except TypeError: 
        exec("m." + i)
    


# In[13]:


import scobra
import get_all_functions as gaf
import re
n = scobra.Model("sample/Supplemental-Data-S1_Core-Leaf-Model.xml")
m = scobra.model(n)
thefile = enumerate(open(gparentdir + "/scobra/classes/model.py"))
flist_more = gaf.get_functions_self_only(thefile)[1]
errors = []
problematic = ['PrintSol', 'BlockedMetabolites', 'FluxVariability', 'GeometricSol', 'DeadMetabolites', 'MOMA2mutant']
for i in flist_more:
    for problem in problematic: 
        if problem in i:
            break
    else: 
        print("executing " + i)
        try:
            exec("m." + i + "()")
        except (TypeError, NameError), e: 
            errors.append(i)
errors = errors + problematic


# In[14]:


n = scobra.Model("sample/Supplemental-Data-S1_Core-Leaf-Model.xml")
m = scobra.model(n)
m.SetObjective('H2O_ec1')
m.SetQuadraticObjective('H2O_ec1')
m.GetConstraint('H2O_ec1')
m.SetConstraints({'H2O_ec1':(0,100)})
m.SetConstraint('H2O_ec1', 0, 100)
m.SetFixedFlux({'H2O_ec1':100})
m.SetState(m.GetState())


# In[15]:


m.SetReacsFixedRatio({'H2O_ec1': 1,'ORNCARBAMTRANSFER_RXN_p1':9})


# In[16]:


m.DelReaction('Pi_PROTON_mc2')
m.AddReaction('Pi_PROTON_mc2', {'PROTON_m2': -1, 'Pi_m2': -1, 'PROTON_c2': 0.7, 'Pi_c2': 0.7, 'aPi_c2': 0.3})
m.DelMetabolite('pALA_b2')
m.AddMetabolite('pALA_b2')
m.SubstituteMetabolite('pALA_b2', 'pALA_b1')
m.ChangeReactionStoichiometry('Pi_PROTON_mc2', {'PROTON_m2': -1, 'Pi_m2': -1, 'PROTON_c2': 0.7, 'Pi_c2': 0.7, 'aPi_c2': 1})
m.SetMetBounds('pALA_b2')


# In[17]:


import scobra
import get_all_functions as gaf
import re
n = scobra.Model("sample/Supplemental-Data-S1_Core-Leaf-Model.xml")
m = scobra.model(n)


# In[18]:


m.ProducedBy('pALA_b2')
m.ConsumedBy('pALA_b2')


# In[19]:


m.GetNeighbours('pALA_b2')
m.GetNeighboursAsDic('pALA_b2')
m.Degree('pALA_b2')


# In[20]:


m.WriteNetwork(currentdir + '/misc/TestNetwork')
m.WriteAttributes(currentdir + '/misc/TestAttributes')


# In[21]:


m.AddProtonsToMet('1_KETO_2_METHYLVALERATE_p2', 'PROTON_e1', 3)
m.AddProtonsToMets({'1_KETO_2_METHYLVALERATE_p2': 2,'D_ERYTHRO_IMIDAZOLE_GLYCEROL_P_p1': 3}, 'PROTON_e1')


# In[22]:


m.CheckReactionBalance('PGLYCDEHYDROG_RXN_p1')


# In[23]:


import scobra
import get_all_functions as gaf
import re


# In[24]:


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
new.SetConstraint('ATPase_tx', 90, 90)
new.SetConstraint('NADPHoxc_tx', 10, 10)
new.SetConstraint('NADPHoxm_tx', 10, 10)
new.SetConstraint('NADPHoxp_tx', 10, 10)
#setting constraints for sucrose entering and exiting cytoplasm
new.SetConstraint('Sucrose_ec', -1000, 1000)

#setting objectives
new.SetObjective('Sucrose_tx')
new.SetObjDirec('Min')

#running scans
new.Solve() 
new.PrintSol()
#new.MinFluxSolve()
sol1 = new.solution


# In[25]:


new.SetConstraint('Photon_tx', 300, 300)
new.Solve()
sol2 = new.solution


# In[26]:


new.solution.status


# In[27]:


new.SolsDiff(sol1.fluxes, sol2.fluxes)

