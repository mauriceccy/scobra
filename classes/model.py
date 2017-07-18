import exceptions
import types
import re
import math
from collections import defaultdict
import numpy
try:
    import scipy
except ImportError:
    pass

import cobra
from cobra import Metabolite
from cobra import Reaction
from cobra import Gene
from cobra.flux_analysis import double_deletion
from cobra.flux_analysis import moma
from cobra.flux_analysis import single_deletion
from cobra.flux_analysis import phenotype_phase_plane

from ..analysis import FVA
from ..analysis import FCA
from ..analysis import Pareto
from ..analysis import Scan
from ..analysis import RWFM
from ..analysis import MOMA
from ..analysis import ROOM
from ..analysis import GeometricFBA
from ..analysis import FluxSum
from ..analysis import Graph
from ..analysis import MinSolve
from ..manipulation import Reversible
from ..classes.flux import flux

#############################################################################


class model(cobra.Model):

    def __init__(self, existing_model=None, bounds=1000.0):
        if type(existing_model) == model:
            self.__dict__ = existing_model.__dict__
        else:
            cobra.Model.__init__(self, existing_model)
            self.objective_direction = "minimize"
            self.solver = None
            self.quadratic_component = None
            self.bounds = bounds
            self.SetBounds(bounds=bounds)

    def WriteModel(self, filename, model_format=None, excel_format="cobra",
                   sbml_level=2, sbml_version=1, fbc=False, ExtReacs=[]):
        """ model_format = "sbml" | "excel" | "matlab" | "json" | "cobra" | "cobra_old" | "scrumpy" """
        from ..io import IO
        IO.WriteModel(model=self, filename=filename, model_format=model_format,
            excel_format=excel_format, sbml_level=sbml_level,
            sbml_version=sbml_version, fbc=fbc, ExtReacs=ExtReacs)

    def WriteFile(self, *args, **kwargs):
        self.WriteModel(*args, **kwargs)

    def ToFile(self, *args, **kwargs):
        self.WriteModel(*args, **kwargs)

    def Copy(self):
        return model(self.copy())

    def SubModel(self, reactions):
        new_model = model()
        for reac in reactions:
            if not isinstance(reac, Reaction):
                reac = self.GetReaction(reac)
            new_model.add_reaction(reac)
        return new_model

    def DuplicateModel(self, suffixes):
        """ suffixes = list of strings of suffixes """
        big_model = model()
        for sf in suffixes:
            sf_model = self.copy()
            for reac in sf_model.reactions:
                reac.id += sf
            for met in sf_model.metabolites:
                met.id += sf
            sf_model.repair()
            big_model.MergeWithModel(sf_model)
        return big_model

    def MergeWithModel(self, other_model, replace_with_new=False):
        """ keep attributes of current model if there is repetition in IDs  """
        for reac in other_model.reactions:
            if reac.id not in self.Reactions():
                self.add_reaction(reac)
            else:
                if replace_with_new:
                    self.DelReaction(reac.id)
                    self.add_reaction(reac)

    def GetReaction(self, reac):
        if not isinstance(reac, Reaction):
            reac = self.reactions[self.reactions.index(reac)]
        return reac

    def GetMetabolite(self, met):
        if not isinstance(met, Metabolite):
            met = self.metabolites[self.metabolites.index(met)]
        return met

    def GetGene(self, gene):
        if not isinstance(gene, Gene):
            gene = self.genes[self.genes.index(gene)]
        return gene

    def GetReactions(self, reactions):
        return [self.GetReaction(reac) for reac in reactions]

    def GetMetabolites(self, metabolites):
        return [self.GetMetabolite(met) for met in metabolites]

    def GetGenes(self, genes):
        return [self.GetGene(gene) for gene in genes]

    def GetReactionName(self, reac):
        if isinstance(reac, Reaction):
            reac = reac.id
        return reac

    def GetMetaboliteName(self, met):
        if isinstance(met, Metabolite):
            met = met.id
        return met

    def GetGeneName(self, gene):
        if isinstance(gene, Gene):
            gene = gene.id
        return gene

    def GetReactionNames(self, reactions):
        return [self.GetReactionName(reac) for reac in reactions]

    def GetMetaboliteNames(self, metabolites):
        return [self.GetMetaboliteName(met) for met in metabolites]

    def GetGeneNames(self, genes):
        return [self.GetGeneName(gene) for gene in genes]

    def Reactions(self, f=None):
        reacs = self.reactions.list_attr("id")
        if f:
            for reac in list(reacs):
                if f not in reac:
                    reacs.remove(reac)
        return reacs

    def Metabolites(self, f=None):
        mets = self.metabolites.list_attr("id")
        if f:
            for met in list(mets):
                if f not in met:
                    mets.remove(met)
        return mets

    def Genes(self, f=None):
        gs = self.genes.list_attr("id")
        if f:
            for g in list(gs):
                if f not in g:
                    gs.remove(g)
        return gs

    def InvolvedWith(self, thing, thing_type=None, AsName=False):
        """ thing_type = None | "reaction" | "metabolite" """
        if thing in self.Reactions() or thing in self.reactions:
            if thing_type == None or 'reac' in thing_type:
                thing = self.GetReaction(thing)
                rv = dict(thing.metabolites)
                if AsName:
                    for m in list(rv.keys()):
                        rv[self.GetMetaboliteName(m)] = rv.pop(m)
                return rv
        elif thing in self.Metabolites() or thing in self.metabolites:
            if thing_type == None or 'met' in thing_type:
                thing = self.GetMetabolite(thing)
                reactions = thing.reactions
                rv = {}
                for reac in reactions:
                    if AsName:
                        rv[self.GetReactionName(reac)
                            ] = reac.metabolites[thing]
                    else:
                        rv[reac] = reac.metabolites[thing]
                return rv

    def PrintReaction(self, reaction, AsMetNames=False):
        reacname = self.GetReactionName(reaction)
        reacstoi = self.GetReaction(reaction).build_reaction_string(AsMetNames)
        print reacname + '\t' + reacstoi

    def PrintReactions(self, reactions=None, AsMetNames=False):
        if reactions == None:
            reactions = self.reactions
        elif isinstance(reactions,str):
            reactions = self.Reactions(reactions)
        for reac in reactions:
            self.PrintReaction(reac, AsMetNames=AsMetNames)

    def AssignMetabolitesNeutralFormula(self):
        element_re = re.compile("([A-Z][a-z]?)([0-9.]+[0-9.]?|(?=[A-Z])?)")
        for met in self.metabolites:
            if met.charge != None and met.formula != None:
                neutral_formula = ''
                tmp_formula = met.formula.formula.replace("*", "")
                parsed = element_re.findall(tmp_formula)
                for (element, count) in parsed:
                    if element != "H":
                        neutral_formula += element + str(count)
                    else:   # H not added if H is not in the formula
                        if count == '':
                            count = 1
                        count = float(count)
                        if count.is_integer():
                            count = int(count)
                        count -= met.charge
                        if count == 1:
                            neutral_formula += element
                        elif count != 0:
                            neutral_formula += element + str(count)
                        else:
                            if len(parsed) == 1:    # for proton
                                neutral_formula += "H"
                met.neutral_formula = neutral_formula

    @property
    def ReactionsToGenesAssociations(self):
        rv = {}
        for reac in self.reactions:
            genes = self.GetGeneNames(reac.genes)
            rv[reac.id] = genes
        return rv

    @property
    def GenesToReactionsAssociations(self):
        rv = {}
        for gene in self.genes:
            reacs = self.GetReactionNames(gene.reactions)
            rv[gene.id] = reacs
        return rv

    @property
    def ReactionsToSubsystemsAssociations(self):
        rv = {}
        for reac in self.reactions:
            subsystems = getattr(reac, 'subsystem', '').split('|')
            if '' in subsystems:
                subsystems.remove('')
            rv[reac.id] = subsystems
        return rv

    @property
    def SubsystemsToReactionsAssociations(self):
        rv = defaultdict(list)
        reac2ss = self.ReactionsToSubsystemsAssociations
        for reac in reac2ss:
            for ss in reac2ss[reac]:
                rv[ss].append(reac)
        return dict(rv)

    @property
    def GenesToSubsystemsAssociations(self):
        rv = {}
        rs = self.ReactionsToSubsystemsAssociations
        for gene in self.genes:
            subsystems = set()
            reacs = self.GetReactionNames(gene.reactions)
            for reac in reacs:
                subsystems = subsystems.union(rs[reac])
            rv[gene.id] = list(subsystems)
        return rv

    @property
    def SubsystemsToGenesAssociations(self):
        rv = defaultdict(list)
        gene2ss = self.GenesToSubsystemsAssociations
        for gene in gene2ss:
            for ss in gene2ss[gene]:
                rv[ss].append(gene)
        return dict(rv)

    def NumberOfAssociations(self, associations='GeneReaction'):
        """ associations = GeneReaction|GeneSubsystem|ReactionSubsystem """
        if isinstance(associations, basestring):
            if ('gene' in associations.lower()) and ('reac' in associations.lower()):
                associations = self.GenesToReactionsAssociations
            elif ('gene' in associations.lower()) and ('subsystem' in associations.lower()):
                associations = self.GenesToSubsystemsAssociations
            elif ('reac' in associations.lower()) and ('subsystem' in associations.lower()):
                associations = self.ReactionsToSubsystemsAssociations
        rv = 0
        for b in associations:
            rv += len(associations[b])
        return rv

    def Isozymes(self):
        iso = []
        skip = []
        for x in range(len(self.reactions)):
            if x not in skip:
                iso_x = [self.reactions[x].id]
                for y in range(x+1, len(self.reactions)):
                    if self.reactions[x].metabolites == self.reactions[y].metabolites:
                        iso_x.append(self.reactions[y].id)
                        skip.append(y)
                if len(iso_x) > 1:
                    iso.append(iso_x)
        return iso

    def SplitRev(self):
        Reversible.SplitRev(self)

    def MergeRev(self, update_solution=True):
        Reversible.MergeRev(self, update_solution=update_solution)

    def Optimal(self):
        if self.solution.status == "optimal" and not math.isnan(
                                                    self.solution.f):
            return True
        else:
            return False

    def GetStatusMsg(self):
        return self.solution.status

    def SetBounds(self, bounds=1000.0, thres=1000.0):
        for reac in self.reactions:
            if reac.lower_bound <= -thres or reac.lower_bound==None:
                reac.lower_bound = -bounds
            if reac.upper_bound >= thres or reac.upper_bound==None:
                reac.upper_bound = bounds
        self.bounds = bounds

    def SetAllRev(self):
        """ remove all constraint!! set all reactions to reversible """
        for reac in self.reactions:
            reac.lower_bound = -self.bounds
            reac.upper_bound = self.bounds

    def Solve(self,PrintStatus=True):
        self.optimize(objective_sense=self.objective_direction,
                      solver=self.solver,
                      quadratic_component=self.quadratic_component)
        #,tolerance_optimality=0.0, tolerance_feasibility=0.0,tolerance_barrier=0.0,tolerance_integer=0.0)
        if PrintStatus:
            print self.solution.status

    def MinFluxSolve(self, PrintStatus=True, PrimObjVal=True,
                     norm="linear", weighting='uniform', ExcReacs=[]):
        """ norm = "linear" | "euclidean"
            weighting = "uniform" | "random" """
        MinSolve.MinFluxSolve(self, PrintStatus=PrintStatus,
                              PrimObjVal=PrimObjVal, norm=norm,
                              weighting=weighting, ExcReacs=ExcReacs)
    def AdjustedMinFluxSolve(self, PrintStatus=True, PrimObjVal=True, weighting='uniform', ExcReacs=[],
                             SolverName=None, StartToleranceVal = 0,DisplayMsg=False):
        
        """ Adjusts the Minflux_objective constraint for feasible solution
            StartToleranceVal = starting tolerance value"""
        MinSolve.AdjustedMinFluxSolve(self, PrintStatus=PrintStatus,
                              PrimObjVal=PrimObjVal,
                              weighting=weighting, ExcReacs=ExcReacs,
                                      SolverName=SolverName, Tolerance = StartToleranceVal,DisplayMsg=DisplayMsg)


        

    def MinReactionsSolve(self, PrintStatus=True, PrimObjVal=True,
                          ExcReacs=[]):
        MinSolve.MinReactionsSolve(self, PrintStatus=PrintStatus,
                              PrimObjVal=PrimObjVal, ExcReacs=ExcReacs)


    def SetObjDirec(self, direc="Min"):
        if direc in ["Min", "min", "minimize", "minimise"]:
            self.objective_direction = "minimize"
        elif direc in ["Max", "max", "maximize", "maximise"]:
            self.objective_direction = "maximize"
        else:
            raise exceptions.ValueError, direc

    def SetObjective(self, objective):
        if isinstance(objective, dict):
            for reac in objective.keys():
                reacval = objective[reac]
                reac = self.GetReaction(reac)
                reac.objective_coefficient = reacval
        elif (type(objective) in types.StringTypes) or isinstance(
                                                objective, Reaction):
            reac = self.GetReaction(objective)
            reac.objective_coefficient = 1
        else:   # list, tuple, set
            for reac in objective:
                reac = self.GetReaction(reac)
                reac.objective_coefficient = 1

    def SetQuadraticObjective(self, objective):
        if self.quadratic_component == None:
            diag = scipy.array([0]*len(self.reactions))
        else:
            diag = self.quadratic_component.diagonal()
        if isinstance(objective, dict):
            for reac in objective.keys():
                reacval = objective[reac]
                reac = self.GetReactionName(reac)
                idx = self.reactions.index(reac)
                diag[idx] = reacval
        elif (type(objective) in types.StringTypes) or isinstance(
                                                objective, Reaction):
            reac = self.GetReactionName(objective)
            idx = self.reactions.index(reac)
            diag[idx] = 1
        else:   # list, tuple, set
            for reac in objective:
                reac = self.GetReactionName(reac)
                idx = self.reactions.index(reac)
                diag[idx] = 1
        q = scipy.sparse.diags([diag],[0], len(self.reactions),
                               len(self.reactions)).todok()
        self.quadratic_component = q

    def ZeroObjective(self, IncQuad=True):
        for reac in self.Reactions():
            self.SetObjective({reac:0})
        if IncQuad:
            self.quadratic_component = None

    def GetObjVal(self):
        return self.solution.f

    def GetObjDirec(self):
        return self.objective_direction

    def GetObjective(self, IncZeroes=False):
        obj = {}
        for reac in self.reactions:
            objcoef = reac.objective_coefficient
            if IncZeroes or (not numpy.allclose(objcoef,0.0)):
                obj[reac.id] = objcoef
        return obj

#######################################################

    def GetConstraints(self, reaclist=None):
        if not reaclist:
            reaclist = self.Reactions()
        elif isinstance(reaclist,str):
            reaclist = self.Reactions(reaclist)
        rv = {}
        for reac in reaclist:
            rv[reac] = self.GetConstraint(reac)
        return rv

    def GetConstraint(self, reac):
        """ post: give constraints in forward direction """
        reac = self.GetReaction(reac)
        lb = reac.lower_bound
        ub = reac.upper_bound
        return (lb,ub)

    def SetConstraints(self, constraintdic):
        """ pre: {"R1":(lb,ub)} """
        for reac in constraintdic.keys():
            self.SetConstraint(reac,constraintdic[reac][0],
                               constraintdic[reac][1])

    def SetConstraint(self, reac, lb, ub):
        """ pre: set constraint in forward direction """
        reac = self.GetReaction(reac)
        if lb == None:
            lb = -self.bounds
        reac.lower_bound = lb
        if ub == None:
            ub = self.bounds
        reac.upper_bound = ub

    def SetFixedFlux(self, fluxdic):
        """ pre: fluxdic = {"R1":1} """
        for reac in fluxdic:
            self.SetConstraint(reac, fluxdic[reac], fluxdic[reac])

    def GetState(self):
        constraintdic = self.GetConstraints()
        obj = self.GetObjective(IncZeroes=True)
        objdirec = self.GetObjDirec()
        solver = self.solver
        quad = self.quadratic_component
        bounds = self.bounds
        sol = self.solution
        return {"constraints":constraintdic, "objective":obj,
                "objective_direction":objdirec, "solver":solver,
                "quaduatic_component":quad, "bounds":bounds, "solution":sol}

    def SetState(self, state, IncSol=True):
        self.SetConstraints(state["constraints"])
        self.SetObjective(state["objective"])
        self.SetObjDirec(state["objective_direction"])
        self.solver = state["solver"]
        self.quadratic_component = state["quaduatic_component"]
        self.SetBounds(bounds=state["bounds"])
        if IncSol:
            self.solution = state["solution"]

    def SetSumReacsConstraint(self, reacsdic, bounds, name=None):
        """ bounds = val | (lb,ub) """
        if not name:
            name = str(reacsdic)
        if name+"_sum_reaction" in self.Reactions() or \
            name+"_sum_metabolite" in self.Metabolites():
            raise ValueError(name+" already in model, constraint not added")
        else:
            metabolite = Metabolite(id=name+"_sum_metabolite")
            for reac in reacsdic:
                reacval = reacsdic[reac]
                reac = self.GetReaction(reac)
                reac.add_metabolites({metabolite:reacval})
            self.AddReaction(name+"_sum_reaction", {metabolite:-1},
                             bounds=bounds)

    def DelSumReacsConstraint(self, sumreacs=None):
        if not sumreacs:
            sumreacs = []
            for reac in self.Reactions():
                if reac.endswith("_sum_reaction"):
                    sumreacs.append(reac)
            for met in self.Metabolites():
                if met.endswith("_sum_metabolite"):
                    sumreacs.append(met)
        elif isinstance(sumreacs,str):
            if not (sumreacs.endswith("_sum_reaction") or
                sumreacs.endswith("_sum_metabolite")):
                sumreacs = [sumreacs+"_sum_reaction",
                            sumreacs+"_sum_metabolite"]
        for sr in sumreacs:
            if sr in self.Reactions():
                self.DelReaction(sr)
            if sr in self.Metabolites():
                self.DelMetabolite(sr)

    def SetObjAsConstraint(self, name='Objective', subopt=1.0):
        self.Solve(PrintStatus=False)
        if self.Optimal():
            objval = self.GetObjVal()
            objective = self.GetObjective()
            if self.GetObjDirec == "minimize":
                bounds = (objval,objval/subopt)
            else:
                bounds = (subopt*objval,objval)
            self.SetSumReacsConstraint(reacsdic=objective, bounds=bounds,
                                       name=name)
        else:
            self.GetStatusMsg()

    def DelObjAsConstraint(self, name='Objective'):
        self.DelSumReacsConstraint(name)

    def SetReacsFixedRatio(self, ratiodic, GetMetName=False):
        """ ratiodic = {"R1":1,"R2":2} """
        temp_rd = {}
        for reac in ratiodic:
            temp_rd[self.GetReaction(reac)] = ratiodic[reac]
        reactions = self.GetReactions(temp_rd.keys())
        
        for reac in reactions[1:]:
            metname = reactions[0].id + "_" + reac.id + "_fixedratio"
            self.AddMetabolite(metname)
            met = self.GetMetabolite(metname)
            reactions[0].add_metabolites({met:-temp_rd[reac]})
            reac.add_metabolites({met:temp_rd[reactions[0]]})
        if GetMetName:
            return metname
    



    def DelReacsFixedRatio(self, fixedratio=None):
        if not fixedratio:
            self.DelMetabolites(self.Metabolites("_fixedratio"))
        elif isinstance(fixedratio, str):
            self.DelMetabolite(fixedratio)
        else:
            self.DelMetabolites(fixedratio)

##############################################################################

    def AddMetabolite(self, met, formula=None, name=None, compartment=None):
        if met in self.Metabolites():
            print met + " is already in the model"
        else:
            metabolite = Metabolite(id=met, formula=formula, name=name,
                                compartment=compartment)
            self.add_metabolites([metabolite])

    def DelMetabolite(self, met, method='subtractive'):
        """ method = 'subtractive'|'destructive' """
        met = self.GetMetabolite(met)
        if method == 'destructive':
            for reac in list(met._reaction):
                #reac.remove_from_model()
                self.DelReaction(reac)
        #met.remove_from_model(method=method)   ### Bug in cobrapy to be fixed
        met.remove_from_model(method='subtractive')

    def DelMetabolites(self, mets, method='subtractive'):
        for met in mets:
            self.DelMetabolite(met, method=method)

    def SubstituteMetabolite(self, met_from, met_to):
        met_from = self.GetMetabolite(met_from)
        met_to = self.GetMetabolite(met_to)
        iw = self.InvolvedWith(met_from)
        for r in iw:
            r.add_metabolites({met_to:iw[r]}, combine=True)
            r.add_metabolites({met_from:-iw[r]}, combine=True)


    def AddReaction(self, reac, stodic, rev=False, bounds=None, name=None,
                    subsystem=None):
        """ bounds = val | (lb,ub) """
        reaction = Reaction(reac)
        if name != None:
            reaction.name = name
        if subsystem != None:
            reaction.subsystem = subsystem
        if bounds != None:
            if isinstance(bounds, tuple) or isinstance(bounds, list):
                reaction.lower_bound = bounds[0]
                reaction.upper_bound = bounds[1]
            else:
                reaction.lower_bound = bounds
                reaction.upper_bound = bounds
        else:
            reaction.upper_bound = self.bounds
            if rev:
                reaction.lower_bound = -self.bounds
            else:
                reaction.lower_bound = 0.0
        newstodic = {}
        for met in stodic:
            stoi = stodic[met]
            if not isinstance(met, Metabolite):
                if met not in self.Metabolites():
                    met = Metabolite(id=met)
                else:
                    met = self.metabolites.get_by_id(met)
            newstodic[met] = stoi
        reaction.add_metabolites(newstodic)
        self.add_reaction(reaction)

    def DelReaction(self, reaction):
        reaction = self.GetReaction(reaction)
        self.remove_reactions([reaction])

    def DelReactions(self, reactions):
        """ reactions = list of reactions """
        for reac in reactions:
            self.DelReaction(reac)
        #self.remove_reactions(reactions)

    def ChangeReactionStoichiometry(self, reaction, metstoidic, combine=False):
        reaction = self.GetReaction(reaction)
        metabolites = {}
        for met_name in metstoidic:
            met = self.GetMetabolite(met_name)
            metabolites[met] = metstoidic[met_name]
        reaction.add_metabolites(metabolites, combine=combine,
                        add_to_container_model=True)

######################################################

    def GetSol(self, IncZeroes=False, AsMtx=False, sol=None, FixSumReacs=True,
               FixMetBounds=True, f=None, met=None, reacs=None, AsID=True,
               tol=1e-10):
        if not sol:
            sol = flux(self.solution.x_dict
                    ) if self.solution.x_dict != None else flux()
        else:
            sol = flux(sol)
        if IncZeroes:
            for reac in self.Reactions():
                if reac not in sol.keys():
                    sol[reac] = 0.0
                else:
                    if abs(sol[reac]) < tol:
                        sol[reac] = 0.0
        else:
            for reac in list(sol.keys()):
                if abs(sol[reac]) < tol :
                    del sol[reac]
        if FixSumReacs:
            for reac in list(sol.keys()):
                if reac.endswith("_sum_reaction"):
                    del sol[reac]
        if FixMetBounds:
            for reac in list(sol.keys()):
                if reac.endswith("_metbounds"):
                    del sol[reac]
        if f != None:
            for reac in list(sol.keys()):
                if f not in reac:
                    del sol[reac]
        if met != None:
            for reac in list(sol.keys()):
                if self.GetMetabolite(met) not in self.InvolvedWith(reac):
                    del sol[reac]
        if reacs != None:
            reacs = self.GetReactionNames(reacs)
            for reac in list(sol.keys()):
                if reac not in reacs:
                    del sol[reac]
        if not AsID:
            newsol = {}
            for reac in sol.keys():
                solval = sol[reac]
                reac = self.GetReaction(reac)
                newsol[reac] = solval
            sol = newsol
        if AsMtx:
            rv = sol.AsMtx()
        else:
            rv = sol
        return rv

    def PrintSol(self, lo=0, hi=float('inf'), f=None, sol=None, met=None,
                 reacs=None, Sort="value", IncZeroes=False, sortabs=True,
                 reverse=True, FixMetBounds=True):
        if not sol:
            sol = self.GetSol(IncZeroes=IncZeroes, AsMtx=False,
                              FixMetBounds=FixMetBounds, f=f, met=met,
                              reacs=reacs)
        flux(sol).Print(lo=lo, hi=hi, f=f, Sort=Sort, sortabs=sortabs,
                  reverse=reverse)

    def SolsDiff(self, sol1, sol2, IncZeroes=False, AsMtx=False, tol=1e-10):
        return flux(sol1).Diff(sol2, IncZeroes=IncZeroes, AsMtx=AsMtx, tol=tol)

    def NetStoi(self, sol=None, IncZeroes=False, tol=1e-10):
        if sol == None:
            sol = self.GetSol()
        rv = {}
        for reac in sol:
            reacstoi = self.InvolvedWith(reac)
            for met in reacstoi:
                if met in rv.keys():
                    rv[met] += reacstoi[met]*sol[reac]
                else:
                    rv[met] = reacstoi[met]*sol[reac]
        if not IncZeroes:
            for met in list(rv.keys()):
                if abs(rv[met]) < tol:
                    del rv[met]
        return rv

#############################################################################

    def SetMetsBounds(self, mets=None, direc="balance"):
        """ pre: direc="balance"|"out"|"in"|"free" """
        if not mets:
            mets = list(self.metabolites)
        elif isinstance(mets,str):
            mets = self.Metabolites(mets)
        for met in mets:
            if direc == "out":
                self.SetMetBounds(met, 0, None)
            elif direc == "in":
                self.SetMetBounds(met, None, 0)
            elif direc == "balance":
                self.SetMetBounds(met, 0, 0)
            elif direc == "free":
                self.SetMetBounds(met, None, None)

    def SetMetBounds(self, met, lo=0, hi=0):
        """ set metabolite mass balance constraint """
        met = self.GetMetabolite(met)
        reac = met.id + '_metbounds'
        if reac not in self.Reactions():
            self.AddReaction(reac,{met:-1},True)    # positive flux = export
        if lo == None:
            lo = -self.bounds
        if hi == None:
            hi = self.bounds
        if not numpy.allclose((lo,hi), (0,0)):
            self.SetConstraint(reac, lo, hi)
        else:
            self.DelReaction(reac)

#############################################################################

    def ProduceMetabolites(self, mets=None, indep=False, rc="all"):
        """ pre: rv="all"|"Produce"|"Not Produce", indep=met produced independently
           post: returns dic or list of metabolites that can(not) be produced given defined inputs """
        state = self.GetState()
        self.ZeroObjective()
        self.SetObjDirec("Min")
        prod = []
        notprod = []
        if not indep:
            self.SetMetsBounds(direc="out")
        if not mets:
            mets = list(self.Metabolites())
        for met in mets:
            self.SetMetBounds(met, 1, 1)
            self.Solve(False)
            if self.Optimal():
                prod.append(met)
            elif self.GetStatusMsg() == "infeasible":
                notprod.append(met)
            else:
                print "error"
            if indep:
                self.SetMetBounds(met, 0, 0)
            else:
                self.SetMetBounds(met, 0, None)
        self.SetState(state)
        self.SetMetsBounds(direc="balance")
        rv = {"all":{"Produce":prod, "Not Produce":notprod}, "Produce":prod,
                                                      "Not Produce":notprod}
        return rv[rc]

    def BlockedMetabolites(self, metabolites=None, fva=None, tol=1e-10):
        if not metabolites:
            metabolites = self.metabolites
        if fva == None:
            fva = self.FVA()
        allowedreacs = fva.Allowed(tol=tol)
        allowed_mets = []
        for r in allowedreacs:
            involved_mets = self.InvolvedWith(r)
            allowed_mets = list(set(allowed_mets).union(involved_mets))
        rv = self.GetMetaboliteNames(list(set(
                self.metabolites).difference(allowed_mets)))
        return rv

#############################################################################

    def FVA(self, reaclist=None, subopt=1.0, IncZeroes=True, VaryOnly=False,
            AsMtx=False, tol=1e-10, PrintStatus=False, cobra=False,
            processes=None):
        rv = FVA.FVA(self, reaclist=reaclist, subopt=subopt,
            IncZeroes=IncZeroes, VaryOnly=VaryOnly, AsMtx=AsMtx, tol=tol,
            PrintStatus=PrintStatus, cobra=cobra)
        if rv: return rv

    def AllFluxRange(self, tol=1e-10, processes=None):
        return FVA.AllFluxRange(self, tol=tol)

    def FluxRange(self, obj, tol=1e-10, resetstate=True):
        """ post: changes objective if resetobj = False!!! """
        return FVA.FluxRange(self, obj=obj, tol=tol, resetstate=resetstate)

    def FluxVariability(self, reffva=None, fva=None, excreacs=[], tol=1e-10,
                        getratio=False):
        rv = FVA.FluxVariability(self, reffva=reffva, fva=fva,
            excreacs=excreacs, tol=tol, getratio=getratio)
        if rv: return rv

    def InternalCycles(self, allowedreacs=None, reacsbounds={}, tol=1e-10):
        """ pre: reacsbounds={reac:(lo,hi)}, all external reactions blocked
           post: model with reactions in internal cycles (for doing elementary modes) """
        rv = FVA.InternalCycles(self, allowedreacs=allowedreacs,
                            reacsbounds=reacsbounds, tol=tol)
        if rv: return rv

############################################################################

    def FCA(self, reacs=None, rangedict=None, tol=1e-10):
        """ pre: lp object
           post: returns dataset of coupling """
        return FCA.FCA(self, reacs=reacs, rangedict=rangedict, tol=tol)

#############################################################################

    def Pareto(self, objectives, objdirec, runs, GetPoints=True, tol=1e-10):
        """ pre: objective = [["reac"],{"reac2":x}]
           post: turning points of Pareto front """
        return Pareto.Pareto(self, objectives, objdirec, runs,
                                GetPoints=GetPoints, tol=tol)

#############################################################################

    def ConstraintScan(self, cd, lo, hi, n_p, MinFlux=True, IncZeroes=True):
        """ scan one reaction flux
            pre: cd = sum of reaction fluxes dictionary """
        return Scan.ConstraintScan(self, cd, lo, hi, n_p, MinFlux=MinFlux, IncZeroes=IncZeroes)

    def RatioScan(self, reac1, reac2, n_p, lo=0, hi=1, flux_val=None,
                  IncZeroes=True, rev=False):
        """ scan the ratio of two reaction fluxes
            pre: flux_val = a fixed flux for the sum of the two reactions """
        return Scan.ConstraintScan(self, reac1, reac2, n_p, lo=lo, hi=hi,
             flux_val=flux_val, IncZeroes=IncZeroes, rev=rev)

    def Constraint2DScan(self, cd1, lo1, hi1, cd2, lo2, hi2, n_p,
                        IncZeroes=True):
        """ scan two reaction fluxes simultaneously """
        return Scan.Constraint2DScan(self, cd1, lo1, hi1, cd2, lo2, hi2, n_p,
                                        IncZeroes=IncZeroes)

    def ConstraintRandomMinFluxScan(self, cd, lo, hi, n_p, it, IncZeroes=True,
                                    reacs=None, exc=[], processes=None):
        """ same as ConstraintScan except using RWFM rather than FBA
            pre: cd = sum of reaction fluxes dictionary """
        return Scan.ConstraintRandomMinFluxScan(self, cd, lo, hi, n_p, it,
             IncZeroes=IncZeroes, reacs=reacs, exc=exc)

    def RatioRandomMinFluxScan(self, reac1, reac2, n_p, it, lo=0, hi=1,
                flux_val=None, IncZeroes=True, reacs=None, exc=[], rev=False,
                processes=None):
        """ same as RatioScan except using RWFM rather than FBA """
        return Scan.RatioRandomMinFluxScan(self, reac1, reac2, n_p, it, lo=lo,
            hi=1, flux_val=flux_val, IncZeroes=IncZeroes, reacs=reacs, exc=exc, rev=rev)

    def WeightingScan(self, objdic, lo, hi, n_p):
        """ scan by changing the objective coefficients for a subset of
            reactions in the objective function """
        return Scan.WeightingScan(self, objdic, lo, hi, n_p)

    def MatchFlux(self,md,vd,lo=0,hi=100,samedirec=True,count=50,display=False,tol=1e-6):
        """ Not functional! To be modified in .analysis.Match
            pre: md = matched flux dict; vd = vary flux dict / vary met bound dict """
        pass

    def MatchRatio(self,numdic,domdic,val,vd,lo=0,hi=100,samedirec=True,count=50,display=False,tol=1e-6):
        """ Not functional! To be modified in .analysis.Match """
        pass

    def MatchScan(self,cd,clo,chi,md,vd,vlo,vhi,n_p,samedirec=True,count=50,display=False,tol=1e-6,IncZeroes=True):
        """ Not functional! To be modified in .analysis.Scan """
        pass

    def PhasePlane(self, reac1, reac2, reac1_max=20, reac2_max=20, reac1_n=50,
            reac2_n=50, solver=None, n_processes=1, tol=1e-10):
        return phenotype_phase_plane.calculate_phenotype_phase_plane(self,
            reac1=reac1 ,reac2=reac2 , reac1_max=reac1_max,
            reac2_max=reac2_max, reac1_n=reac1_n, reac2_n=reac2_n,
            solver=solver, n_processes=n_processes, tol=tol)

###########################################################################################

    def LinearMOMA(self, refflux):
        MOMA.LinearMOMA(self, refflux=refflux)

    def MinDiffFromFlux(self, fluxdist, reacs=None, it=0, cleanup=True):
        """ pre: fluxdist = {reac:flux_val} """
        MOMA.MinDiffFromFlux(self, fluxdist=fluxdist, reacs=reacs, it=it,
                                cleanup=cleanup)

    def CleanUpTempVar(self, var):
        MOMA.CleanUpTempVar(self, var=var)

    def MOMA(self,refflux):
        MOMA.MOMA(self, refflux=refflux)

    def MOMA2mutant(self, mutant_model, objective_sense='maximize', solver=None, tolerance_optimality=1e-8, tolerance_feasibility=1e-8,minimize_norm=False, the_problem='return', lp_method=0,combined_model=None, norm_type='euclidean'):
        moma.moma(self, mutant_model=mutant_model, objective_sense=objective_sense, solver=solver, tolerance_optimality=tolerance_optimality, tolerance_feasibility=tolerance_feasibility,minimize_norm=minimize_norm, the_problem=the_problem, lp_method=lp_method,combined_model=combined_model, norm_type=norm_type)

    def ROOM(self, refflux, reactions=None, delta=0, tol=0, IncZeroes=False,
             AsMtx=False, f=None, reset_state=True):
        """ refflux = {reac_name:flux_val} """
        ROOM.ROOM(self, refflux=refflux, reactions=reactions,
                         delta=delta, tol=tol, IncZeroes=IncZeroes,
                         AsMtx=AsMtx, f=f, reset_state=reset_state)

    def GeometricSol(self, IncZeroes=True, AsMtx=False, tol=1e-6, Print=False):
        return GeometricFBA.GeometricSol(self, IncZeroes=IncZeroes,
                        AsMtx=AsMtx, tol=tol, Print=Print)

    def RandomMinFlux(self, it=1, reacs=None, exc=[], processes=None):
        return RWFM.RandomMinFlux(self, it=it, reacs=reacs, exc=exc,
                            processes=processes)

    def FluxRangeDiff(self, fd1, fd2, thres=1):
        return fd1.FluxRangeDiff(fd2, thres=thres)

    def FluxDiffDirec(self, fd1, fd2):
        return fd1.FluxDiffDirec(fd2)

    def FluxRangeOverlap(self, fd1, fd2):
        return fd1.FluxRangeOverlap(fd2)

##############################################################################################

    def FluxSum(self, met, tol=1e-10):
        rv = FluxSum.FluxSum(self, met=met, tol=tol)
        if rv: return rv

    def ProducedBy(self, met, FixBack=True):
        return FluxSum.ProducedBy(self, met=met, FixBack=FixBack)

    def ConsumedBy(self,met,FixBack=True):
        return FluxSum.ConsumedBy(self, met=met, FixBack=FixBack)

##############################################################################################

    def DeadMetabolites(self, fva=None):
        """ metabolites not involved in any allowed reactions """
        return Graph.DeadMetabolites(self, fva=fva)

    def NoDeadEndModel(self):
        return Graph.NoDeadEndModel(self)

    def DeadEndMetabolites(self, nodeadendmodel=None):
        """ iteratively identify peripheral metabolites """
        return Graph.DeadEndMetabolites(self, nodeadendmodel=nodeadendmodel)

    def PeripheralMetabolites(self, rc="all"):
        """ pre: rv ="all"|"Produced"|"Consumed"|"Orphan"
           post: returns dic or list of deadend metabolites """
        return Graph.PeripheralMetabolites(self, rc=rc)

    def ChokepointReactions(self):
        return Graph.ChokepointReactions(self)

    def GetNeighbours(self, name, exclude=[]):
        return Graph.GetNeighbours(self, name=name, exclude=exclude)

    def GetNeighboursAsDic(self, name, exclude=[]):
        """  pre: name and exclude are reactions or metabolites names
            post: {iw:[neighbours]} """
        return Graph.GetNeighboursAsDic(self, name=name, exclude=exclude)

    def Degree(self, name, bipartite=True):
        return Graph.Degree(self, name, bipartite=bipartite)

    def DegreeDist(self, node_type="metabolites", bipartite=True):
        """ node_type = "metabolites" | "reactions" """
        return Graph.DegreeDist(self, node_type="metabolites", bipartite=True)

    def MetabolitesDegree(self, mets=None, bipartite=True):
        return Graph.MetabolitesDegree(self, mets=mets, bipartite=bipartite)

    def ReactionsDegree(self, reacs=None, bipartite=True):
        return Graph.ReactionsDegree(self, reacs=None, bipartite=True)

#################################################################################################

    def SingleDeletion(self, element_list=None,method='fba', element_type='gene', solver=None):
        return single_deletion(self, element_list=element_list, method=method, element_type=element_type, solver=solver)

    def EssentialGenes(self,tol=1e-10):
        sdel = single_deletion(self, element_type='gene')
        rv = []
        for gene in sdel[1]:
            if sdel[1][gene] == "infeasible":
                rv.append(gene)
        return rv

    def EssentialReactions(self,tol=1e-10):
        sdel = single_deletion(self, element_type='reaction')
        rv = []
        for reac in sdel[1]:
            if sdel[1][reac] == "infeasible":
                rv.append(reac)
        return rv

    def DoubleDeletion(self,element_list_1=None, element_list_2=None, method='fba', single_deletion_growth_dict=None, element_type='gene', solver=None, number_of_processes=None, return_frame=True, zero_cutoff=1e-12, **kwargs):
        """ NOTE: bug with negative value for gene deletion """
        return double_deletion(self, element_list_1=element_list_1, element_list_2=element_list_2, method=method, single_deletion_growth_dict=single_deletion_growth_dict, element_type=element_type, solver=solver, number_of_processes=number_of_processes, return_frame=return_frame, zero_cutoff=zero_cutoff, **kwargs)

#################################################################################################

    def WriteNetwork(self, filename, network_type="rm", ExtReacs=[], ExtMets=[]):
        """ network_type = "rr" | "mr" | "rm" | "mm" """
        from ..io import IO
        ExtReacs = self.GetReactionNames(ExtReacs)
        ExtMets = self.GetMetaboliteNames(ExtMets)
        if network_type == "rr":
            IO.Network.WriteReactionsToReactionsNetwork(self, filename,
                                    ExtReacs=ExtReacs, ExtMets=ExtMets)
        elif network_type == "mr" or network_type == "rm":
            IO.Network.WriteReactionsToMetabolitesNetwork(self, filename,
                                    ExtReacs=ExtReacs, ExtMets=ExtMets)
        elif network_type == "mm":
            IO.Network.WriteMetabolitesToMetabolitesNetwork(self, filename,
                                    ExtReacs=ExtReacs, ExtMets=ExtMets)

    def WriteAttributes(self, filename, attributes=[], node_type="reactions"):
        """ objects = "reactions" | "metabolites" """
        from ..io import IO
        if 'reac' in node_type:
            IO.Network.WriteReactionsAttributes(self, filename, attributes)
        elif 'met' in node_type:
            IO.Network.WriteMetabolitesAttributes(self, filename, attributes)

#################################################################################################

    def AddProtonsToMets(self,met_proton_dic,proton,ExcReacs=None):
        """ met_proton_dic = {met:n_p} where n_p = number of protons to be added to the metabolite (met) """
        proton = self.GetMetabolite(proton)
        for met in met_proton_dic:
            self.AddProtonsToMet(met,proton,met_proton_dic[met],ExcReacs=ExcReacs)

    def AddProtonsToMet(self,met,proton,n_p,ExcReacs=None):
        proton = self.GetMetabolite(proton)
        reactions = self.InvolvedWith(met,'metabolite')
        if ExcReacs:
            if isinstance(ExcReacs,str):
                ExcReacs = [ExcReacs]
            ExcReacs = self.GetReactions(ExcReacs)
            for excreac in ExcReacs:
                if excreac in reactions:
                    del reactions[excreac]
        for reac in reactions:
            reac.add_metabolites({proton:reactions[reac]*-n_p},combine=True)

#################################################################################################

    def ImbalanceReactions(self, elements=None, IncCharge=True, ExcReacs=None,
                           ExcElements=None):
        rv = {}
        reactions = self.reactions
        if ExcReacs:
            ExcReacs = self.GetReactions(ExcReacs)
            reactions = list(set(reactions).difference(ExcReacs))
        for reac in reactions:
            bal_dict = self.CheckReactionBalance(reac, IncCharge=IncCharge,
                                                 ExcElements=ExcElements)
            if bal_dict:
                if not elements:
                    rv[reac.id] = bal_dict
                elif isinstance(elements,str):
                    if elements in bal_dict:
                        rv[reac.id] = bal_dict
                elif isinstance(elements,list):
                    if set(elements).intersection(bal_dict.keys()):
                        rv[reac.id] = bal_dict
        return rv


    def CheckReactionBalance(self, reac, IncCharge=True, ExcElements=None):
        reac = self.GetReaction(reac)
        reaction_element_dict = defaultdict(list)
        for the_metabolite, the_coefficient in reac._metabolites.items():
            if the_metabolite.elements is not None:
                [reaction_element_dict[k].append(the_coefficient*v)
                for k, v in the_metabolite.elements.items()]
                if ExcElements:
                    if isinstance(ExcElements,str):
                        ExcElements = [ExcElements]
                    if len(set(ExcElements).intersection(
                        reaction_element_dict.keys())) > 0:
                        return {}
            if (the_metabolite.charge is not None) and IncCharge:
                reaction_element_dict['Charge'].append(the_metabolite.charge
                                                        *the_coefficient)
        reaction_element_dict = dict([(k, sum(v))
                                for k, v in reaction_element_dict.items()])
        for element in list(reaction_element_dict.keys()):
            if numpy.allclose(reaction_element_dict[element], 0):
                del reaction_element_dict[element]
            elif isinstance(reaction_element_dict[element],float):
                if reaction_element_dict[element].is_integer():
                    reaction_element_dict[element] = int(
                                            reaction_element_dict[element])
#        if sum(map(abs, reaction_element_dict.values())) != 0:
#            return [reac.id, reaction_element_dict]
#        else:
        return dict(reaction_element_dict)
