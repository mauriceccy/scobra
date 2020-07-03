import math
import numpy
import types
import multiprocessing
from ..classes.fva import fva
from .MinSolve import SetLinearMinFluxObjective
from cobra import Reaction
from cobra.flux_analysis import variability

def FVA(model, reaclist=None, subopt=1.0, IncZeroes=True, VaryOnly=False,
        AsMtx=False, tol=1e-10, PrintStatus=False, cobra=True, processes=None,
        loopless=False, pfba_factor=None, reset_state=True):
    if reset_state:
        state = model.GetState()
#    import time
#    print 'before fva solve ' + time.asctime(time.localtime(time.time()))
    model.Solve(PrintStatus=PrintStatus)
#    print 'after fva solve ' + time.asctime(time.localtime(time.time()))
    if model.solution.status != 'optimal' or math.isnan(model.solution.objective_value):
        statusmsg = model.solution.status
        model.SetState(state)
        raise ValueError("no optimal solution, problem " + statusmsg)
    else:
        if reaclist == None:
            reaclist = model.reactions
        elif isinstance(reaclist,str) or isinstance(reaclist, Reaction):
            reaclist = [reaclist]
        if cobra:
#            print 'before cobra fva ' + time.asctime(time.localtime(time.time()))
            reaclist = model.GetReactions(reaclist)
            fvadict = variability.flux_variability_analysis(model=model, 
                reaction_list=reaclist, fraction_of_optimum=subopt,
                loopless=loopless, pfba_factor=pfba_factor)
                #solver=model.solver, objective_sense=model.objective_direction)
#            print 'after cobra fva ' + time.asctime(time.localtime(time.time()))
            rv = fva({}, bounds=model.bounds)
#            for reac in fvadict:
#                lo = fvadict[reac]["minimum"] if abs(
#                        fvadict[reac]["minimum"]) > tol else 0.0
#                hi = fvadict[reac]["maximum"] if abs(
#                        fvadict[reac]["maximum"]) > tol else 0.0
#                rv[reac] = (lo,hi)
            for row in fvadict.iterrows():
                lo = row[1][0] if abs(row[1][0]) > tol else 0.0
                hi = row[1][1] if abs(row[1][1]) > tol else 0.0
                rv[model.GetReactionName(row[0])] = (lo,hi)
#                rv[model.GetReaction(row[0])] = (lo,hi)
        else:
#            print 'not cobra fva'
            model.DelSumReacsConstraint("FVA_objective")
            model.SetObjAsConstraint(name="FVA_objective", subopt=subopt)
            rv = fva({}, bounds=model.bounds)
            pool = multiprocessing.Pool(processes=processes)
            results = [pool.apply_async(FluxRange, args=(model, reac, tol,
                        False, True)) for reac in reaclist]
            pool.close()
            pool.join()
            for x in results:
                rv[model.GetReactionName(x.get().keys()[0])] = x.get().values()[0]
            if "FVA_objective_sum_reaction" in rv:
                rv.pop("FVA_objective_sum_reaction")
#            for reac in reaclist:
#                rv[str(reac)] = pool.apply_async(FluxRange, args=(model, reac, tol,
#                                                                False))
#            for reac in reaclist:
#                lo,hi = model.FluxRange(reac,tol=tol,reset_state=False)
#                if IncZeroes or abs(lo) > tol or abs(hi) > 0.0:
#                    rv[str(reac)] = (lo,hi)
            model.DelSumReacsConstraint("FVA_objective")
        if VaryOnly:
            rv = rv.Variable()
        if AsMtx:
            rv = rv.AsMtx()
#        print 'before fva set state ' + time.asctime(time.localtime(time.time()))
        if reset_state:
            model.SetState(state)
#        print 'after fva set state ' + time.asctime(time.localtime(time.time()))
        return rv


def MinFluxFVA(model, reaclist=None, subopt=1.0, IncZeroes=True, VaryOnly=False, 
                AsMtx=False, tol=1e-10, PrintStatus=False, cobra=True, 
                processes=None, weighting='uniform', ExcReacs=[],
                loopless=False, pfba_factor=1.0, reset_state=True):
    if reset_state:
        state = model.GetState()
    if (cobra) and (not ExcReacs) and (weighting == 'uniform'):
#        import time
#        print 'before cobra min flux fva ' + time.asctime(time.localtime(time.time()))
        rv = FVA(model, reaclist=reaclist, subopt=subopt, IncZeroes=IncZeroes, 
                VaryOnly=VaryOnly, AsMtx=AsMtx, tol=tol, 
                PrintStatus=PrintStatus, cobra=cobra, processes=processes,
                loopless=loopless, pfba_factor=pfba_factor, reset_state=False)
#        print 'after cobra min flux fva' + time.asctime(time.localtime(time.time()))
    else:
#        print 'not cobra min flux fva'
        model.SetObjAsConstraint('Primary_Objective_Constraint', subopt=subopt)
        model.SplitRev()
        SetLinearMinFluxObjective(model, weighting=weighting, ExcReacs=ExcReacs)

        if reaclist:
            tmp_reaclist = []
            for reac in reaclist:
                tmp_reaclist.append(model.GetReaction(reac))
            for reac in list(tmp_reaclist):
                if "reflection" in reac.notes:
                    if reac.reflection not in reaclist:
                        tmp_reaclist.append(reac.reflection)
            reaclist = model.GetReactionNames(tmp_reaclist)
        if not pfba_factor:
            pfba_factor = 1.0
        split_fva = FVA(model, reaclist=reaclist, subopt=pfba_factor, IncZeroes=IncZeroes, 
                    VaryOnly=VaryOnly, AsMtx=AsMtx, tol=tol, 
                    PrintStatus=PrintStatus, cobra=cobra, processes=processes)

        reverse_reactions = [x for x in model.reactions
                             if "reflection" in x.notes and
                             x.id.endswith('_reverse')]
        # If there are no reverse reactions, then there is nothing to do
        if not split_fva:
            model.MergeRev()
            model.DelObjAsConstraint('Primary_Objective_Constraint')
            model.SetState(state)
            return split_fva

        rv = fva(split_fva)
        for reac in rv.keys():
            cobra_reac = model.GetReaction(reac)
            if cobra_reac in reverse_reactions:
                reverse = cobra_reac
                forward = reverse.reflection
                lo_for, hi_for = rv[forward.id]
                lo_rev, hi_rev = rv[reverse.id]
                if ((lo_for > tol) and (hi_rev > tol)) or ((lo_rev > tol) and (hi_for > tol)):
                    raise ValueError(forward.id + " problem with FVA merging")
                if hi_rev < tol:
                    new_range = (lo_for, hi_for)
                elif hi_for <tol:
                    new_range = (-hi_rev, -lo_rev)
                else:
                    new_range = (-hi_rev, hi_for)
                rv[forward.id] = new_range
                rv.pop(reverse.id)
        model.MergeRev()
        model.DelObjAsConstraint('Primary_Objective_Constraint')
    for reac in rv.keys():
        if reac.endswith("_sum_reaction") or reac.endswith("_metbounds"):
            rv.pop(reac)
#    print 'before min flux fva set state ' + time.asctime(time.localtime(time.time()))
    if reset_state:
        model.SetState(state)
#    print 'after min flux fva set state ' + time.asctime(time.localtime(time.time()))
    return rv

def AllFluxRange(model, tol=1e-10, processes=None, reset_state=True):
    rangedict = fva({}, bounds=model.bounds)
    if reset_state:
        state = model.GetState()
    model.Solve(PrintStatus=False)
    if model.Optimal():
        pool = multiprocessing.Pool(processes=processes)
        results = [pool.apply_async(FluxRange, args=(model, reac.id, tol,
                        False, True)) for reac in model.reactions]
        pool.close()
        pool.join()
        for x in results:
            #print(type(x.get()))
            rangedict[list(x.get().keys())[0]] = list(x.get().values())[0]
#        for reac in model.reactions:
#            rangedict[reac.id] = pool.apply(FluxRange, args=(model, reac.id,
#                                                            tol, False))
#            rangedict[reac.id] = model.FluxRange(obj=reac.id, tol=tol,
#                                                reset_state=False)
    if reset_state:
        model.SetState(state)
    return rangedict

def FluxRange(model, obj, tol=1e-10, reset_state=True, return_reac=False):
    """ post: changes objective if resetobj = False!!! """
    if reset_state:
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
        if math.isnan(model.solution.objective_value):
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
        if math.isnan(model.solution.objective_value):
            hi = model.float("inf")
        else:
            hi = model.GetObjVal()
    if abs(lo) < tol:
        lo = 0.0
    if abs(hi) < tol:
        hi = 0.0
    if reset_state:
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
    print ("total variability:", var)
    print ("number of variable reactions before optimisation:", varyreac)
    print ("averge variability:", avgvar)
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
