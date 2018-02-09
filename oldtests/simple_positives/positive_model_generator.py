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
        r=set()
        srel=("%s %s %s\n" % (rindex,tuples,arity))
        while tuples != len(r):
            t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
            if t not in r:
                srel+=" ".join(str(i) for i in t) + "\n"
                r.add(t)
        print("R"+srel)
        rindex+=1
    print("T0"+srel[len(srel.split()[0]):])


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d", "--density", dest="density")
    parser.add_option("-a", "--arity", dest="arity")
    parser.add_option("-u", "--universe", dest="universe")
    parser.add_option("-q", "--quantity", dest="quantity", default = 1)
    parser.add_option("--seed", dest="seed",default=None)

    (options, args) = parser.parse_args()
    
    density = float(options.density)
    arity = int(options.arity)
    universe = int(options.universe)
    quantity = int(options.quantity)
    if options.seed:
        random.seed(int(options.seed))

    positive_generator(universe,[(int((universe**arity)*density),arity)]*quantity)
        
