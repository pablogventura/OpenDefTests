from first_order.formulas import variables, eq, RelSym, true, false
from itertools import product
from random import sample
from first_order.formulas import variables, eq, RelSym, true, false
from first_order.fofunctions import FO_Relation
from first_order.model import FO_Model, FO_Type
import random

def generate(card, barity,bdensity,tarity):
    r=("R",barity)

    r=RelSym(*r)
    vs = variables(*range(tarity))

    result = []
    for i in range(random.randint(1,5)):
        oendo = []
        for j in range(random.randint(1,5)):
            tup = tuple(random.choice(vs) for _ in range(r.arity))
            if random.randint(0,1):
                oendo.append(r(*tup))
            else:
                oendo.append(-r(*tup))
        result.append(oendo.pop())
        while oendo:
            result[-1]=result[-1]&oendo.pop()

    formula=result.pop()
    while result:
        formula=formula|result.pop()

    #print(formula)


    ## aca se hizo la formula, ahora hacemos el modelo

    baserelation=sample(list(product(range(card),repeat=barity)),int(card**barity*bdensity))
    relation = FO_Relation(baserelation,range(card))
    tipo = FO_Type({},{"R":barity})

    modelo = FO_Model(tipo, list(range(card)), {}, {"R":relation})

    targetrel =set()
    for t in product(range(card),repeat=tarity):
        if formula.satisfy(modelo, {v:a for v,a in zip(vs,t)}):
            targetrel.add(t)
    return set(baserelation),targetrel
    

def printmodel(card,barity,bdensity,tarity,definable=True):
    t=set()
    while len(t) == 0 or len(t) == card**tarity:
        b,t=generate(card,barity,bdensity,tarity)
    if not definable:
        t.pop()
    
    print (" ".join(str(j) for j in range(card)))
    print ("")
    print ("R0 %s %s" % (len(b),barity))
    for i in b:
        print (" ".join(str(j) for j in i))
    print ("")
    print ("T0 %s %s" % (len(t),tarity))
    for i in t:
        print (" ".join(str(j) for j in i))
    print ("")
    
    
    
printmodel(10,3,0.1,3, False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
