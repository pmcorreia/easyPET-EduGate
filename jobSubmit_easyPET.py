#! /usr/bin/env python                                                                                                                                                                                                                       
import os
import time
import sys
import string
import subprocess
import math
import datetime
from subprocess import check_call
import shutil

#echo "Running on $SLURM_NNODES nodes."\n\ - not defined in PBS
#echo "Running on $SLURM_NPROCS processors."\n\ - not defined in PBS

GateFile=sys.argv[1]
bashFile=GateFile[0:-4]+'.sh'

jobFile= open(bashFile, "w" )
bashFile_out=GateFile[0:-4]+'_out'
bashFile_err=GateFile[0:-4]+'_err'

jobFile.write('#!/bin/bash\n\
#PBS -l nodes=1\n\
#PBS -l walltime=40:00:00\n\
#PBS -l pmem=50mb\n\
#PBS -o '+bashFile_out+'\n\
#PBS -e '+bashFile_err+'\n\
\n\
\n\
echo "Starting at `date`"\n\
echo "Running on hosts: $PBS_NODEFILE"\n\
echo "Current working directory is `pwd`"\n\
\n\
source ~/.bashrc\n\
\n\
Gate '+str(GateFile)+'\n\
echo "Program finished with exit code $? at: `date`" \n\
\n')

jobFile.close()

os.system('qsub '+bashFile) 
