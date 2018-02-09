import os, sys
import multiprocessing
import glob, os
import subprocess as sp
import time
import datetime

print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

path = "positives2b/"
timeout = "30m"

running = []
waiting = []

cores = 10
arity=int(sys.argv[1])

def num_order(f):
    f = f[:-6]
    f= f.split("_")
    f[0]=f[0].split("/p")[1]
    f=list(map(float,[f[2],f[1],f[3],f[0]]))
    return f

for filein in sorted(glob.glob(path + "*_%s_*.model"%(arity)),key=num_order,reverse=True):

    fileout = filein[:-6]+".result"
    if not os.path.isfile(fileout) :
        waiting.append((filein,["perf", "stat", "timeout", "--signal=SIGINT", timeout, "python3", "main.py"],fileout))
    else:
        print ("File %s already exists" % fileout)


for i in range(cores):
    try:
        filein,call,fileout = waiting.pop(0)
    except IndexError:
        break
    print ("Processing %s" % filein)
    filein  = open(filein,"r")
    fileout = open(fileout, "w")
    running.append((sp.Popen(call,stdin=filein,stdout=fileout,stderr=fileout),filein,fileout))
    

while running:
    time.sleep(1)
    for p,fi,fo in running:
        if p.poll() is not None:
            #delete finished
            fi.close()
            fo.close()
            running.remove((p,fi,fo))
            #run new
            try:
                filein,call,fileout = waiting.pop()
                print ("Processing %s" % filein)
                filein  = open(filein,"r")
                fileout = open(fileout, "w")
                running.append((sp.Popen(call,stdin=filein,stdout=fileout,stderr=fileout),filein,fileout))
            except IndexError:
                continue
        


print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
print("PROCESSING FINISHED")
