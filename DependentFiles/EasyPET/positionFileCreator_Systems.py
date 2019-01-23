#!/usr/bin/env python

import os
import sys
import math
import numbers



debug = False
topStep=float(sys.argv[1]) #degress
acqTime=float(sys.argv[2]) #seconds
topAng=float(sys.argv[3])
botStep=float(sys.argv[4]) #degrees
numberOfTurns=int(float(sys.argv[5])) #number of turns of the bottom motornumberOfTurns=int(float(sys.argv[5])) #number of turns of the bottom motor                                                                  
numberOfInstants=float("{0:.2f}".format(topAng/topStep+1)) #to have positions from -topAng/2 to +topAng/2 
#numberOfInstants=topAng/topStep+1 #to have positions from -topAng/2 to +topAng/2
#numberOfTurns=int(float(sys.argv[5])) #number of turns of the bottom motor
numberOfBottomPositions=numberOfTurns*360./botStep
numberOfTotalInstants=numberOfBottomPositions*numberOfTurns
if numberOfBottomPositions==int(numberOfBottomPositions):
	numberOfBottomPositions=int(numberOfBottomPositions)
	print("pfcsNumber of bottom positions is an integer number :), with the number "+str(numberOfBottomPositions))
else:
	print("pfcsNumber of bottom positions is not an integer number!!!")
	print(numberOfBottomPositions)
	sys.exit(1)


#bottomAngles=range(0, 360+1, botStep)
bottomAngles=[x * botStep for x in range(0, int(360/botStep)+1)]
#print(bottomAngles)
distanceBetweenCristals=28.85*2
rotationAngle=[-float(topAng)/2]
#print("Rotation angle ="+str(rotationAngle))

if numberOfInstants == int(numberOfInstants):
	numberOfInstants=int(numberOfInstants)
	numberOfTotalInstants=int(numberOfTotalInstants)
	print("pfcsNumber of top positions is an integer number :)")
	print(numberOfInstants, numberOfTotalInstants)
else:
	print("pfcsNumber of top positions is not an integer number!!!")
	print(numberOfInstants)
	sys.exit(1)

time=[x * acqTime for x in range(0,numberOfInstants*numberOfBottomPositions)]


cristalCenterPosition=[43.85,0,0]

#topStep=topAng/numberOfInstants


#rotationAngle=[0]
direction=1.
endOfTopScan=0.
rotationAngle=rotationAngle+[rotationAngle[-1]+direction*topStep]
for i in range(1,len(time)):
        
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

filename='positionsScanner1.mac'
file = open(filename,'w')

file.write("####### List of placement (translation and rotation) according to time\n\
###### Column 1      is Time in s (second)\n\
###### Column 2      is rotationAngle in degree\n\
###### Columns 3,4,5 are rotation axis \n\
###### Columns 6,7,8 are translation in mm\n\
Time s\n\
Rotation deg\n\
Translation mm\n")


translationPositionX=[0]
translationPositionY=[0]
translationPositionZ=[0]
rotationBottomAngle=[]

i=0
skipVariable=0
turn=1
step=0
for instant in range(0,len(time)):
    centralPositionX=0;
    centralPositionY=0;
    centralPositionZ=0;
    rotationBottomAngle=rotationBottomAngle+[bottomAngles[i]]
    step=step+1
        
    if ('%.2f' % (rotationAngle[instant])=='%.2f' % (float(topAng)/2) and '%.2f' % (rotationAngle[instant-1])<'%.2f' % (float(topAng)/2)):
        i=i+1
#                skipVariable=1
#                print('CounterClockwise')
#                print(rotationAngle[instant])
#                print('%.2f' % (float(topAng)/2))
                
    elif (i!=0) and ('%.2f' % (rotationAngle[instant])=='%.2f' % (-float(topAng)/2)) and ('%.2f' % abs(rotationAngle[instant-1])<'%.2f' % abs(-float(topAng)/2)):
        i=i+1
#                skipVariable=1
#                print('Clockwise')
#                print(rotationAngle[instant])
#                print('%.2f' % (-float(topAng)/2))

    if (int(instant)==int(len(time)*float(turn)/float(numberOfTurns))-1):
        turn=turn+1
        i=0
                
rotationAxis=[0, 0, 1]


for instant in range(0,len(time)):
	file.write(str(time[instant])+" "+str(rotationBottomAngle[instant])+" "+str(rotationAxis[0])+" "+str(rotationAxis[1])+" "+str(rotationAxis[2])+" "+str(translationPositionX[0])+" "+str(translationPositionY[0])+" "+str(translationPositionZ[0])+"\n")
file.close()

filename2='positionsScanner2.mac'
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

centralPositionX2=0;
centralPositionY2=0;
centralPositionZ2=0;

translationPositionX2=[0]
translationPositionY2=[0]
translationPositionZ2=[0]

#print(str(rotationBottomAngle))
for instant in range(0,len(time)):
	file2.write(str(time[instant])+" "+str(rotationBottomAngle[instant])+" "+str(rotationAxis[0])+" "+str(rotationAxis[1])+" "+str(rotationAxis[2])+" "+str(translationPositionX2[0])+" "+str(translationPositionY2[0])+" "+str(translationPositionZ2[0])+"\n")


file2.close()

