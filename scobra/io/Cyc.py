# -*- coding: utf-8 -*-
import cobra
import sys
import os

from ..classes.reaction import Reaction
from ..classes.metabolite import Metabolite

#FOR TESTING
#from reaction import Reaction
#from metabolite import Metabolite

def ReadCyc(reactionDatFile,compoundsDatFile="",classesDatFile="",enyzmeDatFile="",proteinDatFile="", default_dir="LEFT-TO-RIGHT", Print=False):
    """
    REQUIREMENTS TO USE: reactions.dat, compounds.dat, classes.dat--Either provide 
    the path or put them in the same directory and provide reactions.dat path.

    Read in reactions.dat file from cyc and return a cobra model.
    Returns
    -------
    scobra.Model
    """

    if(not reactionDatFile.endswith("reactions.dat")):
        raise Exception("Input error: not cyc reactions.dat file.")

    model = cobra.Model()
    
    #### KEYWORDS
    UID  = "UNIQUE-ID - "
    lUID= len(UID)
    
    # METABOLITE
    CN = "COMMON-NAME - "
    lCN = len(CN)

    CF = "CHEMICAL-FORMULA - "
    lCF = len(CF)

    AC = "ATOM-CHARGES - "
    lAC = len(AC)

    MW = "MOLECULAR-WEIGHT - "
    lMW = len(MW)

    INCHI = "INCHI - InChI="
    lINCHI = len(INCHI)

    SMILES = "SMILES - "
    lSMILES = len(SMILES)

    COMMENTS = "COMMENT - "
    lCOMMENTS = len(COMMENTS)

    COMPARTMENT = "^COMPARTMENT - "
    lCOMPARTMENT = len(COMPARTMENT)

    # GENE
    ENZYME = "ENZYME - "
    lENZYME = len(ENZYME)

    REACTION = "REACTION -"
    lREACTION = len(REACTION)

    # REACTION
    L = "LEFT - "
    lL= len(L)
    R = "RIGHT - "
    lR= len(R)
    CO = "^COEFFICIENT - "
    lCO = len(CO)
    
    RD = "REACTION-DIRECTION - "
    lRD = len(RD)
    ltr  = "LEFT-TO-RIGHT"
    rev = "REVERSIBLE"
    rtl = "RIGHT-TO-LEFT"

    ENZ_REC = "ENZYMATIC-REACTION - "
    lENZ_REC = len(ENZ_REC)

    EC = "EC-NUMBER - "
    lEC = len(EC)

    PW = "IN-PATHWAY - "
    lPW = len(PW)
    
    #### READING IN METABOLITES FROM COMPOUNDS ####
    metStreamCompounds = None
    
    try:
        if compoundsDatFile == "":
            metStreamCompounds = open(reactionDatFile.replace("reactions.dat","compounds.dat"), 'r', encoding="utf8", errors='ignore')
        else:
            metStreamCompounds = open(compoundsDatFile, 'r', encoding="utf8", errors='ignore')
    except:
        print("compounds.dat is required for importing metabolites but is not provided/found in the directory.")
        return
    #TESTFORMULA = []
    mets_dict = {}
    all_mets = {}
    line = metStreamCompounds.readline()
    metabolite = Metabolite("")
    while(line):
        line = line.rstrip("\n")
        if(line.startswith(UID)):
            if(metabolite.id!=""):
                mets_dict[metabolite.id] = metabolite
                all_mets[metabolite.id] = metabolite
            metabolite = Metabolite(id=line[lUID:].strip(), name=line[lUID:].strip())
            metabolite.charge = 0
        elif(line.startswith(CN)):
            metabolite.name = line[lCN:].strip()

        elif(line.startswith(AC)):
            charge=0
            while(line.startswith(AC)):
                chargeStr = line[lAC:].strip().strip("()").split(" ")[1]
                charge+=int(chargeStr)
                line = metStreamCompounds.readline()
            metabolite.charge=charge
            continue

        elif(line.startswith(CF)):
            formula = ""
            while(line.startswith(CF)):
                chemString = line[lCF:].strip().strip("()").split(" ")
                chemF = chemString[0]+chemString[1]
                formula = formula + chemF
                line = metStreamCompounds.readline()
            #TESTFORMULA.append(formula)
                
            metabolite.formula=formula
            continue

        elif(line.startswith(MW)):
            metabolite.molecular_weights = float(line[lMW:].strip())

        elif(line.startswith(SMILES)):
            metabolite.smiles = line[lSMILES:].strip()
            
        elif(line.startswith(INCHI)):
            metabolite.inchi_id = line[lINCHI:].strip()

        line = metStreamCompounds.readline()

    mets_dict[metabolite.id] = metabolite
    all_mets[metabolite.id] = metabolite
                
    metStreamCompounds.close()

    """
    #### READING IN METABOLITES FROM CLASSES ####
    metStreamClasses = None
    try:
        if classesDatFile == "":
            #print("first one")
            metStreamClasses = open(reactionDatFile.replace("reactions.dat","classes.dat"), 'r', encoding="utf8", errors='ignore')
        else:
            metStreamClasses = open(classesDatFile, 'r', encoding="utf8", errors='ignore')
    except:
        print("classes.dat is required for importing metabolites but is not provided/found in the directory.")

    line = metStreamClasses.readline()
    metabolite = Metabolite("")
    while(line):
        line = line.rstrip("\n")
        if(line.startswith(UID)):
            if(metabolite.id!=""):
                all_mets[metabolite.id] = metabolite
                mets_dict[metabolite.id] = metabolite
            metabolite = Metabolite(id=line[lUID:].strip())
            metabolite.charge = 0
        elif(line.startswith(CN)):
            metabolite.name = line[lCN:].strip()

        elif(line.startswith(COMMENTS)):
            metabolite.COMMENTS = line[lCOMMENTS:].strip()

        line = metStreamClasses.readline()

    all_mets[metabolite.id] = metabolite
    mets_dict[metabolite.id] = metabolite
    metStreamClasses.close()
    """
    #### READING IN PROTEINS ####
    proStream = None
    try:
        if proteinDatFile == "":
            proStream = open(reactionDatFile.replace("reactions.dat","proteins.dat"), 'r', encoding="utf8", errors='ignore')
        else:
            proStream = open(proteinDatFile, 'r', encoding="utf8", errors='ignore')
    except:
        print("classes.dat is required for importing metabolites but is not provided/found in the directory.")

    all_proteins = {}
    #genes = []
    line = proStream.readline()
    protein_name = ""
    gene_associated = ""
    while(line):
        line = line.rstrip("\n")
        if(line.startswith(UID)):
            if(metabolite.id!=""):
                all_proteins[protein_name] = gene_associated
                
            protein_name = line[lUID:].strip()
            
        elif(line.startswith("GENE - ")):
            gene_associated = line[7:].strip()

        line = proStream.readline()

    all_proteins[protein_name] = gene_associated
    model.all_proteins = all_proteins
    proStream.close()

    #### READING IN ENZYMES ####
    enzymeStream = None
    try:
        if enyzmeDatFile == "":
            #print("first one")
            enzymeStream = open(reactionDatFile.replace("reactions.dat","enzrxns.dat"), 'r', encoding="utf8", errors='ignore')
        else:
            enzymeStream = open(enyzmeDatFile, 'r', encoding="utf8", errors='ignore')
    except:
        print("enzrxns.dat is required for importing metabolites but is not provided/found in the directory.")

    line = enzymeStream.readline()

    enzs_dict = {}

    enz_id = ""
    enz_name = ""
    while(line):
        line = line.rstrip("\n")
        if(line.startswith(UID)):
            if(enz_id!=""):
                enzs_dict[enz_id] = enz_name
            enz_id = line[lUID:].strip()
        elif(line.startswith(ENZYME)):
            enz_name = line[lENZYME:].strip()

        line = enzymeStream.readline()

    enzs_dict[enz_id] = enz_name
    enzymeStream.close()

    #### READING IN REACTION ####
    reactionStream = open(reactionDatFile, 'r', encoding="utf8", errors='ignore')

    line = reactionStream.readline()
    #all_stoic_ = []
    all_reactions = {}
    #all_dirs_ = []
    
    #model.metabolites = mets_dict

    no_formula_mets = {}
    unusable_reactions = {}
    reactions_mets_nf = {}

    reaction = Reaction("")
    stoi_dict = {}
    added = 0
    proteins = []
    ec_number = ""
    subsystem = []
    direction = None

    while(line):
        line=line.rstrip("\n")
        if(line.startswith(UID)):
            if(reaction.id!=""):
                #print(stoi_dict)
                reaction.proteins = proteins
                subsys_str = ""
                for v in subsystem:
                    subsys_str += v +"|"
                subsys_str = subsys_str.rstrip("|")
                reaction.subsystem = subsys_str
                
                #print(direction)
                #print(direction==rev)
                if direction == None:
                    direction = default_dir
                reaction.ec_number = ec_number
                reaction.add_metabolites(stoi_dict,reversibly=(direction==rev))
                
                if direction == rev:
                    reaction._upper_bound = float('inf')
                    reaction._lower_bound = float('-inf')
                elif direction == ltr:
                    reaction._upper_bound = float('inf')
                    reaction._lower_bound = 0.0
                elif direction == rtl:
                    reaction._upper_bound = 0.0
                    reaction._lower_bound = float('-inf')
                
                
                all_reactions[reaction.id] = reaction
                #added+=1
                #print(added)
                #all_stoic_.append(stoi_dict)

                #### BUILDING GPR ###
                gpr = ""
                for v in proteins:
                    gpr= gpr +"("+all_proteins[v]+") or "
                gpr = gpr.rstrip(" or ")
                reaction.gene_reaction_rule = gpr
                model.add_reaction(reaction)
                if not reaction.useable:
                    unusable_reactions[reaction.id] = reaction
            stoi_dict = {}
            proteins = []
            ec_number = ""
            subsystem = []
            reaction = Reaction(line[lUID:].strip())
            reaction.name = reaction.id
            direction = None
            #all_reacs_.append(line[lUID:].strip())

        elif(line.startswith(EC)):
            ec_number = line[lEC:]
            
        elif(line.startswith(ENZ_REC)):
            enz_id = line[lENZ_REC:]
            proteins.append(enzs_dict[enz_id])

        elif(line.startswith(PW)):
            subsys = line[lPW:]
            subsystem.append(subsys)

        elif(line.startswith(L)):
            met = line[lL:]
            if met in mets_dict:
                met = mets_dict[met]
            else:
                #MARK NO FORMULA
                no_formula_mets[met] = Metabolite(id = met, name = met)
                met = no_formula_mets[met]
                all_mets[met.id] = met
                reaction.all_mets_has_formula = False
                reaction.useable = False
                if not reaction.id in reactions_mets_nf:
                    reactions_mets_nf[reaction.id] = reaction
            stoi_dict[met] = -1
            line = reactionStream.readline()
            if(line.startswith(CO)):
                try:
                    int(line[lCO:])
                except ValueError:
                    #MARK NO COEFFICIENT
                    line = reactionStream.readline()
                    continue
                stoi_dict[met] = int(line[lCO:])
                line = reactionStream.readline()
            
            #IGNORING COMPARTMENT
            """
            elif(line.startswith(COMPARTMENT)):
                met.compartment = line[lCOMPARTMENT:]
                line = reactionStream.readline()
            """
            continue

        elif(line.startswith(RD)):
            d = line[lRD:]
            direction = ""
            if(ltr in d):
                direction = ltr
            elif(rtl in d):
                direction = rtl
            elif(rev in d):
                direction = rev
            else:
                raise Exception("invalid direction for: "+reaction.id)
            #all_dirs_.append(direction)

        elif(line.startswith(R)):
            met = line[lR:]
            if met in mets_dict:
                met = mets_dict[met]
            else:
                #MARK NO FORMULA
                no_formula_mets[met] = Metabolite(id = met, name = met)
                met = no_formula_mets[met]
                all_mets[met.id] = met
                reaction.all_mets_has_formula = False
                reaction.useable = False
                if not reaction.id in reactions_mets_nf:
                    reactions_mets_nf[reaction.id] = reaction
                    
            stoi_dict[met] = 1
            line = reactionStream.readline()
            if(line.startswith(CO)):
                try:
                    int(line[lCO:])
                except ValueError:
                    #MARK NO COEFFICIENT
                    line = reactionStream.readline()
                    continue
                stoi_dict[met] = int(line[lCO:])
                line = reactionStream.readline()

            #IGNORING COMPARTMENT
            """
            elif(line.startswith(COMPARTMENT)):
                met.compartment = line[lCOMPARTMENT:]
                line = reactionStream.readline()
            """
            continue
        
        line = reactionStream.readline()
    #print(all_stoic_[2])
    #print(all_dirs_[2])
    #print(all_reacs_[2])
    #print(TESTFORMULA)
    #Accounting for last reaction here:
    reaction.proteins = proteins
    reaction.ec_number = ec_number
    reaction.add_metabolites(stoi_dict,reversibly=(direction==rev))
    if direction == rev:
        reaction._upper_bound = float('inf')
        reaction._lower_bound = float('-inf')
    elif direction == ltr:
        reaction._upper_bound = float('inf')
        reaction._lower_bound = 0.0
    elif direction == rtl:
        reaction._upper_bound = 0.0
        reaction._lower_bound = float('-inf')
                
    all_reactions[reaction.id] = reaction
    #added+=1
    #all_stoic_.append(stoi_dict)
    model.add_reaction(reaction)
    if not reaction.useable:
        unusable_reactions[reaction.id] = reaction

    model.all_reactions = all_reactions
    model.reactions_mets_nf = reactions_mets_nf
    model.unusable_reactions = unusable_reactions
    model.all_mets=all_mets
    model.no_formula_mets = no_formula_mets
    #print(model.metabolites)
    #print(model.reactions)

    reactionStream.close()

    return model
