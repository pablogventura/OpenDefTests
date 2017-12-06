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
    
def nuevaclausura(t,grupo):
    result = [tuple(map(lambda i:t[i],tupla)) for tupla in grupo]
    return result
            

def generar(card,barity,diversidad,densidad,tarity,perm):
    grupos = []
    permutaciones =list(permutations(range(barity),barity))
    for c in range(1,len(permutaciones)):
        for conjunto in permutations(permutaciones,c):
            grupo= clausurar((0,1,2),conjunto)
            if grupo not in grupos:
                grupos.append(grupo)
                #print(len(grupos))
                if len(grupos) == 156:
                    break
        if len(grupos) == 156:
                    break
    grupos = sorted(grupos,key=len,reverse=True)
    grupos = grupos[:0]
    #permutaciones = list(set(frozenset(sample(permutaciones, perm)) for i in range(diversidad-2)))
    #print (len(permutaciones))



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
    #print(int(len(tuplas)*density),len(tuplas))
    #assert False
    for i,t in enumerate(sample(tuplas, int(len(tuplas)*density))):#int(bdensity*card**barity))
        if grupos:
            p = choice(grupos)
            ptuplas = ptuplas.union(nuevaclausura(t,p))
        else:
            ptuplas.add(t)


    print (" ".join(str(j) for j in range(card)))
    print ("")
    print ("R0 %s %s" % (len(ptuplas)*15**2,barity+2))
    for t in ptuplas:
        for e1 in universe:
            for e2 in universe:
                print (" ".join(str(e) for e in (t+(e1,e2))))
    print ("")

    print ("T0 %s %s" % (len(ptuplas)*15**2,tarity))
    for t in ptuplas:
        for e1 in universe:
            for e2 in universe:
                print (" ".join(str(e) for e in (t+(e1,e2))))
    print("")



if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d", "--density", dest="density")
    parser.add_option("-s", "--diversity", dest="diversity")
    parser.add_option("-t", "--tarity", dest="tarity")
    parser.add_option("-b", "--barity", dest="barity")
    parser.add_option("-u", "--universe", dest="universe")
    parser.add_option("--seed", dest="seed",default=None)
    parser.add_option("--perm", dest="perm",default=1)

    (options, args) = parser.parse_args()
    
    density = float(options.density)
    tarity = int(options.tarity)
    barity = int(options.barity)
    universe = int(options.universe)
    diversity = int(options.diversity)
    perm = int(options.perm)
    if options.seed:
        seed(int(options.seed))
    generar(universe,barity,diversity,density,tarity,perm)
    
    
barity=5
tarity=5
card=20
diversidad = 6
densidad=0.5
