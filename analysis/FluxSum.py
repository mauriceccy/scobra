

def FluxSum(model,met,tol=1e-10):
    sol = model.GetSol(IncZeroes=True,AsID=False)
    if model.GetSol(IncZeroes=False) == {}:
        state = model.GetState()
        model.Solve(PrintStatus=False)
        sol = model.GetSol(IncZeroes=True,AsID=False)
        model.SetState(state)
    prodreacs = model.ProducedBy(met)
    consreacs = model.ConsumedBy(met)
    prod = 0.0
    for reac in prodreacs.keys():
        reacprod = sol[reac]*prodreacs[reac]
        if reacprod > 0:
            prod += reacprod
    cons = 0.0
    for reac in consreacs.keys():
        reaccons = sol[reac]*consreacs[reac]
        if reaccons < 0:
            cons += reaccons
    if abs(prod + cons) < tol:
        rv = (abs(prod)+abs(cons))/2.0
        return rv
    else:
        print (met + " is external / not balanced")
        print ("net balance = ", prod+cons)


def ProducedBy(model,met,FixBack=True):
    met = model.GetMetabolite(met)
    reactions = model.InvolvedWith(met)
    rv = {}
    for reac in reactions:
        stoi = model.InvolvedWith(reac)[met]
        if reac.reversibility or (stoi > 0):
            rv[reac] = stoi
    return rv

def ConsumedBy(model,met,FixBack=True):
    met = model.GetMetabolite(met)
    reactions = model.InvolvedWith(met)
    rv = {}
    for reac in reactions:
        stoi = model.InvolvedWith(reac)[met]
        if reac.reversibility or (stoi < 0):
            rv[reac] = stoi
    return rv
