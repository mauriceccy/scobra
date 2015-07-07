
import Base, Tags
import OrderedList



DefaultFile="genes.dat"

class Record(Base.Record):
    ChildFields=[Tags.Prod]
    ParentFields=[Tags.CompOf]
    RecordClass = "Gene"

    def Finished(self):
        Base.Record.Finished(self)
        try:
            self.MidPos = (int(self[Tags.LeftEnd][0])+int(self[Tags.RightEnd][0]))/2
        except:
            self.MidPos = 0

class DB(Base.DB):
    def __init__(self,path=Base.DefaultPath,file=DefaultFile,**kwargs):
        Base.DB.__init__(self,path=path,file=file,RecClass=Record,**kwargs)

        ## create the gene position infomation

        self.PosList = []      # ordered list of mid positions
        self.PosDic = {}      # map positions -> UIDs
        self.GenList = []     # list of UIDs orderd by position on chromosome
        self.NoPosList = [] # list of UIDs of genes with no positional information
         
        for gene  in self.values():
            mp = gene.MidPos
            uid = gene.UID
            if mp ==0:
                self.NoPosList.append(uid)
            else:
                self.PosDic[mp] = uid   # we know that mps are unique, so don't check for multiples
                OrderedList.Insert(self.PosList, mp)

        for mp in self.PosList:
            self.GenList.append(self.PosDic[mp])



    def BPSearch(self, targ=0, lo=0, hi=0, targ_t="Mid"):   # search by base pair pos of midpoint
        geneidx = OrderedList.FindNearest(self.PosList,targ)
        gene = self.PosDic[self.PosList[geneidx]]
        uids =  self.Neighbours_b(gene, lo,hi)
        rv = []
        for uid in uids:
            rv.append(self[uid])
        return rv


    def GPSearch(self, targ=0, lo=0, hi=0,**ignore):
        
        lo = int(targ + lo)
        if lo < 0:
            lo = 0
            
        hi = int(targ+hi)
        if hi >= len(self):
            hi = len(self -1)

        rv = []
        for gene in self.GenList[lo:hi+1]:
            rv.append(self[gene])
        return rv
            


    def Neighbours_g(self, uid, lo, hi):
        "uids of neighbouring lo-hi genes, determined by gene order"

        def minmax(x, lolim,hilim):
            if x > hilim: return hilim
            if x < lolim: return lolim
            return x

        if lo >hi: lo,hi=hi,lo
        maxidx = len(self.PosList)-1
        idx = self.GenList.index(uid)
        top = minmax(idx+hi,0,maxidx)
        bot = minmax(idx+lo,0,maxidx)
      
        return self.GenList[bot:top+1]

    def Neighbours_b(self, uid, lo, hi):
        "uids of neighbouring lo-hi genes, determined by base pair"
        if lo >hi: lo,hi = hi,lo
        mp = self[uid].MidPos
        loidx = OrderedList.FindNearest(self.PosList,mp+lo)
        hiidx = OrderedList.FindNearest(self.PosList,mp+hi)
        rv = []
        
        for gene in self.PosList[loidx:hiidx+1]:
            rv.append(self.PosDic[gene])
        return rv


        
            







#
