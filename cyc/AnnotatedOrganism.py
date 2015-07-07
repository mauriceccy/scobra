import types
import Annotate
import Organism

DefaultPath= Organism.Base.DefaultPath #'/home/unni/.ScrumPy/PyoCyc/testorg/'

class AnnotatedOrganism(Organism.Organism):

    def __init__(self, *args, **kwargs):

        Organism.Organism.__init__(self, *args, **kwargs)
        
        AnnoDir = "/".join((self.path, Annotate.DefaultDir))
        AnnoFile= self.data+".dat"
        
        self.AnnoDB = adb = Annotate.DB(path=AnnoDir, file=AnnoFile)
        
        for id in adb.keys():
            if self.has_key(id):
                self[id].Anno = adb[id]
 
    
    def HasAnnotation(self,id):
        return hasattr(self[id], "Anno")
          
    def AddAnnotation(self, id, AnnoDat={}):
        """
        pre:  True
                AnnoDat = {'a' : ['annotation']}
        post: Annotations db[id] updated with AnnoDat (db[id] created if not already present.)
        """

        if not self.HasAnnotation(id):
            self[id].Anno = self.AnnoDB[id] = Annotate.Record(id)

        self.AnnoDB[id].update(AnnoDat)    
     
    def AddToField(self, id, fkey,  contents):
        """ pre: self[id].Anno.has_key(fkey)
           post: contents appended to self[id][fkey]
        """
        ann = self.AnnoDB[id]
        ann[fkey].append(contents)

    def DelField(self, id, fkey):
        """ pre: self[id].Anno.has_key(fkey)
           post: not AnnoDB[id].has_key(fkey) """
        del self.AnnoDB[id][fkey]

    def DelAnnotation(self, id):
        """ pre:  self.HasAnnotation(id)
           post: not self.HasAnnotation(id)
        """
        del self.AnnoDB[id]
        delattr(self[id], "Anno")
        

    def SaveAnnotations(self, file = None, message = ''):
	"""
	   Pre: True
	"""

        if file != None:
            self.AnnoDB.SaveDBToFile(file)
        else:
            self.AnnoDB.Save(message)

#
