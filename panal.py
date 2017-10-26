def ciclo(n):
    assert n%2==0
    for i in range(n):
        print((i,(i+1)%n))
