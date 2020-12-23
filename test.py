import scobra

mExcel = scobra.Model("test_formose1.xml")
mExcel.SetDefaultKinetics(["Form1"])

concDict = {
    'C1': 10,
    'C2': 5,
    'C3ald': 3,
    'C4ket': 3,
    'C3ket': 3,
    'C4ald': 2,
    'C4ket': 1,
    'C4fur': 4}

mExcel.SetConstrFromRateEquation(concDict)
print(mExcel.GetConstraints())
mExcel.WriteModel("excelTest.xls", "excel")

"""
mTest = scobra.Model("Test.xls")
mTest.PrintKinetics()
"""

"""
m2 = scobra.Model('EDIT')
m2.AddReaction('R1', {'A': -1, 'B': -1, 'C': -1, 'D': 1})
m2.AddReaction('R2', {'B': -1, 'C': -3, 'E': 1}, True)
m2.AddReaction('R3', {'E': -1, 'F': 1})
m2.AddReaction('R4', {'G': -1, 'F': 1})

concDict = {
    'A': 0,
    'B': 1,
    'C': 3,
    'D': 3,
    'E': 3,
    'F': 2,
    'G': 1}

constantDict = {'R1': (3),
                'R2': (2),
                'R3': (1),
                'R4': (2)
                }

m2.AddExchangeReactions()

m2.SplitRev(False)
m2.SetDefaultKinetics([])
m2.PrintKinetics()
m2.SetConstrFromRateEquation(concDict)
print(m2.GetConstraints())
m2.WriteModel("test.xls", "excel")
"""

# Week 3 Objectives #
# (*) Import/Export to Excel
# UpdateConcentration()
#   update(Metabolite.concentration), if flux is negative, increases
#   new file called analysis/DFBA
# (*) Documentation + (*) Testing
# Extra: Import/Export SBML
# Extra: Import/Export JSON
