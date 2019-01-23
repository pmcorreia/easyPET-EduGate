#!/usr/bin/env python

import os
import sys
import math
import numbers


	
filename='positions.mac'
file = open(filename,'w')

debug = False
topStep=float(sys.argv[1]) #degress
acqTime=float(sys.argv[2]) #seconds
topAng=float(sys.argv[3])
botStep=float(sys.argv[4]) #degrees
numberOfTurns=int(float(sys.argv[5])) #number of turns of the bottom motor                                                                  
numberOfInstants=float("{0:.2f}".format(topAng/topStep+1)) #to have positions from -topAng/2 to +topAng/2  
#numberOfInstants=topAng/topStep+1 #to have positions from -topAng/2 to +topAng/2
#numberOfTurns=int(float(sys.argv[5])) #number of turns of the bottom motor
numberOfBottomPositions=numberOfTurns*360./botStep
numberOfTotalInstants=numberOfBottomPositions*numberOfTurns
if numberOfBottomPositions==int(numberOfBottomPositions):
	numberOfBottomPositions=int(numberOfBottomPositions)
	print("pfcNumber of bottom positions is an integer number :)")
	print(numberOfBottomPositions)
else:
	print("pfcNumber of bottom positions is not an integer number!!!")
	print(numberOfBottomPositions)
	sys.exit(1)

bottomAngles=[x * botStep for x in range(0, int(360/botStep)+1)]
distanceBetweenCristals=28.85*2
rotationAngle=[-float(topAng)/2]
#print("Rotation angle ="+str(rotationAngle))

if numberOfInstants==int(numberOfInstants):
	numberOfInstants=int(numberOfInstants)
	numberOfTotalInstants=int(numberOfTotalInstants)
	print("pfcNumber of top positions is an integer number :)")
	print(numberOfInstants)
else:
	print("pfcNumber of top positions is not an integer number!!!")
	print(numberOfInstants)
	sys.exit(1)
	
	
time=[x * acqTime for x in range(0,numberOfInstants*numberOfBottomPositions)]
#print("Time lenght ="+str(len(time)))

cristalCenterPosition=[43.85,0,0]

#topStep=topAng/numberOfInstants


#rotationAngle=[0]
direction=1.
endOfTopScan=0.
begin=0
rotationAngle=rotationAngle+[rotationAngle[-1]+direction*topStep]
for i in range(0,len(time)):
        if i==0:
                pass
        else:
                if '%.2f' % (rotationAngle[-1])=='%.2f' % (float(topAng)/2) and endOfTopScan==0:
                        rotationAngle=rotationAngle+[rotationAngle[-1]]
                        endOfTopScan=1
                elif '%.2f' % (rotationAngle[-1])=='%.2f' % (float(topAng)/2) and endOfTopScan==1:
                        direction=-1.
                        endOfTopScan=0
                        rotationAngle=rotationAngle+[rotationAngle[-1]+direction*topStep]
                        
                elif '%.2f' % (rotationAngle[-1])=='%.2f' % (-float(topAng)/2) and endOfTopScan==0:
                        endOfTopScan=1
                        rotationAngle=rotationAngle+[rotationAngle[-1]]
                        
                elif '%.2f' % (rotationAngle[-1])=='%.2f' % (-float(topAng)/2) and endOfTopScan==1:
                        direction=1.
                        endOfTopScan=0
                        rotationAngle=rotationAngle+[rotationAngle[-1]+direction*topStep]
                        
                else:
                        rotationAngle=rotationAngle+[rotationAngle[-1]+direction*topStep]
	
		
if debug:	
	print("Rotation angles = "+str(rotationAngle))

file.write("####### List of placement (translation and rotation) according to time\n\
###### Column 1      is Time in s (second)\n\
###### Column 2      is rotationAngle in degree\n\
###### Columns 3,4,5 are rotation axis \n\
###### Columns 6,7,8 are translation in mm\n\
Time s\n\
Rotation deg\n\
Translation mm\n")


translationPositionX=[]
translationPositionY=[]
translationPositionZ=[]

i=0

endOfTopScan=0.
turn=1
#print(numberOfBottomPositions*numberOfTurns)
#print(len(time))
for instant in range(0,len(time)):
    centralPositionX=43.85;
    centralPositionY=0;
    centralPositionZ=0;
    centralPositionX=centralPositionX-0*(distanceBetweenCristals/2)*(1-math.cos(bottomAngles[i]*math.pi/360))
    centralPositionY=centralPositionY-0*(distanceBetweenCristals/2)*math.sin(bottomAngles[i]*math.pi/360)
    translationPositionX=translationPositionX+[centralPositionX-(15-15*math.cos(rotationAngle[instant]*2*math.pi/360))]
    translationPositionY=translationPositionY+[centralPositionY-15*math.sin(rotationAngle[instant]*2*math.pi/360)]
    translationPositionZ=translationPositionZ+[centralPositionZ]
        
    if str(rotationAngle[instant])==str(float(topAng)/2) and endOfTopScan==0:
        endOfTopScan=1
    elif str(rotationAngle[instant])==str(float(topAng)/2) and endOfTopScan==1:
        i=i+1
        endOfTopScan=0
    elif (i!=0) and (str(rotationAngle[instant])==str(-float(topAng)/2)) and endOfTopScan==0:
        endOfTopScan=1
    elif (i!=0) and (str(rotationAngle[instant])==str(-float(topAng)/2)) and endOfTopScan==1:
        i=i+1
        endOfTopScan=0
    if (int(instant)==int(len(time)*float(turn)/float(numberOfTurns))-1):
 #               print("Instant = "+str(instant))
 #               print("Turn/numberOfTurns="+str(float(turn)/float(numberOfTurns)))
 #               print(rotationAngle[instant])
        turn=turn+1
        i=0
#print("Turns = "+str(turn-1))
rotationAxis=[0, 0, 1]


for instant in range(0,len(time)):
	file.write(str(time[instant])+" "+str(rotationAngle[instant])+" "+str(rotationAxis[0])+" "+str(rotationAxis[1])+" "+str(rotationAxis[2])+" "+str(translationPositionX[instant])+" "+str(translationPositionY[instant])+" "+str(translationPositionZ[instant])+"\n")
file.close()

filename2='positions2.mac'
file2 = open(filename2,'w')

cristalCenterPosition2=[-43.85,0,0]

file2.write("####### List of placement (translation and rotation) according to time\n\
###### Column 1      is Time in s (second)\n\
###### Column 2      is rotationAngle in degree\n\
###### Columns 3,4,5 are rotation axis \n\
###### Columns 6,7,8 are translation in mm\n\
Time s\n\
Rotation deg\n\
Translation mm\n")

centralPositionX2=-43.85;
centralPositionY2=0;
centralPositionZ2=0;

translationPositionX2=[]
translationPositionY2=[]
translationPositionZ2=[]

translationPosition2=[-43.85, 0, 0]

for instant in range(0,len(time)):
    translationPositionX2=translationPositionX2+[centralPositionX2+(distanceBetweenCristals+15)*(1-math.cos(rotationAngle[instant]*2*math.pi/360))]
    translationPositionY2=translationPositionY2+[centralPositionY2+(distanceBetweenCristals+15)*math.sin(rotationAngle[instant]*2*math.pi/360)]
    translationPositionZ2=translationPositionZ2+[centralPositionZ2]
    file2.write(str(time[instant])+" "+str(rotationAngle[instant])+" "+str(rotationAxis[0])+" "+str(rotationAxis[1])+" "+str(rotationAxis[2])+" "+str(translationPositionX2[instant])+" "+str(translationPositionY2[instant])+" "+str(translationPositionZ2[instant])+"\n")


file2.close()

