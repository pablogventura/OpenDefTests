import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple, defaultdict
import os
import glob, os
from types import SimpleNamespace
import sys
import re

timeouts=0

try:
    path = sys.argv[1] + "/"
except:
    print("ERROR: Falta directorio de testing")
    sys.exit(1)

min_universo = int(input("Universo mas chico: "))
max_universo = int(input("Universo mas grande: "))
paso_universo = int(input("Paso universo: "))
titulo =input("Nombre pdfs: ")

data = defaultdict(lambda : defaultdict(lambda : SimpleNamespace(diversities=[],
                                                                  times=[],
                                                                  cancelled=0,
                                                                  definable=0,
                                                                  not_definable=0,
                                                                  total=0,
                                                                  auts=[],
                                                                  isos=[],
                                                                  minion_calls=[],
                                                                  minion_times=[])))
                                                                                          
errors=[]
num_files=0
for f in glob.glob(path + "*.result"):
    num_files+=1
    print ("Processing %s" % f)

    file=open(f,"r")

    s = file.readline()
    state = None
    """
      #Auts = 4
      #Isos = 433
      493 calls to Minion
      Minion total time = 0.476039 secs
    """
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
        elif "#Auts = " in s:
            automorfismos = int(s.split()[-1])
        elif "#Isos = " in s:
            isomorfismos=int(s.split()[-1])
        elif " calls to Minion" in s:
            llamadasminion=int(s.split()[0])
        elif "Minion total time = " in s:
            tiempominion=re.findall("[-+]?\d*\.\d+|[-+]?\d*\,\d+|\d+", s)
            assert len(tiempominion)==1
            tiempominion=float(tiempominion[0])
        s = file.readline()
    
    file.close()
        
    ff=f[len(path)+1:-len(".result")]
    ff=ff.replace("d","")
    ff=ff.replace("a","")
    ff=ff.replace("u","")
    ff=ff.replace("q","")
    i,density,arity,universe,quantity = ff.split("_")
    #i=int(i)
    quantity=int(quantity)
    arity=int(arity)
    density=float(density)

    universe = int(universe)


    #state
    if state == "D":
        data[density][universe].definable+=1
    elif state == "ND":
        data[density][universe].not_definable+=1
    elif state == "C":
        data[density][universe].cancelled+=1
        timeouts+=1
    else:
        errors.append(f)
        continue
        
    #counting
    data[density][universe].total+=1
    
    #diversity
    data[density][universe].diversities.append(diversity)
    
    #time
    data[density][universe].times.append(time)
    
    data[density][universe].auts.append(automorfismos)

    data[density][universe].isos.append(isomorfismos)

    data[density][universe].minion_calls.append(llamadasminion)

    data[density][universe].minion_times.append(tiempominion)

if errors:
    print("PARSE ERROR in:")
    for f in errors:
        print(f)
    sys.exit(1)
    

for density in [0.5/2**4,0.5/2**3,0.5/2**2,0.5/2**1,0.5/2**0]:
    print("    Density: %s" % density)
    for universe in range(min_universo,max_universo+1,paso_universo):
        try:
            print("      Universe: %s" % universe)
            print("        Definables: %.2f%%" % (data[density][universe].definable / data[density][universe].total *100))
            print("        Not definables: %.2f%%" % (data[density][universe].not_definable / data[density][universe].total *100))
            print("        Cancelled: %.2f%%" % (data[density][universe].cancelled / data[density][universe].total *100))
            print("        Diversity: %s" % np.median(data[density][universe].diversities))
            print("        Time: %s" % np.median(data[density][universe].times))
            print("        Auts: %s" % np.median(data[density][universe].auts))
            print("        Isos: %s" % np.median(data[density][universe].isos))
            print("        Minion calls: %s" % np.median(data[density][universe].minion_calls))
            print("        Minion time: %s" % np.median(data[density][universe].minion_times))
        except ZeroDivisionError:
            continue


print("PROCESSING FINISHED of %s files" % num_files)
print("")

markers=[".","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","x","X","D","d","|","_"]
markers=["o","s","p","*","+","D","d","|","_"]


for y_axis in ["time","diversity","definability"]:
    #from mpl_toolkits.mplot3d import Axes3D
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')

    fig, ax = plt.subplots(figsize=(2.5*(2/3.0), 2.5*(2/3.0)))
    marker=0
    max_y=-float("inf")
    min_y=float("inf")
    for universe in range(min_universo,max_universo+1,paso_universo):
        x=[]
        y=[]
        y2=[]
        for density in [0.5/2**4,0.5/2**3,0.5/2**2,0.5/2**1,0.5/2**0]:
            #print("        Diversity: %s" % np.median(data[density][universe].diversities))
            x.append(density)
            if y_axis == "time":
                y.append(np.median(data[density][universe].times))
                y2.append(np.median(data[density][universe].minion_times))
            elif y_axis == "diversity":
                y.append(np.median(data[density][universe].diversities))
                y2.append(np.median(data[density][universe].auts))
            elif y_axis == "definability":
                y.append(data[density][universe].definable / (data[density][universe].total-data[density][universe].cancelled) *100)
            else:
                raise IndexError
            max_y=max(y+[max_y])
            min_y=min(y+[min_y])
        #dict_keys([' ', 'None', '', '-.', ':', '-', '--'])
        ax.plot(x, y, color=(0,0,0), linewidth=1.0, marker=markers[marker], linestyle="-",label="#Universe=%s"%universe)
        if y_axis == "time" or y_axis == "diversity":
            ax.plot(x, y2, color=(0,0,0), linewidth=1.0, marker=markers[marker], linestyle=":",label="#Universe=%s"%universe)
        #ax.loglog(x, y, basex=2)
        ax.set_xscale('log')
        ax.set_xticks(x)
        ax.set_xlim([0.5/2**4.2,0.5/2**-0.2])
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        marker+=1

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    legend = ax.legend(loc='lower right')
    legend.get_frame().set_alpha(0.5)
    s_conf = '+'.join([str(2)]*quantity)+"/"+str(arity)
    fig.suptitle('Random tests, configuration=%s' % (s_conf), fontsize=14, fontweight='bold')
    ax.set_xlabel('Density')

    if min_y == max_y:
       max_y=min_y+1 
    y_margin=(max_y-min_y)/6
    ax.set_ylim([min_y-y_margin,max_y+y_margin])
    if y_axis == "time":
        ax.set_ylabel('Time (s)')
    elif y_axis == "diversity":
        ax.set_ylabel('Diversity ($|\mathcal{S}|$)')
    elif y_axis == "definability":
        ax.set_ylabel('Definability')
    else:
        raise IndexError
    if titulo:
        plt.savefig("random_tests_%s_%s_%s.pdf"%(y_axis,s_conf.replace("/","to"),titulo))
    else:
        plt.savefig("random_tests_%s_%s.pdf"%(y_axis,s_conf.replace("/","to")))
    plt.clf()


print("%s timeouts" % timeouts)


import sys
sys.exit(0)
