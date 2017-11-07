#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
>>> len(DLat.find_models(5))
3
"""
from ..first_order.fotheory import FO_Theory

#########################
# Properties of operations


def assoc(s):
    return '(x' + s + 'y)' + s + 'z = x' + s + '(y' + s + 'z)'


def comm(s):
    return 'x' + s + 'y = y' + s + 'x'


def idem(s):
    return 'x' + s + 'x = x'


def absorption(s, t):
    return '(x' + s + 'y)' + t + 'x = x'


def distr(s, t):
    return 'x' + s + '(y' + t + 'z) = (x' + s + 'y)' + t + '(x' + s + 'z)'


def rdistr(s, t):
    return '(x' + t + 'y)' + s + 'z = (x' + s + 'z)' + t + '(y' + s + 'z)'

#########################
# Properties of relations


def refl(r):
    return "x " + r + " x"


def irrefl(r):
    return "-(x " + r + " x)"


def symm(r):
    return "x " + r + " y -> y " + r + " x"


def asymm(r):
    return "x " + r + " y -> -(y " + r + " x)"


def antisymm(r):
    return "x " + r + " y & y " + r + " x -> x = y"


def trans(r):
    return "x " + r + " y & y " + r + " z -> x " + r + " z"


def linear(r):
    return "(x " + r + " y) | (y " + r + " x)"
#########################
# Sets
SetsED = FO_Theory("Conjuntos con al menos un elemento distinguido", ["exists x r(x)"], options=['op(400, prefix, "r")'])


#########################
# Graphs

DiGraph = FO_Theory("Directed Graphs", ["exists x exists y (x e y)"], options=['op(400, infix, "e")'])

Graph = DiGraph.subclass("Undirected Graphs", [symm("e")])

AsymmGraph = DiGraph.subclass("Asymmetric Graphs", [asymm("e")])

LinearGraph = DiGraph.subclass("Linear Graphs", [linear("e")])

#########################
# (Semi) groups and rings

Sgrp = FO_Theory("Semigroups", [assoc("*")])

CSgrp = FO_Theory("Commutative semigroups", [assoc("+"), comm("+")])

UnSgrp = Sgrp.subclass("Semigroups with order-2 unary operation",
                       ["x'' = x"])

InSgrp = UnSgrp.subclass("Involutive semigroups", ["(x*y)' = y'*x'"])

ISgrp = UnSgrp.subclass("I-Semigroups", ["(x*x')*x = x"])

CompRSgrp = ISgrp.subclass("Completely regular semigroups",
                           ["x'*x = x*x'"])

InvSgrp = ISgrp.subclass("Inverse semigroups",
                         ["(x*x')*(y*y') = (y*y')*(x*x')"])

CliffSgrp = InvSgrp.subclass("Clifford semigroups",
                             ["x'*x = x*x'"])

Mon = FO_Theory("Monoids", [assoc("*"), "x*1 = x", "1*x = x"])

CMon = CSgrp.subclass("Commutative monoids", ["x+0 = x"])

InMon = Mon.subclass("Involutive monoids",
                     ["(x*y)' = y'*x'", "x'' = x"])

Grp = FO_Theory("Groups", [assoc("*"), "x*1 = x", "x*x' = 1"],
                results=["1*x = x", "x'*x = 1", "x'' = x", "(x*y)' = y'*x'"])

AbGrp = CMon.subclass("Abelian groups", ["x + -x = 0"])

Ring = AbGrp.subclass("Rings",
                      [assoc("*"), distr("*", "+"), rdistr("*", "+")],
                      results=["0*x = 0", "x*0 = 0"])

VNRRing = Ring.subclass("Von Neumann regular rings",
                        ["exists y (x*y)*x = x"])

URing = AbGrp.subclass("Unital rings", Mon.axioms +
                       [distr("*", "+"), rdistr("*", "+")])

CRing = Ring.subclass("Commutative rings", [comm("*")])

CURing = URing.subclass("Commutative unital rings", [comm("*")])

BRing = URing.subclass("Boolean rings",
                       ["x*x = x"], results=["x*y = y*x"])


###########################
# (Semi) lattice subclasses

Slat = FO_Theory("Semilattices", [assoc("*"), comm("*"), "x*x = x"])

Lat = FO_Theory("Lattices",
                [assoc(" v "), comm(" v "), assoc("^"), comm("^"),
                 absorption(" v ", "^"), absorption("^", " v ")],
                results=["x v x = x", "x^x = x"])

DLat = Lat.subclass("Distributive lattices", [distr("^", " v ")],
                    results=[distr(" v ", "^"),
                             "((x v y)^(x v z))^(y v z) = ((x^y)v(x^z))v(y^z)"])

MLat = Lat.subclass("Modular lattices", ["x^(y v (x^z)) = (x^y) v (x^z)"])

SDjLat = Lat.subclass("Join-semidistributive lattices",
                      ["x v y = x v z -> x v y = x v(y^z)"])

SDmLat = Lat.subclass("Meet-semidistributive lattices",
                      ["x ^ y = x ^ z -> x ^ y = x^(y v z)"])

SDLat = SDjLat.subclass("Semidistributive lattices", SDmLat)


####################
# Lattice expansions

BLat = Lat.subclass("Bounded lattices", ["0 v x = x", "1 v x = 1"])

BDLat = BLat.subclass("Bounded distributive lattices",
                      [distr("^", " v ")])

BA = DLat.subclass("Boolean algebras", ["x v x' = 1", "x ^ x' = 0"],
                   ["x'' = x", "(x v y)' = x' ^ y'", "(x ^ y)' = x' v y'",
                       "0' = 1"])

DmLat = BLat.subclass("De Morgan lattices",
                      ["x''=x", "(x v y)' = x' ^ y'"])

DmA = BDLat.subclass("De Morgan algebras",
                     ["x''=x", "(x v y)' = x' ^ y'"])

OLat = DmLat.subclass("Ortholattices", ["x v x' = 1"],
                      results=["x^x' = 0", "0' = 1"])

pLat = BLat.subclass("pseudocomplemented lattices", ["-0 = 1",
                                                             "-1 = 0", "x^-(x^y) = x^-y"])

pOLat = OLat.subclass("p-ortholattices", pLat)

StpLat = pLat.subclass("Stonian p-lattices", ["-(x^y) = -x v -y"])

StpOLat = OLat.subclass("Stonian p-ortholattices", ["-0 = 1",
                                                               "x^-(x^y) = x^-y", "-(x^y) = -x v -y"])

ModalLat = BLat.subclass("Modal lattices",
                         ["f(x v y) = f(x) v f(y)", "f(0) = 0"])

ModalA = BA.subclass("Modal algebras",
                     ["f(x v y) = f(x) v f(y)", "f(0) = 0"])

CloA = ModalA.subclass("Closure algebras",
                       ["f(x) ^ x = x", "f(f(x)) = f(x)"])

MonA = CloA.subclass("Monadic algebras", ["f(x') = f(x)'"])

RA = BA.subclass("Relation algebras",
                 ["(x*y)*z=x*(y*z)", "x*e = x", "(x v y)*z = (x*z) v (y*z)", "c(c(x))=x",
                     "c(x v y)=c(x) v c(y)", "c(x*y)=c(y)*c(x)", "(c(x)*((x*y)'))v y'=y'"])

qRA = BLat.subclass("Relation algebras",
                    ["(x*y)*z=x*(y*z)", "x*e = x", "(x v y)*z = (x*z) v (y*z)", "c(c(x))=x",
                     "c(x v y)=c(x) v c(y)", "c(x*y)=c(y)*c(x)", "(c(x)*((x*y)'))v y'=y'"])

DBDLat = BDLat.subclass("Bounded distributive lattices with dense and dual dense element",
                    ["x ^ 2 = 0 -> x = 0", "x v 2 = 1 -> x = 1"])

##########################
# Lattice-ordered algebras

LGrpoid = Lat.subclass("Lattice-ordered groupoids",
                       [distr("*", " v "), rdistr("*", " v ")])

ULGrpoid = LGrpoid.subclass("Unital l-groupoids",
                            ["x*1 = x", "1*x = x"])

ILGrpoid = ULGrpoid.subclass("Integral l-groupoids", ["x v 1 = 1"])

BILGrpoid = ILGrpoid.subclass("Bounded integral l-groupoids",
                              ["x v 0 = x", "x*0 = 0", "0*x = 0"])

LMon = ULGrpoid.subclass("Lattice-ordered monoids", [assoc("*")])

BLMon = LMon.subclass("Bounded l-monoids",
                      ["x v 0 = x", "x*0 = 0", "0*x = 0"])

ILMon = LMon.subclass("Integral l-monoids", ["x v 1 = 1"])

BILMon = ILMon.subclass("Bounded integral l-monoids",
                        ["x v 0 = x", "x*0 = 0", "0*x = 0"])

LGrp = LGrpoid.subclass("Lattice-ordered groups", Grp,
                        results=[distr("^", " v ")])

LGrp1 = Grp.subclass("Lattice-ordered groups",
                     [assoc(" v "), comm(" v "), idem(" v "),
                      distr("*", " v "), rdistr("*", " v "), "x^y = (x' v y')'"],
                     results=[assoc("^"), comm("^"), idem("^"),
                              "x v (x^y) = x", "x^(x v y) = x",
                              rdistr("^", " v ")])

RL = LMon.subclass("Residuated lattices",
                   ["x = x^(((x*y) v z)/y)", "x = x^(y\\((y*x) v z))",
                       "((x/y)*y) v x = x", "(y*(y\\x)) v x = x"])

CRL = LMon.subclass("Commutative residuated lattices", [comm("*"),
                                                               "x = x^(y->((y*x) v z))", "(y*(y->x)) v x = x"])

DRL = RL.subclass("Distributive residuated lattices",
                  [distr("^", " v ")])

CDRL = CRL.subclass("Commutative distributive residuated lattices",
                    [distr("^", " v ")])

RCRL = CRL.subclass("Representable commmutative residuated lattices",
                    ["(x/y v y/x)^1 = 1"])

IRL = RL.subclass("Integral residuated lattices", ["x v 1 = 1"])

CIRL = CRL.subclass("Commutative integral residuated lattices",
                    ["x v 1 = 1"])

DIRL = DRL.subclass("Distributive integral residuated lattices",
                    ["x v 1 = 1"])

CDIRL = CDRL.subclass("Commutative distributive integral residuated lattices",
                      ["x v 1 = 1"])

FL_o = RL.subclass("Full Lambek algebras with bottom", ["x v 0 = x"])

FL_eo = CRL.subclass("Full Lambek algebras with bottom", ["x v 0 = x"])

FL_w = FL_o.subclass("Full Lambek algebras with weakening",
                     ["x v 1 = 1"])

FL_ew = FL_eo.subclass("FL-algebras with exchange and weakening",
                       ["x v 1 = 1"])

GBL = RL.subclass("Generalized BL-algebras", ["x ^ y = y*(y\\(x ^ y))",
                                                     "x ^ y = ((x ^ y)/y)*y"])

GMV = RL.subclass("Generalized MV-algebras", ["x v y = x/((x v y)\\x)",
                                                     "x v y = (x/(x v y))\\x"])

InFL = LMon.subclass("Involutive FL-algebras", ["(x*~(-z*x))v z = z",
                                                        "(-(y*~z)*y) v z = z", "y = y^(~(-(x*y)*x))",
                                                        "x = x^(-(y*~(x*y)))", "~-x = x", "-~x = x",
                                                        "0 = ~1", "0 = -1", "~(x^y) = ~x v ~y", "-(x^y) = -x v -y"],
                     options=['op(350, prefix, "~")'],
                     results=["(x*y) v z = z -> y^-(~z*x) = y"])

DInFL = InFL.subclass("Distributive involutive FL-algebras", [distr("^", " v ")])

CyInFL = LMon.subclass("Cyclic involutive FL-algebras", ["~~x = x", "0 = ~1",
                                                                   "~(x^y)=~x v ~y", "(x*~(~z*x))v z = z", "(~(y*~z)*y) v z = z",
                                                                   "y = y^(~(~(x*y)*x))", "x = x^(~(y*~(x*y)))"],
                       options=['op(350, prefix, "~")'],
                       results=["(x*y) v z = z -> y^~(~z*x) = y"])

MTL = FL_ew.subclass("Monoidal t-norm logic algebras", ["(x->y)v(y->x) = 1"])

HA = BDLat.subclass("Heyting algebras", ["(x->x) = 1", "(x->y)^y = y",
                                               "x^(x->y) = x^y", "(x->(y^z)) = (x->y)^(x->z)",
                                               "((x v y)->z) = (x->z)^(y->z)"],
                    results=["x = x^(y->((y^x) v z))", "(y^(y->x)) v x = x"])

GodelA = HA.subclass("Goedel algebras", ["x/y v y/x = 1"])

MValg = CMon.subclass("MV-algebras", ["~~x = x", "x+~0 = ~0",
                                               "~(~x+y)+y = ~(~y+x)+x"],
                      results=["~(~x+x)+x = x"])

BLalg = MTL.subclass("Basic logic algebras", ["x^y = x*(x->y)"])

# defined above OLat = BLat.subclass("", "Ortholattices", ["x v x' = 1",
# "x^x'=0"])

# OMLat =

# MOLat


#########################################
# Sequent calculi (quasi-equational form)

RLseq = FO_Theory("Residuated lattice sequent calculus", ["(x*y)*z = x*(y*z)",
                                                                   "x*1 = x", "1*x = x", "x <= x",
                                                                   "x <= y  &  y <= x  ->  x = y",
                                                                   "u <= x  ->  u <= x v y",
                                                                   "u <= y  ->  u <= x v y",
                                                                   "(u*x)*v <= z & (u*y)*v <= z  ->  (u*(x v y))*v <= z",
                                                                   "x <= z & y <= z  ->  x v y <= z",
                                                                   "u <= x & v <= y  ->  u*v <= x*y",
                                                                   "u <= x & u <= y  ->  u <= x^y",
                                                                   "(u*x)*v <= z  ->  (u*(x^y))*v <= z",
                                                                   "(u*y)*v <= z  ->  (u*(x^y))*v <= z",
                                                                   "u*y <= x  ->  u <= x/y",
                                                                   "v <= y  &  (u*x)*w <= z  ->  (u*(x/y))*(v*w) <= z",
                                                                   "y*u <= x  ->  u <= y\\x",
                                                                   "v <= y  &  (u*x)*w <= z  ->  (u*v)*((y\\x)*w) <= z"],
                  results=["x v x <= x", "x <= x v x",
                           "x*(y v z) <= (x*y)v(x*z)", "(x*y)v(x*z) <= x*(y v z)"])

FL_oseq = FO_Theory("FL-algebras with bottom sequent calculus", ["(x*0)*y = z"])


###################################
# Semigroup and semiring expansions

DSgrp = Sgrp.subclass("Domain semigroups", ["d(x)*x = x", "d(x*y) = d(x*d(y))",
                                                     "d(d(x)*y) = d(x)*d(y)", "d(x)*d(y) = d(y)*d(x)"],
                      results=["d(d(x)) = d(x)", "d(x)*d(x) = d(x)"])

RSgrp = Sgrp.subclass("Range semigroups", ["x*r(x) = x", "r(x*y) = r(r(x)*y)",
                                                    "r(x*r(y)) = r(x)*r(y)", "r(x)*r(y) = r(y)*r(x)"],
                      results=["r(r(x)) = r(x)", "r(x)*r(x) = r(x)"])

DRSgrp = DSgrp.subclass("Domain-range semigroups",
                        ["x*r(x) = x", "r(x*y) = r(r(x)*y)",
                         "r(x*r(y)) = r(x)*r(y)", "r(x)*r(y) = r(y)*r(x)",
                         "d(r(x)) = r(x)", "r(d(x)) = d(x)"],
                        results=["r(r(x)) = r(x)", "r(x)*r(x) = r(x)"])

AFSys = Sgrp.subclass("Abstract function systems",
                      ["d(x)*x = x", "x*r(x) = x",
                       "d(x*y) = d(x*d(y))", "r(x*y) = r(r(x)*y)",
                       "d(x)*r(y) = r(y)*d(x)", "x*d(y) = d(x*y)*x",
                       "d(r(x)) = r(x)", "r(d(x)) = d(x)"],
                      results=["r(x*r(y)) = r(x)*r(y)",
                               "r(x)*r(y) = r(y)*r(x)",
                               "r(r(x)) = r(x)", "r(x)*r(x) = r(x)"])

RCSgrp = Sgrp.subclass("Right closure semigroups", ["d(x)*x = x",
                                                              "d(x)*d(y) = d(y)*d(x)",
                                                              "d(d(x)) = d(x)", "d(x)*d(x*y) = d(x*y)"],
                       results=["d(x)*d(x) = d(x)", "d(d(x)*y) = d(x)*d(y)"])

tRCSgrp = RCSgrp.subclass("Twisted RC-semigroups", ["x*d(y) = d(x*d(y))*x",
                                                               "d(x*y) = d(x*d(y))"],
                          results=["d(d(x)*y) = d(x)*d(y)"])

DMon = DSgrp.subclass("Domain monoids", ["x*1 = x", "1*x = x"],
                      results=["d(1) = 1"])

RMon = RSgrp.subclass("Range monoids", ["x*1 = x", "1*x = x"],
                      results=["r(1) = 1"])

BDMon = Mon.subclass("Boolean domain monoids", ["x*0=0", "x'*x=0",
                                                         "x'*y'=y'*x'", "x''*x=x", "x'=(x*y)'*(x*y')'"],
                     results=["0' = 1"])

BDRMon = Mon.subclass("Boolean domain-range monoids", ["x*0=0", "x'*x=0",
                                                                 "x'*y'=y'*x'", "x''*x=x", "x'=(x*y)'*(x*y')'",
                                                                 "x*(-x)=0", "-x*(-y)=-y*(-x)", "x*(- -x)=x",
                                                                 "-y=-(-x*y)*-(x*y)", "(-x)''=-x", "- -(x')=x'"],
                      #                      options=['op(350, prefix, "~")'],
                      results=["0' = 1", "0*x=0"])

DRMon = DRSgrp.subclass("Domain-range monoids", ["x*1 = x", "1*x = x"],
                        results=["r(1) = 1"])

Sring = Mon.subclass("Semirings", [assoc("+"), comm("+"), "x+0 = x",
                                            distr("*", "+"), rdistr("*", "+"), "x*0 = 0", "0*x = 0"])

IdSring = Sring.subclass("Idempotent semirings", [idem("+")])

DSring = IdSring.subclass("Domain semirings", ["d(x)*x = x",
                                                         "d(x*y) = d(x*d(y))", "d(x+y) = d(x)+d(y)",
                                                         "d(x)+1 = 1", "d(0) = 0"])

BDSring = IdSring.subclass("Boolean domain semiring", ["a(x)*x = 0",
                                                                  "a(x*y) = a(x*a(a(y)))", "a(x)+a(a(x)) = 1"])

ExpSring = Sring.subclass("Exponential semirings", ["1^x = 1",
                                                                "(x*y)^z = (x^z)*(y^z)", "x^0 = 1", "x^1 = x",
                                                                "x^(y+z) = (x^y)*(x^z)", "x^(y*z) = (x^y)^z"])

KA = CMon.subclass("Kleene algebras", ["x+x = x", assoc(";"),
                                             "x;1 = x", "1;x = x", "x;(y + z) = x;y + x;z",
                                             "(x + y);z = x;z + y;z", "x;0 = 0", "0;x = 0",
                                             "1 + x;x* = x*", "1 + x*;x = x*",
                                             "y;x + x = x  ->  y*;x + x = x",
                                             "x;y + x = x  ->  x;y* + x = x"],
                   results=["x*;x* = x*"],
                   options=["op(300, postfix, *)", "op(400, infix_left, ;)"])

KAseq = FO_Theory("Kleene algebra sequent calculus", ["(x;y);z = x;(y;z)",
                                                               "x;1 = x", "1;x = x", "x <= x", "x;0;y <= z",
                                                               "u <= x  ->  u <= x+y",
                                                               "u <= y  ->  u <= x+y",
                                                               "u;x;v <= z & u;y;v <= z  ->  u;(x+y);v <= z",
                                                               "u <= x & v <= y  ->  u;v <= x;y",
                                                               "u <= 1  ->  u <= x*",
                                                               "u <= x  ->  u <= x*",
                                                               "u <= x* & v <= x*  ->  u;v <= x*",
                                                               "u <= y & x;y <= y  ->  x*;u <= y",
                                                               "u <= y & y;x <= y  ->  u;x* <= y"],
                  results=["x <= x*", "x*;x* <= x*", "x <= x*;x*", "x** <= x*",
                           "x* <= x**", "x*;(y;x*)* <= (x+y)*",
                           "(x+y)* <= x* ;(y;x*)*"],
                  options=["op(300, postfix, *)", "op(400, infix_left, ;)"])

Alleg = InMon.subclass("Unisorted allegories", [assoc("^"), comm("^"),
                                                         idem(
                                                             "^"), "(x^y)'=x'^y'", "(x*(y^z)) ^ (x*y) = x*(y^z)",
                                                         "(x*y)^z = ((x^(z*y'))*y)^z"])

##########################
# Other equational classes

Qdl = FO_Theory("Quandels",
                [idem("*"), "(x*y)/y = x", "(x/y)*y = x", rdistr("*", "*")])

Band = FO_Theory("Bands", [assoc("*"), idem("*")])

RectBand = Band.subclass("Rectangular bands", ["(x*y)*z = x*z"])

Qgrp = FO_Theory("Quasigroups",
                 ["(x*y)/y = x", "(x/y)*y = x", "x\\(x*y) = y", "x*(x\\y) = y"])

Loop = Qgrp.subclass("Loops", ["x*1 = x", "1*x = x"])

STS = Qgrp.subclass("Steiner triple systems", [idem("*"), comm("*")])


#####################
# First-order classes

PreOrd = FO_Theory("Preordered sets", [refl("<="), trans("<=")])

Pos = PreOrd.subclass("Partially ordered sets", [antisymm("<=")])

StrPos = FO_Theory("Strict partially ordered sets", [irrefl("<"), trans("<")])

Chains = Pos.subclass("Linearly ordered sets", ["x<=y | y<=x"])

####################
# Ordered structures

poGrpoid = Pos.subclass("Partially ordered groupoids",
                        ["x<=y -> x*z<=y*z", "x<=y -> z*x<=z*y"])

poCGrpoid = Pos.subclass("Partially ordered commutative groupoids",
                         [comm("*"), "x<=y -> x*z<=y*z"])

oGrpoid = Chains.subclass("Linearly ordered groupoids",
                          ["x<=y -> x*z<=y*z", "x<=y -> z*x<=z*y"])

oCGrpoid = oGrpoid.subclass("Linearly ordered commutative groupoids", [comm("*")])

poSgrp = poGrpoid.subclass("po-semigroups", Sgrp)

poCSgrp = poSgrp.subclass("Partially ordered commutative semigroups", [comm("*")])

oSgrp = oGrpoid.subclass("Linearly ordered semigroups", Sgrp)

oCSgrp = oSgrp.subclass("Linearly ordered commutative semigroups", [comm("*")])

poMon = poGrpoid.subclass("po-monoids", Mon)

poCMon = poMon.subclass("Partially ordered commutative monoids", [comm("*")])

oMon = oGrpoid.subclass("Linearly ordered monoids", Mon)

oCMon = oMon.subclass("Linearly ordered commutative monoids", [comm("*")])

proGrp = poMon.subclass("Protogroups", ["f(x)*x <= 1", "1 <= x*f(x)"],
                        results=["f(x*y) = f(y)*f(x)", "(x*f(x))*x = x"])

prGrp = poMon.subclass("Pregroups", ["f(x)*x <= 1", "1 <= x*f(x)",
                                              "x*g(x) <= 1", "1 <= g(x)*x"],
                       results=["f(g(x)) = x", "g(f(x)) = x",
                                "f(x*y) = f(y)*f(x)", "g(x*y) = g(y)*g(x)",
                                "(x*f(x))*x = x", "(x*g(x))*x = x"])

LprGrp = LMon.subclass("Lattice-ordered pregroups",
                       ["(f(x)*x) v 1 = 1",
                        "1 = 1 ^ (x*f(x))", "(x*g(x)) v 1 = 1", "1 = 1 ^ (g(x)*x)"],
                       results=["f(g(x)) = x", "g(f(x)) = x",
                                "f(x*y) = f(y)*f(x)", "g(x*y) = g(y)*g(x)",
                                "(x*f(x))*x = x", "(x*g(x))*x = x"])

###############################
# Residuated ordered structures

rpoGrpoid = poGrpoid.subclass("Residuated partially ordered groupoids",
                              ["x<=y -> x/z<=y/z", "x<=y -> z\\x<=z\\y",
                               "x*(x\\y)<=y", "y<=x\\(x*y)",
                               "(y/x)*x<=y", "y<=(y*x)/x"],
                              results=["x*(x\\x) = x"])

rpoCGrpoid = poCGrpoid.subclass("Residuated partially ordered commutative groupoids",
                                ["x<=y -> (z->x)<=(z->y)",
                                 "x*(x->y)<=y", "y<=(x->(x*y))"],
                                results=["x*(x->x) = x"])

roGrpoid = oGrpoid.subclass("Residuated linearly ordered groupoids",
                            ["x<=y -> x/z<=y/z", "x<=y -> z\\x<=z\\y",
                             "x*(x\\y)<=y", "y<=x\\(x*y)",
                             "(y/x)*x<=y", "y<=(y*x)/x"])

roCGrpoid = roGrpoid.subclass("Residuated linearly ordered commutative groupoids",
                              [comm("*")])

rpoSgrp = rpoGrpoid.subclass("Residuated po-semigroups", Sgrp)

rpoCSgrp = rpoSgrp.subclass("Residuated partially ordered commutative semigroups",
                            [comm("*")])

roSgrp = roGrpoid.subclass("Residuated linearly ordered semigroups", Sgrp)

roCSgrp = roSgrp.subclass("Residuated linearly ordered commutative semigroups",
                          [comm("*")])

rpoMon = rpoGrpoid.subclass("Residuated po-monoids", Mon)

rpoCMon = poCMon.subclass("Residuated partially ordered commutative monoids",
                          ["x<=y -> (z->x)<=(z->y)",
                           "x*(x->y)<=y", "y<=(x->(x*y))"])

roMon = roGrpoid.subclass("Residuated linearly ordered monoids", Mon)

roCMon = rpoCMon.subclass("Residuated linearly ordered commutative monoids",
                          ["x<=y | y<=x"])

# Integral
irpoGrpoid = rpoGrpoid.subclass("Integral residuated partially ordered groupoids",
                                ["y<=x\\x", "x\\x = y/y"])

irpoCGrpoid = rpoCGrpoid.subclass("Integral residuated partially ordered commutative groupoids",
                                  ["y<=x\\x", "x\\x = y/y"])

iroGrpoid = roGrpoid.subclass("Integral residuated linearly ordered groupoids",
                              ["y<=x\\x", "x\\x = y/y"])

iroCGrpoid = roCGrpoid.subclass("Integral residuated linearly ordered commutative groupoids",
                                ["y<=x\\x", "x\\x = y/y"])

irpoSgrp = irpoGrpoid.subclass("Integral residuated po-semigroups", Sgrp)

irpoCSgrp = rpoCSgrp.subclass("Integral residuated partially ordered commutative semigroups",
                              ["y<=x\\x", "x\\x = y/y"])

iroSgrp = iroGrpoid.subclass("Integral residuated linearly ordered semigroups",
                             Sgrp)

iroCSgrp = roCSgrp.subclass("Integral residuated linearly ordered commutative semigroups",
                            ["y<=x\\x", "x\\x = y/y"])

irpoMon = rpoMon.subclass("Integral residuated po-monoids",
                          ["x<=1"])
porim = irpoMon

irpoCMon = rpoCMon.subclass("Integral residuated partially ordered commutative monoids",
                            ["x<=1"])
pocrim = irpoCMon

iroMon = roMon.subclass("Integral residuated linearly ordered monoids",
                        ["x<=1"])

iroCMon = roCMon.subclass("Integral residuated linearly ordered commutative monoids",
                          ["x<=1"])


#################
# Atom structures

NAat = FO_Theory("Nonassociative relation algebra atomstructures",
                 ["C(x,y,z) -> C(x',z,y)", "C(x,y,z) -> C(z,y',x)",
                  "x=y <-> exists u(E(u) & C(x,u,y))"])

INAat = FO_Theory("Integral nonassociative relation algebra atomstructures",
                  ["C(x,y,z) -> C(x',z,y)", "C(x,y,z) -> C(z,y',x)",
                   "C(x,0,y) <-> x=y"],
                  results=["C(x',z,y) -> C(x,y,z)", "C(z,y',x) -> C(x,y,z)",
                           "x''=x", "C(0,x,y) <-> x=y"])

INAat1 = FO_Theory("Integral nonassociative relation algebra atomstructures",
                   ["C(x,y,z) -> C(x',z,y)", "C(x,y,z) -> C(z,y',x)",
                    "C(x,1,y) <-> x=y"],
                   results=["C(x',z,y) -> C(x,y,z)", "C(z,y',x) -> C(x,y,z)",
                            "x''=x", "C(1,x,y) <-> x=y"])

SNAat = FO_Theory("Symmetric nonassociative relation algebra atomstructures",
                  ["C(x,y,z) -> C(x,z,y)", "C(x,y,z) -> C(z,y,x)",
                   "C(x,0,y) <-> x=y"])

RAat = NAat.subclass("Relation algebra atomstructures",
                     ["exists u(C(x,y,u) & C(u,z,w)) <-> exists v(C(x,v,w) & C(y,z,v))"])

IRAat = INAat.subclass("Integral relation algebra atomstructures",
                       ["exists u(C(x,y,u) & C(u,z,w)) <-> exists v(C(x,v,w) & C(y,z,v))"])

IRAat1 = INAat1.subclass("Integral relation algebra atomstructures",
                         ["exists u(C(x,y,u) & C(u,z,w)) <-> exists v(C(x,v,w) & C(y,z,v))"])

SRAat = SNAat.subclass("Symmetric relation algebra atomstructures",
                       ["exists u(C(x,y,u) & C(u,z,w)) <-> exists v(C(x,v,w) & C(y,z,v))"])

SeqAat = FO_Theory("Sequential algebra atomstructures",
                   ["C(x,y,0) <-> C(y,x,0)", "C(x,0,y) <-> x=y", "C(0,x,y) <-> x=y",
                    "exists u(C(x,y,u) & C(u,z,w)) <-> exists v(C(x,v,w) & C(y,z,v))",
                    "exists u(C(x,u,y) & C(u,w,z)) -> exists v(C(x,z,v) & C(y,w,v))"])


#############################################################
# Propositional Logics

MP = "P(x) & P(x->y) -> P(y)"           # Modus pones
Bb = "P((x->y)->((z->x)->(z->y)))"      # Prefixing
Bp = "P((x->y)->((y->z)->(x->z)))"      # Suffixing
Cc = "P((x->(y->z))->(y->(x->z)))"      # Commutativity
Ii = "P(x->x)"                          # Identity
Kk = "P(x->(y->x))"                     # Integrality
Ss = "P((x->(y->z))->((x->y)->(x->z)))"  # Selfdistributivity
Ww = "P((x->(x->y))->(x->y))"           # Contraction
Pierce = "P(((x->y)->x)->x)"             # Pierce's law
DN = "P(--x->x)"                        # Double negation
CP = "P((x->-y)->(y->-x))"              # Contraposition

BK = FO_Theory("BK logic,  reduct of FL_w", [Bb, Kk, MP,
                                                   "P(y) & P(x->(y->z)) -> P(x->z)"])

BCK = FO_Theory("BCK logic, -> reduct of FL_ew", [Bb, Cc, Kk, MP])

BCKP = FO_Theory("BCK logic + Pierce law, -> reduct of CL", [Bb, Cc, Kk, Pierce, MP])

BCI = FO_Theory("BCI logic, -> reduct of FL_e", [Bb, Cc, Ii, MP])

BCIS = FO_Theory("BCIS=BCIW logic, -> reduct of FL_ec", [Bb, Cc, Ii, Ss, MP])

SK = FO_Theory("Hilbert logic, -> reduct of intuitionistic logic", [Ss, Kk, MP])

CL = FO_Theory("Classical logic", [Ss, Kk, DN, CP, MP])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
