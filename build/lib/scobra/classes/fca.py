from .matrix import matrix
import numpy

class fca(matrix):

    def __init__(self,*args,**kwargs):
        super(matrix,self).__init__(*args,**kwargs)

    def Copy(self):
        return fca(self.copy())

#    def FCAGetReac(self,reac):
#        rv = fca(columns=self.columns)
#        row = []
#        reacs = self.columns.tolist()
#        idx = self.rnames.index(reac)
#        for b in range(len(reacs)):
#            row.append(self[idx][b])
#        rv.NewRow(r=row,name=reac)
#        return fca(self[reac])


    def ReacCoupling(self,reac,coupling="all"):
        reacds = fca(self[reac])
        fc = reacds.FullyCoupled()
        pc = reacds.PartiallyCoupled()
        dc = reacds.DirectionallyCoupled()
        rv = {"all":(fc,pc,dc),"FC":fc,"PC":pc,"DC":dc}
        return rv[coupling]


    def DirectionallyCoupled(self):
        implies = {}    # reac implies reacs, r1 -> r2, equivalent knockout
        impliedby = {}    # reac implied by reacs, r1 <- r2, affected
        txds = self.Copy()
        #txfs = fca(txds.transpose())
        for r in range(len(self.index)):
            rreac = self.index[r]
            impdby = []
            for c in range(len(self.columns)):
                creac = self.columns[c]
                if self.iloc[r,c] == 7:
                    impdby.append((creac,"+"))
                elif self.iloc[r,c] == 8:
                    impdby.append((creac,"-"))
            if len(impdby) > 0:
                impliedby[rreac] = impdby
        for r in range(len(txds.index)):
            rreac = txds.index[r]
            imps = []
            for c in range(len(txds.columns)):
                creac = txds.columns[c]
                if txds.iloc[r,c] == 7:
                    imps.append((creac,"+"))
                elif txds.iloc[r,c] == 8:
                    imps.append((creac,"-"))
            if len(imps) > 0:
                implies[rreac] = imps
        rv = {"Implies":implies,"Implied by":impliedby}
        return rv


    def PartiallyCoupled(self):
        pc = {}
        n = 1
        for r in range(len(self.index)):
            rreac = self.index[r]
            for c in range(len(self.columns)):
                creac = self.columns[c]
                if self.iloc[r,c] == 11 or self.iloc[r,c] == 12:
                    if (rreac not in pc.keys()) and (creac not in pc.keys()):
                        pc[rreac] = "PC"+str(n),"+"
                        if self.iloc[r,c] == 11:
                            pc[creac] = "PC"+str(n),"+"
                        elif self.iloc[r,c] == 12:
                            pc[creac] = "PC"+str(n),"-"
                        n += 1
                    elif (rreac in pc.keys()) and (creac not in pc.keys()):
                        num,sign = pc[rreac]
                        if self.iloc[r,c] == 12:
                            sign = self.SwapSign(sign)
                        pc[creac] = num,sign
                    elif (rreac not in pc.keys()) and (creac in pc.keys()):
                        num,sign = pc[creac]
                        if self.iloc[r,c] == 12:
                            sign = self.SwapSign(sign)
                        pc[rreac] = num,sign
        rv = {}
        for reac in pc:
            num,sign = pc[reac]
            if rv.has_key(num):
                rv[num].append((reac,sign))
            else:
                rv[num] = [(reac,sign)]
        return rv


    def FullyCoupled(self):
        fc = {}
        n = 1
        for r in range(len(self.index)):
            rreac = self.index[r]
            for c in range(len(self.columns)):
                creac = self.columns[c]
                if self.iloc[r,c] == 13 or self.iloc[r,c] == 14:
                    if (rreac not in fc.keys()) and (creac not in fc.keys()):
                        fc[rreac] = "FC"+str(n),"+"
                        if self.iloc[r,c] == 13:
                            fc[creac] = "FC"+str(n),"+"
                        elif self.iloc[r,c] == 14:
                            fc[creac] = "FC"+str(n),"-"
                        n += 1
                    elif (rreac in fc.keys()) and (creac not in fc.keys()):
                        num,sign = fc[rreac]
                        if self.iloc[r,c] == 14:
                            sign = self.SwapSign(sign)
                        fc[creac] = num,sign
                    elif (rreac not in fc.keys()) and (creac in fc.keys()):
                        num,sign = fc[creac]
                        if self.iloc[r,c] == 14:
                            sign = self.SwapSign(sign)
                        fc[rreac] = num,sign
        rv = {}
        for reac in fc:
            num,sign = fc[reac]
            if rv.has_key(num):
                rv[num].append((reac,sign))
            else:
                rv[num] = [(reac,sign)]
        return rv

    def SwapSign(self,sign):
        if sign == "+":
            rv = "-"
        elif sign == "-":
            rv = "+"
        else:
            print("swap sign error")
        return rv

    def RangeType(self,lb,ub,tol,bounds):
        def Eq(a,b,rtol=tol,atol=tol):
            return numpy.allclose(a,b,rtol,atol)
        if lb != lb or ub != ub:    # check for nan
            print("nan problem")
            return float("NaN")
        else:
            if ub >= lb:
                lo = lb
                hi = ub
            elif lb > ub:
                hi = lb
                lo = ub
            else:
                print("range type lb ub error")
    #        if lo == float("-inf") and hi == float("inf"):
            if Eq(lo,-bounds) and Eq(hi,bounds):
                rv = 1    # uncoupled
    #        elif lo > float("-inf") and hi == float("inf"): # lower bound only
            elif lo > -bounds and Eq(hi,bounds): # lower bound only
                if abs(lo) < tol:
                    rv = 2
                elif lo < -tol:
                    rv = 4
                elif lo > tol:
                    rv = 9    # directionally coupled
    #        elif lo == float("-inf") and hi < float("inf"): # upper bound only
            elif Eq(lo,-bounds) and hi < bounds: # upper bound only
                if abs(hi) < tol:
                    rv = 3
                elif hi > tol:
                    rv = 5
                elif hi < -tol:
                    rv = 10   # directionally coupled
    #        elif lo > float("-inf") and hi < float("inf"):  # both bounded
            elif lo > -bounds and hi < bounds:  # both bounded
                if lo > -tol and hi > -tol: # same direction
                    if lo < tol and hi < tol:
                        rv = 15
                    elif lo < tol and hi >= tol:
                        rv = 7    # directionally coupled
                    elif lo >= tol and hi >= tol:
                        if abs(lo-hi) > tol:
                            rv = 11   # partially coupled
                        else:
                            rv = 13   # fully coupled
                elif lo < tol and hi < tol: # opposite direction
                    if lo > -tol and hi > -tol:
                        rv = 15
                    elif lo <= -tol and hi > -tol:
                        rv = 8    # directionally coupled
                    elif lo <= -tol and hi <= -tol:
                        if abs(lo-hi) > tol:
                            rv = 12   # partially coupled
                        else:
                            rv = 14   # fully coupled
                else:
                    rv = 6    # ???...
            else:
                print("range type error")
            return rv

