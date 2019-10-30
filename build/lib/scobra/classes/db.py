from ..cyc import Organism
from ..cyc.BuildModel import BuildRawModelFromDB

class db(Organism):
    def __init__(self, path, *args, **kwargs):

        if '\\' in path:
            path.replace('\\','/')
        if path.endswith('/'):
            path = path[:-1]
        if '/' in path[:-1]:
            path, data = path.rsplit('/', 1)
            path += '/'
        else:
            data = str(path)
            path = ''

        Organism.__init__(self, path=path, data=data, *args, **kwargs)

    @property
    def reactions(self):
        return list(self.Reaction.values())

    @property
    def compounds(self):
        return list(self.Compound.values())

    @property
    def genes(self):
        return list(self.Gene.values())

    @property
    def proteins(self):
        return list(self.Protein.values())

    @property
    def enzrxns(self):
        return list(self.Enzrxn.values())

    @property
    def pathways(self):
        return list(self.Pathway.values())

    def Reactions(self, f=None):
        reacs = list(self.Reaction.keys())
        if f:
            for reac in reacs:
                if f not in reac:
                    reacs.remove(reac)
        return reacs

    def Compounds(self, f=None):
        cpds = list(self.Compound.keys())
        if f:
            for cpd in cpds:
                if f not in cpd:
                    cpds.remove(cpd)
        return cpds

    def Genes(self, f=None):
        gs = list(self.Gene.keys())
        if f:
            for g in gs:
                if f not in g:
                    gs.remove(g)
        return gs

    def Proteins(self, f=None):
        prots = list(self.Protein.keys())
        if f:
            for prot in prots:
                if f not in prot:
                    prots.remove(prot)
        return prots

    def Enzrnxs(self, f=None):
        ers = list(self.Enzrxn.keys())
        if f:
            for er in ers:
                if f not in er:
                    ers.remove(er)
        return ers

    def Pathways(self, f=None):
        ps = list(self.Pathway.keys())
        if f:
            for p in ps:
                if f not in p:
                    ps.remove(p)
        return ps

    def CompoundFormula(self, compound, IncCharge=True):
        formula = self.Compound[compound].EmpForm
        if IncCharge:
            charge = 0
            if self.Compound[compound].has_key('ATOM-CHARGES'):
                for a in self.Compound[compound]['ATOM-CHARGES']:
                    charge += int(a[1:-1].split(' ')[1])
            formula['Charge'] = charge
        return formula

    def CompoundsFormulae(self, IncCharge=True, f=None):
        rv = {}
        for c in self.Compounds(f=f):
            rv[c] = self.CompoundFormula(c, IncCharge=IncCharge)
        return rv

    def BuildModel(self):
        return BuildRawModelFromDB(self)

    def GroupReactions(self):
        rv = {}
        for r in self.reactions:
            if r.SubReactions():
                rv[r.UID] = r.SubReactions()
        return rv