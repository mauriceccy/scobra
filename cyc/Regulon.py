
import Base, Tags

DefaultFile="regulons.dat"



class Record(Base.Record):

    ChildFields=[Tags.CompOf, Tags.Regulates]
    ParentFields=[Tags.Comps, Tags.RegBy ]
    RecordClass = "Regulon"


class DB(Base.DB):
    def __init__(self,path=Base.DefaultPath, file=DefaultFile, RecClass=Record, **kwargs):
        Base.DB.__init__(self,
                         path=path,
                         file=DefaultFile,
                         RecClass=Record,
                         **kwargs)

#
