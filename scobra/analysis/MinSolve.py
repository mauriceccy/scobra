import random
from cobra import Solution
try:
    import scipy
except ImportError:
    pass
from . import ROOM
from cobra.exceptions import Infeasible
#from cobra.manipulation import modify
from cobra.exceptions import Infeasible
from ..manipulation import Reversible
from cobra.flux_analysis.parsimonious import pfba

#def SetValAsConstraint(model, name,objval,objective): # Not require to solve here again
#        bounds = (objval,objval)
#        model.SetSumReacsConstraint(reacsdic=objective, bounds=bounds,name=name)


def SetLinearMinFluxObjective(model, weighting='uniform', ExcReacs=[]):
    """ assume reversible reactions are split """
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
    

def MinFluxSolve(model, PrintStatus=True, PrimObjVal=True, norm="linear", 
                weighting='uniform', ExcReacs=[], adjusted=False, tol_step=1e-9,
                max_tol=1e-8, DisplayMsg=True, cobra=True, subopt=1.0):
    """ norm = "linear" | "euclidean"
        weighting = "uniform" | "random" """
    
#    """Temporary fix, need to change the structure of saving solution objects"""
    if norm == "linear" and weighting=="uniform" and (not ExcReacs) and (not adjusted) and cobra:
#            """Temporary fix, need to change the structure of saving solution objects"""
#            from cobra.flux_analysis.parsimonious import pfba
        sol=None
        try:
            sol = pfba(model, fraction_of_optimum=subopt)
        except Infeasible:
            if DisplayMsg:
                print("no solution")
            model.UpdateSolution(None)
            return
        model.UpdateSolution(sol)
        if DisplayMsg:
            try: 
                print(sol.status)
            except AttributeError: 
                print("no solution")

        return
#            return sol.fluxes
#
#    RemoveReverse(model)
    model.Solve(PrintStatus=PrintStatus)
    if model.Optimal():
        state = model.GetState()
        objective = model.GetObjective()
        objval = model.GetObjVal()
        objbounds = (objval - abs(1-subopt)*objval, objval + abs(1-subopt)*objval)
        #SetValAsConstraint(model,name="MinFlux_Objective", objval=objval,objective=objective)
        #model.SetSumReacsConstraint(reacsdic=objective, bounds=objval,name="MinFlux_Objective")
        model.SetSumReacsConstraint(reacsdic=objective, bounds=objbounds,name="MinFlux_Objective")
        if norm == "linear":
            #modify.convert_to_irreversible(model)
            model.SplitRev()
            SetLinearMinFluxObjective(model=model, weighting=weighting, ExcReacs=ExcReacs)
#            ExcReacs = model.GetReactionNames(ExcReacs)
#            for reaction in model.reactions:
#                if not (reaction.id.endswith("_sum_reaction") or
#                        reaction.id.endswith("_metbounds") or
#                        (reaction.id.split('_reverse')[0] in ExcReacs)):
#                    if weighting == 'uniform':
#                        reaction.objective_coefficient = 1
#                    elif weighting == 'random':
#                        reaction.objective_coefficient = random.random()
#                    else:
#                        #print "wrong weighting"
#                        raise NameError(weighting)
           
            model.SetObjDirec("Min")
            model.Solve(PrintStatus=DisplayMsg)
            
            if adjusted:
                Tolerance = 0
                while (model.Optimal()==False and Tolerance < max_tol):
                    Tolerance = Tolerance + tol_step
                    model.DelObjAsConstraint("MinFlux_Objective")
                    bounds = (objval-Tolerance, objval+Tolerance)
                    if DisplayMsg:
                        print('Objective value = ' + str(objval))
                        print("Modified 'MinFlux_Objective' bounds = " + str(bounds))
                    model.SetSumReacsConstraint(reacsdic=objective, bounds=bounds, name="MinFlux_Objective")
                    model.SetObjDirec("Min")
                    model.Solve(PrintStatus=DisplayMsg)
            #modify.revert_to_reversible(model)
            model.MergeRev(True)
            #print(model.GetConstraints())

        if norm == "euclidean":
            num_reacs = len(model.reactions)
            model.quadratic_component = scipy.sparse.identity(num_reacs).todok()
            model.SetObjDirec("Min")
            model.Solve(PrintStatus=DisplayMsg)

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


#def RevSolve(model,objective,objval,Tolerance,DisplayMsg=False):
#    #RemoveReverse(model)
#    model.DelObjAsConstraint("MinFlux_Objective")    
#    bounds = (objval - Tolerance , objval + Tolerance)
#    if DisplayMsg:
#        print 'Objective value = ',objval
#        print "Modified 'MinFlux_Objective' bounds = ",bounds
#    model.SetSumReacsConstraint(reacsdic=objective, bounds=bounds,name="MinFlux_Objective")
#    model.SetObjDirec("Min")
#    model.Solve(PrintStatus=True)

#def AdjustedMinFluxSolve(model,PrintStatus=True, PrimObjVal=True, weighting='uniform', ExcReacs=[], Tolerance=0, DisplayMsg=False):
##SolverName=None
#    """ weighting = "uniform" | "random"
#        Only enters to the adjusted 'ObjVal' mode if solution after SplitRev() == infeasible"""
#    #RemoveReverse(model)
#    model.Solve(PrintStatus=PrintStatus)
#
#    if model.Optimal():
#        state = model.GetState()
#        objective = model.GetObjective()
#        objval = model.GetObjVal()
#        model.SetSumReacsConstraint(reacsdic=objective, bounds=objval,name="MinFlux_Objective")
#        #SetValAsConstraint(model,name="MinFlux_Objective",objval=objval,objective=objective)
#        #modify.convert_to_irreversible(model)
#        model.SplitRev()
#        ExcReacs = model.GetReactionNames(ExcReacs)
#        for reaction in model.reactions:
#            if not (reaction.id.endswith("_sum_reaction") or  reaction.id.endswith("_metbounds") or (reaction.id.split('_reverse')[0] in ExcReacs)):
#                if weighting == 'uniform':
#                    reaction.objective_coefficient = 1
#                elif weighting == 'random':
#                        reaction.objective_coefficient = random.random()
#                else:
#                    raise NameError(weighting)
#                    
#        model.SetObjDirec("Min")
##        if SolverName!=None:
##            model.solver = SolverName
#            
#        model.Solve(PrintStatus=False)
#            
#        while (model.GetStatusMsg()=='infeasible' or Tolerance >= 1e-5):
#            Tolerance = Tolerance + 1e-9
#            RevSolve(model,objective=objective,objval=objval,Tolerance=Tolerance,DisplayMsg=DisplayMsg)
#                
#        model.MergeRev(True)
#
#        model.DelObjAsConstraint("MinFlux_Objective")
#        model.SetState(state, IncSol=False)
#        if PrimObjVal:
#            try:
#            	model.solution.objective_value = state["solution"].objective_value
#            except AttributeError: 
#            	pass

def MinReactionsSolve(model, PrintStatus=True, PrimObjVal=True, ExcReacs=[]):
    #RemoveReverse(model)
    model.Solve(PrintStatus=PrintStatus)
    if model.Optimal():
        state = model.GetState()
        model.SetObjAsConstraint("MinReacs_Objective")
        ROOM.ROOM(model, {}, reset_state=False)
        model.DelObjAsConstraint("MinReacs_Objective")
        model.SetState(state, IncSol=False)
        if PrimObjVal:
            try:
                model.solution.objective_value = state["solution"].ibjective_value
            except AttributeError: 
                pass

#def RemoveReverse(model): 
#    reverse_reactions = [x for x in model.reactions
#                         if x.id.endswith('_reverse')]
#    model.remove_reactions(reverse_reactions)
#    return 
