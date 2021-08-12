from re import I
import cobra
from functools import reduce
import warnings

class Reaction(cobra.Reaction):
    """
    Reaction inherits from the cobra package reaction that holds information relates to reactions
    with the added list of proteins(enzymes) defined.

    Parameters
    ----------
    proteins: dict of enzyme id and name
    """

    def __init__(self, reaction=None, id=None, name='', subsystem='', lower_bound=float('-inf'), upper_bound=float('inf'), proteins = {}):
        # If cobra.Reaction object is part of argument
        if reaction is not None:
            self.__dict__ = reaction.__dict__
        else:
            super().__init__(id=id, name=name, subsystem=subsystem, lower_bound=lower_bound, upper_bound=upper_bound)
            self.proteins = proteins

        # Clean up
        if 'proteins' in self.__dict__.keys():
            if self.proteins == '{}' or self.proteins == {}:
                self.proteins = None

        if 'notes' in self.__dict__.keys():
            self.notes = None

        self.useable = True
        self.all_mets_has_formula = True

    def IsBalanced(self, IncCharge=True, ExcElements=[]):
        """ Checking whether a reaction is balanced
        """
        assert isinstance(ExcElements, list), f"ExcElements {ExcElements}, but expects a list"
        d = self.GetNetElementsOutput(IncCharge)
        for k, v  in d.items():
            if k in ExcElements:
                continue
            if v != 0:
                return False
        return True

    def IsBalancedOnTarget(self, Target, IncCharge=True, ExcElements=[]):
        """ Checking whether a reaction is balanced
        """
        assert isinstance(ExcElements, list), f"ExcElements {ExcElements}, but expects a list"
        d = self.GetNetElementsOutput(IncCharge)
        for k, v  in d.items():
            if k in ExcElements or k not in Target:
                continue
            if v != 0:
                return False
        return True

    def _sum_atom_dicts(self, d1, d2):
        for k, v in d2.items():
            if k in d1.keys():
                d1[k] = round(d1[k] + v, 8)
            else:
                d1[k] = round(v, 8)
        return d1

    def _metabolite_tup_to_elems_dict(self, t, IncCharge=True):
        """ (metabolite, coefficient) tuple to element counts
        """
        m, c = t
        d = {k: v * c for k, v in m.elements.items()}
        if IncCharge:
            if m.charge is None:
                warnings.warn(f"One of the metabolites ({m.id}) in {self.id} has None as charge")
            else:
                d['Charge'] = m.charge * c
        return d

    def GetNetElementsOutput(self, IncCharge=True):
        tups = map(lambda t: self._metabolite_tup_to_elems_dict(t, IncCharge), self.metabolites.items())
        return reduce(lambda x, y: self._sum_atom_dicts(x, y), tups, {})

    def AddGenes(self, genes):
        l = []
        for x in genes:
            x_ = x.copy()
            setattr(x_, "_model", self._model)
            x._reaction.add(self)
            l.append(x)

        setattr(self, "_genes", set(l))

