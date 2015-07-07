
import Base, Tags

DefaultFile="regulation.dat"

NR = ["Not reported"]
Compulsory = {
    Tags.Regul   : NR,
    Tags.RegEnt  : NR,
    Tags.RegMode : NR
}
# Every record will a regulator (ie the agent that acts to regulate something)
# A regulated entity acted upon by the regulator
# And a mode indicating + or - regulation


class Record(Base.Record):

    ChildFields=[Tags.RegEnt]
    ParentFields=[Tags.Regul ]

    RecordClass = "Regulation"

    def Finished(self):
        for k,v in Compulsory.items():
            if not self.Attributes.has_key(k):
                self.Attributes[k] = v
                


class DB(Base.DB):
    def __init__(self,path=Base.DefaultPath, file=DefaultFile, RecClass=Record, **kwargs):
        Base.DB.__init__(self,
                         path=path,
                         file=DefaultFile,
                         RecClass=Record,
                         **kwargs)

#
