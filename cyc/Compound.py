import Tags, Base

import sys



import OrderedList


DefaultFile="compounds.dat"


class Record(Base.Record):
    RecordClass="Compound"
    def __init__(self,id,**kwargs):
        Base.Record.__init__(self,id,**kwargs)
        self.EmpForm = {}
        self.Atoms = []
	self.Reactions = []

    def NewTag(self,tag,val):
        if tag == Tags.ChemForm:
            self.__NewAtoms__(val)
        Base.Record.NewTag(self,tag,val)

    def __NewAtoms__(self, val):
        AtomValue = val[1:-1].split()
        Atom =  AtomValue[0]
        if len(AtomValue) > 1:
            self.EmpForm[Atom] = int(AtomValue[1])
        else:
            self.EmpForm[Atom] = 1
        self.Atoms.append(Atom)

    def NumAtoms(self,atom):
        try:
            return  self.EmpForm[atom]
        except:
            return 0
 
    def AddReaction(self,reac):
	"""add a reaction this compound is involved with"""
        self.Reactions.append(reac)
        
    def GetReactions(self):
	"""get a list of reactions this metabolite is involved in"""
        return list(set(self.Reactions))

    def GetParents(self):
        " return reaction UIDs that produce or consume this compound "

        # parent types (reactions) are not present in compound records
        # so we generate them on the fly

        try:
            return self.Parents[:]
        except:
            assocs = self.Org.GetAssocs(self.UID)
            uids = []
            self.Parents = []
            for a in assocs:
                uid = a.UID
                if self.Org.WhereIs(uid) == "Reaction" and not uid in uids:
                    self.Parents.append(a)
                    uids.append(uid)
            return self.Parents[:]

    @property
    def Formula(self):
        """ return molecular formula of compound """
        ef = dict(self.EmpForm)
        formula = ''
        if 'C' in ef:
            formula += 'C' + str(ef['C'])
            del ef['C']
        if 'H' in ef:
            formula += 'H' + str(ef['H'])
            del ef['H']
        for atom in sorted(ef.iterkeys()):
            formula += atom + str(ef[atom])
        return formula

    @property
    def Charge(self):
        charge = 0
        atom_charges = self.get(Tags.AtomCharge, [])
        for atom in atom_charges:
            charge += int(atom[1:-1].split()[1])
        return charge

    #def TravParents(self,GetParents=None):
    #    gp = Record.GetParents
    #    return Base.Record.TravParents(self, GetParents=gp)



class DB(Base.DB):
    def __init__(self, path=Base.DefaultPath, file=DefaultFile, RecClass=Record, **kwargs):
        Base.DB.__init__( self,  path, file, RecClass=Record,**kwargs)

        self.MassList = []
        self.MassDic = {}

        for compound in self.values():
            if compound.has_key(Tags.MolWt):
                try:
                    mw = float(compound[Tags.MolWt][0])
                except:
                    print "! Bad MW, ", compound[Tags.MolWt], " for ", str(compound)
                    mw = -1
                OrderedList.Insert(self.MassList, mw)
                if self.MassDic.has_key(mw):
                    self.MassDic[mw].append(compound)
                else:
                    self.MassDic[mw] = [compound]

    def MWSearch(self, targ,lo,hi):

        print targ,lo,hi
        res =  self.InMassRange(targ+lo, targ+hi)
        print res
        return res
        
    def NearestByMass(self, m):
        idx = OrderedList.FindNearest(self.MassList, m)
        return self.MassDic[self.MassList[idx]]

    def InMassRange(self,lo,hi):
        if lo > hi: lo,hi = hi,lo
        lidx = OrderedList.FindNearest(self.MassList,lo)
        hidx = OrderedList.FindNearest(self.MassList,hi)

        if self.MassList[hidx] > hi: hidx -= 1
        if self.MassList[lidx] < lo: lidx += 1

        rv = []
        span = self.MassList[lidx:hidx+1]
        for i in span:
            rv += self.MassDic[i]
        return rv
        
        
    def AtomImbal(self, StoDic):
        """ NET atomic stochiometry described by the dictionary StoDic.
            Will try to handle bad names gracefully.
            rv is a dictionary unbalanced atoms to coeffs.
        """
            
        rv = {}
  
        for s in StoDic:
                        
            coeff = StoDic[s]
            if not self.has_key(s):
                empform = {"Unknown compound " +s:coeff}
            else:
                empform = self[s].EmpForm
                if empform == {}:
                    empform = {"Unknown composition "+s:coeff}

            for atom in empform:
                natoms = coeff * empform[atom]
                if rv.has_key(atom):
                    rv[atom] += natoms
                else:
                    rv[atom] = natoms

      
        for k in rv.keys():
            if rv[k] == 0:
                del rv[k]

        return rv
                
                
        
        

        



        


   
        
        
            
#
