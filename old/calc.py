import math
from math import ceil

def density(size,universe,arity,qrel=3):
    return (size*(qrel**(1/arity)*(universe-1))**(-arity))/arity


def universe(size,density,arity,qrel=3):
    result=(size/(qrel*density*arity))**(1/arity)
    result+=1
    return math.floor(result)

desde=universe(35000,0.5,2,3)
hasta=universe(35000,0.1,2,3)
paso=ceil((universe(35000,0.1,2,3)-universe(35000,0.5,2,3))/6)

print("Desde %s" % desde)
print("Hasta %s" % hasta)
print("Con un paso de %s" % paso)

for size in range(5000,40000,5000):
    print(("Size: %s " % (size))+("*"*45))
    for u in range(desde,hasta+1,paso):
        print("\tUniverse: %s\tDenstity: %s" % (u,density(size,u,2,3)))


