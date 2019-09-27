""" Not functional! To be modified """

def MatchFlux(self, md, vd, lo=0, hi=100, samedirec=True, count=50, 
                display=False, tol=1e-6):
    """ pre: md = matched flux dict; vd = vary flux dict / vary met bound dict """
    state = self.GetState()
    avg = (float(lo)+float(hi))/2
    if set(vd.keys()).issubset(self.cnames.values()):    # vary flux dict
        self.SetSumReacsConstraint(vd,avg)
    elif set(vd.keys()).issubset(self.rnames.values()) or set(vd.keys()).issubset(self.smexterns.rnames): # vary met bound dict
        metdic = {}
        for met in vd:
            metdic[met] = (avg*vd[met],avg*vd[met])
        self.SetMetBounds(metdic)
    else:
        print("vary dict error")
    self.Solve(False)
    reac = md.keys()[0]
    val = md[reac]
    sol = self.GetSol(IncZeroes=True)[reac]
    if set(vd.keys()).issubset(self.cnames.values()):    # vary flux dict
        self.DelSumReacsConstraint()
    elif set(vd.keys()).issubset(self.rnames.values()) or set(vd.keys()).issubset(self.smexterns.rnames): # vary met bound dict
        for met in vd:
            metdic[met] = (0,0)
        self.SetMetBounds(metdic)   # set met bounds back to balance
    self.SetState(state)
    if display:
        print("Varying value = " + str(avg))
        print(reac + " " + str(sol))
    if abs(1-(sol/val)) < tol:
        return avg
    else:
        if samedirec:
            if sol > val:
                hi = avg
            else:
                lo = avg
        else:
            if sol > val:
                lo = avg
            else:
                hi = avg
        count = count - 1
        if count > 0:
            return self.MatchFlux(md, vd, lo, hi, samedirec, count, display, tol)
        else:
            return None
            print("Varying  value = " + str(avg))
            print(reac + " " + str(sol))

def MatchRatio(self,numdic,domdic,val,vd,lo=0,hi=100,samedirec=True,count=50,display=False,tol=1e-6):
    state = self.GetState()

    avg = (float(lo)+float(hi))/2
    if set(vd.keys()).issubset(self.cnames.values()):    # vary flux dict
        self.SetSumReacsConstraint(vd,avg,'matchratio')
    elif set(vd.keys()).issubset(self.rnames.values()) or set(vd.keys()).issubset(self.smexterns.rnames): # vary met bound dict
        metdic = {}
        for met in vd:
            metdic[met] = (avg*vd[met],avg*vd[met])
        self.SetMetBounds(metdic)
    else:
        print("vary dict error")

    self.Solve(False)
    num = 0.0
    for reac in numdic:
        num += self.GetSol(IncZeroes=True)[reac]*numdic[reac]
    dom = 0.0
    for reac in domdic:
        dom += self.GetSol(IncZeroes=True)[reac]*domdic[reac]
    sol = num/dom
    self.SetState(state)
    if set(vd.keys()).issubset(self.cnames.values()):    # vary flux dict
        self.DelSumReacsConstraint('matchratio')
    elif set(vd.keys()).issubset(self.rnames.values()) or set(vd.keys()).issubset(self.smexterns.rnames): # vary met bound dict
        for met in vd:
            metdic[met] = (0,0)
        self.SetMetBounds(metdic)   # set met bounds back to balance

    if display:
        print("Varying  value = " + str(avg))
        print(reac + " " + str(sol))
    if abs(1-(sol/val)) < tol:
        self.SetState(state)
        return avg
    else:
        if samedirec:
            if sol > val:
                hi = avg
            else:
                lo = avg
        else:
            if sol > val:
                lo = avg
            else:
                hi = avg
        count = count - 1
        if count > 0:
            return self.MatchRatio(numdic, domdic, val, vd, lo, hi, samedirec, count, display, tol)
        else:
            self.SetState(state)
            print("Varying  value = " + str(avg))
            print("Ratio =",sol)
