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

activity = 10 #in uCi

SourceFile=SourceFileExecutable[:-3]+'_ID_'+str(SourceID)+'.mac'
#0,00076046
#0,00304183
#0,00684411
#0,01216730
#0,01901141
#0,04562738
#0,91254753

hole1Activity=0.00076046*activity
hole2Activity=0.00304183*activity
hole3Activity=0.00684411*activity
hole4Activity=0.01216730*activity
hole5Activity=0.01901141*activity
topCylinderActivity=0.04562738*activity
bottomCylinderActivity=0.91254753*activity
#Source volumes
#smalll holes, with 23mm width	
#hole diameter(mm) 	#Volume (mm^3)			#fraction
#1			3.14*(0.5)*(0.5)*20=18.055	0,000904977
#2			3.14*(1)*(1)*20=72.22		0,00361991
#3			3.14*(1.5)*(1.5)*20=162.495	0,008144796
#4			3.14*(2)*(2)*20=288.88		0,014479638
#5			3.14*(2.5)*(2.5)*20=451.375	0,022624434

#top cylinder
#diameter 20mm
#width 3mm 
#Volume = 3.14*(10)*(10)*3=942
#fraction of total activity = 942/19950.775=0,047216211

#bottom cylinder
#diameter 30mm
#width 27mm 
#Volume = 3.14*(15)*(15)*27=19075.5
#bottom cylinder holes
#diameter 10mm
#width 13.5mm 
#Volume = 3.14*(5)*(5)*13.5=1059.75
#Bottom Cylinder Volume excluding two holes
#19075.5-2*1059.75=18015.75
#fraction 0,903010033

#Total volume with radioisotope
#18.055+72.22+162.495+288.88+451.375+942+18015.75 = 19950.775

#	
file=open(SourceFile,'w')
file.write("\n\
#  P A R T I C L E   S O U R C E\n\
#=====================================================\n\
\n\
#Plastic phantom around the source\n\
/gate/world/daughters/name Container"+str(SourceID)+"\n\
/gate/world/daughters/insert cylinder\n\
/gate/Container"+str(SourceID)+"/setMaterial PMMA\n\
/gate/Container"+str(SourceID)+"/vis/setColor grey\n\
/gate/Container"+str(SourceID)+"/geometry/setRmin 0 mm\n\
/gate/Container"+str(SourceID)+"/geometry/setRmax 16.75 mm\n\
/gate/Container"+str(SourceID)+"/geometry/setHeight 63 mm\n\
#/gate/Container"+str(SourceID)+"/placement/setRotationAxis 0 0 1\n\
#/gate/Container"+str(SourceID)+"/placement/setRotationAngle 90 deg\n\
/gate/Container"+str(SourceID)+"/placement/setTranslation "+str(positionX)+" "+str(positionY)+" "+str(positionZ)+" mm\n\
/gate/Container"+str(SourceID)+"/vis/forceWireframe \n\
\n\
/gate/geometry/rebuild\n\
\n\
#Holes1\n\
/gate/Container"+str(SourceID)+"/daughters/name Hole1\n\
/gate/Container"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/Hole1/setMaterial Water\n\
/gate/Hole1/vis/setColor red\n\
/gate/Hole1/geometry/setRmin 0 mm\n\
/gate/Hole1/geometry/setRmax 0.5 mm\n\
/gate/Hole1/geometry/setHeight 20 mm\n\
/gate/Hole1/placement/setTranslation  			0 7 11.5 mm #7*cos(90) e 7*sin(90) e 23/2 mm\n\
\n\
/gate/geometry/rebuild\n\
\n\
#Holes2\n\
/gate/Container"+str(SourceID)+"/daughters/name Hole2\n\
/gate/Container"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/Hole2/setMaterial Water\n\
/gate/Hole2/vis/setColor red\n\
/gate/Hole2/geometry/setRmin 0 mm\n\
/gate/Hole2/geometry/setRmax 1 mm\n\
/gate/Hole2/geometry/setHeight 20 mm\n\
/gate/Hole2/placement/setTranslation  			-6.66 2.16 11.5 mm #7*cos(90+72) e 7*sin(90+72)\n\
/gate/geometry/rebuild\n\
\n\
#Holes3\n\
/gate/Container"+str(SourceID)+"/daughters/name Hole3\n\
/gate/Container"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/Hole3/setMaterial Water\n\
/gate/Hole3/vis/setColor red\n\
/gate/Hole3/geometry/setRmin 0 mm\n\
/gate/Hole3/geometry/setRmax 1.5 mm\n\
/gate/Hole3/geometry/setHeight 20 mm\n\
/gate/Hole3/placement/setTranslation  			-4.11 -5.66 11.5 mm\n\
/gate/geometry/rebuild\n\
\n\
\n\
#Holes4\n\
/gate/Container"+str(SourceID)+"/daughters/name Hole4\n\
/gate/Container"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/Hole4/setMaterial Water\n\
/gate/Hole4/vis/setColor red\n\
/gate/Hole4/geometry/setRmin 0 mm\n\
/gate/Hole4/geometry/setRmax 2 mm\n\
/gate/Hole4/geometry/setHeight 20 mm\n\
/gate/Hole4/placement/setTranslation  			4.11 -5.66 11.5 mm\n\
/gate/geometry/rebuild\n\
\n\
#Holes5\n\
/gate/Container"+str(SourceID)+"/daughters/name Hole5\n\
/gate/Container"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/Hole5/setMaterial Water\n\
/gate/Hole5/vis/setColor red\n\
/gate/Hole5/geometry/setRmin 0 mm\n\
/gate/Hole5/geometry/setRmax 2.5 mm\n\
/gate/Hole5/geometry/setHeight 20 mm\n\
/gate/Hole5/placement/setTranslation  			6.66 2.16 11.5 mm\n\
/gate/geometry/rebuild\n\
\n\
#CylinderTop\n\
/gate/Container"+str(SourceID)+"/daughters/name TopCylinder\n\
/gate/Container"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/TopCylinder/setMaterial Water\n\
/gate/TopCylinder/vis/setColor red\n\
/gate/TopCylinder/geometry/setRmin 0 mm\n\
/gate/TopCylinder/geometry/setRmax 10 mm\n\
/gate/TopCylinder/geometry/setHeight 3 mm\n\
/gate/TopCylinder/placement/setTranslation 0. 0. 21.5 mm #20+3/2\n\
/gate/TopCylinder/vis/forceWireframe\n\
/gate/geometry/rebuild\n\
\n\
#CylinderBot\n\
/gate/Container"+str(SourceID)+"/daughters/name BotCylinder\n\
/gate/Container"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/BotCylinder/setMaterial Water\n\
/gate/BotCylinder/vis/setColor red\n\
/gate/BotCylinder/geometry/setRmin 0 mm\n\
/gate/BotCylinder/geometry/setRmax 15 mm\n\
/gate/BotCylinder/geometry/setHeight 30 mm\n\
/gate/BotCylinder/placement/setTranslation 0. 0. -15.0 mm #23/2+3/2\n\
/gate/BotCylinder/placement/setRotationAxis 0 0 1\n\
/gate/BotCylinder/placement/setRotationAngle 45 deg\n\
/gate/BotCylinder/vis/forceWireframe\n\
/gate/geometry/rebuild\n\
\n\
#CylinderBotHoleShell1\n\
/gate/BotCylinder/daughters/name BotCylinderHoleShell1\n\
/gate/BotCylinder/daughters/insert cylinder\n\
/gate/BotCylinderHoleShell1/setMaterial PMMA\n\
/gate/BotCylinderHoleShell1/vis/setColor white\n\
/gate/BotCylinderHoleShell1/geometry/setRmin 0 mm\n\
/gate/BotCylinderHoleShell1/geometry/setRmax 5 mm\n\
/gate/BotCylinderHoleShell1/geometry/setHeight 15 mm\n\
/gate/BotCylinderHoleShell1/placement/setTranslation 7. 0. -7.5 mm #13.5/2\n\
/gate/BotCylinderHoleShell1/vis/forceWireframe\n\
/gate/geometry/rebuild\n\
#CylinderBotHole1\n\
/gate/BotCylinderHoleShell1/daughters/name BotCylinderHole1\n\
/gate/BotCylinderHoleShell1/daughters/insert cylinder\n\
/gate/BotCylinderHole1/setMaterial Water\n\
/gate/BotCylinderHole1/vis/setColor white\n\
/gate/BotCylinderHole1/geometry/setRmin 0 mm\n\
/gate/BotCylinderHole1/geometry/setRmax 4 mm\n\
/gate/BotCylinderHole1/geometry/setHeight 14 mm\n\
/gate/BotCylinderHole1/placement/setTranslation 0. 0. -0.5 mm\n\
/gate/BotCylinderHole1/vis/forceWireframe\n\
/gate/geometry/rebuild\n\
\n\
#CylinderBotHoleShell2\n\
/gate/BotCylinder/daughters/name BotCylinderHoleShell2\n\
/gate/BotCylinder/daughters/insert cylinder\n\
/gate/BotCylinderHoleShell2/setMaterial PMMA\n\
/gate/BotCylinderHoleShell2/vis/setColor white\n\
/gate/BotCylinderHoleShell2/geometry/setRmin 0 mm\n\
/gate/BotCylinderHoleShell2/geometry/setRmax 5 mm\n\
/gate/BotCylinderHoleShell2/geometry/setHeight 15 mm\n\
/gate/BotCylinderHoleShell2/placement/setTranslation -14. 0. -7.5 mm #13.5/2\n\
/gate/BotCylinderHoleShell2/vis/forceWireframe\n\
/gate/geometry/rebuild\n\
#CylinderBotHole2\n\
/gate/BotCylinderHoleShell2/daughters/name BotCylinderHole2\n\
/gate/BotCylinderHoleShell2/daughters/insert cylinder\n\
/gate/BotCylinderHole2/setMaterial Air\n\
/gate/BotCylinderHole2/vis/setColor white\n\
/gate/BotCylinderHole2/geometry/setRmin 0 mm\n\
/gate/BotCylinderHole2/geometry/setRmax 4 mm\n\
/gate/BotCylinderHole2/geometry/setHeight 14 mm\n\
/gate/BotCylinderHole2/placement/setTranslation 0. 0. -0.5 mm\n\
/gate/BotCylinderHole2/vis/forceWireframe\n\
/gate/geometry/rebuild\n\
\n\
\n\
#=====================================================\n\
# INITIALISATION\n\
#=====================================================\n\
\n\
/gate/run/initialize\n\
#\n\
#Sources\n\
/gate/source/addSource F18_Source_Hole1_"+str(SourceID)+"\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/setActivity "+str(hole1Activity)+" muCi\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/gps/particle ion\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/gps/ion 11 22 0 0\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/gps/monoenergy 0. keV\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/gps/type Volume\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/gps/shape Cylinder\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/gps/radius 0.5 mm \n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/gps/halfz 10. mm	#20/2 \n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/gps/angtype iso\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/attachTo Hole1\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/setForcedUnstableFlag true\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/useDefaultHalfLife\n\
/gate/source/F18_Source_Hole1_"+str(SourceID)+"/visualize 20 yellow 3\n\
# The particles emitted by the source are gammas\n\
\n\
/gate/source/addSource F18_Source_Hole2_"+str(SourceID)+"\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/setActivity "+str(hole2Activity)+" muCi\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/gps/particle ion\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/gps/ion 11 22 0 0\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/gps/monoenergy 0. keV\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/gps/type Volume\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/gps/shape Cylinder\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/gps/radius 1 mm \n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/gps/halfz 10.0 mm	#20/2 \n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/gps/angtype iso\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/attachTo Hole2\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/setForcedUnstableFlag true\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/useDefaultHalfLife\n\
/gate/source/F18_Source_Hole2_"+str(SourceID)+"/visualize 20 yellow 3\n\
# The particles emitted by the source are gammas\n\
\n\
\n\
\n\
\n\
/gate/source/addSource F18_Source_Hole3_"+str(SourceID)+"\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/setActivity "+str(hole3Activity)+" muCi\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/gps/particle ion\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/gps/ion 11 22 0 0\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/gps/monoenergy 0. keV\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/gps/type Volume\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/gps/shape Cylinder\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/gps/radius 1.5 mm \n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/gps/halfz 10.0 mm	#20/2 \n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/gps/angtype iso\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/attachTo Hole3\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/setForcedUnstableFlag true\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/useDefaultHalfLife\n\
/gate/source/F18_Source_Hole3_"+str(SourceID)+"/visualize 20 yellow 3\n\
# The particles emitted by the source are gammas\n\
\n\
/gate/source/addSource F18_Source_Hole4_"+str(SourceID)+"\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/setActivity "+str(hole4Activity)+" muCi\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/gps/particle ion\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/gps/ion 11 22 0 0\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/gps/monoenergy 0. keV\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/gps/type Volume\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/gps/shape Cylinder\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/gps/radius 2 mm \n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/gps/halfz 10. mm	#20/2 \n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/gps/angtype iso\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/attachTo Hole4\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/setForcedUnstableFlag true\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/useDefaultHalfLife\n\
/gate/source/F18_Source_Hole4_"+str(SourceID)+"/visualize 20 yellow 3\n\
# The particles emitted by the source are gammas\n\
\n\
/gate/source/addSource F18_Source_Hole5_"+str(SourceID)+"\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/setActivity "+str(hole5Activity)+" muCi\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/gps/particle ion\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/gps/ion 11 22 0 0\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/gps/monoenergy 0. keV\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/gps/type Volume\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/gps/shape Cylinder\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/gps/radius 2.5 mm \n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/gps/halfz 10. mm	#20/2 \n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/gps/angtype iso\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/attachTo Hole5\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/setForcedUnstableFlag true\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/useDefaultHalfLife\n\
/gate/source/F18_Source_Hole5_"+str(SourceID)+"/visualize 20 yellow 3\n\
# The particles emitted by the source are gammas\n\
\n\
/gate/source/addSource F18_Source_TopCylinder_"+str(SourceID)+"\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/setActivity "+str(topCylinderActivity)+" muCi\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/gps/particle ion\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/gps/ion 11 22 0 0\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/gps/monoenergy 0. keV\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/gps/type Volume\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/gps/shape Cylinder\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/gps/radius 10 mm \n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/gps/halfz 1.5 mm	#3/2\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/gps/angtype iso\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/attachTo TopCylinder\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/setForcedUnstableFlag true\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/useDefaultHalfLife\n\
/gate/source/F18_Source_TopCylinder_"+str(SourceID)+"/visualize 20 yellow 3\n\
# The particles emitted by the source are gammas\n\
\n\
\n\
/gate/geometry/rebuild\n\
\n\
/gate/source/addSource F18_Source_BotCylinder_"+str(SourceID)+"\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/setActivity "+str(bottomCylinderActivity)+" muCi\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/particle ion\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/ion 11 22 0 0\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/monoenergy 0. keV\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/type Volume\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/shape Cylinder\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/radius 15 mm \n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/halfz 15. mm	#30/2\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/angtype iso\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/attachTo BotCylinder\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/setForcedUnstableFlag true\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/useDefaultHalfLife\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/Forbid  BotCylinderHoleShell1\n\
#/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/Forbid  BotCylinderHoleShell2\n\
#/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/Forbid  BotCylinderHole1\n\
#/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/gps/Forbid  BotCylinderHole2\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/dump 1\n\
/gate/source/F18_Source_BotCylinder_"+str(SourceID)+"/visualize 20 yellow 3\n\
# The particles emitted by the source are gammas")
file.close()
