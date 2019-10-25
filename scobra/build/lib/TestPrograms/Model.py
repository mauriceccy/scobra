
# coding: utf-8

# In[19]:


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

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

blockPrint()
# In[20]:


###import random
##[m.Genes()[i] for i in random.sample(range(len(m.Genes())), 5)]


# In[21]:


# Creating sample reactions
reac_sample = ['PGLUCISOM_RXN_c', 'ACONITATEHYDR_RXN_c', '2TRANSKETO_RXN_p', 'Pi_PROTON_mc', 'CYS_PROTON_vc']
met_sample = ['PROTON_v', 'SUCROSE_c', 'UBIQUINONE_mi', 'PROTON_e', 'PPI_c']
gen_sample = ['SOLYC12G099650.1', 'SOLYC10G018300.1', 'SOLYC05G008370.1', 'SOLYC02G020940.2', 'SOLYC01G089970.2']


# In[22]:


# MANIPULATING AND WRITING MODELS
m.Copy()
m.SubModel(reac_sample)
m.DuplicateModel(["_c", "_t"])
m.WriteModel(os.path.join(currentdir, "misc", "writemodel.xls"))
m.WriteModel(os.path.join(currentdir, "misc", "writemodel.sbml"))
m.WriteAttributes(os.path.join(currentdir, "misc", "writeattr"))
m.WriteNetwork(os.path.join(currentdir, "misc", "writenetwork"))


# In[23]:


### REACTIONS 
# GETTING REACTIONS
m.GetReactions(reac_sample)
m.GetReactionNames(reac_sample)
m.Isozymes()
# PRINTING REACTIONS
m.PrintReactions(reac_sample)
# ADDING AND REMOVING REACTIONS
m.AddReaction("R1", {"A": 1, "B":-1})
m.ChangeReactionStoichiometry("R1", {"A": 2, "B":-5})
m.DelReactions(["R1"])
# IMBALANCE REACTIONS
m.ImbalanceReactions()
m.CheckReactionBalance(reac_sample[0])


# In[24]:


### METABOLITES
# GETTING METABOLITES
m.GetMetabolites(met_sample)
m.GetMetaboliteNames(met_sample)
m.Metabolites()
# ADDING AND REMOVING METABOLITES
m.AddReaction("R1", {"A": 1, "B":-1})
m.AddMetabolite("D")
m.SubstituteMetabolite("A", "D")
m.DelMetabolites(["A"])
m.DelReaction("R1")
m.AddProtonsToMets({m.GetMetabolite(met_sample[1]): 2, m.GetMetabolite(met_sample[2]): 3},"PROTON_e")
m.AssignMetabolitesNeutralFormula()


# In[25]:


# SOLVING AND PRINTING SOLUTIONS
m.Solve()
m.GetSol()
m.PrintSol()
m.MinFluxSolve()
m.AdjustedMinFluxSolve()
#m.NetStoi
m.ProduceMetabolites()
m.BlockedMetabolites()


# In[26]:


# PARETO 
the_sample = [['PHOSGLYPHOS_RXN_c'], {'H_tx':3, 'F16BDEPHOS_RXN_c':2}]
m.Pareto(the_sample, "Min", 10) # every single run outputs the same result 


# In[27]:


# FLUX SUM
m.FluxSum('PROTON_m')


# In[28]:


# FLUX RANGE
m.RandomMinFlux()


# In[29]:


# GRAPHS
m.DeadEndMetabolites()
m.PeripheralMetabolites()
m.ChokepointReactions()
m.GetNeighbours('PROTON_v')
m.DegreeDist()
m.MetabolitesDegree()
m.ReactionsDegree()


# In[30]:


end = timeit.default_timer()
print(end - start)


# In[ ]:


#import random
#sample = random.sample(range(len(m.Reactions())), 3)
#sample
#the_sample = [m.Reactions()[x] for x in sample]
#the_sample = ['PHOSGLYPHOS_RXN_c', 'H_tx', 'F16BDEPHOS_RXN_c']

