
def compareMetaboliteDicts(d1, d2): 
    sorted_d1_keys = sorted(d1.keys())
    sorted_d2_keys = sorted(d2.keys())
    for i in range(len(sorted_d1_keys)): 
        if not compareMetabolites(sorted_d1_keys[i], sorted_d2_keys[i], naive=True):
            return False
        elif not d1[sorted_d1_keys[i]] == d2[sorted_d2_keys[i]]: 
            return False
    else: 
        return True

def compareMetabolites(met1, met2, naive=False): 
    if isinstance(met1, set): 
        return compareReactions(list(met1), list(met2), naive)
    if isinstance(met1, list): 
        if not isinstance(met2, list): 
            return False
        elif len(met1) != len(met2):
            return False 
        else:
            for i in range(len(met1)): 
                if not compareMetabolites(met1[i], met2[i], naive): 
                    return False 
            else: 
                return True
    else: 
        if not True: 
            #can never be entered
            pass
        elif not met1._bound == met2._bound: 
            return False
        elif not met1._constraint_sense == met2._constraint_sense: 
            return False
        #elif not met1.annotation == met2.annotation: 
        #    return False
        elif not met1.charge == met2.charge: 
            return False
        elif not met1.compartment == met2.compartment: 
            return False
        elif not met1.name == met2.name: 
            return False
        elif not met1.compartment == met2.compartment: 
            return False
        #elif not met1.notes == met2.notes: 
        #    return False
        elif not naive:
            if not compareReactions(met1._reaction, met2._reaction, naive=True): 
                return False
            elif not compareModels(met1._model, met2._model, naive=True): 
                return False
            else: 
                return True
        else: 
            return True

def compareReactions(r1, r2, naive=False): 
    if isinstance(r1, set): 
        return compareReactions(list(r1), list(r2), naive)
    if isinstance(r1, list): 
        if not isinstance(r2, list): 
            return False
        elif len(r1) != len(r2):
            return False 
        else:
            for i in range(len(r1)): 
                if not compareReactions(r1[i], r2[i],naive): 
                    return False 
            else: 
                return True
    else: 
        if not True: 
            #can never be entered
            pass
        #elif not r1._compartments == r2._compartments: 
        #    return False
        #elif not r1._forward_variable == r2._forward_variable:
        #    return False
        elif not r1._gene_reaction_rule == r2._gene_reaction_rule:
            return False
        elif not r1._id == r2._id: 
            return False
        elif not r1._lower_bound == r2._lower_bound: 
            return False 
        #elif not r1._model == r2._model: 
        #    return False
        #elif not r1._reverse_variable == r2._reverse_variable: 
        #    return False 
        elif not r1._upper_bound == r2._upper_bound: 
            return False 
        #elif not r1.annotation == r2.annotation: 
        #    return False 
        elif not r1.name== r2.name: 
            return False
        #elif not r1.notes == r2.notes: 
        #    return False 
        elif not r1.subsystem == r2.subsystem: 
            return False 
        elif not r1.variable_kind == r2.variable_kind: 
            return False 
        elif not naive:
            if not compareMetaboliteDicts(r1._metabolites, r2._metabolites): 
                return False 
            elif not compareGenes(r1._genes,r2._genes, naive=True): 
                return False
            else: 
                return True
        else: 
            return True
   

def compareGenes(g1, g2, naive=False): 
    if isinstance(g1, set): 
        return compareGenes(list(g1), list(g2), naive)
    if isinstance(g1, list): 
        if not isinstance(g2, list): 
            return False
        elif len(g1) != len(g2):
            return False 
        else:
            for i in range(len(g1)): 
                if not compareGenes(g1[i], g2[i], naive): 
                    return False 
            else: 
                return True
    else: 
        if not True: 
            #can never be entered
            pass
        elif not g1._functional == g2._functional: 
            return False
        elif not g1._id == g2._id:
            return False
        #elif not g1._model == g2._model:
        #    return False
        elif not g1.annotation == g2.annotation: 
            return False
        elif not g1.name == g2.name: 
            return False 
        #elif not g1.notes == g2.notes: 
        #    return False
        elif not naive: 
            if not compareReactions(g1._reaction,g2._reaction, naive=True): 
                return False
            else:
                return True
        else: 
            return True
    

def compareModels(m1, m2, naive=False): 
    if not True: 
        #can never be entered
        pass
    #elif not m1._compartments == m2._compartments: 
    #    return False
    #elif not m1._contexts == m2._contexts:
    #    return False
    #elif not m1._solver == m2._solver:
    #    return False
    elif not m1._id == m2._id: 
        return False
    #elif not m1._trimmed == m2.trimmed: 
    #    return False
    #elif not m1._trimmed_genes == m2._trimmed_genes: 
    #    return False 
    #elif not m1._trimmed_reactions == m2._trimmed_reactions: 
    #    return False 
    #elif not m1.annotation == m2.annotation: 
    #    return False 
    elif not m1.bounds == m2.bounds: 
        return False 
    elif not m1.name == m2.name: 
        return False
    #elif not m1.notes == m2.notes: 
    #    return False 
    #elif not m1.quadratic_component == m2.quadratic_component: 
    #    return False
    elif not naive: 
        if not compareGenes(m1.genes, m2.genes): 
            return False 
        elif not compareMetabolites(m1.metabolites, m2.metabolites): 
            return False 
        elif not compareReactions(m1.reactions,m2.reactions): 
            return False
        else: 
            return True
    else: 
        return True
