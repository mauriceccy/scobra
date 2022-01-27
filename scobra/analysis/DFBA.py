import math

def SetEquilibriumConstant(model, reaction, constant):
    """ reaction: str, constant: int
    
    Sets the equilibrium constant of a reaction
    Ex: model.SetEquilibriumConstant('R1', 1) """
    reac = model.GetReaction(reaction)
    reac.equilibrium_constant = constant

def SetEquilibriumConstants(model, constantDic):
    """ constantDic: dictionary of {reaction: constant}
    
    Sets the equilibrium constant of multiple reactions
    Ex: model.SetEquilibriumConstants({'R1':1, 'R2':2, 'R3':3}) """
    for reac in constantDic:
        model.SetEquilibriumConstant(reac, constantDic.get(reac))
        
def SetRateConstant(model, reaction, constant):
    """ reaction: str, constant: int
    
    Sets the rate constant of a reaction
    Ex: model.SetRateConstant('R1', 1) """
    reac = model.GetReaction(reaction)
    reac.rate_constant = constant
        
def SetRateConstants(model, constantDic):
    """ constantDic: dictionary of {reaction: constant}
    
    Sets the rate constant of multiple reactions
    Ex: model.SetRateConstants({'R1':1, 'R2':2, 'R3':3}) """
    for reac in constantDic:
        model.SetRateConstant(reac, constantDic.get(reac))


def SetRateEquation(model, reaction, equation):
    """ reaction: str, equation: str
    
    Sets the rate equation of a reaction. The equation must contain all metabolites on the LHS of the
    reaction.
    Ex: model.SetRateEquation('R1', 'A ** 1 * B ** 2') """
    reac = model.GetReaction(reaction)
    reac.rate_equation = equation


def SetRateEquations(model, equationDic):
    """ equationDic: dictionary of {reactions: equation}
    
    Sets the rate equation of multiple reactions. The equations must contain all metabolites on the LHS of
    the given reaction. """
    # Ex: model.SetRateEquation({'R1': 'A ** 1 * B ** 2', 'R2': 'C ** 1 * B ** 3})
    for reac in equationDic:
        model.SetRateEquation(reac, equationDic.get(reac))


def SetKinetic(model, reaction, constant, equation):
    """ reaction: str, constant: int, equation: str
    
    Sets the rate constant and rate equation of a given reaction. The equation must contain all metabolites
    on the LHS of the given reaction
    Ex: model.SetKinetic('R1', 3, 'A ** 1 * B ** 3') """
    SetEquilibriumConstant(model, reaction, constant)
    SetRateConstant(model, reaction, constant)
    SetRateEquation(model, reaction, equation)


def SetKinetics(model, constantDic, equationDic):
    """ constantDic: dictionary of {reaction: constant}, equationDic: dictionary of {reaction: equation}
    
    Sets the rate constant and rate equation of multiple given reaction. The equation must contain all
    metabolites on the LHS of the given reaction
    Ex: model.SetKinetic({'R1':1, 'R2':2, 'R3':3}, {'R1': 'A ** 1 * B ** 2', 'R2': 'C ** 1 * B ** 3}) """
    SetEquilibriumConstants(model, constantDic)
    SetRateConstants(model, constantDic)
    SetRateEquations(model, equationDic)


def SetDefaultKinetics(model, excludeList=[]):
    """ excludeList: list (default = [])
    
    Sets the default kinetics of each reaction. It is calculated as 1 * Σ (metabolite_conc ** metabolite_coef),
    derived from the reactant (LHS) stoichiometry.
    Users can exclude reactions by passing arguments through excludeList. Exchange reactions added using the
    @AddExchangeReactions() function will also be automatically excluded.
    Ex: model.SetDefaultKinetic(['Carbon_exchange']) """
    for reac in model.reactions:
        reacName = reac.id
        if reacName not in excludeList:
            if ('exchange' in reacName):
                model.SetRateEquation(reac, "EXCHANGE")
                model.SetRateConstant(reac, None)
                model.SetEquilibriumConstant(reac, None)
            elif 'reverse' not in reacName:
                metNum = 1
                equation = ""
                for met in reac.metabolites:
                    if (reac.get_coefficient(met) < 0):
                        equation = equation + \
                            str(met) + " ** " + \
                            str(- reac.get_coefficient(met))
                        
                        if (metNum < len(reac.metabolites)):
                            if (reac.get_coefficient(list(reac.metabolites)[metNum]) < 0):
                                equation = equation + " * "
                    metNum = metNum + 1

                model.SetRateEquation(reac, equation)
                model.SetRateConstant(reac, 1)
                model.SetEquilibriumConstant(reac, 1)
            else:
                metNum = -1
                equation = ""
                for met in reac.metabolites:
                    if (reac.get_coefficient(met) < 0):
                        equation = equation + \
                            str(met) + " ** " + \
                            str(- reac.get_coefficient(met))
                        if (metNum < len(reac.metabolites)):
                            if (reac.get_coefficient(list(reac.metabolites)[metNum]) < 0):
                                equation = equation + " * "
                    metNum = metNum - 1
                model.SetRateEquation(reac, equation)
                model.SetRateConstant(reac, 1)
                model.SetEquilibriumConstant(reac, 1)

def GetEquilibriumConstant(model, reaction):
    """ reaction: str
    
    Returns the equilibrium constant of a reaction
    Ex: model.GetEquilibriumConstant('R1') """
    reac = model.GetReaction(reaction)
    return reac.equilibrium_constant

def GetRateConstant(model, reaction):
    """ reaction: Reaction
    
    Returns the constant of the kinetics of the reaction """
    return(model.GetReaction(reaction).rate_constant)


def GetRateEquation(model, reaction):
    """ reaction: Reaction
    
    Returns the string representation of the equation of the kinetics of the reaction """
    return(model.GetReaction(reaction).rate_equation)


def CheckKinetic(model, reaction):
    """ reaction: Reaction
    
    Returns whether the kinetics (constant and equation) are set for a certain reaction """
    reac = model.GetReaction(reaction)
    if (hasattr(reac, 'rate_equation') == False) or (hasattr(reac, 'rate_constant') == False) or (hasattr(reac, 'equilibrium_constant') == False):
        return False
    else:
        return True

def GetKinetic(model, reaction):
    """ reaction: Reaction
    
    Returns the string representation of the kinetic of a given reaction
    Ex: GetKinetic('R1') """
    reac = model.GetReaction(reaction)
    return(str(reac.rate_constant) + "*" + reac.rate_equation)


def PrintKinetic(model, reaction):
    """ reaction: str
    
    Prints the string representation of the kinetic of a given reaction
    Ex: PrintKinetic('R1') """
    reac = model.GetReaction(reaction)
    out = "Rate Equation for " + reac.id + ": "
    if hasattr(reac, "rate_constant") and hasattr(reac, "rate_equation"):
        out = out + str(reac.rate_constant) + " * (" + reac.rate_equation + ")"
    else:
        out = out + "Not Set"
    print(out)


def PrintKinetics(model, reactionList=None):
    """ reactionList: list (default = None)
    
    Prints the string representation of the kinetic of all given reactions in the reactionList. If no
    arguments are given, kinetics of all reactions in the model are printed
    Ex: PrintKinetics() """
    if reactionList == None:
        for reac in model.reactions:
            model.PrintKinetic(reac)
    else:
        for reac in model.reactions:
            if model.GetReactionName(reac) in reactionList:
                model.PrintKinetic(reac)


def CalConstrFromRateEquation(model, reaction, concDict):
    """ reaction: str, concDict: dictionary of {metabolite: concentration}, zeroLB: Boolean
    
    Calculates the constraints of a reaction from the concentration dictionary and the kinetics of a reaction
    If the reaction is an exchange reaction (therefore contains the str 'EXCHANGE' as the rate equation),
    the constraint would equal to the minimum and maximum bounds of the model (default = inf). If the zeroLB is set
    as True, the lower bound of non-exchange reactions is set as zero.
    Ex: CalConstrFromRateEquation('R1', {'A': 1, 'B': 2}) """
    
    # TODO: If reactant and product metabolite, both have 0 conc.
    # TODO: n_R and n_P equations needs to verified
    
    # For details of the formula, please view the dFBAprotocal file.
    equation = GetKinetic(model, reaction)
    
    if (('EXCHANGE' not in equation) & ('None' not in equation)):
        reac = model.GetReaction(reaction)
        
        # Reaction Quotient, Q
        Q = 1
        
        # Initialize the amount of reactants
        n_R = 1
        
        # Initialize the amount of products
        n_P = 1
        
        # Initialize two booleans to keep track of met with zero concentrations
        zero_reac_conc = False
        zero_pro_conc = False
        
        for met in reac.metabolites:
            met_coeff = reac.get_coefficient(met)
            met_name = str(met)
            
            # Reactant metabolite
            if met_coeff < 0:
                
                # Update the amount of reactants
                n_R *= concDict[met_name]**abs(met_coeff)
                if concDict[met_name] == 0:
                    zero_reac_conc = True
                    
                    # If any product metabolite conc 0, then Q is infinite
                    Q = math.inf
                else:
                    
                    # Update the Q
                    Q *= (1 / concDict[met_name]**abs(met_coeff))
                
            # Product metabolite (met_coeff > 0)
            else:
                
                # Update the amount of products
                n_P *= concDict[met_name]**met_coeff
                if concDict[met_name] == 0:
                    zero_pro_conc = True
                    
                    # If any reactant metabolite conc 0, then Q is 0
                    Q = 0
                else:
                    # Update the Q
                    Q *= (concDict[met_name]**met_coeff)

        # Get equilibrium constant
        K_eq = GetEquilibriumConstant(model, reac)
        
        # Get forward rate constant
        k_fwd = GetRateConstant(model, reac)
        
        # Calculate k_rev and k_exc
        k_rev = k_fwd/K_eq
        k_exc = k_fwd + k_rev
        
        # Reaction in forward direction
        if Q < K_eq:
            lb = k_fwd * n_R
            ub = n_R - (k_rev/ k_exc) * (n_P + n_R)
            
        # Reaction in equilibrium
        elif Q == K_eq:
            ub = lb = 0
        
        # Reaction in backward direction (Q > K_eq)
        else:
            lb = n_R - (k_rev/ k_exc) * (n_P + n_R)
            ub = - k_rev * n_P
        
        # If we have zero concentration metabolite in both reactants and products, set ub = lb = 0
        if zero_reac_conc and zero_pro_conc:
            ub = lb = 0
        
        # Since lower bound cannot be higher upper bound, we set the max of lower bound to be
        # the upper bound
        if (lb > ub):
            lb = ub
            
        return(lb, ub)
            
    else:
        
        # For exchange reactions, the maximum bound cannot exceed the value in the metabolite concentraion dictionary
        ub = concDict.get(list(reaction.metabolites)[0].id)
        return(- model.bounds, ub)


def CalConstrFromRateEquations(model, concDict, simList=None):
    """ concDict: dictionary of {metabolite: concentration}, zeroLB: Boolean
    
    Calculates the constraints of a reaction from the concentration dictionary and the kinetics of a given
    reactions. The constraints of all the reactions in the model are calculated and a constrDict in the form
    of {metabolite: constraint} is returned. If the zeroLB is set as True,
    the lower bound of non-exchange reactions is set as zero.
    Ex: CalConstrFromRateEquations({'A': 1, 'B': 2}) """
    constrDict = {}
    if simList == None:
        for reac in model.reactions:
            if CheckKinetic(model, reac):
                constrDict[reac] = CalConstrFromRateEquation(
                    model, reac, concDict)
    else:
        for reac in simList:
            if CheckKinetic(model, reac):
                constrDict[reac] = CalConstrFromRateEquation(
                    model, reac, concDict)
    return constrDict


def SetConstrFromRateEquation(model, concDict, simList):
    """ concDict: dictionary of {metabolite: concentration}, zeroLB: Boolean
    
    Calculates the constraints of all reactions in a model from the concentration dictionary and the
    kinetics of each reaction. Then, the constraint for corresponding metabolites is set. If the zeroLB is set as True,
    the lower bound of non-exchange reactions is set as zero.
    Ex: SetConstrFromRateEquation({'A': 1, 'B': 2}, True) """
    model.SetConstraints(CalConstrFromRateEquations(
        model, concDict, simList))


def AddExchangeReactions(model, arg=None):
    """ arg = [] OR {} (default = None)
    
    Adds the default exchange reaction of all metabolites in the model, unless the metList is defined.
    If arg = [], we feed the function a list of metabolites to create default exchange reactions
    If arg = {}, we feed the function a dictionary of {reaction : metabolite} to creat custom exchange reactions
    AddExchangeReactions(['A', 'B'])
    AddExchangeReactions({'testReaction', 'testMetabolite'}) """
    if isinstance(arg, list):
        for met in arg:
            if met in model.Metabolites():
                reacName = model.GetMetaboliteName(met) + "_exchange"
                model.AddReaction(reacName, {met: 1}, rev=True)
                model.AddToExchangeDict({model.GetReaction(
                    reacName), model.GetMetabolite(met)})
                model.AddAsExchangeReaction(reacName, met)
    elif isinstance(arg, dict):
        for key in arg.keys():
            model.AddReaction(key, {arg[key]: 1}, rev=True)
            model.SetAsExchangeReaction(key, arg[key])
    else:
        for met in model.Metabolites():
            reacName = model.GetMetaboliteName(met) + "_exchange"
            model.AddReaction(reacName, {met: 1}, rev=True)
            model.SetAsExchangeReaction(reacName, met)


def UpdateConc(model, solution, concDict, constSupplyDict=None, exchangeDic=None):
    for key in solution:
        if "_exchange" in key:
            met = key[:-9]
            if constSupplyDict != None and met in constSupplyDict.keys():
                concDict[met] = constSupplyDict[met]
            else:
                prev = concDict.get(met)
                delta = solution.get(key)
                concDict[met] = (prev - delta)
    model.SetConcentrations(concDict)
