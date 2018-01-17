from ..classes.fca import fca

def FCA(model, reacs=None, rangedict=None, tol=1e-10):
    """ pre: model object
       post: returns dataset of coupling """
    state = model.GetState()

    if rangedict == None:
        rangedict = model.AllFluxRange(tol=tol)
#        allreacs = self.Reactions()   # Forward reaction names
#        allowed = rangedict.Allowed()
#        blockedreacs = rangedict.Blocked().keys()
    allowedreacs = rangedict.Allowed().keys()
    #blocked = self.BlockedReactions(rangedict=rangedict,tol=tol) # Blocked Reactions
    #allreacs = list(set(allreacs).difference(blocked))     # Allowed reactions (forward names only)
    backwardonly = rangedict.BackwardOnly().keys()
    #rev = self.ReversedReaction(rangedict=rangedict,tol=tol)   # Reversible reacs only in -ve direction
    forwardonly = rangedict.ForwardOnly().keys()
    bothdirec = rangedict.BothDirections().keys()
#        for reac in forwardonly:
#            self.SetConstraint(reac,0,None)     # Remove fixed constraints, only looking at structual properties
#        for reac in backwardonly:
#            self.SetConstraint(reac,None,0)
#        for reac in bothdirec:
#            self.SetConstraint(reac,None,None)
    constraintdic = model.GetConstraints()
    ds = fca(columns=allowedreacs)
    if not reacs:
#            reacs = allreacs
        reacs = allowedreacs
    for reac in reacs:          # compute whole matrix for given reactions
        if reac in allowedreacs:                    # reac not blocked
            if reac in backwardonly:
                if rangedict[reac][0]==float("-inf") or rangedict[reac][0]==None:
                    model.SetFixedFlux({reac:rangedict[reac][1]-1})  # any negative number within the range
                else:
                    model.SetFixedFlux({reac:sum(rangedict[reac])/2.0})
            elif reac in forwardonly:
                if rangedict[reac][1]==float("inf") or rangedict[reac][1]==None:
                    model.SetFixedFlux({reac:rangedict[reac][0]+1})  # any positive number within the range
                else:
                    model.SetFixedFlux({reac:sum(rangedict[reac])/2.0})
            elif reac in bothdirec:
                model.SetFixedFlux({reac:rangedict[reac][1]/2.0})  # any positive number within range
            ds.loc[reac] = 0
            for reac2 in allowedreacs:
                if reac != reac2:
                    lo,hi = model.FluxRange(reac2)
                    if reac in backwardonly:
                        ds.loc[reac,reac2] = ds.RangeType(-hi, -lo, tol,
                                                    bounds=model.bounds)
                    else:
                        ds.loc[reac,reac2] = ds.RangeType(lo, hi, tol,
                                                    bounds=model.bounds)
            lb,ub = constraintdic[reac]
            model.SetConstraint(reac, lb, ub)
    model.SetState(state)
    return fca(ds)
