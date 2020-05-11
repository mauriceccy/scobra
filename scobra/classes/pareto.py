from .matrix import matrix
import scipy

class pareto(matrix):

    def __init__(self,*args,**kwargs):
        super(pareto,self).__init__(*args,**kwargs)


    def GetParetoPoints(self,tol=1e-10):
        po2 = pareto()
        for r in self.columns.tolist():
            if r.startswith('Obj'):
                po2[r] = self[r]
        pp = [po2.iloc[0,:].tolist()]
        rv = pareto(columns=po2.columns)
        index = rv.index.tolist()
        rv = rv.append(po2.iloc[0,:])
        rv.index = index + [po2.index.tolist()[0]] 
        for row in po2.index.tolist():
            po2r = po2.loc[row]
            diff = True
            for p in pp:
                if scipy.spatial.distance.cityblock(p,po2r) > tol:
                    diff = False
            if diff:
                index = rv.index.tolist()
                rv = rv.append(po2r)
                rv.index = index + [row]
                pp.append(po2r)
        return rv

