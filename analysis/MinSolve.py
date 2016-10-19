import random
try:
    import scipy
except ImportError:
    pass
from . import ROOM


def SetValAsConstraint(model, name,objval,objective): # Not require to solve here again
        bounds = (objval,objval)
        model.SetSumReacsConstraint(reacsdic=objective, bounds=bounds,name=name)




def MinFluxSolve(model, PrintStatus=True, PrimObjVal=True,
                 norm="linear", weighting='uniform', ExcReacs=[]):
    """ norm = "linear" | "euclidean"
        weighting = "uniform" | "random" """
    model.Solve(PrintStatus=PrintStatus)
    if model.Optimal():
        state = model.GetState()
        objective = model.GetObjective()
        objval = model.GetObjVal()
        SetValAsConstraint(model,name="MinFlux_Objective", objval=objval,objective=objective)

        if norm == "linear":
            #modify.convert_to_irreversible(model)
            model.SplitRev()
            ExcReacs = model.GetReactionNames(ExcReacs)
            for reaction in model.reactions:
                if not (reaction.id.endswith("_sum_reaction") or
                        reaction.id.endswith("_metbounds") or
                        (reaction.id.split('_reverse')[0] in ExcReacs)):
                    if weighting == 'uniform':
                        reaction.objective_coefficient = 1
                    elif weighting == 'random':
                        reaction.objective_coefficient = random.random()
                    else:
                        #print "wrong weighting"
                        raise NameError(weighting)
            model.SetObjDirec("Min")
            model.Solve(PrintStatus=False)
            #modify.revert_to_reversible(model)
            model.MergeRev(True)
        elif norm == "euclidean":
            num_reacs = len(model.reactions)
            model.quadratic_component = scipy.sparse.identity(
                                                    num_reacs).todok()
            model.SetObjDirec("Min")
            model.Solve(PrintStatus=False)
        model.DelObjAsConstraint("MinFlux_Objective")
        model.SetState(state, IncSol=False)
        if PrimObjVal:
            model.solution.f = state["solution"].f



def RevSolve(model,objective,objval,Tolerance,DisplayMsg):
    model.DelObjAsConstraint("MinFlux_Objective")    
    bounds = (objval - Tolerance , objval + Tolerance)
    if DisplayMsg:
        print 'Objective value = ',objval
        print "Modified 'MinFlux_Objective' bounds = ",bounds
    model.SetSumReacsConstraint(reacsdic=objective, bounds=bounds,name="MinFlux_Objective")
    model.SetObjDirec("Min")
    model.Solve(PrintStatus=True)

def AdjustedMinFluxSolve(model,PrintStatus=True, PrimObjVal=True, weighting='uniform', ExcReacs=[], SolverName=None, Tolerance = 0,DisplayMsg=False):
    """ weighting = "uniform" | "random"
        Only enters to the adjusted 'ObjVal' mode if solution after SplitRev() == infeasible"""
    model.Solve(PrintStatus=PrintStatus)

    if model.Optimal():
        state = model.GetState()
        objective = model.GetObjective()
        objval = model.GetObjVal()
        SetValAsConstraint(model,name="MinFlux_Objective",objval=objval,objective=objective)
        model.SplitRev()
        ExcReacs = model.GetReactionNames(ExcReacs)
        for reaction in model.reactions:
            if not (reaction.id.endswith("_sum_reaction") or  reaction.id.endswith("_metbounds") or (reaction.id.split('_reverse')[0] in ExcReacs)):
                if weighting == 'uniform':
                    reaction.objective_coefficient = 1
                elif weighting == 'random':
                        reaction.objective_coefficient = random.random()
                else:
                    raise NameError(weighting)
                    
        model.SetObjDirec("Min")
        if SolverName!=None:
            model.solver = SolverName
            
        model.Solve(PrintStatus=False)
            
        while (model.GetStatusMsg()=='infeasible' or Tolerance >= 1e-5):
            Tolerance = Tolerance + 1e-9
            RevSolve(model,objective=objective,objval=objval,Tolerance=Tolerance,DisplayMsg=DisplayMsg)
                
        model.MergeRev(True)

        model.DelObjAsConstraint("MinFlux_Objective")
        model.SetState(state, IncSol=False)
        if PrimObjVal:
            model.solution.f = state["solution"].f


def MinReactionsSolve(model, PrintStatus=True, PrimObjVal=True, ExcReacs=[]):
    model.Solve(PrintStatus=PrintStatus)
    if model.Optimal():
        state = model.GetState()
        model.SetObjAsConstraint("MinReacs_Objective")
        ROOM.ROOM(model, {}, reset_state=False)
        model.DelObjAsConstraint("MinReacs_Objective")
        model.SetState(state, IncSol=False)
        if PrimObjVal:
            model.solution.f = state["solution"].f
