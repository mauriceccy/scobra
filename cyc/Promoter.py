
import Base, Tags

DefaultFile="promoters.dat"

class Record(Base.Record):

    ChildFields=[Tags.CompOf]
    ParentFields=[Tags.RegBy]
    

    RecordClass = "Promoter"

    def Finished(self):
        for f in Record.ChildFields + Record.ParentFields:
            if not self.Attributes.has_key(f):
                self.Attributes[f] = [Tags.NR] 
                


class DB(Base.DB):
    def __init__(self,path=Base.DefaultPath, file=DefaultFile, RecClass=Record, **kwargs):
        Base.DB.__init__(self,
                         path=path,
                         file=DefaultFile,
                         RecClass=Record,
                         **kwargs)

#
