from ..classes import matrix

def ConstraintScan(model, cd, lo, hi, n_p, MinFlux=True, IncZeroes=True,cobra=True):
    """ scan one reaction flux
        pre: cd = sum of reaction fluxes dictionary """
    state = model.GetState()
    rv = matrix.matrix(columns=["Constraint","ObjVal"])
    lo = float(lo)
    hi = float(hi)
    inc = (hi - lo)/(n_p-1)
    cur = lo
    for n in range(n_p):
        model.SetSumReacsConstraint(cd, cur, name='ConstraintScan')
        if MinFlux:
            model.MinFluxSolve(cobra=cobra,DisplayMsg=False)
        else:
            model.Solve(False)
        sol = model.GetSol(IncZeroes=IncZeroes)

        if not model.Optimal():
            obval = float("NaN") # indicate fail
        else:
            obval =  model.GetObjVal()
        sol["ObjVal"] = obval
        sol["Constraint"] = cur
        rv = rv.UpdateFromDic(sol)
        cur += inc
        model.DelSumReacsConstraint('ConstraintScan')
    model.SetState(state)
    return rv

def RatioScan(model, reac1, reac2, n_p, lo=0, hi=1, flux_val=None,
              IncZeroes=True, rev=False):
    """ scan the ratio of two reaction fluxes
        pre: flux_val = a fixed flux for the sum of the two reactions """
    state = model.GetState()
    rv = matrix.matrix(columns=["Ratio","ObjVal"])
    lo = float(lo)
    hi = float(hi)
    inc = (hi - lo)/(n_p-1)
    cur = lo
    for n in range(n_p):
        ratiodic = {reac1:cur, reac2:1-cur}
        rationame = model.SetReacsFixedRatio(ratiodic, GetMetName=True)
        if flux_val != None:
            model.SetFixedFlux({rationame:flux_val})
        model.Solve(False)
        sol = model.GetSol(IncZeroes=IncZeroes)
        if not model.Optimal():
            obval = float("NaN") # indicate fail
        else:
            obval =  model.GetObjVal()
        sol["ObjVal"] = obval
        sol["Ratio"] = cur
        rv = rv.UpdateFromDic(sol)
        cur += inc
        model.DelReacsFixedRatio(fixedratio=rationame)
    model.SetState(state)
    return rv

def Constraint2DScan(model, cd1, lo1, hi1, cd2, lo2, hi2, n_p, IncZeroes=True):
    """ scan two reaction fluxes simultaneously """
    state = model.GetState()
    rv = matrix.matrix(columns=["Constraint1","Constraint2","ObjVal"])
    lo1 = float(lo1)
    hi1 = float(hi1)
    inc1 = (hi1 - lo1)/(n_p-1)
    cur1 = lo1
    lo2 = float(lo2)
    hi2 = float(hi2)
    inc2 = (hi2 - lo2)/(n_p-1)
    cur2 = lo2
    for n1 in range(n_p):
        model.SetSumReacsConstraint(cd1,cur1,'temp1')
        for n2 in range(n_p):
            model.SetSumReacsConstraint(cd2,cur2,'temp2')
            model.Solve(False)
            sol = model.GetSol(IncZeroes=IncZeroes)
            if not model.Optimal():
                obval = float("NaN") # indicate fail
            else:
                obval =  model.GetObjVal()
            sol["ObjVal"] = obval
            sol["Constraint1"] = cur1
            sol["Constraint2"] = cur2
            rv = rv.UpdateFromDic(sol)
            cur2 += inc2
            model.DelSumReacsConstraint('temp2')
        cur2 = lo2
        cur1 += inc1
        model.DelSumReacsConstraint('temp1')
    model.SetState(state)
    return rv

def ConstraintRandomMinFluxScan(model, cd, lo, hi, n_p, it, IncZeroes=True,
                                reacs=None, exc=[], processes=None):
    """ same as ConstraintScan except using RWFM rather than FBA
        pre: cd = sum of reaction fluxes dictionary """
    state = model.GetState()
    rv = matrix.matrix(columns=["Constraint"])
    lo = float(lo)
    hi = float(hi)
    inc = (hi - lo)/(n_p-1)
    cur = lo
    for n in range(n_p):
        model.SetSumReacsConstraint(cd,cur,name='ConstraintRandomMinFluxScan')
        mtx = model.RandomMinFlux(it=it, reacs=reacs, exc=exc,
                                    processes=processes)
        sol = mtx.AverageFlux()
        sol["Constraint"] = cur
        rv = rv.UpdateFromDic(sol)
        cur += inc
        model.DelSumReacsConstraint('ConstraintRandomMinFluxScan')
    model.SetState(state)
    return rv

def RatioRandomMinFluxScan(model, reac1, reac2, n_p, it, lo=0, hi=1, flux_val=None,
        IncZeroes=True, reacs=None, exc=[], rev=False,processes=None):
    """ same as RatioScan except using RWFM rather than FBA """
    state = model.GetState()
    rv = matrix.matrix(columns=["Ratio"])
    lo = float(lo)
    hi = float(hi)
    inc = (hi - lo)/(n_p-1)
    cur = lo
    for n in range(n_p):
        ratiodic = {reac1:cur,reac2:1-cur}
        rationame = model.SetReacsFixedRatio(ratiodic, GetMetName=True)
        if flux_val != None:
            model.SetFixedFlux({rationame:flux_val})
        mtx = model.RandomMinFlux(it=it, reacs=reacs, exc=exc,
                                processes=processes)
        sol = mtx.AverageFlux()
        sol["Ratio"] = cur
        rv = rv.UpdateFromDic(sol)
        cur += inc
        model.DelReacsFixedRatio(fixedratio=rationame)
    model.SetState(state)
    return rv

def WeightingScan(model,objdic,lo,hi,n_p):
    """ scan by changing the objective coefficients for a subset of
        reactions in the objective function """
    state = model.GetState()
    rv = matrix.matrix(columns=["Weighting"])
    lo = float(lo)
    hi = float(hi)
    inc = (hi - lo)/(n_p-1)
    cur = lo
    for n in range(n_p):
        newobjdic = {}
        for r in objdic.keys():
            newobjdic[r] = objdic[r]*cur
        model.SetObjective(newobjdic)
        model.Solve(False)
        sol = model.GetSol()
        sol["Weighting"] = cur
        rv = rv.UpdateFromDic(sol)
        cur += inc
    model.SetState(state)
    return rv


""" Not functional! To be modified """
def MatchScan(model,cd,clo,chi,md,vd,vlo,vhi,n_p,samedirec=True,count=50,display=False,tol=1e-6,IncZeroes=True):
    state = model.GetState()
    rv = matrix.matrix(columns=["Constraint","VaryFlux","ObjVal"])
    clo = float(clo)
    chi = float(chi)
    inc = (chi - clo)/(n_p-1)
    cur = clo

    for n in range(n_p):
        model.SetSumReacsConstraint(cd,cur,name="cd")
        varyflux = model.MatchFlux(md=md,vd=vd,lo=vlo,hi=vhi,samedirec=samedirec,count=count,display=display,tol=tol)
        if varyflux == None:
            model.DelSumReacsConstraint("cd")
            print("varyflux = None")
            break
        model.SetSumReacsConstraint(vd,varyflux,name="vd")
        model.Solve(False)
        sol = model.GetSol(IncZeroes=IncZeroes)
        if not model.Optimal():
            objval = float("NaN") # indicate fail
        else:
            objval = model.GetObjVal()
        sol["VaryFlux"] = varyflux*vd.values()[0]
        sol["ObjVal"] = objval
        sol["Constraint"] = cur
        rv = rv.UpdateFromDic(sol)
        cur += inc
        model.DelSumReacsConstraint("cd")
        model.DelSumReacsConstraint("vd")
    model.SetState(state)
    return rv
