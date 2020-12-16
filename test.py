import scobra


""" 
Objective 1: Create a function that adds export/import reactions into the model:
Use model.AddExchangeReactions(metList = {}). The default value for metList is ALL
metabolites

m = scobra.Model('EDIT')
m.AddReaction('R1', {'A': -1, 'B': -1, 'C': -1, 'D': 1})
m.AddReaction('R2', {'B': -1, 'C': -3, 'E': 1}, True)
m.AddReaction('R3', {'E': -1, 'F': 1})
m.AddReaction('R4', {'G': -1, 'F': 1})
m.AddExchangeReactions()
m.SplitRev(split_solution=False)
m.PrintReactions()
"""
"""
Objective 2: Create a function that calculates the constraints based on a concentration
dictionary. Use model.CalConstr(concDict, k, split_reversal) The default value for k = 1
and split_reversal is False
"""

m2 = scobra.Model('EDIT')
m2.AddReaction('R1', {'A': -1, 'B': -1, 'C': -1, 'D': 1})
m2.AddReaction('R2', {'B': -1, 'C': -3, 'E': 1}, True)
m2.AddReaction('R3', {'E': -1, 'F': 1})
m2.AddReaction('R4', {'G': -1, 'F': 1})

concDict = {
    'A': (0, 2),
    'B': (1, 2),
    'C': (0, 3),
    'D': (0, 2),
    'E': 1,
    'F': (0, 2),
    'G': (0, 1)
}

rateDict = {'R1': (3, "conc * coef"),
            'R2': (2, "conc * (2 * coef)"),
            'R3': (1, "conc ** coef"),
            'R4': (2, "conc * (2 ** coef)")
            }

m2.AddRateEquations(rateDict)
print(m2.CalConstr(concDict))

# Objective 2': (2.Tues) Change name to _exchange
# Objective 2'': (2.Tues) Debug func in CalConstr
# Objective 3: (2.Wed) User can put in a function a. definning a function for each reaction (reaction.rate_equation, reaction.rate_constant)
# Objective 3': For reversible reactions w/ only one k -> assume the the k is the same (same rate_constant used for reverse reaction)
# Objective 4: Export (and Import) -> new column in excel sheet "rate_equation" (either user equation)
# Objective 5: (2.Wed) PrintReactionEquations
# Objective 6: (2.Wed) For exchange reactions, don't set constraints -> model.bounds

"""
m3 = scobra.Model('EDIT')
m3.AddReaction('R1', {'A': -1, 'B': -1, 'C': -1, 'D': 1})
m3.AddReaction('R2', {'B': -1, 'C': -3, 'E': 1}, True)
m3.AddReaction('R3', {'E': -1, 'F': 1})
m3.AddReaction('R4', {'G': -1, 'F': 1})

rateDict = {'R1': (3, "conc * coef"),
            'R2': (2, "conc * (2 * coef)"),
            'R3': (1, "conc ** coef"),
            'R4': (2, "conc * (2 ** coef)")
            }

m3.AddRateEquations(rateDict)
m3.AddExchangeReactions()
m3.PrintRateEquations()


conc = 3
coef = 4
print(eval("conc * coef"))

"""
