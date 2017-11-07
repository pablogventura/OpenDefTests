#!/usr/bin/env python
# -*- coding: utf8 -*-

from ..functions.functions import Function
from itertools import product
import functools


class FO_Operation(Function):

    r"""
    Operacion de primer orden
    """

    def __init__(self, d, d_universe=None, arity=None):
        super(FO_Operation, self).__init__(d, d_universe=d_universe, arity=arity)
        self.relation = False

    def graph_fo_relation(self, universe):
        """
        Genera la relacion dada por el grafico de la funcion en el universo
        """
        return FO_Relation([tuple(row) for row in self.table()], universe)

    def rename(self, renames):
        """
        Devuelve una nueva operacion reemplazando elementos del universo
        """
        def operation(*args):
            args = [renames[i] for i in args]
            result = self(*args)
            try:
                return renames.index(result)
            except:
                # TODO esto no tiene sentido
                # hace falta porque a veces una subestructura no
                # es subestructura con alguna funcion, y hay que poder traducirla
                return result

        return FO_Operation(operation, d_universe=list(range(len(renames))), arity=self.arity())


class FO_Relation(Function):

    r"""
    Relacion de primer orden

    >>> par = FO_Relation({(0,):1,(1,):0,(2,):1,(3,):0,(4,):1},range(4))
    >>> par(2)
    True
    >>> par(3)
    False
    >>> par.table()
    [[0], [2], [4]]
    """

    def __init__(self, d, d_universe=None, arity=None):
        if d and isinstance(d, list) and isinstance(d[0], tuple):
            d = {k: True for k in d}
        assert d_universe
        super(FO_Relation, self).__init__(d, d_universe=d_universe, arity=arity)
        self.d_universe = d_universe
        self.relation = True

    def rename(self, renames):
        """
        Devuelve una nueva operacion reemplazando elementos del universo
        """
        def relation(*args):
            args = [renames[i] for i in args]
            result = self(*args)
            return result

        return FO_Relation(relation, d_universe=list(range(len(renames))), arity=self.arity())


def FO_Constant(value):
    """
    Facilita la definicion de una operacion 0-aria para constantes
    """
    return FO_Operation({(): value})


def FO_Operation_Product(operations, d_universes):
    """
    Toma una lista de operaciones y de universos
    y devuelve la operacion en el producto de universos
    coordenada a coordenada
    """
    @FO_Operation_decorator(list(product(*d_universes)), operations[0].arity())
    def product_op(*args):
        result = []
        for i, t in enumerate(zip(*args)):
            result.append(operations[i](*t))
        return tuple(result)

    return product_op


def FO_Relation_Product(relations, d_universes):
    """
    Toma una lista de relaciones y de universos
    y devuelve la relacion en el producto de universos
    coordenada a coordenada
    """
    @FO_Relation_decorator(list(product(*d_universes)), relations[0].arity())
    def product_rel(*args):
        result = []
        for i, t in enumerate(zip(*args)):
            result.append(relations[i](*t))
        return all(result)

    return product_rel


#decorators

def FO_Operation_decorator(d_universe, arity=None):
    """
    Decorador para definir facilmente operaciones de primer orden
    con funciones en Python
    """
    def wrap(f):
        return FO_Operation(f, d_universe=d_universe, arity=arity)
    return wrap


def FO_Relation_decorator(d_universe, arity=None):
    """
    Decorador para definir facilmente relaciones de primer orden
    con funciones en Python
    """
    def wrap(f):
        return FO_Relation(f, d_universe=d_universe, arity=arity)
    return wrap

if __name__ == "__main__":
    import doctest
    doctest.testmod()
