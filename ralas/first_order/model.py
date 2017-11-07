#!/usr/bin/env python
# -*- coding: utf8 -*-

from itertools import product, chain

from ..misc.misc import indent, powerset
from ..functions.morphisms import Embedding, Homomorphism
from ..functions.congruence import minorice, is_system, CongruenceSystem, Congruence, maxcon, mincon, sup_proj
from ..first_order.fofunctions import FO_Relation, FO_Operation, FO_Relation_Product, FO_Operation_Product, FO_Constant
from ..first_order.fotype import FO_Type
from ..interfaces import minion
from ..interfaces import latticedraw


class FO_Model(object):

    """
    Modelos de algun tipo de primer orden.
    """

    def __init__(self, fo_type, universe, operations, relations, name=""):
        self.fo_type = fo_type
        assert not isinstance(universe, int)
        self.universe = universe
        self.cardinality = len(universe)
        assert set(operations.keys()) >= set(
            fo_type.operations.keys()), "Estan mal definidas las funciones"
        assert set(relations.keys()) >= set(
            fo_type.relations.keys()), "Estan mal definidas las relaciones"
        self.operations = operations
        self.relations = relations
        self.supermodel = self
        self.name = name

    def __repr__(self):
        if self.name:
            return "FO_Model(name= %s)\n" % self.name
        else:
            result = "FO_Model(\n"
            result += indent(repr(self.fo_type) + ",\n")
            result += indent(repr(self.universe) + ",\n")
            result += indent(repr(self.operations) + ",\n")
            result += indent(repr(self.relations))
            return result + ")"

    def homomorphisms_to(self, target, subtype, inj=None, surj=None, without=[]):
        """
        Genera todos los homomorfismos de este modelo a target, en el subtype.

        >>> from definability.examples.examples import *
        >>> len(retrombo.homomorphisms_to(retrombo,tiporet))
        16
        >>> len(retrombo.homomorphisms_to(rettestlinden,tiporet))
        49
        >>> len(rettestlinden.homomorphisms_to(retrombo,tiporet))
        36
        """
        return minion.homomorphisms(self, target, subtype, inj=inj, surj=surj, without=without)

    def embeddings_to(self, target, subtype, without=[]):
        """
        Genera todos los embeddings de este modelo a target, en el subtype.
        """
        return minion.embeddings(self, target, subtype, without=without)

    def automorphisms(self, subtype, without=[]):
        """
        Genera todos los automorfismos de este modelo, en el subtype.
        """
        return self.isomorphisms_to(self, subtype, without=without)

    def isomorphisms_to(self, target, subtype, without=[]):
        """
        Genera todos los isomorfismos de este modelo a target, en el subtype.
        """
        return minion.isomorphisms(self, target, subtype, without=without)

    def is_homomorphic_image(self, target, subtype, without=[]):
        """
        Si existe, devuelve un homomorfismo de este modelo a target, en el subtype;
        Si no, devuelve False
        """
        return minion.is_homomorphic_image(self, target, subtype, without=without)

    def is_substructure(self, target, subtype, without=[]):
        """
        Si existe, devuelve un embedding de este modelo a target, en el subtype;
        Si no, devuelve False
        """
        return minion.is_substructure(self, target, subtype, without=without)

    def is_isomorphic(self, target, subtype, without=[]):
        """
        Si existe, devuelve un isomorfismo de este modelo a target, en el subtype;
        Si no, devuelve False
        """
        return minion.is_isomorphic(self, target, subtype, without=without)

    def is_isomorphic_to_any(self, targets, subtype, without=[]):
        """
        Si lo es, devuelve el primer isomorfismo encontrado desde este modelo a alguno en targets, en el subtype;
        Si no, devuelve False
        """
        return minion.is_isomorphic_to_any(self, targets, subtype, without=without)

    def subuniverse(self, subset, subtype):
        """
        Devuelve el subuniverso generado por subset para el subtype
        y devuelve una lista con otros conjuntos que tambien hubieran
        generado el mismo subuniverso

        >>> from definability.examples.examples import *
        >>> retrombo.subuniverse([1],tiporet)
        ([1], [[1]])
        >>> retrombo.subuniverse([2,3],tiporet)[0]
        [0, 1, 2, 3]
        >>> retrombo.subuniverse([2,3],tiporet.subtype(["^"],[]))[0]
        [0, 2, 3]
        """
        result = subset
        result.sort()
        partials = [list(subset)]
        increasing = True
        while increasing:
            increasing = False
            for op in subtype.operations:
                for x in product(result, repeat=self.operations[op].arity()):
                    elem = self.operations[op](*x)
                    if elem not in result and elem in self.universe:
                        result.append(elem)
                        result.sort()
                        partials.append(list(result))
                        increasing = True

        return (result, partials)

    def subuniverses(self, subtype):
        """
        NO DEVUELVE EL SUBUNIVERSO VACIO
        Generador que va devolviendo los subuniversos.
        Intencionalmente no filtra por isomorfismos.

        >>> from definability.examples.examples import *
        >>> list(retrombo.subuniverses(tiporet))
        [[0, 1, 2, 3], [0, 1, 2], [0, 1, 3], [0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [0], [1], [2], [3]]
        >>> list(posetrombo.subuniverses(tipoposet)) # debe dar el conjunto de partes sin el vacio, porque no tiene ops
        [[0, 1, 2, 3], [0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3], [0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3], [0], [1], [2], [3]]
        >>> list(retcadena2.subuniverses(tiporetacotado)) # debe dar todo entero, por las constantes
        [[0, 1]]
        """
        result = []
        subsets = powerset(self.universe)
        checked = [[]]
        for subset in subsets:
            if subset not in checked:
                subuniverse, partials = self.subuniverse(subset, subtype)
                for partial in partials:
                    checked.append(partial)
                if subuniverse not in result:
                    result.append(subuniverse)
                    yield subuniverse

    def restrict(self, subuniverse, subtype):
        """
        Devuelve la restriccion del modelo al subuniverso que se supone que es cerrado en en subtype
        """
        return FO_Submodel(subtype, subuniverse, {op: self.operations[op].restrict(subuniverse) for op in self.operations}, {rel: self.relations[rel].restrict(subuniverse) for rel in self.relations}, self)

    def substructure(self, subuniverse, subtype):
        """
        Devuelve una subestructura y un embedding.
        """
        substructure = self.restrict(subuniverse, subtype)
        emb = Embedding(
            {(k,): k for k in subuniverse}, substructure, self, subtype)
        return (emb, substructure)

    def substructures(self, subtype, without=[]):
        """
        Generador que va devolviendo las subestructuras.
        Intencionalmente no filtra por isomorfismos.
        Devuelve una subestructura y un embedding.
        No devuelve las subestructuras cuyos universos estan en without.

        >>> from definability.examples.examples import *
        >>> len(list(retrombo.substructures(tiporet)))
        12
        >>> len(list(retrombo.substructures(tiporet.subtype(["v"],[])))) # debe dar uno mas por el triangulo de arriba
        13
        >>> len(list(retrombo.substructures(tiporet.subtype([],[])))) # debe dar (2**cardinalidad)-1
        15
        """
        without = list(map(set, without))
        for sub in self.subuniverses(subtype):
            if set(sub) not in without:
                # parece razonable que el modelo de una subestructura conserve todas las relaciones y operaciones
                # independientemente de el subtipo del que se buscan
                # embeddings.
                yield self.substructure(sub, subtype)

    def __eq__(self, other):
        """
        Para ser iguales tienen que tener el mismo tipo
        y el mismo comportamiento en las operaciones/relaciones del tipo
        y el mismo universo
        """
        if set(self.universe) != set(other.universe):
            return False
        if self.fo_type != other.fo_type:
            return False
        for op in self.fo_type.operations:
            if self.operations[op] != other.operations[op]:
                return False
        for rel in self.fo_type.relations:
            if self.relations[rel] != other.relations[rel]:
                return False
        return True

    def __ne__(self, other):
        """
        Triste necesidad para la antiintuitiva logica de python
        'A==B no implica !(A!=B)'
        """
        return not self.__eq__(other)

    def __len__(self):
        return self.cardinality

    def join_to_le(self):
        """
        Genera una relacion <= a partir de v
        Solo si no tiene ninguna relacion "<="

        >>> from definability.examples.examples import retrombo
        >>> del retrombo.relations["<="]
        >>> retrombo.join_to_le()
        >>> retrombo.relations["<="]
        Relation(
          [0, 0],
          [0, 1],
          [0, 2],
          [0, 3],
          [1, 1],
          [2, 1],
          [2, 2],
          [3, 1],
          [3, 3],
        )
        """
        if "<=" not in self.relations:
            def leq(x,y):
                return self.operations["v"](x,y) == y
            self.relations["<="] = FO_Relation(leq, self.universe, arity=2)

    def draw_lattice(self):
        return latticedraw.LatDraw(self)

    def diagram(self, c, s=0):
        """
        Devuelve el diagrama de la estructura con el prefijo c y con un
        shift de s.
        """
        result = []
        for x, y in product(self.universe, repeat=2):
            result += ["-(%s%s=%s%s)" % (c, x + s, c, y + s)]
        for op in self.operations:
            if self.operations[op].arity() == 0:
                result += ["(%s=%s%s)" % (op, c, self.operations[op]() + s)]
            else:
                for x, y, z in iter(self.operations[op].table()):
                    result += ["%s%s %s %s%s = %s%s" %
                               (c, x + s, op, c, y + s, c, z + s)]
        for rel in self.relations:
            for x, y in product(self.universe, repeat=2):
                if self.relations[rel](x, y):
                    result += ["(%s%s %s %s%s)" % (c, x + s, rel, c, y + s)]
                else:
                    result += ["-(%s%s %s %s%s)" % (c, x + s, rel, c, y + s)]
        return result

    def __hash__(self):
        """
        Hash para los modelos de primer orden

        >>> from definability.examples.examples import *
        >>> hash(retrombo)==hash(retrombo2)
        False
        >>> from definability.first_order.fotheories import DiGraph
        >>> s=[hash(g) for g in DiGraph.find_models(3)]
        >>> (len(s),len(set(s))) # nunca se repitio un hash
        (103, 103)
        """
        return hash(frozenset(chain([self.fo_type], self.universe, self.operations.items(), self.relations.items())))

    def __mul__(self, other):
        """
        Calcula el producto entre modelos

        >>> from definability.examples.examples import *
        >>> retcadena2.fo_type = retrombo.fo_type
        >>> j=retcadena2*retrombo
        >>> r=retcadena2**3
        >>> bool(j.is_isomorphic(r,tiporet))
        True
        """
        return FO_Product([self, other])

    def __pow__(self, exponent):
        """
        Calcula la potencia de un modelo

        >>> from definability.examples.examples import *
        >>> r=retcadena2**2
        >>> bool(r.is_isomorphic(retrombo,tiporet))
        True
        >>> r=posetcadena2**2
        >>> bool(r.is_isomorphic(posetrombo,tipoposet))
        True
        """
        return FO_Product([self] * exponent)

    def continous(self):
        """
        Devuelve un modelo isomorfo pero de universo [0..n]
        """
        translation = list(self.universe)
        universe = list(range(len(translation)))

        operations = {}
        for op in self.operations:
            operations[op] = self.operations[op].rename(translation)

        relations = {}
        for rel in self.relations:
            relations[rel] = self.relations[rel].rename(translation)

        return (FO_Model(self.fo_type, universe, operations, relations), translation)

    def draw_continous_lattice(self):
        return (self.continous()[0]).draw_lattice()

    def pertenece(self, Q):
        """
        Dada una cuasivariedad Q, se fija si el modelo pertenece a Q. En caso
        de pertenecer, devuelve el morfismo que de la representacion con las
        relativamente subdirectamente irreducibles.
        """
        return Q.contiene(self)

    def is_rgi(self, Q):
        """
        Dada una cuasivariedad Q, se fija si el modelo es relativamente
        globalmente indescomponible en Q.
        """
        return Q.is_rgi(self)

class FO_Submodel(FO_Model):

    """
    Submodelos de algun tipo de primer orden.
    """

    def __init__(self, fo_type, universe, operations, relations, supermodel):
        super(FO_Submodel, self).__init__(
            fo_type, universe, operations, relations)
        self.supermodel = supermodel

    def __repr__(self):
        result = "FO_Submodel(\n"
        result += indent(repr(self.fo_type) + ",\n")
        result += indent(repr(self.universe) + ",\n")
        result += indent(repr(self.operations) + ",\n")
        result += indent(repr(self.relations) + ",\n")
        result += indent("supermodel= " + repr(self.supermodel) + "\n")
        return result + ")"

    def natural_embedding(self):
        """
        Genera el Embedding natural entre el submodelo y el modelo
        """
        d = {(x,): x for x in self.universe}
        return Embedding(d, self, self.supermodel, self.fo_type)

    def is_subdirect(self):
        """
        Dado un submodelo de un producto, decide si es un producto subdirecto o no
        """
        if isinstance(self.supermodel, FO_Product):
            for i in self.supermodel.indices():
                if not set((self.supermodel.projection(i).composition(self.natural_embedding())).image_model().universe) == set(self.supermodel.factors[i].universe):
                    return False
            return True
        return False


class FO_Product(FO_Model):

    def __init__(self, factors):
        """
        Toma una lista de factores
        """
        # TODO falta un armar las operaciones y relaciones
        for f in factors:
            if isinstance(f,FO_Product):
                factors.remove(f)
                factors+=f.factors
        self.factors = factors

        fo_type = factors[0].fo_type
        if any(f.fo_type != fo_type for f in factors):
            raise ValueError("Factors must be all from same fo_type")

        d_universe = list(product(*[f.universe for f in factors]))

        operations = {}
        for op in fo_type.operations:
            if fo_type.operations[op] == 0:
                operations[op] = FO_Constant(tuple([f.operations[op]() for f in factors]))
            else:
                operations[op] = FO_Operation_Product([f.operations[op] for f in factors],[f.universe for f in factors])

        relations = {}
        for rel in fo_type.relations:
            relations[rel] = FO_Relation_Product([f.relations[rel] for f in factors],[f.universe for f in factors])

        super(FO_Product, self).__init__(fo_type,
                                         d_universe,
                                         operations,
                                         relations)

    def projection(self, i):
        """
        Genera el morfismo que es la proyección en la coordenada i
        """
        assert i in self.indices()
        d = {(x,): x[i] for x in self.universe}
        return Homomorphism(d, self, self.factors[i], self.fo_type, surj=True)

    def indices(self):
        return list(range(len(self.factors)))


class FO_SubdirectProduct(FO_Submodel):

    """
    Producto Subdirecto

    >>> from definability.examples.examples import *
    >>> M2=FO_Model(tiporetacotado, [0,1], {'^': FO_Operation({(0,0):0,(0,1): 0,(1,0): 0,(1,1): 1}),'v': FO_Operation({(0,0):0,(0,1): 1,(1,0): 1,(1,1): 1}),'Max': FO_Constant(1),'Min': FO_Constant(0)}, {})
    >>> P=M2*M2*M2
    >>> FO_SubdirectProduct([(1,1,1), (0,0,0), (0,1,1)], P).is_global()
    False
    >>> FO_SubdirectProduct([(1,1,1), (0,0,0), (0,1,1), (1,0,0)], P).is_global()
    True
    """

    def __init__(self, universe, supermodel):
        assert isinstance(supermodel, FO_Product)
        super(FO_SubdirectProduct, self).__init__(
                supermodel.fo_type,
                universe,
                {op: supermodel.operations[op].restrict(universe) for op in supermodel.operations},
                {rel: supermodel.relations[rel].restrict(universe) for rel in supermodel.relations},
                supermodel)
        assert self.is_subdirect()

    def __repr__(self):
        result = "FO_SubdirectProduct(\n"
        result += indent(repr(self.fo_type) + ",\n")
        result += indent(repr(self.universe) + ",\n")
        result += indent(repr(self.operations) + ",\n")
        result += indent(repr(self.relations) + ",\n")
        result += indent("Product= " + repr(self.supermodel) + "\n")
        return result + ")"

    def tita(self, i):
        """
        Congruencia de la forma tita(i) = {(x,y) in A^2 : x(i) = y(i)}
        """
        assert i in self.supermodel.indices()
        return (self.supermodel.projection(i).composition(self.natural_embedding())).kernel()

    def sigma(self):
        """
        sigma = {tita(i)}
        """
        result = []
        for i in self.supermodel.indices():
            result.append(self.tita(i))
        return result

    def is_global(self):
        """
        Determina si el producto subdirecto es global o no
        """
        sigma = self.sigma()
        sigma_m = minorice(sigma)
        n = len(sigma_m)
        for xs in list(product(*[self.universe for i in list(range(n))])):
            if is_system(sigma_m, xs, lambda x, y: sup_proj(sigma, x, y)):
                CS = CongruenceSystem(sigma_m, list(xs), sigma)
                if not CS.has_solution():
                    return False
        return True


class FO_Quotient(FO_Model):

    """
    Modelo Cociente
    Dado un algebra y una congruencia, devuelve el álgebra cociente
    """

    def __init__(self, supermodel, congruence):
        assert supermodel.fo_type.relations == {}
        uni = list(supermodel.universe)
        elim = []
        n = len(uni)
        for i in range(n):
            if uni[i] not in elim:
                for j in range(i + 1, n):
                    if [uni[i], uni[j]] in congruence:
                        elim.append(uni[j])
        for i in elim:
            uni.remove(i)
        operations = {}
        for op in supermodel.operations:
            ope = supermodel.operations[op].restrict(uni)
            d = {}
            if supermodel.operations[op].arity() != 0:
                for i in list(ope.domain()):
                    if not ope(*i) in uni:
                        for j in uni:
                            if [ope(*i), j] in congruence:
                                d[i] = j
                                break
                    else:
                        d[i] = ope(*i)
                operations[op] = FO_Operation(d, uni, ope.arity())
            else:
                if not ope() in uni:
                    for j in uni:
                        if [ope(), j] in congruence:
                            operations[op] = FO_Constant(j)
                else:
                    operations[op] = ope
        super(FO_Quotient, self).__init__(
            supermodel.fo_type, uni, operations, {})
        self.congruence = congruence
        self.supermodel = supermodel

    def natural_map(self):
        """
        Devuelve el mapa natural entre el álgebra y el cociente
        """
        d = {}
        for i in self.supermodel.universe:
            for j in self.universe:
                if [i, j] in self.congruence:
                    d[(i,)] = j
                    break
        return Homomorphism(d, self.supermodel, self, self.fo_type, surj=True)

    def __repr__(self):
        result = "FO_Quotient(\n"
        result += indent(repr(self.fo_type) + ",\n")
        result += indent(repr(self.universe) + ",\n")
        result += indent(repr(self.operations) + ",\n")
        result += indent(repr(self.relations) + ",\n")
        result += indent("congruence= " + repr(self.congruence) + "\n")
        return result + ")"



if __name__ == "__main__":
    import doctest
    doctest.testmod()
