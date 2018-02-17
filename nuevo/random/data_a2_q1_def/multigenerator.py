import os

path="./"

arity=2
quantity=1
try:
    for density in [0.5/2**4,0.5/2**3,0.5/2**2,0.5/2**1,0.5/2**0]:
        for universe in range(50,70+1,10):
            for i in range(500):
                if not os.path.isfile("%sp%s_d%s_a%s_u%s_q%s.model" % (path,i,density,arity,universe,quantity)) :
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

