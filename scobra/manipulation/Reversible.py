from cobra import Reaction
#from cobra.manipulation import modify
from cobra.core.solution import Solution
from pandas import Series
from six import iteritems

def SplitRev(model, split_solution=True):
    #modify.convert_to_irreversible(model)
    reactions_to_add = []
    coefficients = {}
    for reaction in model.reactions:
        # If a reaction is reverse only, the forward reaction (which
        # will be constrained to 0) will be left in the model.
        if reaction.lower_bound < 0:
            reverse_reaction = Reaction(reaction.id + "_reverse")
            reverse_reaction.lower_bound = min(0, reaction.upper_bound) * -1
            reverse_reaction.upper_bound = reaction.lower_bound * -1
            coefficients[reverse_reaction] = reaction.objective_coefficient * -1
            reaction.lower_bound = 0
            reaction.upper_bound = max(0, reaction.upper_bound)
            #Make the directions aware of each other
            reaction.reflection = reverse_reaction
            reverse_reaction.reflection = reaction
            reaction.notes["reflection"] = reverse_reaction.id
            reverse_reaction.notes["reflection"] = reaction.id
            reaction_dict = {k: v * -1
                             for k, v in iteritems(reaction._metabolites)}
            reverse_reaction.add_metabolites(reaction_dict)
            reverse_reaction._model = reaction._model
            reverse_reaction._genes = reaction._genes
            for gene in reaction._genes:
                gene._reaction.add(reverse_reaction)
            reverse_reaction._gene_reaction_rule = reaction._gene_reaction_rule
            reverse_reaction.subsystem = reaction.subsystem
            reactions_to_add.append(reverse_reaction)
    model.add_reactions(reactions_to_add)
    model.SetObjective(coefficients)
    
    if split_solution:
        reverse_reactions = [x for x in model.reactions
                         if "reflection" in x.notes and
                         x.id.endswith('_reverse')]
        if isinstance(model.solution, Solution):
            fluxes = dict(model.solution.fluxes)
            reduced = dict(model.solution.reduced_costs)
            for reverse in reverse_reactions:
                forward = reverse.reflection
                if (forward.id in fluxes) and (reverse.id in fluxes):
                    if fluxes[forward.id] < 0:
                        fluxes[reverse.id] = -fluxes[forward.id]
                        fluxes[forward.id] = 0
                    else:
                        fluxes[reverse.id] = 0
                    if reduced[forward.id] < 0:
                        reduced[reverse.id] = -reduced[forward.id]
                        reduced[forward.id] = 0
                    else:
                        reduced[reverse.id] = 0
#                else:
#                    print(forward.id + ' and ' + reverse.id + ' not in solution')
            split_sol = Solution(model.solution.objective_value, model.solution.status,
                Series(index=fluxes.keys(), data=fluxes.values(), 
                name="fluxes"),
                Series(index=reduced.keys(), data=reduced.values(),
                name="reduced_costs"), model.solution.shadow_prices)
            model.UpdateSolution(split_sol)


def MergeRev(model, update_solution=True):
    ###modify.revert_to_reversible(model, update_solution=update_solution)

    """
        The cobra function above fails to update the solution object when merging. 
        This results in how reactions that goes in the reversible direction to be missing from solution. 
        Fix is made by commenting the remove_reactions function and, instead, changing the solution dict 
        manually in GetSol.
    """

    ### Copied cobra code here

    reverse_reactions = [x for x in model.reactions
                         if "reflection" in x.notes and
                         x.id.endswith('_reverse')]
    # If there are no reverse reactions, then there is nothing to do
    if len(reverse_reactions) == 0:
        return

    if update_solution:
        if isinstance(model.solution, Solution):
            fluxes = dict(model.solution.fluxes)
            reduced = dict(model.solution.reduced_costs)
            for reverse in reverse_reactions:
                forward = reverse.reflection
                if reverse.id in fluxes.keys():
                    fluxes[forward.id] -= fluxes.pop(reverse.id)
                    reduced[forward.id] -= reduced.pop(reverse.id)
            merged_sol = Solution(model.solution.objective_value, model.solution.status,
                            Series(index=fluxes.keys(), data=fluxes.values(), 
                            name="fluxes"),
                            Series(index=reduced.keys(), data=reduced.values(),
                            name="reduced_costs"), model.solution.shadow_prices)
            model.UpdateSolution(merged_sol)

    for reverse in reverse_reactions:
        forward_id = reverse.notes.pop("reflection")
        forward = model.reactions.get_by_id(forward_id)
        forward.lower_bound = -reverse.upper_bound
        if forward.upper_bound == 0:
            forward.upper_bound = -reverse.lower_bound

        if "reflection" in forward.notes:
            forward.notes.pop("reflection")
            
    model.remove_reactions(reverse_reactions)
    
    ###

    # Since the metabolites and genes are all still in
    # use we can do this faster removal step.  We can
    # probably speed things up here.
    #"""
    #This is commented out -> model.remove_reactions(reverse_reactions)
    #"""
    # reverse_reactions = [x for x in model.reactions
    #     if x.reflection is not None and x.id.endswith('_reverse')]
    # for reverse in reverse_reactions:
    #     forward = reverse.reflection
    #     forward.lower_bound = -reverse.upper_bound
    #     if reverse.lower_bound < 0:
    #         forward.upper_bound = -reverse.lower_bound
    #     forward.reflection = None
    # #Since the metabolites and genes are all still in
    # #use we can do this faster removal step.  We can
    # #probably speed things up here.
    # model.remove_reactions(reverse_reactions)
    # # fix the solution
    # if (update_solution) and (model.solution is not None) and (model.solution.x_dict is not None):
    #     x_dict = model.solution.x_dict
    #     for reverse in reverse_reactions:
    #         forward = reverse.reflection
    #         x_dict[forward.id] -= x_dict.pop(reverse.id)
    #     model.solution.x = [x_dict[r.id] for r in model.reactions]

#def MergeSolution(sol): 
#    """
#    This function takes in a Solution object that is unmerged (contains reactions both in the forward and #reverse direction)
#    and combines them to a single reaction.
#    """
#    old_fluxes = dict(sol_object.fluxes)
#    old_reduced = dict(sol_object.reduced_costs)
#    
#    new_fluxes = {}
#    new_reduced = {}
#
#    for reac in old_fluxes.keys(): 
#        if reac.endswith('_reverse'):
#            forward_id = reac[:-len('_reverse')] 
#            if old_fluxes[reac] == 0:
#                new_fluxes[forward_id] = old_fluxes[forward_id]
#            else: 
#                new_fluxes[forward_id] = - old_fluxes[reac]
#        else:
#            new_fluxes[reac] = old_fluxes[reac]
#    for reac in old_reduced.keys(): 
#        if reac.endswith('_reverse'): 
#            forward_id = reac[:-len('_reverse')]  
#            if old_reduced[reac] == 0:
#                new_reduced[forward_id] = old_reduced[forward_id]
#            else: 
#                new_reduced[forward_id] = - old_reduced[reac]
#        else:
#            new_reduced[reac] = old_reduced[reac]
#
#    return Solution(sol_object.objective_value, sol_object.status,
#                    Series(index=new_fluxes.keys(), data=new_fluxes.values(), name="fluxes"),
#                    Series(index=new_reduced.keys(), data=new_reduced.values(),
#                    name="reduced_costs"), sol_object.shadow_prices)
