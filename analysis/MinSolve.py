import random
try:
    import scipy
except ImportError:
    pass
from . import ROOM
from cobra.manipulation import modify
from ..manipulation import Reversible

#def SetValAsConstraint(model, name,objval,objective): # Not require to solve here again
#        bounds = (objval,objval)
#        model.SetSumReacsConstraint(reacsdic=objective, bounds=bounds,name=name)




def MinFluxSolve(model, PrintStatus=True, PrimObjVal=True,
                 norm="linear", weighting='uniform', ExcReacs=[]):
    """ norm = "linear" | "euclidean"
        weighting = "uniform" | "random" """
    
#    """Temporary fix, need to change the structure of saving solution objects"""
#    if norm == "linear":
#            """Temporary fix, need to change the structure of saving solution objects"""
#            from cobra.flux_analysis.parsimonious import pfba
#            sol = pfba(model)
#            return sol.fluxes
#
#    RemoveReverse(model)
    model.Solve(PrintStatus=PrintStatus)
    if model.Optimal():
        state = model.GetState()
        objective = model.GetObjective()
        objval = model.GetObjVal()
        #SetValAsConstraint(model,name="MinFlux_Objective", objval=objval,objective=objective)
        model.SetSumReacsConstraint(reacsdic=objective, bounds=objval,name="MinFlux_Objective")


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
	        #print(model.GetConstraints())

        if norm == "euclidean":
	        num_reacs = len(model.reactions)
	        model.quadratic_component = scipy.sparse.identity(
	                                                num_reacs).todok()
	        model.SetObjDirec("Min")
	        model.Solve(PrintStatus=False)

#"""This whole section used to be run after, either linear or euclidean norms, but tabbed to accomodate temporary change described above"""

        model.DelObjAsConstraint("MinFlux_Objective")
        model.SetState(state, IncSol=False)
        if PrimObjVal:
            try: 
                model.solution.objective_value = state["solution"].objective_value
            except AttributeError: 
            	pass
        #return model.GetSol()
    else:
        print("not feasible")
        #return model.GetSol()


def RevSolve(model,objective,objval,Tolerance,DisplayMsg):
    RemoveReverse(model)
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
    RemoveReverse(model)
    model.Solve(PrintStatus=PrintStatus)

    if model.Optimal():
        state = model.GetState()
        objective = model.GetObjective()
        objval = model.GetObjVal()
        SetValAsConstraint(model,name="MinFlux_Objective",objval=objval,objective=objective)
        modify.convert_to_irreversible(model)
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
            try:
            	model.solution.f = state["solution"].f
            except AttributeError: 
            	pass

def MinReactionsSolve(model, PrintStatus=True, PrimObjVal=True, ExcReacs=[]):
    RemoveReverse(model)
    model.Solve(PrintStatus=PrintStatus)
    if model.Optimal():
        state = model.GetState()
        model.SetObjAsConstraint("MinReacs_Objective")
        ROOM.ROOM(model, {}, reset_state=False)
        model.DelObjAsConstraint("MinReacs_Objective")
        model.SetState(state, IncSol=False)
        if PrimObjVal:
            try:
            	model.solution.f = state["solution"].f
            except AttributeError: 
            	pass

def RemoveReverse(model): 
    reverse_reactions = [x for x in model.reactions
                         if x.id.endswith('_reverse')]
    model.remove_reactions(reverse_reactions)
    return 
