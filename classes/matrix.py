import pandas
import math
from matplotlib import pyplot
from scipy import stats

class matrix(pandas.DataFrame):

    def __init__(self, *args, **kwargs):
        super(matrix, self).__init__(*args, **kwargs)

    def Copy(self):
        return matrix(self.copy())

    @classmethod
    def FromFile(self, path, file_format=None, **kwargs):
        """ file_format = "csv" | "excel" | "pickle" """
        if file_format == "csv" or path.endswith('.csv') or path.endswith('.txt'):
            return matrix(pandas.read_csv(path, **kwargs))
        elif file_format == "excel" or file_format == "xls" or file_format == "xlsx" or path.endswith('.xls') or path.endswith('.xlsx'):
            return matrix(pandas.read_excel(path, **kwargs))
        elif file_format == "pickle" or path.endswith('.p') or path.endswith('.pkl') or path.endswith('.pickle'):
            return matrix(pandas.read_pickle(path))

    def ToFile(self, path, file_format=None, **kwargs):
        """ file_format = "csv" | "excel" | "pickle" """
        if file_format == "csv" or path.endswith('.csv') or path.endswith('.txt'):
            self.to_csv(path, **kwargs)
        elif file_format == "excel" or file_format == "xls" or file_format == "xlsx" or path.endswith('.xls') or path.endswith('.xlsx'):
            self.to_excel(path, **kwargs)
        elif file_format == "pickle" or path.endswith('.p') or path.endswith('.pkl') or path.endswith('.pickle'):
            self.to_pickle(path)

    def Plot(self,x,y=None,**kwargs):
        if y == None:
            self[x].plot(**kwargs)
        else:
            self.plot(kind="scatter",x=x,y=y)
        pyplot.show()

    def VaryReacs(self,tol=1e-10):
        varymtx = self.Copy()
        fixreacs = []
        for reac in self.columns:
            vary = False
            col = list(self[reac])
            for val in col:
                if abs(val-col[0]) > tol:
                    vary = True
            if vary == False:
                fixreacs.append(reac)
        for reac in fixreacs:
            varymtx=varymtx.drop(reac,1)
        return varymtx

    def FixedReacs(self,tol=1e-10):
        fixedmtx = self.Copy()
        varyreacs = []
        for reac in self.columns:
            vary = False
            col = list(self[reac])
            for val in col:
                if abs(val-col[0]) > tol:
                    vary = True
            if vary == True:
                varyreacs.append(reac)
        for reac in varyreacs:
            fixedmtx=fixedmtx.drop(reac,1)
        return fixedmtx

    def NonZeroes(self,tol=1e-10):
        rv = self.Copy()
        zeroreacs = []
        for reac in self.columns:
            zero = True
            col = list(self[reac])
            for val in col:
                if abs(val) > tol:
                    zero = False
            if zero:
                zeroreacs.append(reac)
        for reac in zeroreacs:
            rv = rv.drop(reac,1)
        return rv

    def ZeroReac(self,tol=1e-10):
        rv = []
        for reac in self.columns:
            zero = True
            col = list(self[reac])
            for val in col:
                if abs(val) > tol:
                    zero = False
            if zero:
                rv.append(reac)
        return rv

    def AverageFlux(self,IncZeroes=False,AsMtx=False,tol=1e-10):
        rv = {}
        for reac in self.columns:
            rv[reac] = float(sum(self[reac]))/len(self.index)
        if not IncZeroes:
            for reac in list(rv.keys()):
                if abs(rv[reac]) < tol:
                    del rv[reac]
        if AsMtx:
           rv = matrix({"lp_sol":rv})
        return rv

    def FluxRange(self,IncZeroes=False,AsMtx=False,tol=1e-10):
        from .fva import fva
        rv = fva(bounds=self.bounds)
        for reac in self.columns:
            rv[reac] = (min(self[reac]),max(self[reac]))
        if not IncZeroes:
            rv = rv.Allowed(tol=tol)
        if AsMtx:
           rv = rv.AsMtx()
        return rv

    def DicUpdate(self,dic,row=None):
        s = pandas.Series(dic,name=row)
        self = self.append(s,ignore_index=row==None)
        self = self.fillna(0)
        return matrix(self)

    def UpdateFromDic(self,dic,row=None):
        return self.DicUpdate(dic=dic,row=row)

#    def Tree(self,incobjval=False,tol=1e-10):
#        temp = self.VaryReacs(tol=tol)
#        if incobjval == False and 'ObjVal' in temp.columns:
#            temp = temp.drop('ObjVal',1)
#        temp = temp.T
#        simmtx = temp.RowDiffMtx(lambda x,y: 1-abs(Stats.Pearson_r(x,y)))
#        t = simmtx.ToNJTree()
#        return t

    def ResponseCoef(self,scanvar=None,incobjval=False,tol=1e-10):
        temp = self.VaryReacs(tol=tol)
        if scanvar == None:
            var = temp.iloc[:,0]
        else:
            var = temp[scanvar]
        if incobjval == False and 'ObjVal' in temp.columns:
            temp = temp.drop('ObjVal')
        rv = {}
        for reac in temp.columns:
            rv[reac] = 1-abs(stats.pearsonr(var,temp[reac]))[0]
        return rv

    def PrintResponseCoef(self,lo=0,hi=1,rc=None,f=None,Sort="value",sortabs=True,reverse=True,scanvar=None,incobjval=False,tol=1e-10):
        if rc == None:
            rc = self.ResponseCoef(scanvar=scanvar,incobjval=incobjval,tol=tol)
        if f != None:
            temprc = dict(rc)
            for reac in list(temprc.keys()):
                if f not in reac:
                    del temprc[reac]
            rc = temprc
        if Sort == "value":
            if sortabs:
                function = lambda (k,v): (abs(v),k)
            else:
                function = lambda (k,v): (v,k)
            for key, value in sorted(rc.iteritems(), key=function,reverse=reverse):
                if abs(value) >= lo and abs(value) <= hi:
                    print "%s: %s" % (key, value)
        elif Sort == "key":
            for key in sorted(rc.iterkeys()):
                if abs(rc[key]) >= lo and abs(value) <= hi:
                    print "%s: %s" % (key, rc[key])

    def FluxCorrCoefMtx(self,absolute=False,tol=1e-10):
        vary = self.VaryReacs(tol=tol)
        lenvary = len(vary.columns)
        rv = matrix()
        rv.columns = list(vary.columns)
        for reac in vary.columns:
            rv.loc[reac,:] = 0
        for r1 in range(lenvary):
            for r2 in range(r1, lenvary):
                corrcoef = stats.pearsonr(vary[r1],vary[r2])[0]
                if absolute:
                    corrcoef = abs(corrcoef)
                rv.iloc[r1,r2] = rv.iloc[r2,r1] = corrcoef
        return rv


    def FluxCorrCoef(self,reac1,reac2=None,absolute=False,tol=1e-10):
        temp = self.VaryReacs(tol=tol)
        if reac2 != None:
            if absolute:
                return abs(stats.pearsonr(temp[reac1],temp[reac2]))[0]
            else:
                return stats.pearsonr(temp[reac1],temp[reac2])[0]
        else:
            rv = {}
            for reac in temp.columns:
                if absolute:
                    rv[reac] = abs(stats.pearsonr(temp[reac1],temp[reac]))[0]
                else:
                    rv[reac] = stats.pearsonr(temp[reac1],temp[reac])[0]
            return rv

    def PrintFluxCorrCoef(self,reac,lo=0,hi=1,f=None,Sort="value",sortabs=True,reverse=True,absolute=False,tol=1e-10):
        rc = self.FluxCorrCoef(reac1=reac,reac2=None,absolute=absolute,tol=tol)
        if f != None:
            temprc = dict(rc)
            for reac in list(temprc.keys()):
                if f not in reac:
                    del temprc[reac]
            rc = temprc
        if Sort == "value":
            if sortabs:
                function = lambda (k,v): (abs(v),k)
            else:
                function = lambda (k,v): (v,k)
            for key, value in sorted(rc.iteritems(), key=function,reverse=reverse):
                if abs(value) >= lo and abs(value) <= hi:
                    print "%s: %s" % (key, value)
        elif Sort == "key":
            for key in sorted(rc.iterkeys()):
                if abs(rc[key]) >= lo and abs(value) <= hi:
                    print "%s: %s" % (key, rc[key])


    def StDev(self,reac):
        col = list(self[reac])
        mean = sum(col)/len(col)
        var = 0.0
        for b in col:
            var += (b-mean)**2
        var = var/len(col)
        return abs(math.sqrt(var))


    def RelStDev(self,reac):
        col = list(self[reac])
        mean = sum(col)/len(col)
        var = 0.0
        for b in col:
            var += (b-mean)**2
        var = var/len(col)
        if mean == 0.0:
            return float('nan')
        else:
            return abs(math.sqrt(var)/mean)

    def PrintRSD(self,lo=0,hi=float('inf'),f=None,Sort="value",sortabs=True,reverse=True,tol=1e-10):
        rsd = {}
        for r in self.columns:
            rsd[r] = self.RelStDev(r)
        if f != None:
            temprsd = dict(rsd)
            for reac in list(temprsd.keys()):
                if f not in reac:
                    del temprsd[reac]
            rsd = temprsd
        if Sort == "value":
            if sortabs:
                function = lambda (k,v): (abs(v),k)
            else:
                function = lambda (k,v): (v,k)
            for key, value in sorted(rsd.iteritems(), key=function,reverse=reverse):
                if abs(value) >= lo and abs(value) <= hi:
                    print "%s: %s" % (key, value)
        elif Sort == "key":
            for key in sorted(rsd.iterkeys()):
                if abs(rsd[key]) >= lo and abs(value) <= hi:
                    print "%s: %s" % (key, rsd[key])

    def AverageDev(self,reac):
        col = list(self[reac])
        mean = sum(col)/len(col)
        var = 0.0
        for b in col:
            var += abs(b-mean)
        var = var/len(col)
        return var

    def RelAverageDev(self,reac):
        col = list(self[reac])
        mean = sum(col)/len(col)
        var = 0.0
        for b in col:
            var += abs(b-mean)
        var = var/len(col)
        if mean == 0.0:
            return float('nan')
        else:
            var = var/abs(mean)
            return var

    def PrintRAD(self,lo=0,hi=float('inf'),f=None,Sort="value",sortabs=True,reverse=True,tol=1e-10):
        rad = {}
        for r in self.columns:
            rad[r] = self.RelAverageDev(r)
        if f != None:
            temprad = dict(rad)
            for reac in list(temprad.keys()):
                if f not in reac:
                    del temprad[reac]
            rad = temprad
        if Sort == "value":
            if sortabs:
                function = lambda (k,v): (abs(v),k)
            else:
                function = lambda (k,v): (v,k)
            for key, value in sorted(rad.iteritems(), key=function,reverse=reverse):
                if abs(value) >= lo and abs(value) <= hi:
                    print "%s: %s" % (key, value)
        elif Sort == "key":
            for key in sorted(rad.iterkeys()):
                if abs(rad[key]) >= lo and abs(value) <= hi:
                    print "%s: %s" % (key, rad[key])

    def AsDic(self):
        rv = {}
        for r in self.index:
            row = self.loc[r,:]
            row = tuple(row)
            rv[r] = row
        return rv