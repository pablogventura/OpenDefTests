from itertools import product, permutations
from random import sample,choice
#TODO: densidad de tuplas tomadas




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

def generar(card,barity,diversidad,densidad,tarity):
    permutaciones =list(permutations(range(barity),barity))
    permutaciones = sample(permutaciones, diversidad-2)




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
    for i,t in enumerate(sample(tuplas, int(len(tuplas)*density))):#int(bdensity*card**barity))
        p = choice(permutaciones)
        ptuplas = ptuplas.union(clausurar(t,p))


    print (" ".join(str(j) for j in range(card)))
    print ("")
    print ("R0 %s %s" % (len(ptuplas),barity))
    for t in ptuplas:
        print (" ".join(str(e) for e in t))
    print ("")
    print ("R1 1 %s" % tarity)
    print (" ".join(str(j) for j in range(tarity)))
    print("")

    print ("T0 1 %s" % tarity)
    print (" ".join(str(j) for j in range(tarity)))
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

    (options, args) = parser.parse_args()
    
    density = float(options.density)
    tarity = int(options.tarity)
    barity = int(options.barity)
    universe = int(options.universe)
    diversity = int(options.diversity)
    if options.seed:
        random.seed(int(options.seed))
    generar(universe,barity,diversity,density,tarity)
    
    
barity=5
tarity=5
card=20
diversidad = 6
densidad=0.5
