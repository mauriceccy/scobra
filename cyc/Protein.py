

import Base, Tags

DefaultFile="proteins.dat"



class Record(Base.Record):
    ChildFields=[Tags.Cats,Tags.CompOf]
    ParentFields=[Tags.Gene, Tags.Comps]
    RecordClass="Protein"
    
       
    
class DB(Base.DB):
    def __init__(self,path=Base.DefaultPath, file=DefaultFile, RecClass=Record, **kwargs):
        Base.DB.__init__(self,
                         path=path,
                         file=DefaultFile,
                         RecClass=Record,
                         **kwargs)
    
    
#
