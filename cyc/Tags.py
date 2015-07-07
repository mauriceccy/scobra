AtomCharge =    "ATOM-CHARGES"
CannotBalance =     "CANNOT-BALANCE?"
Cats =            "CATALYZES"
ChemForm = "CHEMICAL-FORMULA"
Coeff =           "^COEFFICIENT"
Comment=     "COMMENT"
ComName =   "COMMON-NAME"
Compartment =   "^COMPARTMENT"
CompOf =      "COMPONENT-OF"
Comps =        "COMPONENTS"
DBLinks =      "DBLINKS"
Delim =          " - "
EC =               "EC-NUMBER"
Enz =              "ENZYME"
EnzReac =       "ENZYMATIC-REACTION"
Gene =            "GENE"
InPath =          "IN-PATHWAY"                                # the pathway(s) in which a reaction is found
InChI =         "INCHI"
Left =              "LEFT"                                             # Left (substrate) of a reaction
LeftEnd =         "LEFT-END-POSITION"                   # leftmost base in a gene
MolWt =           "MOLECULAR-WEIGHT"
Prod=              "PRODUCT"
Reac =             "REACTION"
ReacEq =         "REACTION-EQUATION"
ReacList =       "REACTION-LIST"                              # reactions in a pathway
ReacDir =        "REACTION-DIRECTION"

RecEnd =        "//"                           # End of Record

RegBy=          "REGULATED-BY"
Regul =         "REGULATOR"
Regulates =    "REGULATES"
RegEnt =       "REGULATED-ENTITY"

RegMode =     "MODE"
Right =           "RIGHT"                                             # Right (product) of reaction
RightEnd =     "RIGHT-END-POSITION"                     # rightmost base in a gene
SMILES =        "SMILES"
SuPath =         "SUPER-PATHWAY"                            # defined but not used in ecocyc ? future expansion ?
Synonyms =      "SYNONYMS"
TransDir=       "TRANSCRIPTION-DIRECTION"
Types  =     "TYPES"
UID =              "UNIQUE-ID"


Import =        "#IMPORT"                                        # not part of ecocyc - use to identify files imported from 3rd party input


                       ## tagged comments, generated when converting non-biocyc - biocyc
TCReac=         "COMMENT <Reaction>"

NR = "Not reported"   # not strictly a Tag, default value for missing essential fields




def IsComment(string):                                           # global comment, not comment field in record
    return string.find("#") ==0  or string.find(RecEnd) == 0

#
