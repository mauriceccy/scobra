import multiprocessing
import sys 
from ..classes.matrix import matrix
from .RWFMSolveMinFlux import RWFMSolveMinFlux #had to put function in diff .py because windows glitch
import time #added time for speed record

def RandomMinFlux(model,it=1,reacs=None,exc=[],processes=None):
    start=time.time()
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
    stop=time.time()
    end_time= stop-start
    
    print("Processing {} took {} seconds".format((model),end_time))
    return mtx