import math
import numpy
import types
import multiprocessing
from ..classes.fva import fva
from cobra import Reaction
from cobra.flux_analysis import variability

def FVA(model, reaclist=None, subopt=1.0, IncZeroes=True, VaryOnly=False,
        AsMtx=False, tol=1e-10, PrintStatus=False, cobra=False, processes=None):
    state = model.GetState()
    model.Solve(PrintStatus=PrintStatus)
    if model.solution.status != 'optimal' or math.isnan(model.solution.f):
        statusmsg = model.solution.status
        model.SetState(state)
        print "no optimal solution, problem "+statusmsg
    else:
        if reaclist == None:
            reaclist = model.Reactions()
        elif (type(reaclist) in types.StringTypes) or isinstance(
                                                reaclist, Reaction):
            reaclist = [reaclist]
        if not cobra:
            model.DelSumReacsConstraint("FVA_objective")
            model.SetObjAsConstraint(name="FVA_objective", subopt=subopt)
            rv = fva(bounds=model.bounds)
            pool = multiprocessing.Pool(processes=processes)
            results = [pool.apply_async(FluxRange, args=(model, reac, tol,
                        False, True)) for reac in reaclist]
            pool.close()
            pool.join()
            for x in results:
                rv[x.get().keys()[0]] = x.get().values()[0]
#            for reac in reaclist:
#                rv[str(reac)] = pool.apply_async(FluxRange, args=(model, reac, tol,
#                                                                False))
#            for reac in reaclist:
#                lo,hi = model.FluxRange(reac,tol=tol,resetstate=False)
#                if IncZeroes or abs(lo) > tol or abs(hi) > 0.0:
#                    rv[str(reac)] = (lo,hi)
            model.DelSumReacsConstraint("FVA_objective")
        else:
            fvadict = variability.flux_variability_analysis(
                cobra_model=model, reaction_list=reaclist,
                fraction_of_optimum=subopt, solver=model.solver,
                objective_sense=model.objective_direction)
            rv = fva(bounds=model.bounds)
            for reac in fvadict:
                lo = fvadict[reac]["minimum"] if abs(
                        fvadict[reac]["minimum"]) > tol else 0.0
                hi = fvadict[reac]["maximum"] if abs(
                        fvadict[reac]["maximum"]) > tol else 0.0
                rv[reac] = (lo,hi)
        if VaryOnly:
            rv = rv.Variable()
        if AsMtx:
            rv = rv.AsMtx()
        model.SetState(state)
        return rv

def AllFluxRange(model, tol=1e-10, processes=None):
    rangedict = fva(bounds=model.bounds)
    state = model.GetState()
    model.Solve(PrintStatus=False)
    if model.Optimal():
        pool = multiprocessing.Pool(processes=processes)
        results = [pool.apply_async(FluxRange, args=(model, reac.id, tol,
                        False, True)) for reac in model.reactions]
        pool.close()
        pool.join()
        for x in results:
            rangedict[x.get().keys()[0]] = x.get().values()[0]
#        for reac in model.reactions:
#            rangedict[reac.id] = pool.apply(FluxRange, args=(model, reac.id,
#                                                            tol, False))
#            rangedict[reac.id] = model.FluxRange(obj=reac.id, tol=tol,
#                                                resetstate=False)
    model.SetState(state)
    return rangedict

def FluxRange(model, obj, tol=1e-10, resetstate=True, return_reac=False):
    """ post: changes objective if resetobj = False!!! """
    if resetstate:
        state = model.GetState()
    model.ZeroObjective()
    model.SetObjective(obj)
    model.SetObjDirec("Min")
    model.Solve(PrintStatus=False)
    if model.solution.status != 'optimal':
        if model.solution.status == 'unbound':
            lo = float("-inf")
        else:
            lo = float("NaN")
    else:
        if math.isnan(model.solution.f):
            lo = float("-inf")
        else:
            lo = model.GetObjVal()
    model.SetObjDirec("Max")
    model.Solve(PrintStatus=False)
    if model.solution.status != 'optimal':
        if model.solution.status == 'unbound':
            hi = float("inf")
        else:
            hi = float("NaN")
    else:
        if math.isnan(model.solution.f):
            hi = model.float("inf")
        else:
            hi = model.GetObjVal()
    if abs(lo) < tol:
        lo = 0.0
    if abs(hi) < tol:
        hi = 0.0
    if resetstate:
        model.SetState(state)
    if return_reac:
        return {obj:(lo, hi)}
    else:
        return (lo, hi)

def FluxVariability(model, reffva=None, fva=None, excreacs=[], tol=1e-10,
                    getratio=False):
    if reffva == None:
        reffva = model.AllFluxRange(tol=tol)
    if fva == None:
        fva = model.FVA(tol=tol)
    rv = {}
    var = 0
    varyreac = 0
    for reac in reffva.keys():
        if reac not in excreacs:
            refrange = reffva[reac][1] - reffva[reac][0]
            if refrange > tol and (not numpy.allclose(
                                                refrange,float("inf"))):
                varyreac += 1
                reacrange = fva[reac][1] - fva[reac][0]
                ratio = reacrange/float(refrange)
                var += ratio
                rv[reac] = ratio
    avgvar = var/varyreac
    print "total variability:", var
    print "number of variable reactions before optimisation:", varyreac
    print "averge variability:", avgvar
    if getratio:
        return rv

def InternalCycles(model, allowedreacs=None, reacsbounds={}, tol=1e-10):
    """ pre: reacsbounds={reac:(lo,hi)}, all external reactions blocked
       post: model with reactions in internal cycles (for doing elementary modes) """
    state = model.GetState()
    model.SetConstraints(reacsbounds)
    if allowedreacs == None:
        rd = model.AllFluxRange()
        allowedreacs = rd.Allowed(tol=tol).keys()
    model.SetState(state)
    if len(allowedreacs) > 0:
        armodel = model.SubModel(allowedreacs)
        return armodel
