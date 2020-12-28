from ..classes import model, reaction


def SetRateConstant(model, reaction, constant):
    # reaction: str, constant: int
    #
    # Sets the rate constant of a reaction
    # Ex: model.SetRateConstant('R1', 1)
    reac = model.GetReaction(reaction)
    reac.rate_constant = constant


def SetRateConstants(model, constantDic):
    # constantDic: dictionary of {reaction: constant}
    #
    # Sets the rate constant of multiple reactions
    # Ex: model.SetRateConstants({'R1':1, 'R2':2, 'R3':3})
    for reac in constantDic:
        model.SetRateConstant(reac, constantDic.get(reac))


def SetRateEquation(model, reaction, equation):
    # reaction: str, equation: str
    #
    # Sets the rate equation of a reaction. The equation must contain all metabolites on the LHS of the
    # reaction.
    # Ex: model.SetRateEquation('R1', 'A ** 1 * B ** 2')
    reac = model.GetReaction(reaction)
    reac.rate_equation = equation


def SetRateEquations(model, equationDic):
    # equationDic: dictionary of {reactions: equation}
    #
    # Sets the rate equation of multiple reactions. The equations must contain all metabolites on the LHS of
    # the given reaction.
    # Ex: model.SetRateEquation({'R1': 'A ** 1 * B ** 2', 'R2': 'C ** 1 * B ** 3})
    for reac in equationDic:
        model.SetRateEquation(reac, equationDic.get(reac))


def SetKinetic(model, reaction, constant, equation):
    # reaction: str, constant: int, equation: str
    #
    # Sets the rate constant and rate equation of a given reaction. The equation must contain all metabolites
    # on the LHS of the given reaction
    # Ex: model.SetKinetic('R1', 3, 'A ** 1 * B ** 3')
    SetRateConstant(model, reaction, constant)
    SetRateEquation(model, reaction, equation)


def SetKinetics(model, constantDic, equationDic):
    # constantDic: dictionary of {reaction: constant}, equationDic: dictionary of {reaction: equation}
    #
    # Sets the rate constant and rate equation of multiple given reaction. The equation must contain all
    # metabolites on the LHS of the given reaction
    # Ex: model.SetKinetic({'R1':1, 'R2':2, 'R3':3}, {'R1': 'A ** 1 * B ** 2', 'R2': 'C ** 1 * B ** 3})
    SetRateConstants(model, constantDic)
    SetRateEquations(model, equationDic)


def SetDefaultKinetics(model, excludeList=[]):
    # excludeList: list (default = [])
    #
    # Sets the default kinetics of each reaction. It is calculated as 1 * Σ (metabolite_conc ** metabolite_coef),
    # derived from the reactant (LHS) stoichiometry.
    # Users can exclude input reactions (in the form of '<=> metabolite') by passing arguments through excludeList
    # The kinetics of exclude reactions will be denotated as 'None*EXCHANGE'. Input reactions added using the
    # @AddExchangeReactions() function will also be automatically excluded.
    # Ex: model.SetDefaultKinetic(['Carbon_exchange'])
    for reac in model.reactions:
        reacName = reac.id
        if ('exchange' in reacName) or (reacName in excludeList):
            model.SetRateEquation(reac, "EXCHANGE")
            model.SetRateConstant(reac, None)
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


def GetKinetic(model, reaction):
    # reaction: str
    #
    # Returns the string representation of the kinetic of a given reaction
    # Ex: GetKinetic('R1')
    reac = model.GetReaction(reaction)
    return(str(reac.rate_constant) + "*" + reac.rate_equation)


def PrintKinetic(model, reaction):
    # reaction: str
    #
    # Prints the string representation of the kinetic of a given reaction
    # Ex: PrintKinetic('R1')
    reac = model.GetReaction(reaction)
    print("Rate Equation for " + reac.id + ": " +
          str(reac.rate_constant) + " * (" + reac.rate_equation + ")")


def PrintKinetics(model, reactionList=None):
    # reactionList: list (default = None)
    #
    # Prints the string representation of the kinetic of all given reactions in the reactionList. If no
    # arguments are given, kinetics of all reactions in the model are printed
    # Ex: PrintKinetics()
    if reactionList == None:
        for reac in model.reactions:
            model.PrintKinetic(reac)
    else:
        for reac in model.reactions:
            if model.GetReactionName(reac) in reactionList:
                model.PrintKinetic(reac)


def CalConstrFromRateEquation(model, reaction, concDict):
    # reaction: str, concDict: dictionary of {metabolite: concentration}
    #
    # Calculates the constraints of a reaction from the concentration dictionary and the kinetics of a reaction
    # If the reaction is an exchange reaction (therefore contains the str 'EXCHANGE' as the rate equation),
    # the constraint would equal to the minimum and maximum bounds of the model (default = inf)
    # Ex: CalConstrFromRateEquation('R1', {'A': 1, 'B': 2})
    # TODO: Currently, the function calculates one value and returns it as a couple such as (1, 1). Extend
    #       the function so that a range of constraints can be calculated
    equation = GetKinetic(model, reaction)
    if (('EXCHANGE' not in equation) & ('None' not in equation)):
        return eval(equation, concDict)
    else:
        # For exchange reactions, the maximum bound cannot exceed the value in the metabolite concentraion dictionary
        ub = concDict.get(list(reaction.metabolites)[0].id)
        return(- model.bounds, ub)


def CalConstrFromRateEquations(model, concDict):
    # concDict: dictionary of {metabolite: concentration}
    #
    # Calculates the constraints of a reaction from the concentration dictionary and the kinetics of a given
    # reactions. The constraints of all the reactions in the model are calculated and a constrDict in the form
    # of {metabolite: constraint} is returned.
    # Ex: CalConstrFromRateEquations({'A': 1, 'B': 2})
    constrDict = {}
    for reac in model.reactions:
        constrDict[reac] = CalConstrFromRateEquation(model, reac, concDict)
    return constrDict


def SetConstrFromRateEquation(model, concDict):
    # concDict: dictionary of {metabolite: concentration}
    #
    # Calculates the constraints of all reactions in a model from the concentration dictionary and the
    # kinetics of each reaction. Then, the constraint for corresponding metabolites is set
    # Ex: SetConstrFromRateEquation({'A': 1, 'B': 2})
    model.SetConstraints(CalConstrFromRateEquations(model, concDict))


def AddExchangeReactions(model, metList=None):
    # metList = [] (default = None)
    #
    # Adds the exchange reaction of all metabolites in the model, unless the desired metabolites are specified
    # in the metList.
    # AddExchangeReactions(['A', 'B'])
    if metList is not None:
        for met in model.Metabolites():
            if met in metList:
                reacName = model.GetMetaboliteName(met) + "_exchange"
                model.AddReaction(reacName, {met: 1}, rev=True)
    else:
        for met in model.Metabolites():
            reacName = model.GetMetaboliteName(met) + "_exchange"
            model.AddReaction(reacName, {met: 1}, rev=True)


def UpdateConc(model, solution, concDict):
    for key in solution:
        if "exchange" in key:
            met = key[:-9]
            prev = concDict.get(met)
            delta = solution.get(key)
            concDict[met] = (prev - delta)
    return concDict


"""  End of new functions in dev.  """
""""""""""""""""""""""""""""""""""""""
