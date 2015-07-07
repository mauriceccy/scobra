from ..classes.pareto import pareto

def Pareto(model, objectives, objdirec, runs, GetPoints=True, tol=1e-10):
    """ pre: objective = [["reac"],{"reac2":x}]
       post: turning points of Pareto front """
    state = model.GetState()
    rv = pareto()
    model.SetObjDirec(objdirec)
    anchor = []
    for obj in objectives:
        model.ZeroObjective()
        model.SetObjective(obj)
        model.Solve(PrintStatus=False)
        if model.Optimal():
            anchor.append(model.GetObjVal())
        else:
            print "Error:",obj,model.GetStatusMsg()
    if len(anchor) == len(objectives):
        for n in range(runs):
            model.ZeroObjective()
            coef = []
            for b in range(len(objectives)):
                coef.append(random.random())
            sumcoef = sum(coef)
            for b in range(len(objectives)):
                coef[b] = coef[b]/anchor[b]/sumcoef
            objdic = {}
            for b in range(len(objectives)):
                thisobjdic = {}
                if isinstance(objectives[b],list):
                    for reac in objectives[b]:
                        thisobjdic[reac] = coef[b]
                elif isinstance(objectives[b],dict):
                    for reac in objectives[b]:
                        thisobjdic[reac] = objectives[b][reac]*coef[b]
                for r in thisobjdic:
                    if r in objdic.keys():
                        objdic[r] += thisobjdic[r]
                    else:
                        objdic[r] = thisobjdic[r]
            model.SetObjective(objdic)
            model.Solve(PrintStatus=False)
            sol = model.GetSol(IncZeroes=True)
            for b in range(len(objectives)):
                sol["coef"+str(b+1)] = coef[b]
                if isinstance(objectives[b],list):
                    sol["Obj"+str(b+1)] = sol[objectives[b][0]]
                elif isinstance(objectives[b],dict):
                    objsol = 0
                    for reac in objectives[b]:
                        objsol += sol[reac]*objectives[b][reac]
                    sol["Obj"+str(b+1)] = objsol
            rv.UpdateFromDic(sol)
    model.SetState(state)
    if len(anchor) == len(objectives) and GetPoints:
        return rv.GetParetoPoints(tol)
    else:
        return rv
