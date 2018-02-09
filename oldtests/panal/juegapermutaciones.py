from itertools import permutations
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
ies = []
permutaciones = list(permutations(range(5),5))

for p in permutaciones:
    i=0
    result = permutar(p,p)
    while result != p:
        i+=1
        result = permutar(result,p)
    ies.append(i)
print(sum(ies)/float(len(ies)))

print(max(ies))
print(min(ies))
