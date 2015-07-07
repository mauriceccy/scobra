import Base, Tags

DefaultFile="pathways.dat"

class Record(Base.Record):
    ParentFields = [Tags.ReacList]
    ChildFields = [Tags.SuPath]
    RecordClass="Pathway"


class DB(Base.DB):
    def __init__(self,path=Base.DefaultPath,**kwargs):
        Base.DB.__init__(
            self,
            path=path,
            file=DefaultFile,
            RecClass=Record,
            **kwargs
        )
#
