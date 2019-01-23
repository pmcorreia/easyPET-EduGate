#!/usr/bin/env python                                                                                                                                                                                                                         

import os
import sys
import math
import numbers

SourceFileExecutable = sys.argv[0]
SourceID = int (sys.argv[1])
positionX=float(sys.argv[2])
positionY=float(sys.argv[3])
positionZ=float(sys.argv[4])


SourceFile=SourceFileExecutable[:-3]+'_ID_'+str(SourceID)+'.mac'

file=open(SourceFile,'w')
file.write("\n\
#  P A R T I C L E   S O U R C E\n\
#=====================================================\n\
\n\
#Plastic phantom around the source\n\
/gate/world/daughters/name              Container"+str(SourceID)+"\n\
/gate/world/daughters/insert            box\n\
/gate/Container"+str(SourceID)+"/setMaterial            PMMA\n\
/gate/Container"+str(SourceID)+"/vis/setColor           grey\n\
/gate/Container"+str(SourceID)+"/geometry/setXLength    1. cm\n\
/gate/Container"+str(SourceID)+"/geometry/setYLength    1. cm\n\
/gate/Container"+str(SourceID)+"/geometry/setZLength    1. cm\n\
/gate/Container"+str(SourceID)+"/placement/setTranslation  "+str(positionX)+" "+str(positionY)+" "+str(positionZ)+" mm\n\
\n\
#=====================================================\n\
# INITIALISATION\n\
#=====================================================\n\
\n\
#initialization was moved to the source file\n\
/gate/run/initialize\n\
\n\
#################\n\
#               #\n\
#  S O U R C E  #\n\
#               #\n\
#################\n\
\n\
\n\
/gate/source/addSource                                  na22_"+str(SourceID)+"\n\
/gate/source/na22_"+str(SourceID)+"/setActivity         28 muCi\n\
/gate/source/na22_"+str(SourceID)+"/gps/particle        ion\n\
/gate/source/na22_"+str(SourceID)+"/gps/ion		11 22 0 0\n\
/gate/source/na22_"+str(SourceID)+"/gps/monoenergy	0. keV\n\
/gate/source/na22_"+str(SourceID)+"/gps/type	        Volume\n\
/gate/source/na22_"+str(SourceID)+"/gps/shape	        Sphere\n\
/gate/source/na22_"+str(SourceID)+"/gps/radius	        0.125 mm \n\
/gate/source/na22_"+str(SourceID)+"/gps/angtype	        iso\n\
/gate/source/na22_"+str(SourceID)+"/attachTo		Container"+str(SourceID)+"\n\
/gate/source/na22_"+str(SourceID)+"/setForcedUnstableFlag	true\n\
/gate/source/na22_"+str(SourceID)+"/useDefaultHalfLife\n\
\n\
/gate/source/na22_"+str(SourceID)+"/visualize 200 yellow 3\n\
# The particles emitted by the source are gammas")
file.close()
