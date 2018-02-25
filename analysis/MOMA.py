

def LinearMOMA(model, refflux):
    model.MinDiffFromFlux(refflux, reacs=refflux.keys(), it=0, cleanup=True)

def MinDiffFromFlux(model, fluxdist, reacs=None, it=0, cleanup=True):
    """ pre: fluxdist = {reac:flux_val} """
    state = model.GetState()
    obj = {}
    if not reacs:
        reacs = fluxdist.keys()
    for r in reacs:
        rowname = r+"_"+str(it)+"_mindifffromflux"
        colplus = r+"_"+str(it)+"_mindifffromflux+"
        colminus = r+"_"+str(it)+"_mindifffromflux-"
        model.AddMetabolite(rowname)
        model.GetReaction(r).add_metabolites({model.GetMetabolite(rowname):1})
        model.AddReaction(colplus,{model.GetMetabolite(rowname):1})
        model.AddReaction(colminus,{model.GetMetabolite(rowname):-1})
        model.SetMetBounds(rowname, fluxdist[r], fluxdist[r])
        obj[colplus] = 1
        obj[colminus] = 1
    model.ZeroObjective()
    model.SetObjective(obj)
    model.SetObjDirec("Min")
    model.Solve(False)
    ### cleanup
    if cleanup:
        model.CleanUpTempVar("_mindifffromflux")
    model.SetState(state,IncSol=False)

def CleanUpTempVar(model, var):
    for row in model.Metabolites():
        if var in row:
            model.SetMetBounds(row, 0, 0)
            #model.DelMetabolite(row)
    for col in model.Reactions():
        if var in col:
            model.DelReaction(col)
    if len(model.solution.x_dict) != 0:
        for x in list(model.solution.x_dict.keys()):
            if var in x:
                del model.solution.x_dict[x]
    #if len(model.solution.x) != 0:
    #    model.solution.x = model.solution.x[:len(model.reactions)]
    if len(model.solution.y_dict) != 0:
        for y in list(model.solution.y_dict.keys()):
            if var in y:
                del model.solution.y_dict[y]
    #if len(model.solution.y) != 0:
    #    model.solution.y = model.solution.y[:len(model.metabolites)]
    ### x and y attributes of model.solution does not have a 
    ### setter property; thus, their values cannot be changed. 
    ### To access a similar data, use x_dict and y_dict. 

def MOMA(model, refflux):
    state = model.GetState()
    model.ZeroObjective()
    model.SetObjDirec("Min")
    for reac in refflux:
        model.SetQuadraticObjective({reac:1})
        model.SetObjective({reac:-refflux[reac]})
    model.Solve(False)
    model.SetState(state,IncSol=False)


