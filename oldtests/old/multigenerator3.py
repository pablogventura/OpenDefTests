import os

path = "positives2b/"
for quantity in [2,3]:
    for density in [0.1,0.2,0.3,0.4,0.5]:
        for universe in range(30,90+1,15):
            for i in range(50):
                s = "python3 generator2.py"
                s += " -d%s -a%s -u%s -q%s > %s" % (density,2,universe, quantity,path)
                s += "p%s_%s_%s_%s.model" % (i,density,quantity,universe)
                print("Generating %sp%s_%s_%s_%s.model" % (path,i,density,quantity,universe))
                os.system(s)
print("GENERATION FINISHED")
