import numpy
from .matrix import matrix

class fva(dict):

    def __init__(self, content, bounds=float("inf")):
        super(fva, self).__init__(content)
        self.bounds = bounds

    def __call__(self, string=''):
        rv = fva({})
        for r in self:
            if string in r:
                rv[r] = self[r]
        return rv

    def Blocked(self,tol=1e-10):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
            if (abs(self[reac][0]) < tol) and (abs(self[reac][1]) < tol):
                rv[reac] = self[reac]
        return rv

    def Allowed(self,tol=1e-10):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
            if (abs(self[reac][0]) > tol) or (abs(self[reac][1]) > tol):
                rv[reac] = self[reac]
        return rv

    def Variable(self,tol=1e-10):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
            diff = self[reac][0] - self[reac][1]
            if abs(diff) > tol:
                rv[reac] = self[reac]
        return rv

    def Fixed(self,tol=1e-10):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
            diff = self[reac][0] - self[reac][1]
            if abs(diff) < tol:
                rv[reac] = self[reac]
        return rv

    def Essential(self,tol=1e-10):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
            if (self[reac][0] > tol) or (self[reac][1] < -tol):
                rv[reac] = self[reac]
        return rv

    def Substitutable(self,tol=1e-10):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
            diff = self[reac][0] - self[reac][1]
            if (self[reac][0] <= tol and self[reac][1] >= -tol) and abs(diff) > tol:
                rv[reac] = self[reac]
        return rv

    def Unbounded(self):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
#            if self[reac][0] == float("-inf") or self[reac][1] == float("inf"):
            if numpy.allclose(self[reac][0],-self.bounds) or numpy.allclose(self[reac][1],self.bounds):
                rv[reac] = self[reac]
        return rv

    def Bounded(self):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
#            if self[reac][0] != float("-inf") and self[reac][1] != float("inf"):
            if (not numpy.allclose(self[reac][0],-self.bounds)) and (not numpy.allclose(self[reac][1],self.bounds)):
                rv[reac] = self[reac]
        return rv

    def BothDirections(self,tol=1e-10):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
            if self[reac][0] < -tol and self[reac][1] > tol:
                rv[reac] = self[reac]
        return rv

    def ForwardOnly(self,tol=1e-10):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
            if self[reac][0] > -tol and self[reac][1] > tol:
                rv[reac] = self[reac]
        return rv

    def BackwardOnly(self,tol=1e-10):
        rv = fva({}, bounds=self.bounds)
        for reac in self:
            if self[reac][0] < -tol and self[reac][1] < tol:
                rv[reac] = self[reac]
        return rv

    def AsMtx(self):
        return matrix(self, index=['Min','Max']).transpose()

    def GetReacs(self,reacs):
        rv = fva({}, bounds=self.bounds)
        for reac in reacs:
            if reac in self.keys():
                rv[reac] = self[reac]
        return rv

    def GetReacsMeanFlux(self,reacs):
        rv = {}
        for reac in reacs:
            rv[reac] = (self[reac][0]+self[reac][1])/2.0
        return rv

    def MaxDiff(self):
        diff = []
        for reac in self.keys():
            diff.append(abs(self[reac][1]-self[reac][0]))
        return max(diff)

    def FluxRangeDiff(self, fd, thres=1):
        """ a measure of flux difference with another fva object
            pre: thres -- only get reactions with difference > thres """
        rv = {}
        both1n2 = list(set(self.keys()).intersection(fd.keys()))
        diffdirec = self.FluxDiffDirec(fd) # reac in different direc
        comparereacs = list(set(both1n2).difference(diffdirec))
        overlaps = self.FluxRangeOverlap(fd)   # reac with overlap flux range
        comparereacs = list(set(comparereacs).difference(overlaps))
        for r in comparereacs:
            max1 = max(self[r])
            min1 = min(self[r])
            max2 = max(fd[r])
            min2 = min(fd[r])
            if (max1 > 0) or (max2 > 0):    # positive flux
                if (min1*thres) > max2:
                    rv[r] = max2/min1
                elif (min2*thres) > max1:
                    rv[r] = -max1/min2
            elif (min1 < 0) or (min2 < 0):  # negative flux
                if (max1*thres) < min2:
                    rv[r] = min2/max1
                elif (max2*thres) < min1:
                    rv[r] = -min1/max2
            else:
                print(r)
        return rv

    def FluxDiffDirec(self, fd):
        """ Compare with another fva object and get reactions with different directions """
        rv = []
        both1n2 = list(set(self.keys()).intersection(fd.keys()))
        for r in both1n2:
            max1 = max(self[r])
            min1 = min(self[r])
            max2 = max(fd[r])
            min2 = min(fd[r])
            if (min1 >= 0) and (max2 <= 0):
                rv.append(r)
            elif (min2 >= 0) and (max1 <= 0):
                rv.append(r)
        return rv

    def FluxRangeOverlap(self, fd):
        """ Compare with another fva object and get reactions with overlapping flux range """
        both1n2 = list(set(self.keys()).intersection(fd.keys()))
        nonoverlap = []
        for r in both1n2:
            max1 = max(self[r])
            min1 = min(self[r])
            max2 = max(fd[r])
            min2 = min(fd[r])
            if (min1 > max2) or (min2 > max1):
                nonoverlap.append(r)
        rv = list(set(both1n2).difference(nonoverlap))
        return rv
