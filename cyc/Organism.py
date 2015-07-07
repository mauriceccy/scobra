##Organism.py
##defines the class Organism to integrate the various BioCyc databases

import types

import Base, Tags

import Reaction,  Regulation, Transunit, Regulon, Enzrxn,  Compound, Protein, Gene, Pathway, Types
import Promoter
BasicModules = [
    Reaction,
    Enzrxn,
    Compound,
    Protein,
    Gene,
    Pathway,
    Types
]

ExtendedModules = [
    ## Gene regulation and related
    ## Experimental
    Regulation,
    Promoter,
    Transunit,
    Regulon
]



import Transporter # transporters are a special case

try:
    import ScrumPy
    ScrumPy.Init(Batch=1)
except:
    pass  # only for devel/bebug

key, assoc = "key", "assoc"
exact, sub,  super = "exact", "sub", "super"

def _IsSuper(s1, s2):
    return s1.find(s2) != -1

def _IsSub(s1, s2):
    return s2.find(s1) != -1


def Pass(*foo,**bar):
    pass

def Rep(a,b):
    print a, b

class Organism:
    def __init__(self, path=Base.DefaultPath,data="MetaCyc",ModDBRep=Rep,DBRecRep=Pass, UseExtended=False, Typed = True):
        self.data=data
        self.path=path
        m = self.Missing = {}
        self.DBs = [m]
        self.DBdic = {"Missing":m}
        self.Assocs = {}
        self.AssocXref = {}

        Modules=BasicModules
        if UseExtended:
            Modules += ExtendedModules

        for Mod in Modules:
            dbname = Mod.__name__.split(".")[-1:][0]

            db = Mod.DB(path=path+data,Org=self,RecRep=DBRecRep)
            setattr(self, dbname, db)
            self.DBs.append(db)
            self.DBdic[dbname] =db
            ModDBRep(1, dbname)

        if '# MetaCyc\n' in self.Reaction.Comments: # not a specific organism, try to pick up any non-biocyc reactions
            ExtraReacs = Reaction.DB(path=path, file = "ExtraReacs.dat")
            self.DBs.append(ExtraReacs)
            self.DBdic["ExtraReacs"] = ExtraReacs



#        self.tx = Transporter.DB(path=path,Org=self) # these copy themselves into the Reaction db, can discard tx
                                                                              # hang on to tx for testing
        self.AssocXref = {}    # AssocXref gets huge, and never need it again, leave empty in case something tries to look for it
        if Typed:
            self.Typify()

    def Typify(self):
	"""generate the Type associations"""
        for db in self.DBs:
            for item in db.keys():
                if "TYPES" in db[item].Attributes:
                    try:
                        for Type in db[item]["TYPES"]:
                            self[Type].AddInstance(db[item])
                    except:
                        pass

    def __getitem__(self,k):
        for db in self.DBs:
            if db.has_key(k):
                return db[k]
        return []


    def has_key(self,k):
        for db in self.DBs:
            if db.has_key(k):
                return True
        return False

    def keys(self):
        rv = []
        for db in self.DBs:
            rv += db.keys()
        return rv



    def AddAssoc(self, keys, record):
        uid = record.UID
        for key in keys:
            ku = key+uid
            if not self.AssocXref.has_key(ku):                             # only consider new key/uid combinations
                self.AssocXref[ku] = 1
                if self.Assocs.has_key(key):
                    self.Assocs[key].append(record)
                else:
                    self.Assocs[key] = [record]


    def StrSearch(self, targ="", stype=key, opt=exact):

        rv = []
        if stype==assoc:
            targ = targ.upper()

        dic = {
            key:self,
            assoc:self.Assocs
        }[stype]

        if opt == exact:
            if stype ==key:
                rv = [dic[targ]]
            else:
                rv += dic[targ]
        else:
            fun  = {
                super:_IsSuper,
                sub:_IsSub
            }[opt]

            for k in dic.keys():
                if fun(targ,k):
                    result = dic[k]
                    if type(result)==types.ListType:
                        rv+= result
                    else:
                        rv.append(dic[k])

        return rv


    def GetAssocs(self,key):

        k = key.upper()
        rv = {}
        if self.Assocs.has_key(k):
            rv = self.Assocs[k]
        else:
            self.Assocs[k] = rv

        return rv

    def SearchAssocs(self,targ): # deprecated - use Search

        rv = []
        targ = targ.upper()

        for item in self.Assocs.items():
            if item[0].find(targ) != -1:   # item[0] is the key
                rv += item[1][:]               # item[1] is the "value"
        return rv

    def FieldSearch(self, targ, Fields=["UNIQUE-ID"],dbs="All",SubStr=False):
        if dbs == "All":
            dbs=self.DBdic.keys()

        rv = []
        targ = targ.upper()
        for db in dbs:
            for rec in self.DBdic[db].values():
                for f in Fields:
                    if rec.has_key(f):
                        fvals = rec[f]
                        if f == "UNIQUE-ID":
                            fvals = [fvals]
                        fvals = map(lambda x:x.upper(),fvals)
                        if SubStr:
                            fvals = " ".join(fvals)

                        if targ in fvals:
                            rv.append(rec)
                            break

        return rv





    def Print(self,list):

        for item in list:
            print self[item]


    def WhereIs(self,key):
        try:
            return self[key].RecordClass
        except:
            return "Nowhere"

    def Gene2Path(self,gene):
        if type(gene) == types.StringType:
            gene = self[gene]

        cs = gene.TravChildren()
        ps = []
        for c in cs:
            if c.RecordClass == "Pathway":
                ps.append(c)
        return ps


    def Gene2Reac(self, gene):
        if type(gene) == types.StringType:
            gene = self[gene]

        cs = gene.TravChildren()
        rs = []
        for c in cs:
            if c.RecordClass == "Reaction":
                rs.append(c)
        return rs

    def GetGenes(self, targ):
        if type(targ) == types.StringType:
            targ = self[targ]

        ps = targ.TravParents()
        gs = []
        for p in ps:
            if p.RecordClass == "Gene":
                gs.append(p)
        return gs


    def ToScrumPy(self, FileName):

        file = open(FileName, "w")

        file.write("Structural()\nElType(int)\n")

        for r in self.Reaction.values():
            if len(r[Tags.Left])>0  and len(r[Tags.Right])>0:
                file.write(r.AsScrumPy())

        file.close()
        return ScrumPy.Model(FileName)



#
