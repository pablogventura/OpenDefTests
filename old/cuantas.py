from collections import namedtuple, defaultdict
import os
from types import SimpleNamespace
negative=0
ejemplos=0
postimes=0
negtimes=0
path = "positives11/"
esneg=False
import glob, os
for f in glob.glob(path + "*0.1.result"):
    ejemplos+=1
    esneg=False
    print ("Processing %s" % f)
    #p10_30_2_0.2.result
    file=open(f,"r")
    s = file.readline()
    while s:
        if "NOT DEFINABLE" in s:
            esneg=True
        elif "\tUser time (seconds): " in s:
            time = float(s[len("\tUser time (seconds): "):])
        elif "\tSystem time (seconds): " in s:
            time += float(s[len("\tSystem time (seconds): "):])
            if esneg:
                negative+=1
                negtimes+=time
            else:
                postimes+=time
        s = file.readline()
    
    file.close()
    


print("PROCESSING FINISHED")
print(ejemplos-negative)
print(ejemplos)
print((ejemplos-negative)/ejemplos)
print("*"*80)

print(postimes/(ejemplos-negative))
print(negtimes/(negative))
