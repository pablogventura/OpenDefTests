from collections import namedtuple, defaultdict
import os
import glob, os
from types import SimpleNamespace


path = "positives/"

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
    i,size,arity,universe = f[len(path)+1:-len(".result")].split("_")
    i=int(i)
    size=int(size)
    arity=int(arity)
    universe = int(universe)
    
    #exit_status 124
    
    s=s.splitlines()

        
    if timeout:
        #timeout case
        #data[arity][universe].max_s=None
        #data[arity][universe].min_s=None
        #data[arity][universe].average_s=None
        
        #data[arity][universe].max_time=None
        #data[arity][universe].min_time=None
        #data[arity][universe].average_time=None
        
        #data[arity][universe].succesfull=0
        data[size][arity][universe].timeouts+=1
    else:
        #succesful case 
        if data[size][arity][universe].max_s <= diversity:
            data[size][arity][universe].max_s=diversity
        if data[size][arity][universe].min_s >= diversity:
            data[size][arity][universe].min_s=diversity
        data[size][arity][universe].average_s+=diversity
        
        if data[size][arity][universe].max_time <= time:
            data[size][arity][universe].max_time=time
        if data[size][arity][universe].min_time >= time:
            data[size][arity][universe].min_time=time
        data[size][arity][universe].average_time+=time
        
        data[size][arity][universe].succesfull+=1
        
    
for size in range(5000,40000,5000):
    arity = 2
    for universe in range(200,450,50):
        try:
            data[size][arity][universe].average_s/=data[size][arity][universe].succesfull
            data[size][arity][universe].average_time/=data[size][arity][universe].succesfull
        except ZeroDivisionError:
            data[size][arity][universe].average_s=0
            data[size][arity][universe].average_time=3600

for size in range(5000,40000,5000):
    arity = 3
    for universe in range(25,45,5):
        try:
            data[size][arity][universe].average_s/=data[size][arity][universe].succesfull
            data[size][arity][universe].average_time/=data[size][arity][universe].succesfull
        except ZeroDivisionError:
            data[size][arity][universe].average_s=0
            data[size][arity][universe].average_time=3600


print("PROCESSING FINISHED")
print("")


import numpy as np
import matplotlib.pyplot as plt

#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

fig, ax = plt.subplots()

c=1/len(list(range(200,450,50)))#color
color=c
arity=2
for universe in range(200,450,50):
    x=[]
    y=[]
    for size in range(5000,40000,5000):
        if data[size][arity][universe].average_time != 3600:
            x.append(size)
            y.append(data[size][arity][universe].average_time)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, arity=%s' % arity)
ax.set_xlabel('Model Size')
ax.set_ylabel('Time (seconds)')
#plt.yscale('log')
plt.savefig("positive_tests_arity_%s_%s.pdf"%(arity,"time"))
plt.clf()

fig, ax = plt.subplots()

c=1/len(list(range(200,450,50)))#color
color=c
arity=2
for universe in range(200,450,50):
    x=[]
    y=[]
    for size in range(5000,40000,5000):
        if data[size][arity][universe].average_s:
            x.append(size)
            y.append(data[size][arity][universe].average_s)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, arity=%s' % arity)
ax.set_xlabel('Model Size')
ax.set_ylabel('Diversity (#S)')
#plt.yscale('log')
plt.savefig("positive_tests_arity_%s_%s.pdf"%(arity,"diversity"))
plt.clf()


fig, ax = plt.subplots()

c=1/len(list(range(25,45,5)))#color
color=c
arity=3
for universe in range(25,45,5):
    x=[]
    y=[]
    for size in range(5000,40000,5000):
        if data[size][arity][universe].average_time != 3600:
            x.append(size)
            y.append(data[size][arity][universe].average_time)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, arity=%s' % arity)
ax.set_xlabel('Model Size')
ax.set_ylabel('Time (seconds)')
plt.savefig("positive_tests_arity_%s_%s.pdf"%(arity,"time"))
plt.clf()

fig, ax = plt.subplots()

c=1/len(list(range(25,45,5)))#color
color=c
arity=3
for universe in range(25,45,5):
    x=[]
    y=[]
    for size in range(5000,40000,5000):
        if data[size][arity][universe].average_s:
            x.append(size)
            y.append(data[size][arity][universe].average_s)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, arity=%s' % arity)
ax.set_xlabel('Model Size')
ax.set_ylabel('Diversity (#S)')
#plt.yscale('log')
plt.savefig("positive_tests_arity_%s_%s.pdf"%(arity,"diversity"))
