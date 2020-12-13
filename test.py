import scobra

m = scobra.Model('EDIT')

concDict = {
    'A': 2,
    'B': 2,
    'C': 3,
    'D': 2,
    'E': 1,
    'F': 2,
    'G': 1
}

k = 1

m.AddReaction('R1', {'A': -1, 'B': -1, 'C': -1, 'D': 1})
m.AddReaction('R2', {'B': -1, 'C': -3, 'E': 1}, True)
m.AddReaction('R3', {'E': -1, 'F': 1})
m.AddReaction('R4', {'G': -1, 'F': 1})

""" 
Objective 1: Create a function that adds export/import reactions into the model:
Use model.AddExchangeReactions(metList = {}). The default value for metList is ALL
metabolites
"""

print("---- Given these reactions: ----")
m.PrintReactions()

print()
print("---- These concentrations are calculated: ----")
print("---- using m.calConc(concDict, k) ----")
print(m.CalConstr(concDict, k))

print()
print("---- using m.calConc(concDict, k, split_reversal = True) ----")
print(m.CalConstr(concDict, k, True))
