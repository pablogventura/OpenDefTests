import random
def ciclo(p,u):
    result = []
    u+=1
    cant = (u-p)
    for i in range(p,u):
        result.append((i,p+(i+1-p)%cant))
    return result

def completo(p,u):
    result=[]
    u+=1
    for i in range(p,u):
        for j in range(p,u):
            result.append((i,j))
    return result

def quitarayas(m,p):
    """m model, p proporcion"""
    return set(random.sample(m,int(len(m)*(1-p))))
    

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
    return list(result)

def pegaraleatorio(e1,e2):
    if not e1:
        return e2
    if not e2:
        return e1
    l1=random.choice(e1)
    l2=random.choice(e2)
    return pegar(e1,e2,l1,l2)

def continuo(m):
    result = set()
    renombre=sorted(set.union(*[set(t) for t in m]))
    for t in m:
        result.add(tuple(renombre.index(e) for e in t))
    return list(result)
    
def pseudopanal(cantelem,cants):
    result =[]
    a=0
    b=cantelem
    for i in range(cants):
        result = pegaraleatorio(result,ciclo(a,b-1))
        a+=cantelem
        b+=cantelem
    return continuo(result)
