import os, types, exceptions
import Tags


##DefaultPath = "/usr/local/share/bio/db/biocyc/"
DefaultPath = os.getcwd() + os.sep

def Pass(*foo,**bar):
    pass

def Field2Str(u,v="",sep = Tags.Delim):
  "field as a \n terminated string: u - UID, v - Value, sep - seperator between u and v"
  return u + sep + str(v) + "\n"


class Record:  # base class for BioCyc Records

    ChildFields = []
    ParentFields = []
    RecordClass = "Base" # these three should be defined by sub-classes

    def __init__(self, id,Org=None):
        # id is the biocyc unique id
        self.Attributes = {}
        self.Attributes[Tags.UID] = id
        self.UID = id
        self.Org = Org


    def __getitem__(self, k):
        return self.Attributes[k]

    def __setitem__(self, k, i):
        self.Attributes[k] = i

    def __getattr__(self, a):
        return getattr(self.Attributes, a)

    def __len__(self):
        return len(self.Attributes)

    def __str__(self):
        keys = self.keys()
        keys.remove(Tags.UID)
        rv = Field2Str(Tags.UID, self[Tags.UID])
        for k in keys:
            rec = self[k]
            for r in rec:
                rv += Field2Str(k, r)
        return rv

    def __repr__(self):
        return self[Tags.UID]

    def __cmp__(self,other):
	#if the other item is None, it is definitely not the same as a record!
	if other == None:
            return -1        
	if self.UID == other.UID:
            return 0
        if self.UID < other.UID:
            return -1
        return 1

    def __eq__(self,other):
	"""Define an equality to be able to distinguish using standard functions"""
        if other == None:
            return False
        if self.UID == other.UID:
            return True
        return False

    def __hash__(self):
        return self.UID.__hash__()

    def write(self, f):
        """ pre: f = (FileName, "w")
           post: contents of self written to FileName """

        f.write(str(self)+Tags.RecEnd+"\n")




    def ValStr2AssocKeys(self, ValStr):
        """ convert string val into a set of keys for the association dict.
            Subclasses can overload this to fine tune the keys that get into
            the assoc dic."""

        StripChars = ["(", ")", ",","'",'"',"\t", "=","<", ">","/","SUP","SUB"]
        rv = []

        for c in StripChars:
            ValStr = ValStr.replace(c, " ")
        Vals = ValStr.split()

        for Val in Vals:
            if not (Val[0].isdigit() and Val[-1].isdigit()): # if start and end with digit assume int or float - ignore
                if len(Val) >2:
                    rv.append(Val.upper())
        return rv



    def NewTag(self, tag,val):
        self.CurTag = tag
        try:
            self[tag].append(val)
        except:
            self[tag] = [val]
        if val !=None and self.Org != None:
            self.Org.AddAssoc(self.ValStr2AssocKeys(val), self)

    def ContTag(self,val):    # continue the current tag - needed in multiline fields
        self[self.CurTag].append(val)


    def Finished(self):
        """invoked when the end-of-record is read, sub-classes can overload this as needed """
        pass


    def GetTypes(self):
	"""Get all Types this entry belongs to. This includes supertypes of direct Types"""
        rv = []
        if Tags.Types in self.Attributes:
            for t in self[Tags.Types]:
              rv.append(t)
              if t in self.Org.keys():
                  rv.extend(self.Org[t].GetTypes())
        return list(set(rv))

    def GenChildren(self):
        self.Children = []
        for cf in self.ChildFields:
            if self.has_key(cf):
                for c in self[cf]:
                    if self.Org.has_key(c):
                        self.Children.append(self.Org[c])
                    else:
                        self.Org.Missing[c] = NRRecord(c)
                        self.Children.append(self.Org[c])


    # if a sublcass of Record overloads GetChildren, it must also overload TravChildren,
    # passing the new GetChildren to Base.Record.TravChildren, ditto GetParents/TravParents
    def GetChildren(self):
        try:
            return self.Children[:]
        except:
            self.GenChildren()
            return self.Children[:]


    def TravChildren(self):
        seen = {}
        return self.__travc(seen)


    def __travc(self, Seen):

        rv = []
        Seen[self.UID]=1
        for c in self.GetChildren():
            if not Seen.has_key(c.UID):     # prevent cyclic recursion
                rv.append(c)
                rv.extend(c.__travc(Seen))

        return rv

#EG10443
    def GenParents(self):

        self.Parents = []
        for pf in self.ParentFields:
            if self.has_key(pf):
                for p in self[pf]:
                    if self.Org.has_key(p):
                        self.Parents.append(self.Org[p])
                    else:
                        self.Org.Missing[p] = NRRecord(p)
                        self.Parents.append(self.Org[p])


    def GetParents(self):

        try:
            return self.Parents[:]
        except:
            self.GenParents()
            return self.Parents[:]





    def TravParents(self):
        Seen = {}
        return self.__travp(Seen)

    def __travp(self, Seen):

        rv = []
        Seen[self.UID]=1
        for p in self.GetParents():
            if not Seen.has_key(p.UID) :     # prevent cyclic recursion
                rv.append(p)
                rv.extend(p.__travp(Seen=Seen))
        return rv



# EG10864
    def MultiTrav(self, GoingUp=True, bounces=0):

        if GoingUp:
            rv = self.TravParents()
        else:
            rv = self.TravChildren()

        if bounces >0:
            rv2 = rv[:]
            for rec in rv2:
                if hasattr(rec,"MultiTrav"):
                    rv.extend(rec.MultiTrav(not GoingUp, bounces-1))
        return rv


    def Traverse(self, GetRels="GetParents", **kwargs):  # kwargs ignored at present
        """ pre: GetRels = ["GetParents" | "GetChildren"]
            post: returns a traversed tree in list form [Parent[Child]] in direction of GetRels"""

        rv = []
        rels = getattr(self, GetRels)()
        for r in rels:
           rv.append(r)
           try:
               more = r.Traverse(GetRels)
               if len(more) > 0:
                   rv.append(more)
           except:
               pass

        return rv

    def GetReactions(self):
      " get any reactions that are descendents of self "


      reacs = []
      next = []

      ch = self.GetChildren()
      for c in ch:
        if hasattr(c, "RecordClass"):
            if c.RecordClass=="Reaction":
              reacs.append(c)
            else:
                if c.RecordClass != self.RecordClass:
                    next.append(c)

      for n in next:
        reacs += n.GetReactions()
      return reacs


class NRRecord(Record):
    """ A recoeded to indicate expected, but missing (Not Reported) data """

    RecordClass = Tags.NR

    def __init__(self, *args, **kwargs):

        Record.__init__(self, *args, **kwargs)

        self.NewTag(Tags.Comment, Tags.NR)
        self.NewTag(Tags.Types, Tags.NR)





class DB:   # base class for BioCyc databases
    def __init__(self,
                 path,                            #  directory containing file
                 file,                              #  file in biocyc dat format
                 RecClass=Record,       #  what kind of record we contain (Base.Record or sub-class thereof)
                 RecRep=Pass,              #  invoke for each new record - optional - progress indicator etc.
                 **kwargs):


        self.Records = {}
        self.Comments = []
        self.Org = None
        self.RecClass=RecClass
        if kwargs.has_key("Org"):
            self.Org = kwargs["Org"]


        LineNo = 0
        if type(file) != types.FileType:
          try:
            file = open(path + os.sep + file)
          except:
            print "couldn't open ",path + os.sep + file, " this db will be empty"
            return

        for line in file.readlines():
            LineNo += 1
            if len(line)>0:
                if line[0] =="#" :            # comments on a per db basis
                    self.Comments.append(line)
                elif line[0:2] == "//":    # record seperator, ignore - we use UID to identify start of record
                    self.CurRec.Finished()
                elif line [0] == "/":        # continuation of a previously started field
                    self.CurRec.ContTag(line[1:].rstrip()) # add to current record removing leading "/" and trailing ws
                else:
                    tagval = line.rstrip().split(" - ",1)
                    tag = tagval[0]
                    if len(tagval) == 2:
                        val = tagval[1]
                    else:
                        val = None
                    if tag == Tags.UID:
                        self.CurRec = RecClass(val,**kwargs)
                        self.Records[val]=self.CurRec
                        RecRep()                  # report the creation of a new record, if anyone's interested
                    else:
                        RecClass.NewTag(self.CurRec,tag,val)

        if len(self.Comments) >0:
           self.Imported = self.Comments[0].rstrip() == Tags.Import
           if self.Imported:
               self.GetReactions = self.__iGetReactions
        else:
            self.Imported = False



    def __getitem__(self, k):
        return self.Records[k]

    def __getattr__(self, a):
        return getattr(self.Records,a)

    def __len__(self):
        return len(self.Records)

    def write(self, f):
        """ pre: f= open(FileName, "w")
           post: self written to file such that DB(FileName) is equivalent to self """

        for c in self.Comments:
            f.write(c)

        for r in self.values():
            self.RecClass.write(r,f)

    def Prune(self, fun, **kwargs):
        """ pre: bool fun(record, **kwargs)
           post: fun(record, **kwargs) => record not in self' """

        for k in self.keys():
            if fun(self[k], **kwargs):
                del self[k]

    def GetReactions(self, uid):
        if self.has_key(uid):
            rv =  self[uid].GetReactions()
        else:
            rv = [uid+" Not found"]

        return rv


    def __iGetReactions(self,uid):
        if self.has_key(uid):
            if self[uid].has_key(Tags.Reac):
                return self[uid][Tags.Reac]
            else:
                return []
        else:
            return [uid+" Not found"]

    def Duplicates(self, field):
        """dictionary of records with identical values in field, field values are keys in the return dictionary
           records not contaning field are assumed to have the value "None" """

        rv = {}
        for rec in self.values():
            if rec.has_key(field):
                fk = rec[field][0]
            else:
                fk = None

            if rv.has_key(fk):
                rv[fk].append(rec)
            else:
                rv[fk] = [rec]

        for k in rv.keys():
            if len(rv[k]) == 1:
                del rv[k]

        return rv


"""
    def ExSearch(self, targ):


        rv = []
        for item in self.items():
            hit = 0
            for field in item[1].items():
                for fi in field[1]:
                    if  fi.find(targ) != -1:
                        rv.append([fi, field[0], item[0]])
                        hit = 1
                        break
                if hit:
                    hit = 0
                    break
        return rv
"""



#
