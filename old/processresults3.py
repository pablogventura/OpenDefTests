from collections import namedtuple, defaultdict
import os
import glob, os
from types import SimpleNamespace


path = "positives2b/"

data = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : SimpleNamespace(max_s=float("-inf"),
                                                                                      min_s=float("inf"),
                                                                                      average_s=0,
                                                                                      max_time=float("-inf"),
                                                                                      min_time=float("inf"),
                                                                                      average_time=0,
                                                                                      succesfull=0,
                                                                                      timeouts=0))))

for f in glob.glob(path + "*.result"):
    print ("Processing %s" % f)
    #p10_30_2_0.2.result
    file=open(f,"r")
    timeout = False
    s = file.readline()
    while s:
        if "Diversity=" in s:
            diversity = int(s[len("Diversity="):])
        elif "KeyboardInterrupt" in s:
            timeout = True
        elif " seconds time elapsed" in s:
            time = float(s.split()[0])
        s = file.readline()
    
    file.close()
    print(f[len(path)+1:-len(".result")].split("_"))
    i,density,quantity,universe = f[len(path)+1:-len(".result")].split("_")
    i=int(i)
    density=float(density)
    quantity=int(quantity)
    universe = int(universe)
    
    #exit_status 124
    
    s=s.splitlines()

        
    if timeout:
        #timeout case
        #data[quantity][universe].max_s=None
        #data[quantity][universe].min_s=None
        #data[quantity][universe].average_s=None
        
        #data[quantity][universe].max_time=None
        #data[quantity][universe].min_time=None
        #data[quantity][universe].average_time=None
        
        #data[quantity][universe].succesfull=0
        data[density][quantity][universe].timeouts+=1
    else:
        #succesful case 
        if data[density][quantity][universe].max_s <= diversity:
            data[density][quantity][universe].max_s=diversity
        if data[density][quantity][universe].min_s >= diversity:
            data[density][quantity][universe].min_s=diversity
        data[density][quantity][universe].average_s+=diversity
        
        if data[density][quantity][universe].max_time <= time:
            data[density][quantity][universe].max_time=time
        if data[density][quantity][universe].min_time >= time:
            data[density][quantity][universe].min_time=time
        data[density][quantity][universe].average_time+=time
        
        data[density][quantity][universe].succesfull+=1
        
    
for density in [0.1,0.2,0.3,0.4,0.5]:
    quantity = 2
    for universe in range(30,90+1,15):
        try:
            data[density][quantity][universe].average_s/=data[density][quantity][universe].succesfull
            data[density][quantity][universe].average_time/=data[density][quantity][universe].succesfull
        except ZeroDivisionError:
            data[density][quantity][universe].average_s=0
            data[density][quantity][universe].average_time=3600

for density in [0.1,0.2,0.3,0.4,0.5]:
    quantity = 3
    for universe in range(30,90+1,15):
        try:
            data[density][quantity][universe].average_s/=data[density][quantity][universe].succesfull
            data[density][quantity][universe].average_time/=data[density][quantity][universe].succesfull
        except ZeroDivisionError:
            data[density][quantity][universe].average_s=0
            data[density][quantity][universe].average_time=3600


print("PROCESSING FINISHED")
print("")


import numpy as np
import matplotlib.pyplot as plt

#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

fig, ax = plt.subplots()

c=1/len(list(range(30,90+1,15)))#color
color=c
quantity=2
for universe in range(30,90+1,15):
    x=[]
    y=[]
    for density in [0.1,0.2,0.3,0.4,0.5]:
        if data[density][quantity][universe].average_time != 3600:
            x.append(density)
            y.append(data[density][quantity][universe].average_time)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, quantity=%s' % quantity)
ax.set_xlabel('Model density')
ax.set_ylabel('Time (seconds)')
#plt.yscale('log')
plt.savefig("positive_tests_quantity_%s_%s.pdf"%(quantity,"time"))
plt.clf()

fig, ax = plt.subplots()

c=1/len(list(range(30,90+1,15)))#color
color=c
quantity=2
for universe in range(30,90+1,15):
    x=[]
    y=[]
    for density in [0.1,0.2,0.3,0.4,0.5]:
        if data[density][quantity][universe].average_s:
            x.append(density)
            y.append(data[density][quantity][universe].average_s)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, quantity=%s' % quantity)
ax.set_xlabel('Model density')
ax.set_ylabel('Diversity (#S)')
#plt.yscale('log')
plt.savefig("positive_tests_quantity_%s_%s.pdf"%(quantity,"diversity"))
plt.clf()


fig, ax = plt.subplots()

c=1/len(list(range(30,90+1,15)))#color
color=c
quantity=3
for universe in range(30,90+1,15):
    x=[]
    y=[]
    for density in [0.1,0.2,0.3,0.4,0.5]:
        if data[density][quantity][universe].average_time != 3600:
            x.append(density)
            y.append(data[density][quantity][universe].average_time)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, quantity=%s' % quantity)
ax.set_xlabel('Model density')
ax.set_ylabel('Time (seconds)')
plt.savefig("positive_tests_quantity_%s_%s.pdf"%(quantity,"time"))
plt.clf()

fig, ax = plt.subplots()

c=1/len(list(range(30,90+1,15)))#color
color=c
quantity=3
for universe in range(30,90+1,15):
    x=[]
    y=[]
    for density in [0.1,0.2,0.3,0.4,0.5]:
        if data[density][quantity][universe].average_s:
            x.append(density)
            y.append(data[density][quantity][universe].average_s)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, quantity=%s' % quantity)
ax.set_xlabel('Model density')
ax.set_ylabel('Diversity (#S)')
#plt.yscale('log')
plt.savefig("positive_tests_quantity_%s_%s.pdf"%(quantity,"diversity"))
