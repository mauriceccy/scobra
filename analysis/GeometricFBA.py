

def GeometricSol(model, IncZeroes=True, AsMtx=False, tol=1e-6, Print=False):
    state = model.GetState()
    reacs = list(model.Reactions())
    model.SetObjAsConstraint(name='FluxDiff'+str(0)+'_mindifffromflux')
    ### iteraion 1
    model.SetObjDirec("Min")
    it = 1
    model.ZeroObjective()
    model.SplitRev()
    model.SetObjective(model.Reactions())
    model.Solve(False)
    model.SetObjAsConstraint(name='FluxDiff'+str(it)+'_mindifffromflux')
    fva = model.FVA(reaclist=reacs,tol=tol,PrintStatus=False, cobra=False)
    meanflux = fva.GetReacsMeanFlux(fva.keys())
    flux = dict(meanflux)
    delta = fva.MaxDiff()
    variablereacs = fva.Variable(tol)
    if Print:
        print "Iteration "+str(it)+", "+str(len(variablereacs))+" varible reactions, Max difference = "+str(delta)
    it += 1
    ### iteration n
    while (delta > tol):
        model.MinDiffFromFlux(flux, variablereacs.keys(), it, cleanup=False)
        model.SetObjAsConstraint(name='FluxDiff'+str(it)+'_mindifffromflux')
        fva = model.FVA(reaclist=variablereacs.keys(), tol=0,
                            PrintStatus=False, cobra=False)
        meanflux = fva.GetReacsMeanFlux(fva.keys())
        flux.update(meanflux)
        variablereacs = fva.Variable(tol)
        delta = fva.MaxDiff()
        if Print:
            print "Iteration "+str(it)+", "+str(len(variablereacs))+" varible reactions, Max difference = "+str(delta)
        it += 1
    ### cleanup
    model.CleanUpTempVar("_mindifffromflux")
    model.MergeRev()
    model.SetState(state)
    rv = model.GetSol(IncZeroes=True,AsMtx=False,sol=flux)
    return rv
