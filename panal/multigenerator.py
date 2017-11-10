import os

path="data/"

barity=5
tarity=5
for diversity in range(2,80+1,5):
    for density in [0.1,0.2]:
        for universe in range(20,30+1,10):
            for i in range(500):
                if not os.path.isfile("%sp%s_%s_%s_%s_%s_q%s.model" % (path,i,barity,tarity,universe,diversity,density)) :
                    s = "python3 cuaddiver.py"
                    s += " -b%s -t%s -u%s -s%s -d%s > %s" % (barity,tarity,universe,diversity,density,path)
                    s += "p%s_%s_%s_%s_%s_q%s.model" % (i,barity,tarity,universe,diversity,density)
                    print("Generating %sp%s_%s_%s_%s_%s_q%s.model" % (path,i,barity,tarity,universe,diversity,density))
                    os.system(s)
                else:
                    print ("File %s already exists" % ("%sp%s_%s_%s_%s_q%s.model" % (path,i,barity,tarity,universe,diversity,density)))
     
print("GENERATION FINISHED")


# python cuaddiver.py -b5 -t2 -u10 -s4 -d0.01
