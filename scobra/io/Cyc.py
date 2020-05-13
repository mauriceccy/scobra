# -*- coding: utf-8 -*-
import cobra
import sys
import os

from ..classes.reaction import Reaction
from ..classes.metabolite import Metabolite

#FOR TESTING
#from reaction import Reaction
#from metabolite import Metabolite

def ReadCyc(reactionDatFile,compoundsDatFile="",classesDatFile="",enyzmeDatFile="",Print=False):
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

        line = metStreamCompounds.readline()

    mets_dict[metabolite.id] = metabolite
    all_mets[metabolite.id] = metabolite
                
    metStreamCompounds.close()


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
    proteins = {}

    while(line):
        line=line.rstrip("\n")
        if(line.startswith(UID)):
            if(reaction.id!=""):
                #print(stoi_dict)
                reaction.proteins = proteins
                #print(direction)
                #print(direction==rev)
                
                reaction.add_metabolites(stoi_dict,reversibly=(direction==rev))
                if direction == rev:
                    reaction._upper_bound = 1000.0
                    reaction._lower_bound = -1000.0
                elif direction == ltr:
                    reaction._upper_bound = 1000.0
                    reaction._lower_bound = 0.0
                elif direction == rtl:
                    reaction._upper_bound = 0.0
                    reaction._lower_bound = -1000.0
                all_reactions[reaction.id] = reaction
                #added+=1
                #print(added)
                #all_stoic_.append(stoi_dict)
                if reaction.useable:
                    model.add_reaction(reaction)
                else:
                    unusable_reactions[reaction.id] = reaction
            stoi_dict = {}
            proteins = {}
            reaction = Reaction(line[lUID:].strip())
            #all_reacs_.append(line[lUID:].strip())
            
        elif(line.startswith(ENZ_REC)):
            enz_id = line[lENZ_REC:]
            proteins[enz_id] = enzs_dict[enz_id]

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
                if reaction.id in reactions_mets_nf:
                    reactions_mets_nf[reaction.id].append(met)
                else:
                    reactions_mets_nf[reaction.id] = [met]
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
                if reaction.id in reactions_mets_nf:
                    reactions_mets_nf[reaction.id].append(met)
                else:
                    reactions_mets_nf[reaction.id] = [met]
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
            continue
        
        line = reactionStream.readline()
    #print(all_stoic_[2])
    #print(all_dirs_[2])
    #print(all_reacs_[2])
    #print(TESTFORMULA)
    #Accounting for last reaction here:
    reaction.proteins = proteins
    reaction.add_metabolites(stoi_dict,reversibly=(direction==rev))
    if direction == rev:
        reaction._upper_bound = 1000.0
        reaction._lower_bound = -1000.0
    elif direction == ltr:
        reaction._upper_bound = 1000.0
        reaction._lower_bound = 0.0
    elif direction == rtl:
        reaction._upper_bound = 0.0
        reaction._lower_bound = -1000.0
    all_reactions[reaction.id] = reaction
    #added+=1
    #all_stoic_.append(stoi_dict)
    if reaction.useable:
        model.add_reaction(reaction)
    else:
        unusable_reactions[reaction.id] = reaction

    model.all_reactions = all_reactions
    model.reactions_mets_nf = reactions_mets_nf
    model.unusable_reactions = unusable_reactions
    #print(model.metabolites)
    #print(model.reactions)

    reactionStream.close()

    return model
