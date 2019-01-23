#!/usr/bin/env python

import os
import sys
import math
import numbers

positionX=float(sys.argv[1]) 
positionY=float(sys.argv[2]) 
positionZ=float(sys.argv[3]) 
containerFileName='PlasticSourceContainer.mac'
file=open(containerFileName,'w')
file.write("#=====================================================\n\
#  P A R T I C L E   S O U R C E\n\
#=====================================================\n\
\n\
#Plastic phantom around the source\n\
/gate/world/daughters/name		AcrylicBox\n\
/gate/world/daughters/insert		box\n\
/gate/AcrylicBox/setMaterial		PMMA\n\
/gate/AcrylicBox/vis/setColor		grey\n\
/gate/AcrylicBox/geometry/setXLength	1. cm\n\
/gate/AcrylicBox/geometry/setYLength	1. cm\n\
/gate/AcrylicBox/geometry/setZLength	1. cm\n\
/gate/AcrylicBox/placement/setTranslation  "+str(positionX)+" "+str(positionY)+" "+str(positionZ)+" mm")
file.close()
