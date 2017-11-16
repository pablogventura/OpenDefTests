import os

path="data2/"

arity = 3
for quantity in [1]:
    for density in [0.1,0.2,0.3,0.4,0.5]:
        for universe in range(20,40+1,10):
            for i in range(50):
                s = "python3 positive_model_generator.py"
                s += " -d%s -a%s -u%s -q%s > %s" % (density,arity,universe,quantity,path)
                s += "p%s_%s_%s_%s_q%s.model" % (i,density,arity,universe,quantity)
                print("Generating %sp%s_%s_%s_%s_q%s.model" % (path,i,density,arity,universe,quantity))
                os.system(s)            
print("GENERATION FINISHED")
