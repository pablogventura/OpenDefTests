from itertools import product
from random import sample

barity=5
tarity=5
bdensity=0.005
card=30

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
tuplas = sample(tuplas, 10000)#int(bdensity*card**barity))

tuplas.append(tuple(reversed(tuplas[0])))

print (" ".join(str(j) for j in range(card)))
print ("")
print ("R0 %s %s" % (len(tuplas),barity))
for t in tuplas:
    print (" ".join(str(e) for e in t))
print ("")

ttuplas = [tuplas[0]]
ttuplas.append(tuple(reversed(tuplas[0])))
print ("T0 %s %s" % (len(ttuplas),tarity))
for t in ttuplas:
    print (" ".join(str(e) for e in t))
print ("")

