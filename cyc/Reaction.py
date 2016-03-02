from collections import defaultdict
import Base
import Tags
from ECEquivs import ECEquivs

DefaultFile = "reactions.dat"

from lexer import t_Irrev,  t_BackIrrev,  t_Rever

DirecMap = {
    'IRREVERSIBLE-RIGHT-TO-LEFT' : t_BackIrrev,
    'PHYSIOL-RIGHT-TO-LEFT'      : t_BackIrrev,
    'LEFT-TO-RIGHT'              : t_Rever,
    'REVERSIBLE'                 : t_Rever,
    'RIGHT-TO-LEFT'              : t_BackIrrev,
    'IRREVERSIBLE-LEFT-TO-RIGHT' : t_Irrev,
    'PHYSIOL-LEFT-TO-RIGHT'      : t_Irrev
}
## Better to define these strings as consdtants in Tags ??
DefaultDirec = DirecMap['LEFT-TO-RIGHT']


class Record(Base.Record):
    ParentFields=[Tags.EnzReac]
    ChildFields = [Tags.Left, Tags.Right, Tags.InPath]
    RecordClass="Reaction"
    def __init__(self, id,BadCoeffs=[],**kwargs):
        Base.Record.__init__(
            self,
            id,
            **kwargs)
        self.lhs = []
        self.rhs = []
        self[Tags.Left] = []
        self[Tags.Right] = []

###        self.CoeffDic={}
        self.CoeffDic = defaultdict(int)
        self.CurMet = ""
        self.CurDirec = ""
        self.BadCoeffs =BadCoeffs  # add our self to this list if we have bad coeffs, eg substrate is polymer

    def __AddLeft__(self, met):
        self.CoeffDic[met] += -1
        self.lhs.append(met)
	#create the reaction association for the added compound. 
	comp = met[:]
	#eliminate surrounding pipes, as they are not part of the actual identifier
	if met.startswith("|"):
            comp = met[1:-1]

        if comp in self.Org.keys():
            try:
                self.Org[comp].AddReaction(self)
            except:
                print "Could not add "+ self.UID + "to the reactions involving "+ met 

    def __AddRight__(self, met):
        self.CoeffDic[met] += 1
        self.rhs.append(met)
	#create the reaction association for the added compound. 
	comp = met[:]
	#eliminate surrounding pipes, as they are not part of the actual identifier
	if met.startswith("|"):
            comp = met[1:-1]

        if comp in self.Org.keys():
            try:
                self.Org[comp].AddReaction(self)
            except:
                print "Could not add "+ self.UID + "to the reactions involving "+ met 

    def __AddCoeff__(self, k):
        if self.CurDirec=="LEFT":
            self.CoeffDic[self.CurMet] -= (k-1)
        elif self.CurDirec=="RIGHT":
            self.CoeffDic[self.CurMet] += (k-1)

    def NewTag(self, tag, val):
        if tag == Tags.Left:
            self.CurDirec="LEFT"
            self.CurMet=val
            self.__AddLeft__(val)
        elif tag == Tags.Right:
            self.CurDirec="RIGHT"
            self.CurMet=val
            self.__AddRight__(val)
        elif tag == Tags.Coeff:
            try:
                k = int(val)
                self.__AddCoeff__(k)
            except:
                self.BadCoeffs.append(self)
###            try:
###                self.__AddCoeff__(val)
###            except:
###                self.BadCoeffs.append(self)
        elif tag == Tags.Compartment:
###            self.CurMet += '__' + val
            pass
        Base.Record.NewTag(self,tag,val)



    def strhs(self, side):
        if side ==[]:
            return "NOTHING"
        met = side[0]
        coeff =  abs(self.CoeffDic[met])
        if coeff == 1:    # coeff of first met = 1 ?
            rv = '"'+met+'"'     #  yes - just keep the met not the 1
        else:
            rv = str(coeff) + ' "' + met+'"'   # no - record the coeff and the met

        for met in side[1:]:    # do the same on the rest
            coeff =  abs(self.CoeffDic[met])
            if coeff ==1:
                rv +=' + "' + met +'"'
            else:
                rv += " + " + str(coeff) + '  "' + met +'"'
        return rv

    def AsScrumPy(self,Prep=""):

        Name = "".join(['"',Prep,self.UID,'":'])
        RevCom = ""
        Indent = " "*4
                        
        if self.lhs==[] or self.rhs==[]:
            print "Warning :", self.UID, " has missing reactants(s)"

        lhs = self.strhs(self.lhs)
        rhs = self.strhs(self.rhs)
        Direc = DefaultDirec

        if self.has_key(Tags.ReacDir):
            Rev =  self[Tags.ReacDir][0]
            RevCom= "".join([Indent,"#",Rev])
            if DirecMap.has_key(Rev):
                Direc = DirecMap[Rev]
            else:
                print " ".join(["!! Warning:", Name,  "has unknown",  Tags.ReacDir,  "using",  Direc,  "!!"] )


        Stoich = "".join([Indent, lhs, Direc, rhs])
        Kins = Indent + "~"

        return "\n".join([Name, Stoich, Kins,  RevCom,  "\n"])


    def __str__(self):
        keys = self.keys()
        keys.remove(Tags.UID)
        rv = Base.Field2Str(Tags.UID, self[Tags.UID])
        for k in keys:
            if k not in [Tags.Coeff, Tags.Right,Tags.Left]:  # The order matters for these so do themseperately
                rec = self[k]
                for r in rec:
                    rv += Base.Field2Str(k, r)

        for left in self[Tags.Left]:
           rv += Base.Field2Str(Tags.Left, left)
           if self.CoeffDic.has_key(left):
               rv += Base.Field2Str(Tags.Coeff, self.CoeffDic[left])

        for right in self[Tags.Right]:
           rv += Base.Field2Str(Tags.Right, right)
           if self.CoeffDic.has_key(right):
               rv += Base.Field2Str(Tags.Coeff, self.CoeffDic[right])

        try:
            cat = Base.TabStrFormat("Catalyses", self.strhs(self.lhs) + " -> " + self.strhs(self.rhs))
        except:
            cat = ""
        return rv + cat

    def AtomSto(self, side):
        """pre: side == Tags.Left' || side ==  Tags.Right
          post: AtomSto => dictionary of atomic stoichiometry of l or r hs """

        rv = {}
        if not self.has_key(side):
            return rv
        for comp in self[side]:
            if comp[0] == "|":
                c2=comp[1:-1]
                self.CoeffDic[c2]=self.CoeffDic[comp]
                comp=c2
            if self.Org.Compound.has_key(comp):
                atoms = self.Org.Compound[comp].EmpForm
                coeff = abs(self.CoeffDic[comp])
                for k in atoms.keys():
                    if rv.has_key(k):
                        rv[k] +=  coeff *atoms[k]
                    else:
                        rv[k] = coeff*atoms[k]
            else:
                #print "!!! missing compound ", comp, " for reaction ", self[Tags.UID], " !!!"
                rv ["Missing "+ comp] = 1
        return rv


    def NetBal(self):
        BalDic = self.AtomSto(Tags.Left)
        right = self.AtomSto(Tags.Right)
        for k in right.keys():
            if BalDic.has_key(k):
                BalDic[k] -= right[k]
            else:
                BalDic[k] = -right[k]
        return BalDic

    def ImBal(self):
        bal = self.NetBal()
        for met in bal.keys():
            if bal[met]==0:
                del bal[met]
        return bal

    def GetEnzReacs(self, AsStr=False):
        if AsStr:
            return self[Tags.EnzReac]
        else:
            return self.GetParents()

    def GetProteins(self, AsStr=False):
        rv = []
        enzreacs = self.GetEnzReacs()
        for er in enzreacs:
            if AsStr:
                rv.extend(er.get(Tags.Enz, []))
            else:
                rv.extend(er.GetParents())
        return rv

    def GetGenes(self, AsStr=False):
        rv = []
        proteins = self.GetProteins()
        for p in proteins:
            if AsStr:
                rv.extend(p.get(Tags.Gene, []))
            else:
                rv.extend(p.GetParents())
        return rv

    def SubReactions(self):
        if Tags.ReacList in self.keys():
            return self[Tags.ReacList]

class DB(Base.DB):
    def __init__(self,
                 path=Base.DefaultPath,
                 file=DefaultFile,
                 RecClass=Record,
                 **kwargs):


        BadCoeffs = []

        Base.DB.__init__(
            self,
            path,
            file,
            RecClass=Record,
            BadCoeffs = BadCoeffs,
            **kwargs
        )

        self.ECNos = {}
        self.BadCoeffs = BadCoeffs                           # list of reactions for which coeff could not be dermined
        for reac in self.values():                   #  for every reaction
            if reac.has_key(Tags.EC):             # if that record has an EC field
                ec = reac[Tags.EC][0]               # get the ec number
                if self.ECNos.has_key(ec):        # have we seen this before ?
                    self.ECNos[ec].append(reac)    # yes, put it in with the others
                else:
                    self.ECNos[ec] = [reac]            # no, start a new list

        self.ExtraReacs = {}
        if '# MetaCyc\n' in self.Comments:     # if we are a metacyc db look for extra reactions
            self.ExtraReacs = DB(path=path, file="ExtraReacs.dat")


    def __getitem__(self,k):

        try:
            return Base.DB.__getitem__(self,k)    # is the key present ?
        except:
            try:
                return self.ECNos[k]                      # no - is it present as an ec number ?
            except:
                try:
                    return self.ECNos[ECEquivs[k]]    # no - can we get an equivalent ec number ?
                except:
                    try:
                        return self.ExtraReacs[k]            # finally, see if we have it in extra reacctions
                    except: return []


    def has_key(self, k):

        return len(self[k]) != 0 # yes, very icky - has_key and getitem need re-writing nicely


    def GoodBadBals(self):
        """ pre: True
          post: returns (good,bad) dictionaries of reactions wich do/not balance"""


        rv = ({},{})
        for k in self.keys():
            dic = 0
            bal = self[k].NetBal()
            for v in bal.values():
                if v != 0:
                    dic = 1
                    break
            rv[dic][k] = bal
        return rv

#
