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
    for tuples,arity in rels:
        if rindex == 0:
            trel =set()
        r=set()
        srel=("%s %s %s\n" % (rindex,tuples,arity))
        while tuples != len(r):
            t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
            if t not in r:
                srel+=" ".join(str(i) for i in t) + "\n"
                r.add(t)
                if rindex==0 and t[0]==t[2]:
                    trel.add(t[:2])
        print("R"+srel)
        rindex+=1
        
    srel=("T%s %s %s\n" % (0,len(trel),2))
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
    arity = 3
    universe = int(options.universe)
    quantity = 1
    if options.seed:
        random.seed(int(options.seed))

    positive_generator(universe,[(int((universe**arity)*density),arity)]*quantity)
        
