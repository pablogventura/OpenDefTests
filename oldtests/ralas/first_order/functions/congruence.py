#!/usr/bin/env python
# -*- coding: utf8 -*-

from .first_order.fofunctions import FO_Relation
from ..misc.misc import indent


class Eq_Rel(FO_Relation):

    """
    Relacion binaria que cumple los axiomas de equivalencia

    >>> from definability.examples import examples
    >>> rel = Eq_Rel([(0, 0),(1, 1),(2, 2),(3, 3),(4, 4),(2, 3),(3, 2)], examples.retdiamante)
    >>> rel(2, 3)
    True
    >>> rel(4, 3)
    False
    >>> rel.table()
    [[0, 0], [1, 1], [2, 2], [2, 3], [3, 2], [3, 3], [4, 4]]
    """

    def __init__(self, d, model):
        assert d and isinstance(d, list) and isinstance(d[0], tuple)
        self.model = model
        self.d = d
        super(Eq_Rel, self).__init__(d, model.universe)
        assert self.symm() and self.refl() and self.trans()

    def refl(self):
        for x in self.model.universe:
            if not (x, x) in self.d:
                return False
        return True

    def symm(self):
        for r in self.d:
            if not (r[1], r[0]) in self.d:
                return False
        return True

    def trans(self):
        for r in self.d:
            for s in self.d:
                if r[1] == s[0]:
                    if not (r[0], s[1]) in self.d:
                        return False
        return True


class Congruence(Eq_Rel):

    """
    Congruencia

    >>> from definability import fotheories
    >>> rel = Congruence([(1, 1),(2, 2),(3, 3),(0, 0),(1, 3),(3, 1),(0, 2),(2, 0)], fotheories.Lat.find_models(4)[0])
    >>> rel(1, 3)
    True
    >>> rel(0, 3)
    False
    >>> rel.table()
    [[0, 0], [0, 2], [1, 1], [1, 3], [2, 0], [2, 2], [3, 1], [3, 3]]
    """

    def __init__(self, d, model):
        assert d and isinstance(d, list) and isinstance(d[0], tuple)
        assert model
        self.model = model
        self.d = d
        super(Congruence, self).__init__(d, model)
        assert self.preserva_operaciones()

    def relacionados(self, t, s):
        for i in range(len(t)):
            if not (t[i], s[i]) in self.d:
                return False
        return True

    def __preserva_operacion(self, op):
        if self.model.operations[op].arity() == 0:
            pass
        else:
            for t in self.model.operations[op].domain():
                for s in self.model.operations[op].domain():
                    if self.relacionados(t, s):
                        if not (self.model.operations[op](*t), self.model.operations[op](*s)) in self.d:
                            return False
        return True

    def preserva_operaciones(self):
        result = True
        for op in self.model.operations:
            result = result and self.__preserva_operacion(op)
        return result

    def equiv_class(self, x):
        return {y for y in self.model.universe if (x, y) in self.d}

    def __and__(self, other):
        """
        Genera la congruencia a partir de la intersección de 2 congruencias
        """
        assert self.model == other.model
        result = list(set(self.d) & set(other.d))
        return Congruence(result, self.model)

    def __or__(self, other):
        """
        Genera la congruencia a partir de la unión de 2 congruencias
        """
        assert self.model == other.model
        result_ant = {}
        result = set(self.d) | set(other.d)
        while (result != result_ant):
            result_ant = result
            for x in self.model.universe:
                for y in self.model.universe:
                    if not (x, y) in result_ant:
                        for z in self.model.universe:
                            if (x, z) in result_ant and (z, y) in result_ant:
                                result = result | {(x, y), (y, x)}
        return Congruence(list(result), self.model)

    def __lt__(self, other):
        if self & other == self and self != other:
            return True
        return False

    def __le__(self, other):
        if self & other == self:
            return True
        return False

    def __eq__(self, other):
        if self.model != other.model:
            return False
        if set(self.d) != set(other.d):
            return False
        return True


    def __hash__(self):
        return hash(frozenset(self.dict.items()))


    def __repr__(self):
        result = "Congruence(\n"
        table = ["%s," % x for x in self.table()]
        table = indent("\n".join(table))
        return result + table + ")"


class CongruenceSystem(object):

    """
    Sistema de Congruecias
    Dado una lista de congruencias, una lista de elementos y un sigma generador
    del proyecto, genera el Sistema de Congruencias para ese proyectivo

    >>> from definability import fotheories
    >>> C1 = Congruence([(1, 1),(2, 2),(3, 3),(0, 0),(1, 3),(3, 1),(0, 2),(2, 0)], fotheories.Lat.find_models(4)[0])
    >>> C2 = Congruence([(1, 1),(2, 2),(3, 3),(0, 0),(0, 3),(3, 0),(1, 2),(2, 1)], fotheories.Lat.find_models(4)[0])
    >>> CS = CongruenceSystem([C1, C2], [2, 3])
    >>> CS.solutions()
    {0}
    """

    def __init__(self, cong, elem, sigma=None):
        assert cong and isinstance(cong, list)
        assert elem and isinstance(elem, list)
        assert len(cong) == len(elem)
        for tita in cong:
            assert tita.model == cong[0].model and isinstance(tita, Congruence)
        for x in elem:
            assert x in cong[0].model.universe
        self.model = cong[0].model
        self.cong = cong
        self.elem = elem
        if sigma:
            assert is_system(cong, elem, lambda x, y: sup_proj(sigma, x, y))
        else:
            assert is_system(cong, elem)
        self.sigma = sigma

    def solutions(self):
        sol = self.cong[0].equiv_class(self.elem[0])
        for i in list(range(len(self.cong))):
            if i != 0:
                sol = sol & self.cong[i].equiv_class(self.elem[i])
        return sol

    def has_solution(self):
        if len(self.solutions()) == 0:
            return False
        else:
            return True


def maxcon(model):
    univ = [(x, y) for x in model.universe for y in model.universe]
    return Congruence(univ, model)


def mincon(model):
    univ = [(x, x) for x in model.universe]
    return Congruence(univ, model)


def sup_proj(sigma, x, y):
    """
    Devuelve el supremo entre x e y dentro del reticulado de congruencias
    generado por el conjunto sigma
    """
    xy_up = {c for c in sigma if (set(x.d) <= set(c.d) and set(y.d) <= set(c.d))}
    e = maxcon(x.model)
    for r in xy_up:
        e = e & r
    return e


def is_system(cong, elem, sup=lambda x, y: x | y):
    for i in list(range(len(cong))):
        for j in list(range(len(cong))):
            if i != j:
                if [elem[i], elem[j]] not in sup(cong[i], cong[j]):
                    return False
    return True


def minorice(sigma):
    """
    Dado un conjunto de congruecias devuelve el conjunto minimo
    {tita: tita in sigma tal que no existe delta in sigma con delta contenido en sigma}
    """
    rem = []
    sigma = list(set(sigma))
    for i in list(range(len(sigma))):
        if i not in rem:
            for j in range(i + 1, len(sigma)):
                if sigma[i] & sigma[j] == sigma[j]:
                    rem.append(i)
                    break
                elif sigma[i] & sigma[j] == sigma[i]:
                    rem.append(j)
    return [x for x in sigma if sigma.index(x) not in rem]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
