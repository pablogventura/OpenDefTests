#!/bin/sh
python processresults.py data_a3_q1_def/ < aridad3
python processresults.py data_a3_q5_def/ < aridad3
python processresults.py data_a3_q10_def/ < aridad3
python processresults.py data_a2_q1_def/ < aridad2
python processresults.py data_a2_q5_def/ < aridad2
python processresults.py data_a2_q10_def/ < aridad2
mv *pdf graficos_paper/
