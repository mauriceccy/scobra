import random
try:
    import scipy
except ImportError:
    pass
from . import ROOM

def MinFluxSolve(model, PrintStatus=True, PrimObjVal=True,
                 norm="linear", weighting='uniform', ExcReacs=[]):
    """ norm = "linear" | "euclidean"
        weighting = "uniform" | "random" """
    model.Solve(PrintStatus=PrintStatus)
    if model.Optimal():
        state = model.GetState()
        model.SetObjAsConstraint("MinFlux_Objective")
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
