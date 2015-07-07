
import Base
import Tags

DefaultFile = "enzrxns.dat"


class Record(Base.Record):
    ParentFields = [Tags.Enz,Tags.Cats]
    ChildFields =[Tags.Reac]
    RecordClass = "Enzyme reaction"
    def __init__(self, id,**kwargs):
        Base.Record.__init__(self, id,**kwargs)

  

class DB(Base.DB):
    def __init__(self, path=Base.DefaultPath, file=DefaultFile, RecClass=Record, **kwargs):
        Base.DB.__init__(
            self,
            path,
            file,
            RecClass=Record,
            **kwargs
        )

    def Reaction(self, k):
        rv = []
        for r in self[k][Tags.Reac]:
            rv.append(self.Org.Reactions[r])
        return rv

    


        
        
    
    
#
