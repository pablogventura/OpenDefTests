import os, sys
import multiprocessing
import glob, os
import subprocess as sp
import time
import datetime

print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

path = "data/"
timeout = "90m"

running = []
waiting = []

cores = 10


def num_order(f):
    f=f.replace("q","")
    f=f.split("/p")[1]
    f=f[:-len(".model")]
    f= f.split("_")
    f=list(map(float,f))
    return f

for filein in sorted(glob.glob(path + "*.model"),key=num_order,reverse=True):

    fileout = filein[:-6]+".result"
    if not os.path.isfile(fileout) :
        waiting.append((filein,["perf_4.13", "stat", "timeout", "--signal=SIGINT", timeout, "python3", "../../relationaldef/main.py"],fileout))
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
