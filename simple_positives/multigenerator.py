import os

path="data/"

arity = 2
for quantity in range(1,4+1,1):
    for density in [0.1,0.2,0.3,0.4,0.5]:
        for universe in range(50,100+1,10):
            for i in range(50):
                s = "python3 positive_model_generator.py"
                s += " -d%s -a%s -u%s -q%s > %s" % (density,arity,universe,quantity,path)
                s += "p%s_%s_%s_%s_q%s.model" % (i,density,arity,universe,quantity)
                print("Generating %sp%s_%s_%s_%s_q%s.model" % (path,i,density,arity,universe,quantity))
                os.system(s)
arity = 3
for quantity in range(1,1+1,1):
    for density in [0.1,0.2,0.3,0.4,0.5]:
        for universe in range(23,27+1,1):
            for i in range(50):
                s = "python3 positive_model_generator.py"
                s += " -d%s -a%s -u%s -q%s > %s" % (density,arity,universe,quantity,path)
                s += "p%s_%s_%s_%s_q%s.model" % (i,density,arity,universe,quantity)
                print("Generating %sp%s_%s_%s_%s_q%s.model" % (path,i,density,arity,universe,quantity))
                os.system(s)            
print("GENERATION FINISHED")
