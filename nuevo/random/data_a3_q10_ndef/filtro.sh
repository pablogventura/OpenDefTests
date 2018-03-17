#!/bin/sh
grep -rIL "NOT DEFINABLE" ./*result > definibles
sed -i 's/result/*/g' definibles
for f in $(cat definibles) ; do 
  rm "$f"
done
python3 multigenerator.py
