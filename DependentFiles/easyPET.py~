#! /usr/bin/env python
import os
import time
import sys
import string
import subprocess
import math
import datetime
from subprocess import check_call

debug = 0
OutputFilesDirectory=sys.argv[1]
print(OutputFilesDirectory)

f = open(OutputFilesDirectory+'/parameters.txt', 'r')

sFile = {}
positionX = []
positionY = []
positionZ = []
sourceFile = {}


lines=f.readlines()
numberOfSources=len(lines)-5
sliceTime=float(lines[0].split("=")[1])
topStep=float(lines[1].split("=")[1])
topAng=float(float(lines[2].split("=")[1]))
botStep=float(lines[3].split("=")[1])
numberOfTurns=int(float(lines[4].split("=")[1]))
for i in range(0, numberOfSources):
    sFile[i]=lines[5+i].split(" ")[1]
    positionX.append(float(lines[5+i].split(" ")[2]))
    positionY.append(float(lines[5+i].split(" ")[3]))
    positionZ.append(float(lines[5+i].split(" ")[4]))

f.close()

if debug:
    print(sliceTime)
    print(topStep)
    print(topAng)
    print(botStep)
    print(numberOfTurns)
    for i in range(0, numberOfSources):
        print("Source "+str(sFile[i]))
        print(positionX[i])
        print(positionY[i])
        print(positionZ[i])


sliceTime=sliceTime/1000 #conversion milisec->sec
numberOfInstants=topAng/topStep+1
numberOfBottomPositions=numberOfTurns*360./botStep
acqTime=sliceTime
finalTime=acqTime*numberOfInstants*numberOfBottomPositions
#partsRange=range(1, int(finalTime/10)+1)



print(math.modf(acqTime))
print(str(math.modf(acqTime)[0])[2:])
print(math.modf(acqTime))

data=datetime.datetime.now()
#os.getcwd()+'/'+str(data.day)+'-'+str(data.strftime("%B"))+'-'+str(data.year)+'_'+str(data.hour)+'h'+str(data.minute)+'_'+str(numberOfTurns)+'turn_'+str(int(math.modf(acqTime)[1]))+'p'+str(math.modf(acqTime)[0])[2:]+'s_'+str(int(math.modf(botStep)[1]))+'p'+str(math.modf(botStep)[0])[2:]+'bot_'+str(int(math.modf(topStep)[1]))+'p'+str(math.modf(topStep)[0])[2:]+'top_range'+str(topAng)+'_'+sourceFileDir

os.system('python DependentFiles/EasyPET/positionFileCreator.py '+str(topStep)+' '+str(sliceTime)+' '+str(topAng)+' '+str(botStep)+' '+str(numberOfTurns))
os.system('python DependentFiles/EasyPET/positionFileCreator_Systems.py '+str(topStep)+' '+str(sliceTime)+' '+str(topAng)+' '+str(botStep)+' '+str(numberOfTurns))
os.system('mv positions.mac '+OutputFilesDirectory)
os.system('mv positions2.mac '+OutputFilesDirectory)
os.system('mv positionsScanner1.mac '+OutputFilesDirectory)
os.system('mv positionsScanner2.mac '+OutputFilesDirectory)

for i in range(0, numberOfSources):
    if debug:
        print('python SourcesFiles/'+sFile[i]+' '+str(i)+' '+str(positionX[i])+' '+str(positionY[i])+' '+str(positionZ[i]))
    os.system('python SourcesFiles/'+sFile[i]+' '+str(i)+' '+str(positionX[i])+' '+str(positionY[i])+' '+str(positionZ[i]))

#os.system('python DependentFiles/EasyPET/PlasticSourceContainer.py '+str(positionX)+' '+str(positionY)+' '+str(positionZ))
#sourceContainerFile='PlasticSourceContainer.mac'

#sourceFileDir, sourceFileExtension = os.path.splitext(raw_input('What is the source file?\n'))
for i in range(0, numberOfSources):
    sourceFileOutput, sourceFileExtension = os.path.splitext(sFile[i])
    sourceFile[i]=sourceFileOutput+'_ID_'+str(i)+'.mac'

if debug:
    print(sourceFile)
    print(sourceFileDir)
    print(OutputFilesDirectory)

#os.mkdir(OutputFilesDirectory)
for i in range(0, numberOfSources):
    os.system('mv SourcesFiles/'+sourceFile[i]+' '+OutputFilesDirectory)
os.system('cp DependentFiles/EasyPET/GateMaterials.db '+OutputFilesDirectory)
#os.system('cp Materials.xml '+OutputFilesDirectory)
os.system('cp DependentFiles/EasyPET/scanner1.mac '+OutputFilesDirectory)
os.system('cp DependentFiles/EasyPET/scanner2.mac '+OutputFilesDirectory)
os.system('cp DependentFiles/EasyPET/digitizerScanner1.mac '+OutputFilesDirectory)
os.system('cp DependentFiles/EasyPET/digitizerScanner2.mac '+OutputFilesDirectory)
#os.system('mv '+sourceContainerFile+' '+OutputFilesDirectory)

time.sleep(10)

#for part in partsRange:
subfile=OutputFilesDirectory+"/easyPET_part.sub"
subfileout=OutputFilesDirectory+"/easyPET"
gateFileName=OutputFilesDirectory+"/easyPET"
rootFilesDirectory=OutputFilesDirectory+"/easyPET"
startTime=0
endTime=finalTime
fh=open(gateFileName+".mac",'w')
fh.write('#  *******************************************************\n\
#  * DISCLAIMER                                                        *\n\
#  *                                                                   *\n\
#  * Neither the authors of this software system, nor their employing  *\n\
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
                                                          \n\
#-------------------oooooOOOOO00000OOOOOooooo---------------------#\n\
#\n\
#         D E F I N E   Y O U R   S C A N N E R   A N D       \n\
#                                                             \n\
#        Y O U R   C O M P L E T E   S I M U L A T I O N   \n\
#                                                             \n\
#        F O R   I M A G I N G    A P P L I CA T I O N S       \n\
#                                                     \n\
#-------------------oooooOOOOO00000OOOOOooooo---------------------#\n\
\n\
\n\
#=====================================================\n\
# VISUALISATION\n\
#=====================================================\n\
\n\
/vis/disable\n\
/vis/open                           OGLSQt\n\
/vis/viewer/set/viewpointThetaPhi   0 0\n\
/vis/viewer/zoom                    2.0\n\
/vis/drawVolume\n\
#/tracking/storeTrajectory           1\n\
#/vis/scene/add/trajectories\n\
#/vis/scene/endOfEventAction         accumulate\n\
/vis/scene/add/axes\n\
\n\
\n\
#=====================================================\n\
# GEOMETRY\n\
#=====================================================\n\
\n\
\n\
/gate/geometry/setMaterialDatabase    '+OutputFilesDirectory+'/GateMaterials.db\n\
\n\
\n\
#\n\
#     W O R L D\n\
#\n\
/gate/world/geometry/setXLength       20. cm\n\
/gate/world/geometry/setYLength       20. cm\n\
/gate/world/geometry/setZLength       20. cm\n\
/gate/world/setMaterial                 Air\n\
\n\
\n\
#-------------------oooooOOOOO00000OOOOOooooo---------------------#\n\
#                                                                 #\n\
#     D E F I N I T I O N   A N D   D E S C R I T I O N           #\n\
#        O F   Y O U R   P E T   D E V I C E                      ##	CYLINDRICAL\n\
\n\
#create geometry of the scanner1\n\
/control/execute '+OutputFilesDirectory+'/scanner1.mac\n\
\n\
#create geometry of the scanner2\n\
/control/execute '+OutputFilesDirectory+'/scanner2.mac\n\
\n\
/gate/head/moves/insert							genericMove\n\
/gate/head/genericMove/setPlacementsFilename	'+OutputFilesDirectory+'/positions.mac\n\
\n\
/gate/scanner1/moves/insert						genericMove\n\
/gate/scanner1/genericMove/setPlacementsFilename	'+OutputFilesDirectory+'/positionsScanner1.mac\n\
\n\
\n\
/gate/head2/moves/insert							genericMove\n\
/gate/head2/genericMove/setPlacementsFilename		'+OutputFilesDirectory+'/positions2.mac\n\
\n\
/gate/scanner2/moves/insert						genericMove\n\
/gate/scanner2/genericMove/setPlacementsFilename	'+OutputFilesDirectory+'/positionsScanner2.mac\n\
\n\
\n\
##PHANTOM\n\
#/gate/world/daughters/name my_phantom\n\
#/gate/world/daughters/insert cylinder\n\
#/gate/my_phantom/setMaterial Water\n\
#/gate/my_phantom/vis/setColor grey\n\
#/gate/my_phantom/geometry/setRmax   27.5 mm\n\
#/gate/my_phantom/geometry/setHeight 15. mm\n\
\n\
#=====================================================\n\
# PHYSICS\n\
#=====================================================\n\
\n\
/gate/physics/addPhysicsList emstandard_opt2\n\
/gate/physics/addProcess			Decay\n\
/gate/physics/addProcess			RadioactiveDecay\n\
/gate/physics/addProcess            PositronAnnihilation\n\
##\n\
\n\
\n\
/gate/physics/processList Enabled\n\
/gate/physics/processList Initialized\n\
\n\
#=====================================================\n\
# CUTS\n\
#=====================================================\n\
\n\
#/gate/physics/Gamma/SetCutInRegion      NEMA_IQ_0 0.1 mm\n\
#/gate/physics/Electron/SetCutInRegion   NEMA_IQ_0 0.1 mm\n\
#/gate/physics/Positron/SetCutInRegion   NEMA_IQ_0 0.1 mm\n\
#/gate/physics/processes/PhotoElectric/setXRayCut 100. keV\n\
#/gate/physics/processes/PhotoElectric/setDeltaRayCut 100. keV\n\
/gate/physics/processes/PhotoElectric/setXRayCut 100. keV\n\
/gate/physics/processes/PhotoElectric/setDeltaRayCut 100. keV\n\
#/gate/physics/gamma/setElectronCut 1. km\n\
\n\
\n\
\n\
\n\
/gate/geometry/rebuild\n\
\n\
#=====================================================\n\
# Show how the geometry moves with time\n\
#=====================================================\n\
\n\
#/control/execute                        MoveVisu.mac\n\
\n\
\n\
#=====================================================\n\
#	C O I N C I D E N C E    S O R T E R\n\
#===================================================== \n\
\n\
\n\
\n\
#/gate/digitizer/name                            delay\n\
#/gate/digitizer/insert                          coincidenceSorter\n\
#/gate/digitizer/delay/setWindow                 10. ns\n\
#/gate/digitizer/delay/setOffset                 500. ns\n\
#/gate/digitizer/delay/setOffset                 500. ns\n\
\n\
#=====================================================\n\
#  P A R T I C L E   S O U R C E\n\
#=====================================================\n')
for i in range(0, numberOfSources):
    fh.write('/control/execute '+OutputFilesDirectory+'/'+sourceFile[i]+'\n')

fh.write('\n\
#=====================================================\n\
#   D I G I T I Z E R: DETECTOR ELECTRONIC RESPONSE\n\
#=====================================================\n\
\n\
/control/execute	 '+OutputFilesDirectory+'/digitizerScanner1.mac\n\
\n\
/control/execute	 '+OutputFilesDirectory+'/digitizerScanner2.mac\n\
\n\
\n\
#=====================================================\n\
# INITIALISATION\n\
#=====================================================\n\
\n\
#initialization was moved to the source file\n\
#/gate/run/initialize\n\
#=====================================================\n\
#  D A T A   O U T P U T   \n\
#=====================================================\n\
\n\
/gate/output/root/enable\n\
/gate/output/root/setFileName                '+rootFilesDirectory+'\n\
/gate/output/root/setRootHitFlag              0\n\
/gate/output/root/setRootSinglesFlag          1\n\
#/gate/output/root/setRootSinglesBlurringFlag  1\n\
\n\
\n\
#====================================================\n\
#  R A N D O M   E N G I N E  A N D  S E E D\n\
#====================================================\n\
# JamesRandom Ranlux64 MersenneTwister\n\
/gate/random/setEngineName MersenneTwister\n\
#/gate/random/setEngineSeed default\n\
/gate/random/setEngineSeed auto\n\
#/gate/random/setEngineSeed 123456789\n\
#/gate/random/setEngineSeed default\n\
#/gate/random/resetEngineFrom fileName\n\
#/gate/random/verbose 0\n\
#/control/verbose 0\n\
#/grdm/verbose 0\n\
#/run/verbose 0\n\
#/tracking/verbose 0\n\
#/process/verbose 0\n\
\n\
#/gate/application/verbose 0\n\
#/gate/generator/verbose 0\n\
#/gate/source/verbose 0\n\
\n\
#=====================================================\n\
#   M E A S U R E M E N T   S E T T I N G S   \n\
#=====================================================\n\
\n\
/gate/application/setTimeSlice   '+str(sliceTime)+' s\n\
/gate/application/setTimeStart   '+str(startTime)+'   s\n\
/gate/application/setTimeStop    '+str(endTime)+' s\n\
\n\
/gate/application/startDAQ\n\
\n\
\n')
fh.close()
