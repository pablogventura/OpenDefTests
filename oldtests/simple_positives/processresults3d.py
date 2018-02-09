import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple, defaultdict
import os
import glob, os
from types import SimpleNamespace
import sys




path = "data/"

data = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda :defaultdict(lambda : SimpleNamespace(diversities=[],
                                                                                          times=[],
                                                                                          cancelled=0,
                                                                                          definable=0,
                                                                                          not_definable=0,
                                                                                          total=0)))))
                                                                                          
errors=[]
num_files=0
for f in glob.glob(path + "*.result"):
    num_files+=1
    print ("Processing %s" % f)

    file=open(f,"r")

    s = file.readline()
    state = None
    while s:
        s=s.strip()
        if "Diversity = " in s:
            diversity = int(s[len("Diversity = "):])
        elif "CANCELLED" in s:
            state = "C"
        elif "DEFINABLE" in s:
            if "NOT" in s:
                state = "ND"
            else:
                state = "D"
        elif " seconds time elapsed" in s:
            time = float(s.split()[0])
        s = file.readline()
    
    file.close()
        
    i,density,arity,universe,quantity = f[len(path)+1:-len(".result")].split("_")
    i=int(i)
    density=float(density)
    arity=int(arity)
    universe = int(universe)
    quantity = int(quantity[1:])

    #state
    if state == "D":
        data[density][arity][universe][quantity].definable+=1
    elif state == "ND":
        data[density][arity][universe][quantity].not_definable+=1
    elif state == "C":
        data[density][arity][universe][quantity].cancelled+=1
    else:
        errors.append(f)
        continue
        
    #counting
    data[density][arity][universe][quantity].total+=1
    
    #diversity
    data[density][arity][universe][quantity].diversities.append(diversity)
    
    #time
    data[density][arity][universe][quantity].times.append(time)

if errors:
    print("PARSE ERROR in:")
    for f in errors:
        print(f)
    sys.exit(1)

    
arity = 2
print("Arity: %s" % arity)
for quantity in range(1,4+1,1):
    print("  Quantity: %s" % quantity)
    for density in [0.1,0.2,0.3,0.4,0.5]:
        print("    Density: %s" % density)
        for universe in range(50,100+1,10):
            print("      Universe: %s" % universe)
            print("        Definables: %.2f%%" % (data[density][arity][universe][quantity].definable / data[density][arity][universe][quantity].total *100))
            print("        Not definables: %.2f%%" % (data[density][arity][universe][quantity].not_definable / data[density][arity][universe][quantity].total *100))
            print("        Cancelled: %.2f%%" % (data[density][arity][universe][quantity].cancelled / data[density][arity][universe][quantity].total *100))
            print("        Diversity: %s" % np.median(data[density][arity][universe][quantity].diversities))
            print("        Time: %s" % np.median(data[density][arity][universe][quantity].times))
arity = 3
print("Arity: %s" % arity)
for quantity in range(1,1+1,1):
    print("  Quantity: %s" % quantity)
    for density in [0.1,0.2,0.3,0.4,0.5]:
        print("    Density: %s" % density)
        for universe in range(23,27+1,1):
            print("      Universe: %s" % universe)
            print("        Definables: %.2f%%" % (data[density][arity][universe][quantity].definable / data[density][arity][universe][quantity].total *100))
            print("        Not definables: %.2f%%" % (data[density][arity][universe][quantity].not_definable / data[density][arity][universe][quantity].total *100))
            print("        Cancelled: %.2f%%" % (data[density][arity][universe][quantity].cancelled / data[density][arity][universe][quantity].total *100))
            print("        Diversity: %s" % np.median(data[density][arity][universe][quantity].diversities))
            print("        Time: %s" % np.median(data[density][arity][universe][quantity].times))



print("PROCESSING FINISHED of %s files" % num_files)
print("")





for y_axis in ["time","diversity"]:
    arity = 2
    for quantity in range(1,4+1,1):
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        #fig, ax = plt.subplots()
        c=1/len(list(range(50,100+1,10)))#color
        color=c
        for universe in range(50,100+1,10):
            x=[]
            y=[]
            z=[]
            for density in [0.1,0.2,0.3,0.4,0.5]:
                #print("        Diversity: %s" % np.median(data[density][arity][universe][quantity].diversities))
                x.append(density)
                y.append(universe)
                if y_axis == "time":
                    z.append(np.median(data[density][arity][universe][quantity].times))
                elif y_axis == "diversity":
                    z.append(np.median(data[density][arity][universe][quantity].diversities))
                else:
                    raise IndexError
            #dict_keys([' ', 'None', '', '-.', ':', '-', '--'])
            x,y=np.meshgrid(x,y)
            ax.plot_surface(x, y, z)#,linewidth=1.0, marker='o', linestyle="-")
            color+=c

        s_conf = '+'.join([str(arity)]*quantity)+"/"+str(arity)
        ax.set_title('Positive tests, arity=%s, configuration=%s' % (arity,s_conf))
        ax.set_xlabel('Density')
        ax.set_ylabel('Universe')
        if y_axis == "time":
            ax.set_zlabel('Time (seconds)')
        elif y_axis == "diversity":
            ax.set_zlabel('Diversity (#S)')
        else:
            raise IndexError
        #plt.yscale('log')
        plt.savefig("positive_tests_arity_%s_%s_%s.pdf"%(arity,y_axis,s_conf.replace("/","to")))
        plt.clf()


    arity = 3
    for quantity in range(1,1+1,1):
        fig, ax = plt.subplots()
        c=1/len(list(range(23,27+1,1)))#color
        color=c
        for universe in range(23,27+1,1):
            x=[]
            y=[]
            for density in [0.1,0.2,0.3,0.4,0.5]:
                #print("        Diversity: %s" % np.median(data[density][arity][universe][quantity].diversities))
                x.append(density)
                if y_axis == "time":
                    y.append(np.median(data[density][arity][universe][quantity].times))
                elif y_axis == "diversity":
                    y.append(np.median(data[density][arity][universe][quantity].diversities))
                else:
                    raise IndexError

            ax.plot(x, y, color=(color,0,0), linewidth=1.0, marker='o', linestyle="-",label="#Universe=%s"%universe)
            color+=c

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        legend = ax.legend(loc='lower right')
        legend.get_frame().set_alpha(0.5)
        s_conf = '+'.join([str(arity)]*quantity)+"/"+str(arity)
        ax.set_title('Positive tests, arity=%s, configuration=%s' % (arity,s_conf))
        ax.set_xlabel('Density')
        if y_axis == "time":
            ax.set_ylabel('Time (seconds)')
        elif y_axis == "diversity":
            ax.set_ylabel('Diversity (#S)')
        else:
            raise IndexError
        #plt.yscale('log')
        plt.savefig("positive_tests_arity_%s_%s_%s.pdf"%(arity,y_axis,s_conf.replace("/","to")))
        plt.clf()


import sys
sys.exit(0)
