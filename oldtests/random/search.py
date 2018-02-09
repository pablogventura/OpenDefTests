import os, sys
import multiprocessing
import glob, os
import subprocess as sp
import time
import datetime

total=20
definables=0

running=[]

for i in range(total):
    g = sp.Popen(["python","random_model_generator.py", "-d0.2", "-a2","-u20", "-q10"],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE)
    running.append(sp.Popen(["python","../../main.py"],stdin=g.stdout,stdout=sp.PIPE,stderr=sp.PIPE))

while running:
    time.sleep(1)
    for p in running:
        if p.poll() is not None:
            #delete finished
            stdout = p.stdout.read().decode()
            if "NOT DEFINABLE" in stdout:
                print("nd")
            elif "DEFINABLE" in stdout:
                print("d")
                definables+=1
            else:
                print("er")
                print(p.stderr.read().decode())
            running.remove(p)

print("Definability: %.2f"%(definables/total))
