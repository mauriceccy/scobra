import re
import pandas
import cobra
from fractions import Fraction


def ReadExcel(excel_file, parse="cobra_string", Print=False):
    """ parse = "cobra_string" | "cobra_position"
    cobra_string
    % INPUT
    % fileName      xls spreadsheet, with one 'Reaction List' and one 'Metabolite List' tab
    %
    % 'Reaction List' tab: Required headers (case sensitive):
    %   'Abbreviation'      HEX1
    %   'Description'       Hexokinase
    %   'Reaction'          1 atp[c] + 1 glc-D[c] --> 1 adp[c] + 1 g6p[c] + 1 h[c]
    %   'GPR'               (3098.3) or (80201.1) or (2645.3) or ...
    %   'Genes'             2645.1,2645.2,2645.3,...  (optional)
    %   'Proteins'          Flj22761.1, Hk1.3, Gck.2,...  (optional)
    %   'Subsystem'         Glycolysis
    %   'Reversible'        0 (false) or 1 (true)
    %   'Lower bound'       0
    %   'Upper bound'       1000
    %   'Objective'         0   (optional)
    %   'Confidence Score'  0,1,2,3,4
    %   'EC Number'         2.7.1.1,2.7.1.2
    %   'Notes'             'Reaction also associated with EC 2.7.1.2' (optional)
    %   'References'        PMID:2043117,PMID:7150652,...   (optional)
    %
    % 'Metabolite List' tab: Required headers (case sensitive): (needs to be complete list of metabolites, i.e., if a metabolite appears in multiple compartments it has to be represented in multiple rows. Abbreviations need to overlap with use in Reaction List
    %   'Abbreviation'      glc-D or glc-D[c]
    %   'Description'       D-glucose
    %   'Neutral formula'   C6H12O6
    %   'Charged formula'   C6H12O6
    %   'Charge'            0
    %   'Compartment'       cytosol
    %   'KEGG ID'           C00031
    %   'PubChem ID'        5793
    %   'ChEBI ID'          4167
    %   'InChI string'      InChI=1/C6H12O6/c7-1-2-3(8)4(9)5(10)6(11)12-2/h2-11H,1H2/t2-,3-,4+,5-,6?/m1/s1
    %   'SMILES'            OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O
    %   'HMDB ID'           HMDB00122
    %
    % OPTIONAL INPUT (may be required for input on unix macines)
    % biomassRxnEquation        .xls may have a 255 character limit on each cell,
    %                           so pass the biomass reaction separately if it hits this maximum.
    %
    % OUTPUT
    % model         COBRA Toolbox model

    cobra_position
    % INPUT
    % excel_file      xls spreadsheet, with one 'reactions' and one 'metabolites' tab
    %
    % 'reactions' tab: Required headers:
    %               col 0     Abbreviation     HEX1
    %               col 1     Description      Hexokinase
    %               col 2     Reaction         1 atp[c] + 1 glc-D[c] --> 1 adp[c] + 1 g6p[c] + 1 h[c]
    %               col 3     GPR              b0001
    %               col 4     Genes            b0001 (optional: column can be empty)
    %               col 5     Proteins         AlaS (optional: column can be empty)
    %               col 6     Subsystem        Glycolysis
    %               col 7     Reversible       0
    %               col 8     Lower bound      0
    %               col 9     Upper bound      1000
    %               col 10    Objective        0    (optional: column can be empty)
    %               col 11    Confidence Score 0,1,2,3,4
    %               col 12    EC. Number       1.1.1.1
    %               col 13    Notes            N/A  (optional: column can be empty)
    %               col 14    References       PMID: 1111111  (optional: column can be empty)
    %
    % 'metabolites' tab: Required headers: needs to be complete list of metabolites, i.e., if a metabolite appears in multiple compartments it has to be represented in multiple rows. Abbreviations needs to overlap with use in Reaction List
    %               col 0     Abbreviation
    %               col 1     Description
    %               col 2     Neutral formula
    %               col 3     Charge formula
    %               col 4     Charge
    %               col 5     Compartment
    %               col 6     KEGG ID
    %               col 7     PubChem ID
    %               col 8     ChEBI ID
    %               col 9     InChI string
    %               col 10    SMILES
    %               col 11    HMDB ID
    %
    %
    % OUTPUT
    % model         cobrapy model """

    excel = pandas.ExcelFile(excel_file)
    for sheet in excel.sheet_names:
        if sheet == "Reaction List" and parse == "cobra_string":
            reactions = excel.parse(sheet,index_col=None)
        elif 'reaction' in sheet.lower():
            reactions = excel.parse(sheet,index_col=None)
        if sheet == "Metabolite List" and parse == "cobra_string":
            metabolites = excel.parse(sheet,index_col=None)
        elif 'metabolite' in sheet.lower():
            metabolites = excel.parse(sheet,index_col=None)

    cobra_reaction_position = ['Abbreviation','Description','Reaction','GPR','Genes','Proteins','Subsystem','Reversible','Lower bound','Upper bound','Objective','Confidence Score','EC Number','Notes','References']
    cobra_metabolite_position = ['Abbreviation','Description','Neutral formula','Charged formula','Charge','Compartment','KEGG ID','PubChem ID','ChEBI ID','InChI string','SMILES','HMDB ID']

    if parse == "cobra_position":
        if len(reactions.columns) > 15:
            reactions = reactions.iloc[:,:15]
            reactions.columns = cobra_reaction_position
        else:
            reactions.columns = cobra_reaction_position[:len(reactions.columns)]
        if len(metabolites.columns) > 12:
            metabolites = metabolites.iloc[:,:12]
            metabolites.columns = cobra_metabolite_position
        else:
            metabolites.columns = cobra_metabolite_position[:len(metabolites.columns)]

    model = cobra.Model()
    metabolite_dic = {}
    element_re = re.compile("([A-Z][a-z]?)([0-9.]+[0-9.]?|(?=[A-Z])?)")
    for met in metabolites.index:
        met_row = metabolites.loc[met]  # pandas.Series of the metabolites
        met_id = str(met_row['Abbreviation'])
        #met_name = str(met_row[1]) if pandas.notnull(met_row[1]) else None
        met_name = str(met_row['Description']) if ('Description' in met_row.index) and pandas.notnull(met_row['Description']) else None

        if ('Charged formula' in met_row.index) and pandas.notnull(met_row['Charged formula']):
            met_formula = str(met_row['Charged formula'])
        elif ('Neutral formula' in met_row.index) and pandas.notnull(met_row['Neutral formula']):
            if ('Charge' in met_row.index) and pandas.notnull(met_row['Charge']):
                met_formula = ''
                tmp_formula = str(met_row['Neutral formula'])
                tmp_formula = tmp_formula.replace("*", "")
                parsed = element_re.findall(tmp_formula)
                for (element, count) in parsed:
                    if element != "H":
                        met_formula += element + str(count)
                    else:
                        if count == '':
                            count = 1
                        count = float(count)
                        if count.is_integer():
                            count = int(count)
                        charge = float(met_row['Charge'])
                        if charge.is_integer():
                            charge = int(charge)
                        count += charge
                        if count == 1:
                            met_formula += element
                        elif count != 0:
                            met_formula += element + str(count)
            else:
                met_formula = None
        else:
            met_formula = None
        met_compartment = str(met_row['Compartment']) if 'Compartment' in met_row.index and pandas.notnull(met_row['Compartment']) else None
        metabolite = cobra.Metabolite(met_id, formula=met_formula, name=met_name, compartment=met_compartment)
        if ('Charge' in met_row.index) and pandas.notnull(met_row['Charge']):
            metabolite.charge = float(met_row['Charge'])
            if metabolite.charge.is_integer():
                metabolite.charge = int(metabolite.charge)
        if ('KEGG ID' in met_row.index) and pandas.notnull(met_row['KEGG ID']): metabolite.kegg_id = met_row['KEGG ID']
        if 'PubChem ID' in met_row.index and pandas.notnull(met_row['PubChem ID']): metabolite.pubchem_id = str(met_row['PubChem ID'])
        if 'ChEBI ID' in met_row.index and pandas.notnull(met_row['ChEBI ID']): metabolite.chebi_id = str(met_row['ChEBI ID'])
        if 'InChI string' in met_row.index and pandas.notnull(met_row['InChI string']): metabolite.inchi_id = str(met_row['InChI string'])
        if 'SMILES' in met_row.index and pandas.notnull(met_row['SMILES']): metabolite.smiles = str(met_row['SMILES'])
        if 'HMDB ID' in met_row.index and pandas.notnull(met_row['HMDB ID']): metabolite.hmdb_id = str(met_row['HMDB ID'])
        metabolite_dic[met_id] = metabolite
        if Print:
            print(metabolite.id)

    for reac in reactions.index:
        reac_row = reactions.loc[reac]
        reaction = cobra.Reaction(str(reac_row['Abbreviation']))

        stoichiometry_list = []
        metabolite_list = []
        new_metabolite = True
        product = False
        compartment = ''
        reaction_string = reac_row['Reaction'].split(' ')
        for s in reaction_string:
            if s.startswith('['):
                if s.endswith(']:'):
                    compartment = s[:-1]
                else:
                    compartment = s
            elif s == ":" or s == "":
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
                    if s[0] == "(" and s[-1] == ")":
                        s = s[1:-1]
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
            met_id = str(metabolite_list[b])
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
                    print(met_id + " added to metabolite list in " + str(reac_row['Abbreviation']) + " in row " + str(reac+2))
                    additional_metabolite = cobra.Metabolite(met_id)
                    met = metabolite_dic[met_id] = additional_metabolite
            stoi_dic[met] = stoichiometry_list[b]
        reaction.add_metabolites(stoi_dic)
        #
        reaction.lower_bound = float('-inf')
        reaction.upper_bound = float('inf')
        if direction == 'LEFT-TO-RIGHT':
            reaction.lower_bound = 0.0
        elif direction == 'RIGHT-TO-LEFT':
            reaction.upper_bound = 0.0

        if ('Description' in reac_row.index) and pandas.notnull(reac_row['Description']): reaction.name = str(reac_row['Description'])
        if ('GPR' in reac_row.index) and pandas.notnull(reac_row['GPR']): reaction.gene_reaction_rule = str(reac_row['GPR'])
        if ('Proteins' in reac_row.index) and pandas.notnull(reac_row['Proteins']): reaction.proteins = str(reac_row['Proteins'])
        if ('Subsystem' in reac_row.index) and pandas.notnull(reac_row['Subsystem']): reaction.subsystem = str(reac_row['Subsystem'])
        if ('Lower bound' in reac_row.index) and pandas.notnull(reac_row['Lower bound']): reaction.lower_bound = float(reac_row['Lower bound'])
        if ('Upper bound' in reac_row.index) and pandas.notnull(reac_row['Upper bound']): reaction.upper_bound = float(reac_row['Upper bound'])
        if direction != "REVERSIBLE" and (reaction.lower_bound == float('-inf') or reaction.lower_bound == -1000.0) and (reaction.upper_bound == float('inf') or reaction.upper_bound == 1000.0): print("WARNING: The bounds of non-reversible reaction {} is set to (-inf, inf)".format(reaction.id))
        #print(str(reaction.lower_bound)+" "+str(reaction.upper_bound))
        if ('Confidence Score' in reac_row.index) and pandas.notnull(reac_row['Confidence Score']): reaction.confidence_score = int(reac_row['Confidence Score'])
        if ('EC Number' in reac_row.index) and pandas.notnull(reac_row['EC Number']): reaction.ec_number = str(reac_row['EC Number'])
        if ('Notes' in reac_row.index) and pandas.notnull(reac_row['Notes']): reaction.notes = {"notes":str(reac_row['Notes'])}
        if ('References' in reac_row.index) and pandas.notnull(reac_row['References']): reactions.references = str(reac_row['References'])

        model.add_reaction(reaction)
        if ('Objective' in reac_row.index) and pandas.notnull(reac_row['Objective']): reaction.objective_coefficient = float(reac_row['Objective'])
        if Print:
            print(reaction.reaction)
 
    return model

def WriteExcel(model,filename,excel_format="cobra"):
    """ excel_format = "cobra" | "cobra_old" """
    r_dict = {'Abbreviation':{},'Description':{},'Reaction':{},'GPR':{},'Genes':{},'Proteins':{},'Subsystem':{},'Reversible':{},'Lower bound':{},'Upper bound':{},'Objective':{},'Confidence Score':{},'EC Number':{},'Notes':{},'References':{}}
    for r in model.reactions:
        r_dict['Abbreviation'][r.id] = r.id
        r_dict['Description'][r.id] = getattr(r,'name','')
        r_dict['Reaction'][r.id] = r.reaction
        r_dict['GPR'][r.id] = getattr(r,'gene_reaction_rule','')
        genes = ''
        if hasattr(r,'genes'):
            for gene in r.genes:
                genes = genes + gene.id + ' '
            genes = genes[:-1]
        r_dict['Genes'][r.id] = genes
        proteins_list = getattr(r,'proteins','')
        p_str = ""
        if isinstance(proteins_list,list):
            for v in proteins_list:
                p_str += v + " or "
                p_str = p_str.rstrip(" or ")
        else:
            p_str = proteins_list
        r_dict['Proteins'][r.id] = p_str
        r_dict['Subsystem'][r.id] = getattr(r,'subsystem','')
        r_dict['Reversible'][r.id] = 1 if r.reversibility else 0
        r_dict['Lower bound'][r.id] = r.lower_bound
        r_dict['Upper bound'][r.id] = r.upper_bound
        r_dict['Objective'][r.id] = getattr(r,'objective_coefficient','')
        r_dict['Confidence Score'][r.id] = getattr(r,'confidence_score','')
        r_dict['EC Number'][r.id] = getattr(r,'ec_number','')
        r_dict['Notes'][r.id] = str(getattr(r,'notes','')) if str(getattr(r,'notes','')) != '{}' else ''
        r_dict['References'][r.id] = getattr(r,'references','')

    m_dict = {'Abbreviation':{},'Description':{},'Neutral formula':{},'Charged formula':{},'Charge':{},'Compartment':{},'KEGG ID':{},'PubChem ID':{},'ChEBI ID':{},'InChI string':{},'SMILES':{},'HMDB ID':{}, "Molecular Weights":{}}
    element_re = re.compile("([A-Z][a-z]?)([0-9.]+[0-9.]?|(?=[A-Z])?)")
    for m in model.metabolites:
        m_dict['Abbreviation'][m.id] = m.id
        m_dict['Description'][m.id] = getattr(m,'name','')
        neutral_formula = ''
        if m.charge != None and m.formula != None:
            tmp_formula = str(m.formula).replace('*', '')
            parsed = element_re.findall(tmp_formula)
            for (element, count) in parsed:
                if element != 'H':
                    neutral_formula += element + str(count)
                else:
                    if count == '':
                        count = 1
                    count = float(count)
                    if count.is_integer():
                        count = int(count)
                    count -= m.charge
                    if count == 1:
                        neutral_formula += element
                    elif count != 0:
                        neutral_formula += element + str(count)
        m_dict['Neutral formula'][m.id] = neutral_formula
        m_dict['Charged formula'][m.id] = str(getattr(m,'formula','')) if getattr(m,'formula','') != None else ''
        m_dict['Charge'][m.id] = getattr(m,'charge','')
        m_dict['Compartment'][m.id] = getattr(m,'compartment','') if getattr(m,'compartment','') != None else ''
        m_dict['KEGG ID'][m.id] = getattr(m,'kegg_id','')
        m_dict['PubChem ID'][m.id] = getattr(m,'pubchem_id','')
        m_dict['ChEBI ID'][m.id] = getattr(m,'chebi_id','')
        m_dict['InChI string'][m.id] = getattr(m,'inchi_id','')
        m_dict['SMILES'][m.id] = getattr(m,'smiles','')
        m_dict['HMDB ID'][m.id] = getattr(m,'hmdb_id','')
        m_dict["Molecular Weights"][m.id] = getattr(m,'molecular_weights','')

    reactions = pandas.DataFrame(r_dict, columns=['Abbreviation','Description','Reaction','GPR','Genes','Proteins','Subsystem','Reversible','Lower bound','Upper bound','Objective','Confidence Score','EC Number','Notes','References'])
#    reactions = reactions.loc[:, ~reactions.isin(['',None]).all()]

    metabolites = pandas.DataFrame(m_dict, columns=['Abbreviation','Description','Neutral formula','Charged formula','Charge','Compartment','KEGG ID','PubChem ID','ChEBI ID','InChI string','SMILES','HMDB ID',"Molecular Weights"])
#    metabolites = metabolites.loc[:, ~metabolites.isin(['',None]).all()]

    excel_file = pandas.ExcelWriter(filename)
    if excel_format == "cobra_old":
        reactions.to_excel(excel_file,'reactions',index=False)
    elif excel_format == "cobra":
        reactions.to_excel(excel_file,'Reaction List',index=False)
    if excel_format == "cobra_old":
        metabolites = metabolites.drop('HMDB ID', 1)
        metabolites.to_excel(excel_file,'metabolites',index=False)
    elif excel_format == "cobra":
        metabolites.to_excel(excel_file,'Metabolite List',index=False)
    excel_file.save()
