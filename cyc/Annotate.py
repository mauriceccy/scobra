import types, os
import Base, Tags
import SvnClient

DefaultFile="annotations.dat"
DefaultDir= "Annotations"

class Record(Base.Record):

    RecordClass="Annotations"

    def ModifyField(self, id, contents):

        id = id.upper()
        if id == Tags.UID:
            print "not modifying ", id, "!!"
        elif id not in self.keys():
            print "the id ", id, " cannot be found"
        elif contents == "":
            print "no contents specified to modify ", id
        else:
            if type(contents) != types.ListType:
                contents = [contents]
            self[id] = contents
            
    def AddToField(self, id, contents):

        id = id.upper()
        if type(contents) != types.ListType:
                contents = [contents]

        self[id].extend(contents)
        

    def AddNewField(self, id, contents):

        id = id.upper()

        if self.has_key(id):
            print "not adding duplicate UID ", id, "to", self.UID
        else:
            if type(contents) != types.ListType:
                contents = [contents]

            self[id] = contents

    def SaveStr(self):
        return str(self) + Tags.RecEnd + "\n"
        

    def DelField(self, id):
        if id == Tags.UID:
            print "not removing UID ", id ,"!!"
        else:
            del self[id]

   
  
class DB(Base.DB):

    def __init__(self, path=Base.DefaultPath, file=DefaultFile, RecClass=Record, **kwargs):
        Base.DB.__init__(self,  path, file, RecClass=Record,**kwargs)
        
        self.path = path
        self.file = os.sep.join((path, file))
        self.svn = SvnClient.SvnClient(path)

    def SaveDBToFile(self, file):

        if  type(file) == types.StringType:
            file = open(file, "w")

        for rec in self:
            file.write(self[rec].SaveStr())

    def Save(self, message):

        self.SaveDBToFile(self.file)
        # Commiting to the database
        rv = self.svn.Commit(message)
        return rv

#
