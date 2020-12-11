import scobra

m = scobra.Model('EDIT')

m.AddReaction('R4', {'A': -1, 'B': -1, 'C': -1, 'D': 1})
m.AddReaction('R5', {'B': -1, 'C': -3, 'E': 1}, True)
m.AddReaction('R6', {'E': -1, 'F': 1})
m.AddReaction('R9', {'G': -1, 'F': 1})
m.AddReaction('R10', {'A': 1})

m.AddExchangeReactions()

m.PrintReactions()
