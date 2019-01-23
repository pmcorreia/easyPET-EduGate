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


GateFile=sys.argv[1]
bashFile=GateFile[0:-4]+'.sh'

jobFile= open(bashFile, "w" )
bashFile_out=GateFile[0:-4]+'_out'
bashFile_err=GateFile[0:-4]+'_err'

jobFile.write('#!/bin/bash\n\
#SBATCH --nodes=1\n\
#SBATCH --time=200\n\
#SBATCH --mem-per-cpu=400\n\
#SBATCH -o '+bashFile_out+'\n\
#SBATCH -e '+bashFile_err+'\n\
\n\
\n\
echo "Starting at `date`"\n\
echo "Running on hosts: $SLURM_NODELIST"\n\
echo "Running on $SLURM_NNODES nodes."\n\
echo "Running on $SLURM_NPROCS processors."\n\
echo "Current working directory is `pwd`"\n\
\n\
source ~/.bashrc\n\
\n\
Gate '+str(GateFile)+'\n\
echo "Program finished with exit code $? at: `date`" \n\
\n')

jobFile.close()

os.system('sbatch '+bashFile) 
