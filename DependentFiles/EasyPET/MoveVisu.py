#!/usr/bin/env python

import os
import sys
import math
import numbers


filename='MoveVisu.mac'
file = open(filename,'w')

debug = False
topStep=0.9 #degress
acqTime=0.025 #seconds
topAng=90
botStep=.9 #degrees
numberOfInstants=topAng/topStep
numberOfTurns=1 #number of turns of the bottom motor
numberOfBottomPositions=numberOfTurns*360./botStep
if numberOfBottomPositions==int(numberOfBottomPositions):
	numberOfBottomPositions=int(numberOfBottomPositions)
	print("Number of bottom positions is an integer number :)")
	#print(numberOfBottomPositions)
else:
	print("Number of bottom positions is not an integer number!!!")
	print(numberOfBottomPositions)
	sys.exit(1)

bottomAngles=[x * botStep for x in range(0, int(360/botStep))]
distanceBetweenCristals=28.85*2
rotationAngle=[-float(topAng)/2]
print("Rotation angle ="+str(rotationAngle))

if numberOfInstants==int(numberOfInstants):
	numberOfInstants=int(numberOfInstants)
	print("Number of top positions is an integer number :)")
	#print(numberOfInstants)
else:
	print("Number of top positions is not an integer number!!!")
	print(numberOfInstants)
	sys.exit(1)
	
	
#time=[x * acqTime  for x in range(0,numberOfInstants*numberOfBottomPositions+1, 100)]
time=[x * acqTime for x in range(0,numberOfInstants*numberOfBottomPositions+1)]

file.write('#  ********************************************************\n\
#  * DISCLAIMER                                                      *\n\
#  *                                                                 *\n\
#  * Neither the authors of this software system, nor their employing*\n\
#  * institutes, nor the agencies providing financial support for this *\n\
#  * work make any representation or warranty, express or implied,     *\n\
#  * regarding this software system or assume any liability for its    *\n\
#  * use.                                                              *\n\
#  *                                                                   *\n\
#  * This code implementation is the intellectual property of the      *\n\
#  * OpenGATE collaboration.                                           *\n\
#  * By copying, distributing or modifying the Program (or any work    *\n\
#  * based on the Program) you indicate your acceptance of this        *\n\
#  * statement, and all its terms.                                     *\n\
#  *********************************************************************\n\
#\n\
\n')
for i in range(0,len(time)):
	file.write('/gate/timing/setTime     '+str(time[i])+' s\n')

file.close()
