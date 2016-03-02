import multiprocessing
from ..classes.matrix import matrix

def RandomMinFlux(model,it=1,reacs=None,exc=[],processes=None):
    state = model.GetState()
    if reacs == None:
        reacs = model.Reactions()
    else:
        reacs = model.GetReactionNames(reacs)
    for reac in exc:
        reac = model.GetReactionName(exc)
        if reac in reacs:
            reacs.remove(reac)
    mtx = matrix()
    pool = multiprocessing.Pool(processes=processes)
    results = [pool.apply_async(RWFMSolveMinFlux, args=(model,)) for x in range(it)]
    pool.close()
    pool.join()
    sols = [x.get() for x in results]
    for sol in sols:
        mtx = mtx.UpdateFromDic(sol)
    model.SetState(state)
    return mtx

def RWFMSolveMinFlux(model):
    model.ZeroObjective()
    model.MinFluxSolve(PrintStatus=False,weighting='random')
    sol = model.GetSol(IncZeroes=True)
    return sol
