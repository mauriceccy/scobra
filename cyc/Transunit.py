
import Base, Tags

DefaultFile="transunits.dat"

# Every record will a regulator (ie the agent that acts to regulate something)
# A regulated entity acted upon by the regulator
# And a mode indicating + or - regulation


class Record(Base.Record):

    ChildFields=[Tags.Comps]
    ParentFields=[Tags.CompOf, Tags.RegBy]
    

    RecordClass = "Transunit"

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
