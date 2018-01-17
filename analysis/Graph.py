

def DeadMetabolites(model, fva=None, reaclist=None, cobra=False):
    """ metabolites not involved in any allowed reactions """
    if fva == None:
        fva = model.FVA(reaclist=reaclist, cobra=cobra)
    allowed_mets =																																																					 []
    for r in fva.Allowed():
        for met in model.InvolvedWith(r):
            if model.GetMetaboliteName(met) not in allowed_mets:
                allowed_mets.append(model.GetMetaboliteName(met))
    return list(set(model.Metabolites()).difference(allowed_mets))

def NoDeadEndModel(model):
    tempmodel = model.Copy()
    pmets = tempmodel.PeripheralMetabolites()
    while len(pmets) > 0:
        tempmodel.DelMetabolites(pmets)
        pmets = tempmodel.PeripheralMetabolites()
    return tempmodel

def DeadEndMetabolites(model, nodeadendmodel=None):
    """ iteratively identify peripheral metabolites """
    if nodeadendmodel == None:
        nodeadendmodel = model.NoDeadEndModel()
    return list(set(model.Metabolites()).difference(nodeadendmodel.Metabolites()))

def PeripheralMetabolites(model, rc="all"):
    """ pre: rv ="all"|"Produced"|"Consumed"|"Orphan"
       post: returns dic or list of deadend metabolites """
    produced = []
    consumed = []
    orphan = []
    for met in model.Metabolites():
        prod = model.ProducedBy(met).keys()
        cons = model.ConsumedBy(met).keys()
        iw = list(set(prod).union(cons))
        if len(iw) == 1:
            orphan.append(met)
        if len(cons) == 0:
            produced.append(met)
        if len(prod) == 0:
            consumed.append(met)
    peri = list(set(produced).union(consumed).union(orphan))
    rvdic = {"all":peri,"Produced":produced,"Consumed":consumed,"Orphan":orphan}
    return rvdic[rc]

def ChokepointReactions(model):
    rv = []
    nodeadendmodel = model.NoDeadEndModel()
    for met in nodeadendmodel.Metabolites():
        prod = nodeadendmodel.ProducedBy(met)
        cons = nodeadendmodel.ConsumedBy(met)
        if len(prod) == 1:
            if prod.keys()[0] not in rv:
                rv.append(prod.keys()[0])
        if len(cons) == 1:
            if cons.keys()[0] not in rv:
                rv.append(cons.keys()[0])
    return model.GetReactionNames(rv)
    
def GetNeighbours(model, name, exclude=[]):
    rv = []
    nd = model.GetNeighboursAsDic(name,exclude)
    for neighbours in nd.values():
        for neighbour in neighbours:
            if neighbour not in rv:
                rv.append(neighbour)
    return rv

def GetNeighboursAsDic(model, name, exclude=[]):
    """  pre: name and exclude are reactions or metabolites names
        post: {iw:[neighbours]} """
    rv = {}
    iws = model.InvolvedWith(name,AsName=True)
    iws = list(set(iws).difference(exclude))
    for iw in iws:
        neighbours = model.InvolvedWith(iw, AsName=True).keys()
        neighbours = list(set(neighbours).difference([name]))
        neighbours = list(set(neighbours).difference(exclude))
        rv[iw] = neighbours
    return rv

def Degree(model, name, bipartite=True):
    if bipartite:
        n = model.InvolvedWith(name).keys()
    else:
        n = model.GetNeighbours(name)
    return len(n)

def DegreeDist(model, node_type="metabolites", bipartite=True):
    """ node_type = "metabolites" | "reactions" """
    rv = {}
    if 'met' in node_type:
        names = model.Metabolites()
    elif 'reac' in node_type:
        names = model.Reactions()
    for n in names:
        deg = model.Degree(n,bipartite=bipartite)
        if deg in rv.keys():
            rv[deg] = rv[deg] + 1
        else:
            rv[deg] = 1
    return rv

def MetabolitesDegree(model, mets=None, bipartite=True):
    rv = {}
    if not mets:
        mets = model.metabolites
    mets = model.GetMetabolites(mets)
    for met in mets:
        rv[met.id] = model.Degree(met, bipartite=bipartite)
    return rv

def ReactionsDegree(model, reacs=None, bipartite=True):
    rv = {}
    if not reacs:
        reacs = model.reactions
    reacs = model.GetReactions(reacs)
    for reac in reacs:
        rv[reac.id] = model.Degree(reac, bipartite=bipartite)
    return rv
