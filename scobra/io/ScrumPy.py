import cobra
from fractions import Fraction

def ReadScrumPyModel(spy_file, compartment_dic={}, Print=False, AutoExt=True):
    """
    Take a ScrumPy model file generated in ScrumPy with m.smexterns.ToScrumPy()
    Cannot take a master model file with links to children files
    Does not work if the model file is not in the following format:

    Reaction name:
        5 metabolite_A + 10 metabolite_B -> 1 metabolite_C
        ~

    Note that each reaction must be separated into 3 lines
    """
    model_string = open(spy_file,'r').read()
    model_string = model_string.replace('\t','')
    model_string = model_string.replace('    ','')
    string_list = model_string.split('\n')

    model = cobra.Model()

    externals = []
    metabolite_dic = {}

    reac_name = None
    DeQuote = False
    for string in string_list:
        if string == '' or string.startswith("#"):
            pass
        elif string == 'Structural()':
            pass
        elif string == 'DeQuote()':
            DeQuote = True
        elif string.startswith('ElType(') and string.endswith(')'):
            pass
        elif string.startswith("External(") and string.endswith(")"):
            ext_string = string[9:-1]
            ext_string = ext_string.replace(' ','')
            ext_list = ext_string.split(',')
            externals.extend(ext_list)
        elif string.endswith(':'):
            reac_name = string[:-1]
        elif reac_name and string == '~':
            reac_name = None
        elif reac_name and string != '~':
            if DeQuote:
                if (reac_name.startswith('"') and reac_name.endswith('"')) or (reac_name.startswith("'") and reac_name.endswith("'")):
                    reac_name = reac_name[1:-1]
            reaction = cobra.Reaction(reac_name)
            stoichiometry_list = []
            metabolite_list = []
            new_metabolite = True
            product = False
            compartment = ''
            s_list = string.split(' ')
            for s in s_list:
                if s == ":" or s == "":
                    pass
                elif s == "+":
                    new_metabolite = True
                elif s == "->" or s == "-->" or s == "=>" or s == u'\u2192':
                    direction = 'LEFT-TO-RIGHT'
                    product = True
                    new_metabolite = True
                elif s == "<>" or s =="<=>" or s == "<==>" or s == "<->" or s == u'\u2194':
                    direction = 'REVERSIBLE'
                    product = True
                    new_metabolite = True
                elif s == "<-" or s == "<--" or s == "<=" or s == u'\u2190':
                    direction = 'RIGHT-TO-LEFT'
                    product = True
                    new_metabolite = True
                else:
                    try:
                        s = Fraction(s)
                        s = float(s)
                        if not product:
                            s = -s
                        stoichiometry_list.append(s)
                        new_metabolite = False
                    except ValueError:
                        metabolite_list.append(s + compartment)
                        if new_metabolite:
                            if not product:
                                stoichiometry_list.append(-1)
                            else:
                                stoichiometry_list.append(1)
                            new_metabolite = True
            stoi_dic = {}
            for b in range(len(metabolite_list)):
                met_id = metabolite_list[b]
                if met_id not in externals:
                    if (met_id.startswith('"') and met_id.endswith('"')) or (met_id.startswith("'") and met_id.endswith("'")):
                        dmet_id = met_id[1:-1]
                        if DeQuote:
                            met_id = met_id[1:-1]
                    else:
                        dmet_id = met_id
                    if AutoExt and (dmet_id.startswith('X_') or dmet_id.startswith('x_')):
                        externals.append(met_id)
                    else:
                        try:
                            met = metabolite_dic[met_id]
                        except KeyError:    # try case-insensitive
                            met_key = []
                            for key in metabolite_dic:
                                if key.lower() == met_id.lower():
                                    met_key.append(key)
                            if len(met_key) == 1:
                                met = metabolite_dic[met_key[0]]
                            else:
                                met_compartment = None
                                for c in compartment_dic:
                                    if met_id.endswith(c):
                                        met_compartment = compartment_dic[c]
                                met = cobra.Metabolite(met_id,compartment=met_compartment)
                                metabolite_dic[met_id] = met
                        stoi_dic[met] = stoichiometry_list[b]
            reaction.add_metabolites(stoi_dic)
            reaction.lower_bound = -float('inf')
            reaction.upper_bound = float('inf')
            if direction == 'LEFT-TO-RIGHT':
                reaction.lower_bound = 0.0
            elif direction == 'RIGHT-TO-LEFT':
                reaction.upper_bound = 0.0
            model.add_reaction(reaction)
            if Print:
                print(reaction.reaction)
    return model

def WriteScrumPyModel(model,filename, ExtReacs={}):
    """ ExtReacs = {reac_id:stoichiotry} """
    model = model.copy()
    arrow_dic = {'<--':'<-','<=>':'<>','-->':'->'}
    out_file = 'Structural()\n'
    if len(model.reactions) > 0:
        if not ((model.reactions[0].id.startswith('"') and model.reactions[0].id.endswith('"')) or (model.reactions[0].id.startswith("'") and model.reactions[0].id.endswith("'"))):
            out_file += 'DeQuote()\n'
    reactions_string = ''
    external_metabolites = []
    if isinstance(ExtReacs, str):
        ExtReacs = {ExtReacs:1}
    elif isinstance(ExtReacs, list):
        ExtReacs = dict((reac,1) for reac in ExtReacs)
    for met in model.metabolites:
        if not (met.id.startswith('"') and met.id.endswith('"')):
            met.id = '"' + met.id + '"'
    for reac in model.reactions:
        reactions_string += '"' + reac.id + '":\n'
        reac_string = reac.reaction
        for arrow in arrow_dic:
            reac_string = reac_string.replace(arrow,arrow_dic[arrow])
        if reac_string.startswith('<>') or reac_string.startswith('->') or reac_string.startswith(' <>') or reac_string.startswith(' ->') or reac_string.startswith('<-') or reac_string.startswith(' <-'):
            external_met = '"X_' + reac.id + '"'
            reactions_string += '    ' + external_met + reac_string + '\n    ~\n'
            external_metabolites.append(external_met)
        elif reac_string.endswith('<>') or reac_string.endswith('->') or reac_string.endswith('<> ') or reac_string.endswith('-> ') or reac_string.endswith('<-') or reac_string.endswith('<- '):
            external_met = '"X_' + reac.id + '"'
            reactions_string += '    ' + reac_string + external_met + '\n    ~\n'
            external_metabolites.append(external_met)
        elif reac.id in ExtReacs.keys():
            external_met = '"X_' + reac.id + '"'
            if ExtReacs[reac.id] > 0:
                reactions_string += '    ' + reac_string + ' + ' + str(abs(float(ExtReacs[reac.id]))) + ' ' + external_met + '\n    ~\n'
            elif ExtReacs[reac.id] < 0:
                reactions_string += '    ' + str(abs(float(ExtReacs[reac.id]))) + ' ' + external_met + ' + ' + reac_string + '\n    ~\n'
            external_metabolites.append(external_met)
        else:
            reactions_string += '    ' + reac_string + '\n    ~\n'
    if external_metabolites:
        ext_mets_string = ''
        for met in external_metabolites:
            ext_mets_string += str(met) + ','
        out_file += 'External(' + ext_mets_string[:-1] + ')\n'
    out_file += reactions_string
    open(filename,'w').write(out_file)


