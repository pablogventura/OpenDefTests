import os

path="data/"


for density in [0.1,0.2,0.3,0.4,0.5]:
    for universe in range(50,100+1,10):
        for i in range(50):
            s = "python3 projection_model_generator.py"
            s += " -d%s -u%s > %s" % (density,universe,path)
            s += "p%s_%s_%s.model" % (i,density,universe)
            print("Generating %sp%s_%s_%s.model" % (path,i,density,universe))
            os.system(s)          
print("GENERATION FINISHED")
