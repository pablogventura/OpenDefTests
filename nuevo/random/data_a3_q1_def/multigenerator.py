import os

path="./"

arity=3
quantity=1
try:
    for density in [0.1,0.2,0.3,0.4,0.5]:
        for universe in range(20,30+1,5):
            for i in range(100):
                if not os.path.isfile("%sp%s_%s_%s_%s_q%s.model" % (path,i,density,arity,universe,quantity)) :
                    s = "python3 ../random_model_generator_D.py"
                    s += " -d%s -a%s -u%s -q%s > %s" % (density,arity,universe,quantity,path)
                    s += "p%s_d%s_a%s_u%s_q%s.model" % (i,density,arity,universe,quantity)
                    print("Generating %sp%s_d%s_a%s_u%s_q%s.model" % (path,i,density,arity,universe,quantity))
                    os.system(s)
                else:
                    print ("File %s already exists" % ("%sp%s_d%s_a%s_u%s_q%s.model" % (path,i,density,arity,universe,quantity)))
     
    print("GENERATION FINISHED")
    
except:
    print("GENERATION FAILED")

