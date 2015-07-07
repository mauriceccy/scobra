
import Tags, Base, Reaction

DefaultFile="transporters.dat"

class Record(Reaction.Record):
    RecordClass="Transporter"
    

def CheckMulti(k,ids):
    if len(ids) > 1:
        print "! Multi react for ", k, " ",
    return ids[0]

class DB(Reaction.DB):   # transporters are a sub-class of reaction
    def __init__(self,path=Base.DefaultPath,**kwargs):
        Reaction.DB.__init__(self,path=path,file=DefaultFile,RecClass=Record, **kwargs)

        
        """
        Tranpsoprters are tricky, because they may well already be in the Prorein DB
        If that is the case we must look up the associated reaction, and replace the stoichiometries
        with our own. The Reaction DB does not hold the compartmentel information, we do
        """
        if self.Org == None:
            return # the above doesn't apply if we are acting as a stand alone db

        Org = self.Org

        for txid in self.keys():
            tx = self[txid]                                                    # get the reaction for the transporter UID
            if  Org.Protein.has_key(txid):                            # this UID already in the protein DB
                enzrxns = Org.Protein[txid][Tags.Cats]        # get the enzyme UIDs for protein
                eid = CheckMulti(txid, enzrxns)
                reacids = Org.Enzrxn[eid][Tags.Reac]      # get the reaction UIDs for the enzyme
                reacid = CheckMulti(txid, reacids)
                reac = Org.Reaction[reacid]                       # get the reaction for the enzyme                      
                                                
                for k in tx.keys():                   # update the reaction with the transporter values
                    if k != Tags.UID:                # except the UID :-)
                        reac[k] = tx[k]
                reac.lhs = tx.lhs[:]
                reac.rhs = tx.rhs[:]
            else:
                Org.Reaction.Records[txid] = self[txid] # if not already present add direct to the reaction DB
                
                        
                
                
                    
                
    
    
#
