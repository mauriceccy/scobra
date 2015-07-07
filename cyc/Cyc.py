import os

def ReactionGeneAssociation(sm,rawsm=None,isos=None,db=None,compartment=True):
    sm.DeQuote()
    db = SetUpDB(db)
    if rawsm == None:
        rawsm = MakeAll(db=db)
        SubstMets(rawsm)
        os.remove("temp.spy")
    if isos == None:
        isos = GetAllIsoforms(rawsm,True)
    rv = rgdict()
    for reac in sm.cnames:
        if compartment:
            tempreac = reac.split("_")[0]
        genes = GetAllGenes(rawsm,tempreac,isos,db,AsString=False)
        rv[reac] = genes
    return rv




##def GeneReactionToFile(grdict,filename="GeneReactionAssociation.xls"):
##    outstring = ""
##    for reac in grdict.keys():
##        genes = str(grdict[reac])[1:-1]
##        genes = genes.replace("'","")
##        outstring = outstring + reac + "\t" + genes + "\n"
##    outfile = open(filename,'w').write(outstring)
##
##def UniqueGenes(grdict):
##    rv = []
##    for reac in grdict.keys():
##        for gene in grdict[reac]:
##            if gene not in rv:
##                rv.append(gene)
##    return rv
##
##def ReactionsWithGenes(grdict):
##    rv = []
##    for reac in grdict.keys():
##        if grdict[reac] != []:
##            rv.append(reac)
##    return rv


def UnwantedCompounds(sm, db=None):
    SetUpDB(db)
    missing = []
    unknown = []
    for met in sm.rnames:
        if aracyc.Compound.has_key(met):
            if aracyc[met].EmpForm == {}:
                unknown.append(met)
        else:
            missing.append(met)
    return (unknown,missing)


def FindImBal(sm, db=None):
    ibs = {"Missing":{}, "Unknown":{}, "Bad":{}}
    for r in sm.cnames:
        if ("(NAD)" not in r) and ("(NADP)" not in r): # ie been through FixNads()
            ar = r[1:-1]
            ib = aracyc[ar].ImBal()
            if len(ib) > 0:
                allk = "".join(ib.keys())
                if "Missing" in allk:
                    ibs["Missing"][r] = ib
                elif "Unknown" in allk:
                    ibs["Unknown"][r] = ib
                else:
                    ibs["Bad"][r] = ib
    return ibs


def GetAllIsoforms(sm,SingleList=False):
    newsm = sm.Copy()
    newsm.DeQuote()
    if 'WATER' in newsm.rnames:
        newsm.DelRow('WATER')  # make sure that reactions that only differ in these two
    if 'PROTON' in newsm.rnames:
        newsm.DelRow('PROTON') # get seen as isostoichiometric
    if SingleList == False:
        isos = newsm.FindIsoforms()
    else:
        stodic = {}
        for reac in newsm.cnames:
            strcol = str(newsm.GetCol(reac))
            if stodic.has_key(strcol):
                stodic[strcol].append(reac)
            else:
                stodic[strcol] = [reac]
        isos = []
        for reac in stodic.values():
            if len(reac)>1:
                for r in reac:
                    r.replace("\"","")
                    isos.append(r)
    return isos


def GetIsoforms(sm,reac):
    newsm = sm.Copy()
    newsm.DeQuote()
    newsm.DelRow('WATER')  # make sure that reactions that only differ in these two
    newsm.DelRow('PROTON') # get seen as isostoichiometric
    rv = []
    col = newsm.GetCol(reac)
    for r in newsm.cnames:
        if newsm.GetCol(r) == col:
            rv.append(r)
    return rv


def CheckBal(m,atoms=["C","N","S","P","O"],ReportUnknown=False,db=None,exceptions=[]):
    m.sm.DeQuote()
    db = SetUpDB(db)

    imbs = {}
    nonara = ReportNonAra(m,db)
    checked = Substitutes.ImBal
    for reac in m.sm.cnames:
        if not reac.endswith("--TRNA-LIGASE-RXN"):
            if reac not in exceptions:
                if reac.endswith("-(NAD)"):
                    reac = reac[:-6]
                elif reac.endswith("-(NADP)"):
                    reac = reac[:-7]
                if reac not in nonara:
                    if reac not in Substitutes.ImBal:
                        imb = db[reac].ImBal()
                        if ReportUnknown or  "Unknown" not in "".join(imb.keys()):
                            for k in imb.keys():
                                if imb[k] ==0 or not k in atoms:
                                    del imb[k]
                            if len(imb) >0:
                                imbs[reac] = imb
    return imbs


def GetAllGenes(sm,reac,isos=None,db=None,DeQuote=False,AsString=True):
    if reac.endswith("_tx"):
        pass #print reac
    else:
        if isos == None:
            reacs = GetIsoforms(sm,reac)
        else:
            if reac in isos:
                reacs = GetIsoforms(sm,reac)
            else:
                reacs = [reac]
        genedic = FindGenes(reacs,db,DeQuote,IncEmpty=False)
        #print str(len(genedic))+" reaction(s)"
        #print reac
        genes = []
        for reac in genedic.keys():
            for gene in genedic[reac]:
                if gene not in genes:
                    genes.append(gene)
        if AsString:
            rv = str(genes)[1:-1]
            rv = rv.replace("'","")
        else:
            rv = genes
        return rv


def FindGenes(reacs,db=None,DeQuote=False,IncEmpty=True):
    db = SetUpDB(db)
    genedic = {}
    for reac in reacs:
        if DeQuote:
            reac = reac[1:-1]
        if reac.endswith("-(NAD)"):
            reac = reac[:-6]
        elif reac.endswith("-(NADP)"):
            reac = reac[:-7]
	if db.has_key(reac):
	    if db.GetGenes(reac) != []:
                genedic[reac] = db.GetGenes(reac)
            else:
                if IncEmpty:
                    genedic[reac] = []
        else:
            if IncEmpty:
                genedic[reac] = []
    return genedic



class rgdict(dict):

    def __init__(self):
        pass

    def ToFile(self,filename="ReactionGeneAssociation.xls"):
        outstring = ""
        for reac in self.keys():
            genes = str(self[reac])[1:-1]
            genes = genes.replace("'","")
            outstring = outstring + reac + "\t" + genes + "\n"
        open(filename,'w').write(outstring)

    def GenesAsStr(self):
        rv = rgdict()
        for reac in self.keys():
            genelist = []
            for gene in self[reac]:
                genelist.append(gene.UID)
            rv[reac] = genelist
        return rv

    def UniqueGenes(self):
        rv = []
        for reac in self.keys():
            for gene in self[reac]:
                if gene not in rv:
                    rv.append(gene)
        return rv

    def ReactionsWithGenes(self):
        rv = []
        for reac in self.keys():
            if self[reac] != []:
                rv.append(reac)
        return rv

    def GeneProteinAssociation(self,genes=None):
        if genes == None:
            genes = self.UniqueGenes()
        rv = rgdict()
        for gene in genes:
            rv[gene.UID] = gene.GetChildren()
        return rv

    def UniqueProteins(self,gpdict=None):
        if gpdict == None:
            gpdict = self.GeneProteinAssociation()
        rv = []
        for gene in gpdict.keys():
            for protein in gpdict[gene]:
                if protein not in rv:
                    rv.append(protein)
        return rv

    def ProteinReactionAssociation(self,proteins=None):
        if proteins == None:
            proteins = self.UniqueProteins()
        rv = rgdict()
        for protein in proteins:
            rv[protein.UID] = protein.GetReactions()
        return rv

    def GeneReactionAssociation(self,genes=None):
        if genes == None:
            genes = self.UniqueGenes()
        rv = rgdict()
        for gene in genes:
            rv[gene.UID] = gene.GetReactions()
        return rv


    def ReactionProteinAssociation(self,gpdict=None):
        if gpdict == None:
            gpdict = self.GeneProteinAssociation()
        rv = {}
        for reac in self.keys():
            genes = self[reac]
            proteins = []
            for gene in genes:
                geneproteins = gpdict[gene.UID]
                for protein in geneproteins:
                    if protein not in proteins:
                        proteins.append(protein)
            rv[reac] = proteins
        return rv

    def ProteinGeneAssociation(self,proteins=None):
        if proteins == None:
            proteins = self.UniqueProteins()
        rv = rgdict()
        for protein in proteins:
            rv[protein.UID] = protein.GetParents()
        return rv
