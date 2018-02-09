def ciclo(p,u):
    result = []
    u+=1
    cant = (u-p)
    assert cant%2==0
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
    
    
def panal(maxx,maxy):#,maxz):
    assert (maxx % 2 and maxy % 2)
    result = []
    def i(x,y):
        if 0 <= x and x < maxx and 0 <= y and y < maxy:
            return x + y*maxy# + z*maxy*maxz
        else:
            return None
            
    for x in range(maxx):
        for y in range(maxy):
            if i(x,y) % 2 == 0:
                if i(x-1,y) is not None:
                    result.append((i(x,y),i(x-1,y)))
                if i(x+1,y) is not None:
                    result.append((i(x,y),i(x+1,y)))
            else:
                if i(x,y-1) is not None:
                    result.append((i(x,y),i(x,y-1)))
                if i(x,y+1) is not None:
                    result.append((i(x,y),i(x,y+1)))                
    return result
                
                
def model(maxx,maxy):
    def i(x,y):
        if 0 <= x and x < maxx and 0 <= y and y < maxy:
            return x + y*maxy# + z*maxy*maxz
        else:
            return None
    r= panal(maxx,maxy)
    print (" ".join(str(j) for j in range(maxx * maxy)))
    print ("")
    print ("R0 %s 2" % len(r))
    for a,b in r:
        if a == 1:
            print (" ".join(str(j) for j in (b,a)))
        elif b == i(0,1):
            print (" ".join(str(j) for j in (b,a)))
        else:
            print (" ".join(str(j) for j in (a,b)))
    
    target = [(1,)]        
    print ("")
    print ("T0 %s %s" % (len(target),len(target[0])))
    for t in target:
        print (" ".join(str(j) for j in t))
    print ("")
    
                
                
model(3,3)
                
                
                
                
                
                
                
                
                
                
