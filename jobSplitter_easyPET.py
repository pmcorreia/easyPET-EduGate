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

nParts=100
fileToCopy=sys.argv[1]
filesPath=os.path.dirname(fileToCopy)+"/SimulationFiles"
os.mkdir(filesPath)
source= open(fileToCopy, "r" )
for line in source:
        
        lineSplit=line.split()
        if len(lineSplit)>1 and (lineSplit[0]== '/gate/application/setTimeStart') :
            timeStart = float(lineSplit[1])
        elif len(lineSplit)>1 and (lineSplit[0]== '/gate/application/setTimeStop') :
            timeEnd = float(lineSplit[1])
        elif len(lineSplit)>1 and (lineSplit[0]== '/gate/application/setTimeSlice') :
            timeSlice = float(lineSplit[1])
source.close()        

for i in range(0,nParts):
    
    fileToSave=filesPath+"/"+os.path.basename(fileToCopy)[0:-4]+'_part'+str(i)+'.mac'

    destination= open(fileToSave, "w" )
    source= open(fileToCopy, "r" )
    for line in source:
        lineSplit=line.split()
#        print(lineSplit)
        if len(lineSplit)>0 and (lineSplit[0]== '/gate/output/root/setFileName') :
                lineSplit[1]=lineSplit[1]+'_part'+str(i)
                line=' '.join(lineSplit)+'\n'
                destination.write( line )
        elif len(lineSplit)>1 and (lineSplit[0]== '/gate/application/setTimeStart') :
                lineSplit[1]=str(timeStart+timeEnd*i/nParts)
                line=' '.join(lineSplit)+'\n'
                destination.write( line )
        elif len(lineSplit)>1 and (lineSplit[0]== '/gate/application/setTimeStop') :
                lineSplit[1]=str(timeStart+timeEnd*(i+1)/nParts)
                line=' '.join(lineSplit)+'\n'
                destination.write( line )
        else :
                destination.write( line )


    source.close()
    destination.close()
    os.system("python jobSubmit_easyPET.py "+fileToSave)
    