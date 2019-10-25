import pandas

def WriteReactionsToMetabolitesNetwork(model, filename, ExtReacs=[], ExtMets=[]):
    """ ExtReacs = []; ExtMets = [reac_id] """
    rm = pandas.DataFrame(columns=['reaction','metabolite','stoichiometry'])
    for reac in model.reactions:
        if reac.id not in ExtReacs:
            mets = reac.metabolites
            for met in mets:
                if met.id not in ExtMets:
                    rm = rm.append({'reaction':reac.id, 'metabolite':met.id, 'stoichiometry':reac.metabolites[met]}, ignore_index=True)
    if filename.endswith('xls') or filename.endswith('xlsx'):
        rm.to_excel(filename, index=False)
    else:
        rm.to_csv(filename, index=False, sep='\t')

def WriteReactionsToReactionsNetwork(model, filename, ExtReacs=[], ExtMets=[]):
    """ ExtReacs = []; ExtMets = [reac_id] """
    rr = pandas.DataFrame(columns=['reaction1','reaction2'])
    reacs_mets = {}
    for reac in model.reactions:
        reacs_mets[reac] = set(reac.metabolites)
    for r1 in range(len(model.reactions)):
        reac1 = model.reactions[r1]
        for r2 in range(r1,len(model.reactions)):
            reac2 = model.reactions[r2]
            if len(reacs_mets[reac1].intersection(reacs_mets[reac2])) > 0:
                rr = rr.append({'reaction1':reac1.id,
                                'reaction2':reac2.id},
                                ignore_index=True)
    if filename.endswith('xls') or filename.endswith('xlsx'):
        rr.to_excel(filename, index=False)
    else:
        rr.to_csv(filename, index=False, sep='\t')

def WriteMetabolitesToMetabolitesNetwork(model, filename, ExtReacs=[], ExtMets=[]):
    """ ExtReacs = []; ExtMets = [reac_id] """
    mm = pandas.DataFrame(columns=['metabolite1','metabolite2'])
    mets_reacs = {}
    for met in model.metabolites:
        mets_reacs[met] = set(met.reactions)
    for m1 in range(len(model.metabolites)):
        met1 = model.metabolites[m1]
        for m2 in range(m1,len(model.metabolites)):
            met2 = model.metabolites[m2]
            if len(mets_reacs[met1].intersection(mets_reacs[met2])) > 0:
                mm = mm.append({'metabolite1':met1.id,
                                'metabolite2':met2.id},
                                ignore_index=True)
    if filename.endswith('xls') or filename.endswith('xlsx'):
        mm.to_excel(filename, index=False)
    else:
        mm.to_csv(filename, index=False, sep='\t')

def WriteReactionsAttributes(model, filename, attributes=[]):
    df = pandas.DataFrame(columns=attributes)
    df.index.name = 'ID'
    for reac in model.reactions:
        for attr in attributes:
            df.loc[reac.id,attr] = getattr(reac,attr)
    if filename.endswith('xls') or filename.endswith('xlsx'):
        df.to_excel(filename)
    else:
        df.to_csv(filename, sep='\t')

def WriteMetabolitesAttributes(model, filename, attributes=[]):
    df = pandas.DataFrame(columns=attributes)
    df.index.name = 'ID'
    for met in model.metabolites:
        for attr in attributes:
            df.loc[met.id,attr] = getattr(met,attr)
    if filename.endswith('xls') or filename.endswith('xlsx'):
        df.to_excel(filename)
    else:
        df.to_csv(filename, sep='\t')
