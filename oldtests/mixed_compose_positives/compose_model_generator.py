# -*- coding: utf-8 -*-
#!/usr/bin/env python

import random

def positive_generator(cardinality,rels):
    """
    Target is the last relation repeated.
    """

    print(" ".join(str(i) for i in range(cardinality)))
    print("")
    rindex=0
    relations=[]
    for tuples,arity in rels:
        if rindex == 0:
            trel =[]
        r=set()
        srel=("%s %s %s\n" % (rindex,tuples,arity))
        while tuples != len(r):
            t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
            if t not in r:
                srel+=" ".join(str(i) for i in t) + "\n"
                r.add(t)
                for j in r:
                    if t[1] == j[0]:
                        new = (t[0],t[1],j[1])
                        if new not in trel:
                            trel.append(new)
        print("R"+srel)
        rindex+=1
        relations.append(r)
    
    trel=set()
    r1,r2=relations
    for s in r1:
        for t in r2:
            if s[1]==t[0]:
                trel.add((s[0],s[1],t[1]))
    srel=("T%s %s %s\n" % (0,len(trel),3))
    for t in trel:
        srel+=" ".join(str(i) for i in t) + "\n"
    print(srel)


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d", "--density", dest="density")
    parser.add_option("-u", "--universe", dest="universe")
    parser.add_option("--seed", dest="seed",default=None)

    (options, args) = parser.parse_args()
    
    density = float(options.density)
    universe = int(options.universe)
    quantity = 2
    arity = 2
    if options.seed:
        random.seed(int(options.seed))

    positive_generator(universe,[(int((universe**arity)*density),arity)]*quantity)
        
