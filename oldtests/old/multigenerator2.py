import os

path = "positives/"
arity = 2
for size in range(5000,40000,5000):
    for universe in range(200,450,50):
        for i in range(50):
            s = "python3 generator2.py"
            s += " -s%s -a%s -u%s > %s" % (size,arity,universe,path)
            s += "p%s_%s_%s_%s.model" % (i,size,arity,universe)
            print("Generating %sp%s_%s_%s_%s.model" % (path,i,size,arity,universe))
            os.system(s)
arity = 3
for size in range(5000,40000,5000):
    for universe in range(25,45,5):
        for i in range(50):
            s = "python3 generator2.py"
            s += " -s%s -a%s -u%s > %s" % (size,arity,universe,path)
            s += "p%s_%s_%s_%s.model" % (i,size,arity,universe)
            print("Generating %sp%s_%s_%s_%s.model" % (path,i,size,arity,universe))
            os.system(s)
print("GENERATION FINISHED")
