def ciclo(p,u):
    result = []
    u+=1
    cant = (u-p)
    for i in range(p,u):
        result.append((i,p+(i+1-p)%cant))
    return result


def pegar(e1,e2,l1,l2):
    #l2 va a desaparecer
    result = set(e1)
    for a,b in e2:
        ap,bp=a,b
        if a in l2:
            ap=l1[l2.index(a)]
        if b in l2:
            bp=l1[l2.index(b)]
        result.add((ap,bp))
    return result

def continuo(m):
    result = set()
    renombre=sorted(set.union(*[set(t) for t in m]))
    for t in m:
        result.add(tuple(renombre.index(e) for e in t))
    return result
