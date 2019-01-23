#!/usr/bin/env python

import os
import sys
import math
import numbers

SourceID = int (sys.argv[1])
positionX=float(sys.argv[2]) 
positionY=float(sys.argv[3]) 
positionZ=float(sys.argv[4])
SourceGeometryFile = sys.argv[5] 
containerFileName='SourceContainer_'+str(SourceID)+'.mac'

os.system(".py")
