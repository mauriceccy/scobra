import cobra
from ..classes.model import model
import Tags

DirecMap = {
    'IRREVERSIBLE-RIGHT-TO-LEFT' : (None, 0),
    'PHYSIOL-RIGHT-TO-LEFT'      : (None, 0),
    'LEFT-TO-RIGHT'              : (0, None),
    'REVERSIBLE'                 : (None, None),
    'RIGHT-TO-LEFT'              : (None, 0),
    'IRREVERSIBLE-LEFT-TO-RIGHT' : (0, None),
    'PHYSIOL-LEFT-TO-RIGHT'      : (0, None)
}
DefaultDirec = ['LEFT-TO-RIGHT']

def BuildRawModelFromDB(db):
    ### create model with all reactions in the database
    m = model()
    metabolite_dic = {}
    for reac in db.reactions:
        cobra_reac = cobra.Reaction(reac.UID)
        stoi_dic = {}
        for met in reac.CoeffDic:
            coeff = reac.CoeffDic[met]
            if met.startswith("|") and met.endswith("|"):
                met = met[1:-1]
            if met not in metabolite_dic:
                if not db[met]:
                    cobra_met = cobra.Metabolite(met, name=met)
                else:
                    db_met = db[met]
                    met_id = db_met.UID
                    met_formula = getattr(db_met, "Formula", None)
                    if Tags.ComName in db_met.keys():
                        met_name = db_met[Tags.ComName][0]
                    elif Tags.Synonyms in db_met.keys():
                        met_name = db_met[Tags.Synonyms][0]
                    else:
                        met_name = met_id
                    cobra_met = cobra.Metabolite(met_id, formula=met_formula, name=met_name, compartment=None)
                    if hasattr(met, 'Charge'): cobra_met.charge = db_met.Charge
                    if Tags.InChI in db_met.keys(): cobra_met.inchi_id = db_met[Tags.InChI]
                    if Tags.SMILES in db_met.keys(): cobra_met.smiles = db_met[Tags.SMILES]
                metabolite_dic[met] = cobra_met
            else:
                cobra_met = metabolite_dic[met]
            stoi_dic[cobra_met] = coeff
        cobra_reac.add_metabolites(stoi_dic)
        cobra_reac.lower_bound, cobra_reac.upper_bound = DirecMap[reac.get(Tags.ReacDir, DefaultDirec)[0]]
        if Tags.ComName in reac.keys():
            cobra_reac.name = reac[Tags.ComName][0]
        elif Tags.Synonyms in reac.keys():
            cobra_reac.name = reac[Tags.Synonyms][0]
        genes = reac.GetGenes(AsStr=True)
        if genes: cobra_reac.gene_reaction_rule = ' or '.join(genes)
        proteins = reac.GetProteins(AsStr=True)
        if proteins: cobra_reac.proteins = ' or '.join(proteins)
        if Tags.InPath in reac.keys(): cobra_reac.subsystem = '|'.join(reac[Tags.InPath])
        if Tags.EC in reac.keys(): cobra_reac.ec_number = '|'.join(reac[Tags.EC])
        m.add_reaction(cobra_reac)
    return m

def RemoveImbalancedReactions(db, m):
    """ remove reactions with CANNOT-BALANCE? - T """
    for reac in list(m.reactions):
        if db[reac]:
            if Tags.CannotBalance in db[reac.id].keys():
                if db[reac.id][Tags.CannotBalance][0] == 'T':
                    m.DelReaction(reac)

def FixP_OR_NOP(m):
    """ fix NAD-P-OR-NOP and NADH-P-OR-NOP """
    nad = m.GetMetabolite('NAD')
    nadh = m.GetMetabolite('NADH')
    nadp = m.GetMetabolite('NADP')
    nadph = m.GetMetabolite('NADPH')
    ox = m.GetMetabolite('NAD-P-OR-NOP')
    red = m.GetMetabolite('NADH-P-OR-NOP')
    ox_reacs = m.InvolvedWith('NAD-P-OR-NOP').keys()
    red_reacs = m.InvolvedWith('NADH-P-OR-NOP').keys()
    reacs = list(set(red_reacs).union(ox_reacs))
    for reac in reacs:
        sd = m.InvolvedWith(reac)
        ox_stoi = sd[ox]
        red_stoi = sd[red]
        nop_reac = reac.copy()
        nop_reac.id = reac.id + '-NAD'
        m.add_reaction(nop_reac)
        m.ChangeReactionStoichiometry(nop_reac, {nad:ox_stoi, nadh:red_stoi, ox:0, red:0})
        p_reac = reac.copy()
        p_reac.id = reac.id + '-NADP'
        m.add_reaction(p_reac)
        m.ChangeReactionStoichiometry(p_reac, {nadp:ox_stoi, nadph:red_stoi, ox:0, red:0})
        m.DelReaction(reac)
    m.DelMetabolites([ox, red])

def SubMetabolites(m, subdic):
    """ substitute metabolites """
    for submet in subdic.keys():
        newmet = subdic[submet]
        if newmet in m.Metabolites():
            newmet = m.GetMetabolite(newmet)
        else:
            newmet = m.GetMetabolite(submet).copy()
            newmet.id = subdic[submet]
        for reac in m.InvolvedWith(submet):
            m.ChangeReactionStoichiometry(reac, {newmet:m.InvolvedWith(submet)[reac], submet:0})
        m.DelMetabolite(submet)

def NoFormulaMetabolites(db, m):
    """ get metabolites in model without molecular formula """
    rv = []
    for met in m.Metabolites():
        if not db[met]:
            rv.append(met)
        else:
            if Tags.ChemForm not in db[met]:
                rv.append(met)
    return rv

def RemoveMetabolites(m, metabolites):
    """ remove problematic metabolites and the reactions associated with the metabolites """
    m.DelMetabolites(metabolites, 'destructive')

def RemoveReactions(m, reactions):
    """ remove problematic reactions """
    m.DelReactions(reactions)

def IsomeraseReversible(m):
    """ make isomerases reversible """
    for r in m.reactions:
        if r.upper_bound <= 0 or r.lower_bound >= 0:
            invw = m.InvolvedWith(r)
            if (len(invw) == 2):
                if (invw.values()[0] == -1) and (invw.values()[1] == 1):
                    m.GetConstraint(r, None, None)

def ChangeReactionsDirection(m, direc_dic):
    """ direc_dic = {'reversible':[reacs], 'irreversible':[reacs], 'back_irreversible':[reacs]} """
    for direc in direc_dic:
        if direc == 'reversible':
            for r in direc_dic[direc]:
                m.SetConstraint(r, None, None)
        elif direc == 'irreversible':
            for r in direc_dic[direc]:
                m.SetConstraint(r, 0, None)
        elif direc == 'back_irreversible':
            for r in direc_dic[direc]:
                m.SetConstraint(r, None, 0)

def CompartmentModel(m, compartments):
    """ compartments = {"default":"cpt", "compartments":{"cpt":[]}, "suffix":{"cpt":"suffix"}} """
    default_cpm = compartments["default"]
    if not compartments["compartments"].has_key(default_cpm):
        compartments["compartments"][default_cpm] = []
    if not compartments.has_key["suffix"]:
        cpms = compartments["compartments"].keys()
        compartments["suffix"] = dict(zip(cpms, cpms))
    reacs_not_default_cpm = []
    for cpm in compartments["compartments"]:
        if cpm != default_cpm:
            for reac in compartments["compartments"][cpm]:
                if reac not in compartments["compartments"][default_cpm]:
                    reacs_not_default_cpm.append(reac)
    for reac in m.Reactions():
        if reac not in reacs_not_default_cpm:
            compartments["compartments"][default_cpm].append(reac)
    compartmented_model = model()
    for cpm in compartments["compartments"]:
        cpm_suffix = compartments["suffix"][cpm]
        for reac in compartments["compartments"][cpm]:
            cpm_reac = m.GetReaction(reac).copy()
            cpm_reac.id = reac + cpm_suffix
            compartmented_model.add_reaction(cpm_reac)
            for met in list(cpm_reac.metabolites):
                SubMetabolites(compartmented_model, {met, met+cpm_suffix})
    return compartmented_model

def CorrectStoichiometry(m, reac_stoi_dic):
    """ reac_stoi_dic = {reac:{met:stoi}} """
    for reac in reac_stoi_dic:
        corr_reac = m.GetReaction(reac)
        corr_reac.clear_metabolites()
        m.ChangeReactionStoichiometry(corr_reac, reac_stoi_dic[reac])

def ExtraReactions(m, extra_model):
    """ extra_model = model object containing extra reactions """
    m.MergeWithModel(extra_model)