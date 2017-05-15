# -*- coding: utf-8 -*-
#!/usr/bin/env python

import random

def generator(cardinality,base_rels,target_rels):
    print(" ".join(str(i) for i in range(cardinality)))
    print("")
    rindex=0
    for tuples,arity in base_rels:
        r=set()
        print ("R%s %s %s" % (rindex,tuples,arity))
        while tuples != len(r):
            t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
            if t not in r:
                print(" ".join(str(i) for i in t))
                r.add(t)
        print("")
    tindex=0
    for tuples,arity in target_rels:
        r=set()
        print ("T%s %s %s" % (tindex,tuples,arity))
        while tuples != len(r):
            t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
            if t not in r:
                print(" ".join(str(i) for i in t))
                r.add(t)    
        print("")

def negative_generator_wr(cardinality,base_rels,target_rels):
    print(" ".join(str(i) for i in range(cardinality)))
    print("")
    rindex=0
    for tuples,arity in base_rels:
        r=set()
        print ("R%s %s %s" % (rindex,tuples,arity))
        while tuples != len(r):
            t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
            if t not in r:
                print(" ".join(str(i) for i in t))
                r.add(t)
        print("")
    tindex=0
    for tuples,arity in target_rels:
        r=set()
        print ("T%s %s %s" % (tindex,tuples,arity))
        while tuples != len(r):
            t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
            if t not in r and len(set(t))==arity:
                print(" ".join(str(i) for i in t))
                r.add(t)    
        print("")

def negative_generator2(cardinality,density):
    print(" ".join(str(i) for i in range(cardinality+2)))
    print("")
    rindex=0
    arity = 2
    tuples = int((cardinality**2)*density)
    r=set()
    f=set()
    srel = ""
    while tuples != len(r):
        t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
        if t not in r:
            srel+=" ".join(str(i) for i in t) + "\n"
            r.add(t)
    count=0
    for t in r:
        if t == (0,0):
            count += 1
            srel+=" ".join(str(i) for i in (cardinality,cardinality)) + "\n"
        elif t == (0,1):
            count += 1
            srel+=" ".join(str(i) for i in (cardinality,cardinality+1)) + "\n"
        elif t == (1,0):
            count += 1
            srel+=" ".join(str(i) for i in (cardinality+1,cardinality)) + "\n"
        elif t == (1,1):
            count += 1
            srel+=" ".join(str(i) for i in (cardinality+1,cardinality+1)) + "\n"
    srel=("%s %s %s\n" % (rindex,tuples + count,arity)) + srel
    print("R"+srel)

    print("T0 1 2")
    print("0 1")
    print("")

def positive_generator(cardinality,rels):
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
        print("T"+srel)

def negative_generator(cardinality,rels):
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
        print("T"+srel)

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-u", "--universe", dest="universe")
    parser.add_option("-a", "--arity", dest="arity")
    parser.add_option("-d", "--density", dest="density")

    (options, args) = parser.parse_args()
    
    universe = int(options.universe)
    arity = int(options.arity)
    density = float(options.density)
    
    #positive_generator(universe,[(int((universe**arity)*density),arity)])
    generator(universe,[(int((universe**arity)*density),arity)],[(int((universe**arity)*density),arity)])
    #negative_generator2(universe,density)
    #positive_generator(50,[((50**3)-2000,3)])
    #positive_generator(universe,[(int((universe**arity)*density),arity)])
