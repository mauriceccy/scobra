import scobra
from scobra.classes.reaction import Reaction
from scobra.classes.metabolite import Metabolite

#import the core model--Modify the path
#peanut = scobra.Model("peanut_exports/peanut_core.xlsx")

#import the compartment file
import Compartments as cps

def compartment_reaction(model, r, compartment, compartmented):
    #print(r.id, flush=True)
    if r.id[-2:] in ["_p", "_x", "_m", "_c"]:
        model.add_reaction(r)
        return compartmented
    #print("passed", flush=True)
    cpt_r = r.copy()
    cpt_r.id = r.id+compartment

    new_stoi = {}
    for m in r._metabolites:
        cpt_m = None
        if not m.id in compartmented:
            cpt_m = Metabolite()
            cpt_m = m.copy()
            cpt_m.compartment = compartment[1]
            cpt_m.id = m.id + compartment
            compartmented[cpt_m.id] = cpt_m
            
        if m.id in compartmented and m.id in model.Metabolites():
            cpt_m = model.GetMetabolite(m.id)
        else:
            cpt_m = compartmented[m.id+compartment]
            
        new_stoi[cpt_m] = r._metabolites[m]
    
    cpt_r.subtract_metabolites(r._metabolites, reversibly=r.reversibility)
    cpt_r.add_metabolites(new_stoi, reversibly=r.reversibility)
    model.add_reaction(cpt_r)

    return compartmented

list_new_reactions = []

def compartmenting(model):
    reactions = model.Reactions()
    compartmented = {}
    
    for r in reactions:
        found = False
        r = model.GetReaction(r)

        model.DelReaction(r.id)
        
        if r.id in cps.Plastid:
            found = True
            compartmented = compartment_reaction(model, r, "_p", compartmented)

        if r.id in cps.Mitochondria:
            found = True
            compartmented = compartment_reaction(model, r, "_m", compartmented)

        if r.id in cps.Peroxisome:
            found = True
            compartmented = compartment_reaction(model, r, "_x", compartmented)

        if not found:
            list_new_reactions.append(r)

        if r.id in cps.Cytosol or not found:
            compartmented = compartment_reaction(model, r, "_c", compartmented)

    m_list = model.Metabolites()
    for m in m_list:
        m = model.GetMetabolite(m)
        if len(m._reaction) == 0:
            model.remove_metabolites(m)
    return model

def writeNewReactions(filename):
    f = open(filename, "w")
    for i in list_new_reactions:
        f.write(i.id + ", " + i.reaction + "\n")

    f.flush()
    f.close()
    return
