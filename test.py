import scobra

mExcel = scobra.Model("test_formose1.xml")
mExcel.SetDefaultKinetics(["Form1"])
mExcel.DelReactions(['Out3k', 'Out4k', 'OutPdt',
                     'Out2', 'Out3a', 'Out4a', 'Form1'])
mExcel.AddExchangeReactions()

mExcel.SetRateConstants({
    'Form2': 0.0001,
    'Form3': 0.0001,
    'Isom3': 0.0001,
    'Form4': 0.0001,
    'Ring4': 0.0001,
    'Split4': 0.0001
})

concDict = {
    'C1': 100,
    'C2': 100,
    'C3ald': 100,
    'C4ket': 100,
    'C3ket': 100,
    'C4ald': 100,
    'C4fur': 100}


mExcel.SetConstrFromRateEquation(concDict)
mExcel.SetObjective(['Isom3'])
mExcel.SetObjDirec('Max')
print(mExcel.GetConstraints())

mExcel.Solve()
print(mExcel.GetSol())

sol = mExcel.GetSol(IncZeroes=True)
mExcel.UpdateConc(sol, concDict)

print(concDict)
mExcel.WriteFile("formoseOut.xls", "excel")

"""
mTest = scobra.Model("testIn.xls")
mTest.SplitRev(False)
mTest.AddExchangeReactions()
mTest.SetDefaultKinetics()

concDict = {
    'A': 10,
    'B': 10,
    'C': 10,
    'D': 10,
    'E': 10,
    'F': 10,
    'G': 10
}

mTest.SetRateConstants({'R1': 0.0005,
                        'R2': 0.0002,
                        'R3': 0.2,
                        'R4': 0.2
                        })

mTest.SetConstrFromRateEquation(concDict)

mTest.SetObjective('R1')
mTest.SetObjDirec('Min')
mTest.Solve()
sol = mTest.GetSol(IncZeroes=True)
mTest.UpdateConc(sol, concDict)

print(concDict)

mTest.WriteModel("testOut.xls", "excel")
"""
