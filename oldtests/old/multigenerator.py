import os

universe = 30
path = "positives/"
for arity in [2,3,4]:
    for density in [0.1,0.2,0.3,0.4,0.5]:
        for i in range(50):
            s = "python generator.py"
            s += " -u%s -a%s -d%s > %s" % (universe,arity,density,path)
            s += "p%s_%s_%s_%s.model" % (i,universe,arity,density)
            print("Generating %sp%s_%s_%s_%s.model" % (path,i,universe,arity,density))
            os.system(s)
print("GENERATION FINISHED")
