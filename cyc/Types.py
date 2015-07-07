import Tags,Base

import Compound,Reaction

import sys



import OrderedList


DefaultFile="classes.dat"


class Record(Base.Record):
    ParentFields=[]
    ChildFields = []
    RecordClass="Classes"
    def __init__(self,id,BadCoeffs=[],**kwargs):
        Base.Record.__init__(self,id,**kwargs)
        self.Instances = set([])
        self.Reactions = []
        
    def NewTag(self,tag,val):
        Base.Record.NewTag(self,tag,val)

    def AddInstance(self,record):
        self.Instances.add(record)

    def AddReaction(self,reac):
        self.Reactions.append(reac)

    def GetReactions(self):
        return list(set(self.Reactions))
    
    def GetInstances(self):
        rv = []
        for instance in self.Instances:
            if isinstance(instance,Record):
                rv.extend(instance.GetInstances())
            rv.append(instance)
        return rv

class DB(Base.DB):
    def __init__(self, path=Base.DefaultPath, file=DefaultFile, RecClass=Record, **kwargs):

        #initialize for both Compound and Reaction infos
        BadCoeffs = []
        Base.DB.__init__(
            self,
            path,
            file,
            RecClass=Record,
            BadCoeffs = BadCoeffs,
            **kwargs
        )
        
        
        

    

                
        
