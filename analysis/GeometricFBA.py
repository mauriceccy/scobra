from cobra.manipulation import modify

def GeometricSol(model, IncZeroes=True, AsMtx=False, tol=1e-6, Print=False, cobra=False):
    state = model.GetState()
    reacs = model.reactions
    model.SetObjAsConstraint(name='FluxDiff'+str(0)+'_mindifffromflux')
    ### iteraion 1
    model.SetObjDirec("Min")
    it = 1
    model.ZeroObjective()
    modify.convert_to_irreversible(model)
    model.SetObjective(model.Reactions())
    model.Solve(False)
    model.SetObjAsConstraint(name='FluxDiff'+str(it)+'_mindifffromflux')
    fva = model.FVA(reaclist=reacs,tol=tol,PrintStatus=False, cobra=cobra)
    meanflux = fva.GetReacsMeanFlux(fva.keys())
    flux = dict(meanflux)
    flux_id = {}
    for reac in flux: 
    	flux_id[reac.id] = flux[reac]
    delta = fva.MaxDiff()
    variablereacs = fva.Variable(tol)
    variablereacs_id = [reac.id for reac in variablereacs]
    if Print:
        print("Iteration "+str(it)+", "+str(len(variablereacs))+" varible reactions, Max difference = "+str(delta))
    it += 1
    ### iteration n
    print(variablereacs)
    while (delta > tol):
        model.MinDiffFromFlux(flux_id, variablereacs_id, it, cleanup=False)
        model.SetObjAsConstraint(name='FluxDiff'+str(it)+'_mindifffromflux')
        fva = model.FVA(reaclist=variablereacs.keys(), tol=0,
                            PrintStatus=False, cobra=cobra)
        meanflux = fva.GetReacsMeanFlux(fva.keys())
        flux.update(meanflux)
        variablereacs = fva.Variable(tol)
        delta = fva.MaxDiff()
        if Print:
            print("Iteration "+str(it)+", "+str(len(variablereacs))+" varible reactions, Max difference = "+str(delta))
        it += 1
    ### cleanup
    model.CleanUpTempVar("_mindifffromflux")
    model.MergeRev()
    model.SetState(state)
    rv = model.GetSol(IncZeroes=True,AsMtx=False,sol=flux)
    return rv
