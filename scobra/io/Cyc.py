# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cobra
import sys
import os

def ReadCyc(datFile,Print=False):
    """Read in reactions.dat file from cyc and return a cobra model.
    Returns
    -------
    cobra.Model
    """
    if(!datFile.endsWith("reactions.dat")):
        raise Exception("Input error: not cyc reactions.dat file.")

    model = cobra.Model()
    metabolites_dict = {}
    
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
    
    #### READING IN METABOLITES ####
    metStream = open(datFile.replace("reactions.dat","compounds.dat"),'r')
    mets_dict = {}
    line = metStream.readline()
    metabolite = cobra.Metabolie("")
    while(line):
        line = line.rstrip("\n")
        if(line.startswith(UID)):
            if(metabolite.id!=""):
                mets_dict[metabolite.id] = metabolite
            metabolite = cobra.Metabolie(id=line[lUID:].strip())
            metabolite.charge = 0
        elif(line.startswith(CN)):
            metabolite.name = line[lCN:].strip()
        elif(line.startswith(AC)):
            charge = 0
            while(line.startswith(AC)):
                chargeString = line[AC:].strip().strip("()").split(" ")
                chargeF = (int)chargeString[1]
                charge = charge + chargeF
                line = metStream.readline()
            continue
        elif(line.startswith(CF)):
            formula = ""
            while(line.startswith(CF)):
                chemString = line[lCF:].strip().strip("()").split(" ")
                chemF = chemString[0]+chemString[1]
                formula = formula + chemF
                line = metStream.readline()
            continue

        line = metStream.readline()

    #### READING IN REACTION ####
    stream = open(datFile,'r')

    line = stream.readline()
    all_stoic_ = []
    all_reacs_ = []
    all_dirs_ = []
    model = cobra.Model()
    reaction = cobra.Reaction("")
    while(line):
        line=line.rstrip("\n")
        if(line.startswith(UID)):
            if(reaction.id!=""):
                #reaction.add_metabolites(stoi_dict)
                all_stoic_.append(stoi_dict)
                #model.add_reaction(reaction)
            stoi_dict = {}
            reaction = cobra.Reaction(line[lUID:].strip())
            all_reacs_.append(line[lUID:].strip())
            
        elif(line.startswith(L)):
            met = line[lL:]
            stoi_dict[met] = -1
            line = stream.readline()
            if(line.startswith(CO)):
                try:
                    int(line[lCO:])
                except ValueError:
                    line = stream.readline()
                    continue
                stoi_dict[met] = int(line[lCO:])
                line = stream.readline()
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
            all_dirs_.append(direction)
        elif(line.startswith(R)):
            met = line[lR:]
            stoi_dict[met] = 1
            line = stream.readline()
            if(line.startswith(CO)):
                try:
                    int(line[lCO:])
                except ValueError:
                    line = stream.readline()
                    continue
                stoi_dict[met] = int(line[lCO:])
                line = stream.readline()
            continue
        
        line = stream.readline()
    #print(all_stoic_[2])
    #print(all_dirs_[2])
    #print(all_reacs_[2])
    return model

ReadCyc("/Users/sewenthy/Downloads/pineapplecyc/2.0/data/reactions.dat")