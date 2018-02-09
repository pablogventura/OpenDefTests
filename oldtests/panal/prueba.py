from itertools import product, permutations
from random import sample,choice,seed


def permutar(t,p):
    result = {}
    for i,j in enumerate(p):
        result[i] = t[j]
    return tuple(result[i] for i in range(len(t)))

def clausurar(t,permutaciones):
    result = set([t])
    viejos = 0
    while viejos != len(result):
        viejos = len(result)
        tuplas = set()
        for tupla in result:
            for p in permutaciones:
                tuplas.add(permutar(tupla,p))
        result=result.union(tuplas)
        
    return result

permutaciones =list(permutations(range(barity),barity))

t=(0,1,2,3,4)
print clausurar(t,[choice(permutaciones) for i in range(2)])
