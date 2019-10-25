

def ROOM(model, refflux, reactions=None, delta=0, tol=0, IncZeroes=False,
         AsMtx=False, f=None, reset_state=True):
    """ refflux = {reac_name:flux} """
    if reset_state:
        state = model.GetState()
    model.ZeroObjective()
    if not reactions:
        reactions = model.Reactions()
    else:
        reactions = model.GetReactionNames(reactions)
    for reac in reactions:
        lb,ub = model.GetConstraint(reac)
        if reac in refflux:
            val = refflux[reac]
        else:
            val = 0.0
        hival = val + delta*abs(val) + tol
        loval = val - delta*abs(val) - tol
        model.AddMetabolite(reac+"_ROOMVarhi")
        model.SetMetBounds(reac+"_ROOMVarhi", -model.bounds*2, hival)
        model.AddMetabolite(reac+"_ROOMVarlo")
        model.SetMetBounds(reac+"_ROOMVarlo", loval, model.bounds*2)
        model.GetReaction(reac).add_metabolites({model.GetMetabolite(
            reac+"_ROOMVarhi"):1, model.GetMetabolite(reac+"_ROOMVarlo"):1})
        model.AddReaction(reac+"_ROOMVar",{model.GetMetabolite(
            reac+"_ROOMVarhi"):-(ub-hival), model.GetMetabolite(
            reac+"_ROOMVarlo"):-(lb-loval)}, bounds=(0,1))
        model.GetReaction(reac+"_ROOMVar").variable_kind = 'integer'
        model.SetObjective({reac+"_ROOMVar":1})
    model.SetObjDirec("Min")
    model.Solve(False)
    model.CleanUpTempVar("_ROOMVar")
    rv = model.GetSol(IncZeroes=IncZeroes,AsMtx=AsMtx,f=f)
    if reset_state:
        model.SetState(state, IncSol=False)
    return rv

def CleanUpROOM(model):
    model.CleanUpTempVar("_ROOMVar")