#from cobra import Reaction
from cobra.manipulation import modify

def SplitRev(model):
    modify.convert_to_irreversible(model)
    # reactions_to_add = []
    # for reaction in model.reactions:
    #     #Potential bug because a reaction might run backwards naturally
    #     #and this would result in adding an empty reaction to the
    #     #model in addition to the reverse reaction.
    #     if reaction.lower_bound < 0:
    #         reverse_reaction = Reaction(reaction.id + "_reverse")
    #         reverse_reaction.lower_bound = min(0, reaction.upper_bound) * -1
    #         reverse_reaction.upper_bound = reaction.lower_bound * -1
    #         reaction.lower_bound = 0
    #         reaction.upper_bound = max(0, reaction.upper_bound)
    #         #Make the directions aware of each other
    #         reaction.reflection = reverse_reaction
    #         reverse_reaction.reflection = reaction
    #         reaction_dict = dict([(k, v*-1)
    #                               for k, v in reaction._metabolites.items()])
    #         reverse_reaction.add_metabolites(reaction_dict)
    #         reverse_reaction._model = reaction._model
    #         reverse_reaction._genes = reaction._genes
    #         for gene in reaction._genes:
    #             gene._reaction.add(reverse_reaction)
    #         reverse_reaction._gene_reaction_rule = reaction._gene_reaction_rule
    #         reactions_to_add.append(reverse_reaction)
    # model.add_reactions(reactions_to_add)



def MergeRev(model, update_solution=True):
    modify.revert_to_reversible(model, update_solution=update_solution)
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
