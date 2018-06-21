import cobra
from ..classes.model import model
import Tags

DirecMap = {
    'IRREVERSIBLE-RIGHT-TO-LEFT' : (-1000, 0),
    'PHYSIOL-RIGHT-TO-LEFT'      : (-1000, 0),
    'LEFT-TO-RIGHT'              : (0, 1000),
    'REVERSIBLE'                 : (-1000, 1000),
    'RIGHT-TO-LEFT'              : (-1000, 0),
    'IRREVERSIBLE-LEFT-TO-RIGHT' : (0, 1000),
    'PHYSIOL-LEFT-TO-RIGHT'      : (0, 1000)
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
                    cobra_met = cobra.Metabolite(met_id)
                    AddMetaboliteInfo(db_met, cobra_met)
                metabolite_dic[met] = cobra_met
            else:
                cobra_met = metabolite_dic[met]
            stoi_dic[cobra_met] = coeff
        cobra_reac.add_metabolites(stoi_dic)
        cobra_reac.lower_bound, cobra_reac.upper_bound = DirecMap[reac.get(Tags.ReacDir, DefaultDirec)[0]]
        AddReactionInfo(reac, cobra_reac)
        m.add_reaction(cobra_reac)
    return model(m)

def AddMetaboliteInfo(db_met, cobra_met):
    if hasattr(db_met, "Formula"): cobra_met.formula = cobra.core.formula.Formula(db_met.Formula)
    if Tags.ComName in db_met.keys():
        cobra_met.name = db_met[Tags.ComName][0]
    elif Tags.Synonyms in db_met.keys():
        cobra_met.name = db_met[Tags.Synonyms][0]
    else:
        cobra_met.name = cobra_met.id
    if hasattr(db_met, 'Charge'): cobra_met.charge = db_met.Charge
    if Tags.InChI in db_met.keys(): cobra_met.inchi_id = db_met[Tags.InChI]
    if Tags.SMILES in db_met.keys(): cobra_met.smiles = db_met[Tags.SMILES]

def AddReactionInfo(db_reac, cobra_reac):
    if Tags.ComName in db_reac.keys():
        cobra_reac.name = db_reac[Tags.ComName][0]
    elif Tags.Synonyms in db_reac.keys():
        cobra_reac.name = db_reac[Tags.Synonyms][0]
    genes = db_reac.GetGenes(AsStr=True)
    if genes: cobra_reac.gene_reaction_rule = ' or '.join(genes)
    proteins = db_reac.GetProteins(AsStr=True)
    if proteins: cobra_reac.proteins = ' or '.join(proteins)
    if Tags.InPath in db_reac.keys(): cobra_reac.subsystem = '|'.join(db_reac[Tags.InPath])
    if Tags.EC in db_reac.keys(): cobra_reac.ec_number = '|'.join(db_reac[Tags.EC])

def GetImbalancedReactions(db, m):
    """ remove reactions with CANNOT-BALANCE? - T """
    rv = []
    for reac in list(m.reactions):
        if db[reac]:
            if Tags.CannotBalance in db[reac.id].keys():
                if db[reac.id][Tags.CannotBalance][0] == 'T':
                    rv.append(reac.id)
    return rv

def RemoveImbalancedReactions(db, m):
    """ remove reactions with CANNOT-BALANCE? - T """
    imbal_reacs = GetImbalancedReactions(db, m)
    m.DelReactions(imbal_reacs)

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
    m.repair()

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

def RemoveNoFormulaMetabolites(db, m, exclude=[]):
    """ remove metabolites with no molecular formula except in the exclude list,
        and remove all associated reactions """
    m.DelMetabolites(set(NoFormulaMetabolites(db, m)).difference(exclude), 'destructive')

def SubMetabolites(m, subdic):
    """ substitute metabolites; subdic = {"old_met":"new_met"} """
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
    m.repair()

def RemoveMetabolites(m, metabolites):
    """ remove problematic metabolites and the reactions associated with the metabolites """
    m.DelMetabolites(metabolites, 'destructive')

def CombineIsozymes(m, isozymes):
    """ combine isostoichiometric reactions into a single reaction
        isozymes = {main_isozyme:[list of isozymes]} """
    for reac in isozymes:
        if isinstance(isozymes, dict):
            isos = isozymes[reac]
            if reac not in m.Reactions():
                main_iso_original = isos[0]
                main_iso = m.GetReaction(isos[0])
                main_iso.id = reac
            else:
                main_iso_original = reac
                main_iso = m.GetReaction(reac)
        elif isinstance(isozymes, list):
            isos = reac
            main_iso_original = isos[0]
            main_iso = m.GetReaction(isos[0])
        main_genes = set(getattr(main_iso, 'gene_reaction_rule', '').split(' or ')).difference([''])
        main_proteins = set(getattr(main_iso, 'proteins', '').split(' or ')).difference([''])
        main_subsystems = set(getattr(main_iso, 'subsystem', '').split('|')).difference([''])
        main_ec = set(getattr(main_iso, 'ec_number', '').split('|')).difference([''])
        for iso in isos:
            if not iso == main_iso_original:
                iso_reac = m.GetReaction(iso)
                main_genes = main_genes.union(getattr(iso_reac, 'gene_reaction_rule', '').split(' or ')).difference([''])
                main_proteins = main_proteins.union(getattr(iso_reac, 'proteins', '').split(' or ')).difference([''])
                main_subsystems = main_subsystems.union(getattr(iso_reac, 'subsystem', '').split('|')).difference([''])
                main_ec = main_ec.union(getattr(iso_reac, 'ec_number', '').split('|')).difference([''])
        main_iso.gene_reaction_rule = ' or '.join(main_genes)
        main_iso.proteins = ' or '.join(main_proteins)
        main_iso.subsystem = '|'.join(main_subsystems)
        main_iso.ec_number = '|'.join(main_ec)
    m.repair()

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
                    m.SetConstraint(r, None, None)

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
    if not compartments.has_key("suffix"):
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
            if reac not in compartments["compartments"][default_cpm]: #Added this line of code to prevent Reactions already present in the default compartment to be appended to itself again
                compartments["compartments"][default_cpm].append(reac)
    compartmented_model = model()
    for cpm in compartments["compartments"]:
        cpm_suffix = compartments["suffix"][cpm]
        for reac in compartments["compartments"][cpm]:
            cpm_reac = m.GetReaction(reac).copy()
            cpm_reac.id = reac + cpm_suffix
            compartmented_model.add_reaction(cpm_reac)
            for met in list(cpm_reac.metabolites):
                SubMetabolites(compartmented_model, {met: met+cpm_suffix})
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
