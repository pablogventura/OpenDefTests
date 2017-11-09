from itertools import product, permutations
from random import sample,choice

barity=5
tarity=5
bdensity=0.005
card=20

permutaciones =list(permutations(range(barity),barity))

def permutar(t,p):
    result = {}
    for i,j in enumerate(p):
        result[i] = t[j]
    return tuple(result[i] for i in range(len(t)))

def clausurar(t,p):
    result = set([t])
    viejos = 0
    while viejos != len(result):
        viejos = len(result)
        tuplas = set()
        for tupla in result:
            tuplas.add(permutar(tupla,p))
        result=result.union(tuplas)
        
    return result


#assert 2**card <= bdensity*card**barity

universe = range(card)
tuplas = set()
conjuntos = set()

for t in product(universe,repeat=barity):
    ct = frozenset(t)
    if len(ct)==barity and ct not in conjuntos:
        tuplas.add(t)
        conjuntos.add(ct)
#print (len(tuplas))
#assert False
ptuplas = set()        
for i,t in enumerate(sample(tuplas, 10000)):#int(bdensity*card**barity))
    p = choice(permutaciones)
    ptuplas = ptuplas.union(clausurar(t,p))


print (" ".join(str(j) for j in range(card)))
print ("")
print ("R0 %s %s" % (len(tuplas),barity))
for t in tuplas:
    print (" ".join(str(e) for e in t))
print ("")
print ("R1 1 5")
print("0 1 2 3 4")
print("")

print ("T0 1 5")
print("0 1 2 3 4")
print("")
