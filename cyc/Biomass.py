
##from ScrumPy.Util import Set

import MolWts

reload(MolWts)


class Composition(dict):

    def __init__(self, ammount, components={}):
        
        self.ammount = float(ammount)
        self.update(components)


    def __float__(self):
        
        return self.ammount

    def Copy(self):

        components = {}
        for k in self.keys():
            if hasattr(self[k], "Copy"):
                components[k] = self[k].Copy()
            else:
                components[k] = self[k]

        return Composition(self.ammount, components)


    def AmmountOf(self, i):

        rv = 0.0

        if self.has_key(i):
            rv =  float(self) * float(self[i])
        
        else:
            for k in self:
                rec = self[k]
                if hasattr(rec, "AmmountOf"):
                    rv += float(self) * rec.AmmountOf(i)
                    
        return rv


    def MolsOf(self,i,StrFilt=None):
        """ StrFilt function to remove compartmental suffixes etc from i """

        if StrFilt == None:
            i2 = i
        else:
            i2 = StrFilt(i)
            

        return self.AmmountOf(i) / MolWts.MolWt(i2)
    

    def GetLeaves(self):

        rv = []

        for k in self:
            if hasattr(self[k], "GetLeaves"):
                rv.extend(self[k].GetLeaves())
            else:
                rv.append(k)
        return rv
                        
            

        
                    
                    
    

 
def WhatExports(m, compound):

    for reac in m.sm.InvolvedWith(compound).keys():
##        if "_tx" in reac and len(Set.Intersect(m.sm.Externs, m.smexterns.InvolvedWith(reac).keys())) != 0:
        if "_tx" in reac and len(set(m.sm.Externs).intersection(m.smexterns.InvolvedWith(reac).keys())) != 0:
            return reac
