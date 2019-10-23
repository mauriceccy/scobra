def RWFMSolveMinFlux(model):
    model.ZeroObjective()
    model.MinFluxSolve(PrintStatus=False,weighting='random')
    sol = model.GetSol(IncZeroes=True)
    return sol