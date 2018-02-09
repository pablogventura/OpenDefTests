#!/usr/bin/env python
# -*- coding: utf8 -*-

from ..first_order.model import FO_Model, FO_Product, FO_Quotient, FO_SubdirectProduct
from ..functions.morphisms import Homomorphism
from ..first_order.fofunctions import FO_Operation, FO_Constant
from ..first_order.fotype import FO_Type
from ..functions.congruence import minorice, is_system, CongruenceSystem, Congruence, maxcon, mincon, sup_proj
from ..definability.relationalmodels import check_isos
import itertools


class Quasivariety(object):
    """
    Cuasivariedad generada por un conjunto de algebras finitas.
    """

    def __init__(self, generators, name=""):
        self.fo_type = generators[0].fo_type
        for i in range(len(generators)):
            assert generators[i].fo_type == self.fo_type, "Los generadores no tienen el mismo tipo"
        self.generators = generators
        self.name = name

    def rsi(self):
        """
        Dada un conjunto de álgebras, devuelve el conjunto de álgebras relativamente
        subdirectamente irreducibles para la cuasivariedad generada.

        >>> from definability.first_order.fotheories import Lat
        >>> len(Quasivariety(Lat.find_models(5)).rsi())
        3
        """

        sub = []
        for a in self.generators:
            suba = a.substructures(a.fo_type)
            for s in suba:
                if len(s[1]) != 1 and not check_isos(s[1], sub, self.fo_type):
                    sub.append(s[1].continous()[0])
        n = len(sub)
        for i in range(n - 1, -1, -1):
            ker = {(x, y) for x in sub[i].universe for y in sub[i].universe}
            mincon = {(x, x) for x in sub[i].universe}
            t = False
            for j in range(0, len(sub)):
                if i != j:
                    for f in sub[i].homomorphisms_to(sub[j], self.fo_type, surj=True):
                        ker = ker & {tuple(t) for t in f.kernel().table()}
                        if ker == mincon:
                            sub.pop(i)
                            t = True
                            break
                if t:
                    break
        self.rsi = sub
        return sub

    def contiene(self, a):
        """
        Dada un algebra a, se fija si a pertenece a la cuasivariedad

        >>> from definability.first_order.fotheories import Lat
        >>> from definability.functions.morphisms import Homomorphism
        >>> type(Quasivariety(list(Lat.find_models(5))[0:3]).contiene(list(Lat.find_models(5))[3])) == Homomorphism
        True
        """
        if type(self.rsi) == list:
            rsi = self.rsi
        else:
            rsi = self.rsi()
        if check_isos(a, rsi, self.fo_type):
            return "El álgebra es relativamente subirectamente irreducible"
        else:
            F = set()
            ker = {(x, y) for x in a.universe for y in a.universe}
            mincon = {(x, x) for x in a.universe}
            t = False
            for b in rsi:
                for f in a.homomorphisms_to(b, a.fo_type, surj=True):
                    ker = ker & {tuple(t) for t in f.kernel().table()}
                    F.add(f)
                    if ker == mincon:
                        t = True
                        break
                if t:
                    break
        if t:
            target = FO_Product([f.target for f in F])
            d = {}
            for x in a.universe:
                d[(x,)] = tuple([f(x,) for f in F])
            return Homomorphism(d, a, target, a.fo_type)
        else:
            return False

    def cmi(self, a):
        """
        Dada un algebra a que pertenece a Q devuelve el conjunto de las
        congruencias completamente meet irreducibles.
        """
        if type(self.rsi) == list:
            rsi = self.rsi
        else:
            rsi = self.rsi()
        f = self.contiene(a)
        if type(f) == bool:
            return "El álgebra no pertenece a Q"
        elif type(f) == Homomorphism:
            result = []
            for b in rsi:
                for f in a.homomorphisms_to(b, a.fo_type, surj=True):
                    result.append(f.kernel())
            return list(set(result))
        return [mincon(a)]

    def congruence_lattice(self, a):
        """
        Dada un algebra a que pertenece a Q devuelve ConQ(a).
        """
        cmi = self.cmi(a)
        if type(cmi) == list:
            subs = []
            univ = [maxcon(a)]
            for n in range(len(cmi) + 1):
                for s in itertools.combinations(cmi, n):
                    subs.append(s)
            for s in subs:
                e = maxcon(a)
                for x in s:
                    e = e & x
                if e not in univ:
                    univ.append(e)
            tiporetacotado = FO_Type({"^": 2, "v": 2, "Max": 0, "Min": 0}, {})
            lat = FO_Model(tiporetacotado, univ, {
                     'Max': FO_Constant(maxcon(a)),
                     'Min': FO_Constant(mincon(a)),
                     '^': FO_Operation({(x,y): x & y for x in univ for y in univ}),
                     'v': FO_Operation({(x,y): sup_proj(cmi, x, y) for x in univ for y in univ})}, {})
            return lat
        return "El álgebra no pertenece a Q"

    def is_rgi(self, a):
        """
        Determina si el algebra a es relativamente subdirectamente
        indescomponible en Q
        """
        if type(self.rsi) == list:
            rsi = self.rsi
        else:
            rsi = self.rsi()
        if a in rsi:
            return True
        cmi = self.cmi(a)
        tiporetacotado = FO_Type({"^": 2, "v": 2, "Max": 0, "Min": 0}, {})
        univ = [maxcon(a), mincon(a)]
        lat = FO_Model(tiporetacotado, univ, {
         'Max': FO_Constant(mincon(a)),
         'Min': FO_Constant(maxcon(a)),
         '^': FO_Operation({(x, y): x & y for x in univ for y in univ}),
         'v': FO_Operation({(x, y): sup_proj(cmi, x, y) for x in univ for y in univ})}, {})
        atomics = []
        lat = increasing_lattice(lat, cmi, a)
        t = gen_atomics_rec(cmi, a, lat, atomics)
        return t

    def has_global_desc_of(self, a):
        """
        Dado un álgebra, decide si se descompone como producto global de
        elementos RGI en la cuasivariedad
        """
        if not self.contiene(a):
            return "El álgebra no pertenece a la cuasivariedad"
        con = self.congruence_lattice(a).universe.copy()
        con.remove(maxcon(a))
        con.remove(mincon(a))
        if con == []:
            return True
        cocientes = [FO_Quotient(a, c) for c in con]
        cocientes = [a for a in cocientes if self.is_rgi(a)]
        producto = FO_Product(cocientes)
        univ = []
        for i in a.universe:
            x = [C.natural_map()(i,) for C in producto.factors]
            univ.append(tuple(x))
        subdirect = FO_SubdirectProduct(univ, producto)
        return subdirect.is_global()


def limpiar_isos(algebras):
    """
    Dado un cojunto de álgebras, devuelve el conjunto que deja un representante
    por álgebras isomórficas

    >>> from definability.first_order.fotheories import Lat
    >>> len(limpiar_isos(Lat.find_models(5)))
    5
    >>> len(limpiar_isos( list(Lat.find_models(5)) + [Lat.find_models(5)[1]] ))
    5
    """
    n = len(algebras)
    for i in range(n - 1, 0, -1):
        if check_isos(algebras[i], algebras[0:i], algebras[i].fo_type):
            algebras.pop(i)
    return algebras


def atoms(lat, model):
    """
    Devuelve los atomos del reticulado lat
    """
    mc = mincon(model)
    return minorice([x for x in lat.universe if x != mc])


def gen_lattice_cmi(universe, cmi, model, delta):
    """
    genera un reticulado apartir de un universo y una congruencia cmi
    """
    tiporetacotado = FO_Type({"^": 2, "v": 2, "Max": 0, "Min": 0}, {})
    univ = universe.copy()
    for c in universe:
        univ.append(c & delta)
    univ = list(set(univ))
    lat = FO_Model(tiporetacotado, univ, {
         'Max': FO_Constant(mincon(model)),
         'Min': FO_Constant(maxcon(model)),
         '^': FO_Operation({(x, y): x & y for x in univ for y in univ}),
         'v': FO_Operation({(x, y): sup_proj(cmi, x, y) for x in univ for y in univ})}, {})
    return lat


def increasing_lattice(sublat, cmi, model):
    """
    Dado un subreticulado de congruencias, le agrega los elementos para que
    quede un subreticulado creciente
    """
    atomss = set(atoms(sublat, model))
    for delta in cmi:
        if delta not in sublat.universe:
            for atom in atomss:
                if atom <= delta:
                    sublat = gen_lattice_cmi(sublat.universe, cmi, model, delta)
                    atomss = set(atoms(sublat, model))
                    break
    return (sublat, atomss)


def every_system_has_solution(atomic, model, cmi):
    """
    Chequea si todo sistema tiene solución para una tupla atómica dada
    """
    n = len(atomic)
    atomic = list(atomic)
    for xs in list(itertools.product(*[model.universe for i in list(range(n))])):
        if is_system(atomic, xs, lambda x, y: sup_proj(cmi, x, y)):
            CS = CongruenceSystem(atomic, list(xs), cmi)
            if not CS.has_solution():
                return False
    return True


def gen_atomics_rec(cmi, model, inc_lat, atomics):
    if (len(inc_lat[1]) > 1) & (inc_lat[1] not in atomics):
        atomics.append(inc_lat[1])
        if every_system_has_solution(inc_lat[1], model, cmi):
            return False
    if (inc_lat[1] not in atomics):
        cmi_set = set(cmi) - set(inc_lat[0].universe)
        for delta in cmi_set:
            lat = gen_lattice_cmi(inc_lat[0].universe, cmi, model, delta)
            lat = increasing_lattice(lat, cmi, model)
            if not gen_atomics_rec(cmi, model, lat, atomics):
                return False
    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
