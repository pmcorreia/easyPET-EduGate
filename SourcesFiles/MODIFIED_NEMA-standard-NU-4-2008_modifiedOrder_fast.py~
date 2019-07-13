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

OutputFilesDirectory=sys.argv[5]

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
# NEMA Specification NU 4-2008: Image Quality Phantom\n\
# Created by Geron Bindseil, Western University, 2012.\n\
\n\
#Total phantom for moving the entire phantom at once\n\
/gate/world/daughters/name NEMA_IQ_"+str(SourceID)+"\n\
/gate/world/daughters/insert cylinder\n\
/gate/NEMA_IQ_"+str(SourceID)+"/setMaterial Air\n\
/gate/NEMA_IQ_"+str(SourceID)+"/geometry/setRmax   16.75 mm\n\
/gate/NEMA_IQ_"+str(SourceID)+"/geometry/setRmin   0. mm\n\
/gate/NEMA_IQ_"+str(SourceID)+"/geometry/setHeight 80. mm\n\
/gate/NEMA_IQ_"+str(SourceID)+"/placement/setTranslation "+str(positionX)+" "+str(positionY)+" "+str(positionZ)+" mm\n\
/gate/NEMA_IQ_"+str(SourceID)+"/placement/alignToZ\n\
/gate/NEMA_IQ_"+str(SourceID)+"/vis/forceWireframe\n\
/gate/NEMA_IQ_"+str(SourceID)+"/vis/setColor white\n\
/gate/NEMA_IQ_"+str(SourceID)+"/vis/setVisible 0\n\
\n\
#Body hollow part (top) that is attached to the fixed top cover\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name body_hollow\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/body_hollow/setMaterial Plexiglass\n\
/gate/body_hollow/geometry/setRmax   16.75 mm\n\
/gate/body_hollow/geometry/setRmin   15. mm\n\
/gate/body_hollow/geometry/setHeight 30. mm\n\
/gate/body_hollow/placement/setTranslation 0. 0. 15. mm\n\
/gate/body_hollow/vis/forceWireframe\n\
/gate/body_hollow/vis/setColor green\n\
\n\
#Water contained in the chamber\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name body_hollow_water\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/body_hollow_water/setMaterial Water\n\
/gate/body_hollow_water/geometry/setRmax   15. mm\n\
/gate/body_hollow_water/geometry/setRmin   0. mm\n\
/gate/body_hollow_water/geometry/setHeight 30. mm\n\
/gate/body_hollow_water/placement/setTranslation 0. 0. 15. mm\n\
/gate/body_hollow_water/vis/forceWireframe\n\
/gate/body_hollow_water/vis/setColor white\n\
\n\
#Now the twin cold chambers (chamber 1 has Air, chamber 2 has Water)\n\
\n\
#Fixed top cover chamber #1 sitting in the water\n\
/gate/body_hollow_water/daughters/name top_cover_chamber_1\n\
/gate/body_hollow_water/daughters/insert cylinder\n\
/gate/top_cover_chamber_1/setMaterial Plexiglass\n\
/gate/top_cover_chamber_1/geometry/setRmax   5. mm\n\
/gate/top_cover_chamber_1/geometry/setRmin   0. mm\n\
/gate/top_cover_chamber_1/geometry/setHeight 15. mm\n\
/gate/top_cover_chamber_1/placement/setTranslation 7.5 0. 7.5 mm\n\
/gate/top_cover_chamber_1/vis/forceWireframe\n\
/gate/top_cover_chamber_1/vis/setColor white\n\
\n\
#Fill chamber #1 with air\n\
/gate/top_cover_chamber_1/daughters/name top_cover_chamber_1_contents\n\
/gate/top_cover_chamber_1/daughters/insert cylinder\n\
/gate/top_cover_chamber_1_contents/setMaterial Air\n\
/gate/top_cover_chamber_1_contents/geometry/setRmax   4. mm\n\
/gate/top_cover_chamber_1_contents/geometry/setRmin   0. mm\n\
/gate/top_cover_chamber_1_contents/geometry/setHeight 14. mm\n\
/gate/top_cover_chamber_1_contents/placement/setTranslation 0. 0. 0.5 mm\n\
/gate/top_cover_chamber_1_contents/vis/forceWireframe\n\
/gate/top_cover_chamber_1_contents/vis/setColor white\n\
\n\
#Fixed top cover chamber #2 sitting in the water\n\
/gate/body_hollow_water/daughters/name top_cover_chamber_2\n\
/gate/body_hollow_water/daughters/insert cylinder\n\
/gate/top_cover_chamber_2/setMaterial Plexiglass\n\
/gate/top_cover_chamber_2/geometry/setRmax   5. mm\n\
/gate/top_cover_chamber_2/geometry/setRmin   0. mm\n\
/gate/top_cover_chamber_2/geometry/setHeight 15. mm\n\
/gate/top_cover_chamber_2/placement/setTranslation -7.5 0. 7.5 mm\n\
/gate/top_cover_chamber_2/vis/forceWireframe\n\
/gate/top_cover_chamber_2/vis/setColor white\n\
\n\
#Fill chamber #2 with water\n\
/gate/top_cover_chamber_2/daughters/name top_cover_chamber_2_contents\n\
/gate/top_cover_chamber_2/daughters/insert cylinder\n\
/gate/top_cover_chamber_2_contents/setMaterial Water\n\
/gate/top_cover_chamber_2_contents/geometry/setRmax   4. mm\n\
/gate/top_cover_chamber_2_contents/geometry/setRmin   0. mm\n\
/gate/top_cover_chamber_2_contents/geometry/setHeight 14. mm\n\
/gate/top_cover_chamber_2_contents/placement/setTranslation 0. 0. 0.5 mm\n\
/gate/top_cover_chamber_2_contents/vis/forceWireframe\n\
/gate/top_cover_chamber_2_contents/vis/setColor white\n\
\n\
#Fixed Top Cover\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name fixed_top_cover\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/fixed_top_cover/setMaterial Plexiglass\n\
/gate/fixed_top_cover/geometry/setRmax   16.75 mm\n\
/gate/fixed_top_cover/geometry/setRmin   0. mm\n\
/gate/fixed_top_cover/geometry/setHeight 5. mm\n\
/gate/fixed_top_cover/placement/setTranslation 0. 0. 32.5 mm\n\
/gate/fixed_top_cover/vis/forceWireframe\n\
/gate/fixed_top_cover/vis/setColor green\n\
\n\
#Now define the screw 3 large shafts contained in the fixed top cover (excludes head and gasket)\n\
\n\
#Shaft 1\n\
/gate/fixed_top_cover/daughters/name shaft_1\n\
/gate/fixed_top_cover/daughters/insert cylinder\n\
/gate/shaft_1/setMaterial Nylon\n\
/gate/shaft_1/geometry/setRmax   1.75 mm\n\
/gate/shaft_1/geometry/setRmin   0. mm\n\
/gate/shaft_1/geometry/setHeight 5. mm\n\
/gate/shaft_1/placement/setTranslation 7.5 0. 0. mm\n\
/gate/shaft_1/vis/forceWireframe\n\
/gate/shaft_1/vis/setColor blue\n\
\n\
#Shaft 2\n\
/gate/fixed_top_cover/daughters/name shaft_2\n\
/gate/fixed_top_cover/daughters/insert cylinder\n\
/gate/shaft_2/setMaterial Nylon\n\
/gate/shaft_2/geometry/setRmax   1.75 mm\n\
/gate/shaft_2/geometry/setRmin   0. mm\n\
/gate/shaft_2/geometry/setHeight 5. mm\n\
/gate/shaft_2/placement/setTranslation -7.5 0. 0. mm\n\
/gate/shaft_2/vis/forceWireframe\n\
/gate/shaft_2/vis/setColor blue\n\
\n\
#Shaft 3\n\
/gate/fixed_top_cover/daughters/name shaft_3\n\
/gate/fixed_top_cover/daughters/insert cylinder\n\
/gate/shaft_3/setMaterial Nylon\n\
/gate/shaft_3/geometry/setRmax   1.75 mm\n\
/gate/shaft_3/geometry/setRmin   0. mm\n\
/gate/shaft_3/geometry/setHeight 5. mm\n\
/gate/shaft_3/placement/setTranslation 0. 7.5 0. mm\n\
/gate/shaft_3/vis/forceWireframe\n\
/gate/shaft_3/vis/setColor blue\n\
\n\
#Now make the o-rings and screw heads associated with these 3 large screws on the top fixed cover\n\
#Screw shaft protrudes 1.5 mm out of the main phantom, so make those separately from the heads\n\
\n\
#O-ring 1\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name o_ring_1\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/o_ring_1/setMaterial Buna\n\
/gate/o_ring_1/geometry/setRmax   3.65 mm\n\
/gate/o_ring_1/geometry/setRmin   2. mm\n\
/gate/o_ring_1/geometry/setHeight 1.5 mm\n\
/gate/o_ring_1/placement/setTranslation 7.5 0. 35.75 mm\n\
/gate/o_ring_1/vis/forceWireframe\n\
/gate/o_ring_1/vis/setColor red\n\
\n\
#O-ring 2\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name o_ring_2\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/o_ring_2/setMaterial Buna\n\
/gate/o_ring_2/geometry/setRmax   3.65 mm\n\
/gate/o_ring_2/geometry/setRmin   2. mm\n\
/gate/o_ring_2/geometry/setHeight 1.5 mm\n\
/gate/o_ring_2/placement/setTranslation -7.5 0. 35.75 mm\n\
/gate/o_ring_2/vis/forceWireframe\n\
/gate/o_ring_2/vis/setColor red\n\
\n\
#O-ring 3\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name o_ring_3\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/o_ring_3/setMaterial Buna\n\
/gate/o_ring_3/geometry/setRmax   3.65 mm\n\
/gate/o_ring_3/geometry/setRmin   2. mm\n\
/gate/o_ring_3/geometry/setHeight 1.5 mm\n\
/gate/o_ring_3/placement/setTranslation 0. 7.5 35.75 mm\n\
/gate/o_ring_3/vis/forceWireframe\n\
/gate/o_ring_3/vis/setColor red\n\
\n\
#Screw head 1 protruding shaft\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name screw_head_shaft_1\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/screw_head_shaft_1/setMaterial Nylon\n\
/gate/screw_head_shaft_1/geometry/setRmax   1.75 mm\n\
/gate/screw_head_shaft_1/geometry/setRmin   0. mm\n\
/gate/screw_head_shaft_1/geometry/setHeight 1.5 mm\n\
/gate/screw_head_shaft_1/placement/setTranslation 7.5 0. 35.75 mm\n\
/gate/screw_head_shaft_1/vis/forceWireframe\n\
/gate/screw_head_shaft_1/vis/setColor blue\n\
\n\
#Screw head 2 protruding shaft\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name screw_head_shaft_2\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/screw_head_shaft_2/setMaterial Nylon\n\
/gate/screw_head_shaft_2/geometry/setRmax   1.75 mm\n\
/gate/screw_head_shaft_2/geometry/setRmin   0. mm\n\
/gate/screw_head_shaft_2/geometry/setHeight 1.5 mm\n\
/gate/screw_head_shaft_2/placement/setTranslation -7.5 0. 35.75 mm\n\
/gate/screw_head_shaft_2/vis/forceWireframe\n\
/gate/screw_head_shaft_2/vis/setColor blue\n\
\n\
#Screw head 3 protruding shaft\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name screw_head_shaft_3\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/screw_head_shaft_3/setMaterial Nylon\n\
/gate/screw_head_shaft_3/geometry/setRmax   1.75 mm\n\
/gate/screw_head_shaft_3/geometry/setRmin   0. mm\n\
/gate/screw_head_shaft_3/geometry/setHeight 1.5 mm\n\
/gate/screw_head_shaft_3/placement/setTranslation 0. 7.5 35.75 mm\n\
/gate/screw_head_shaft_3/vis/forceWireframe\n\
/gate/screw_head_shaft_3/vis/setColor blue\n\
\n\
#Screw head 1\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name screw_head_1\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/screw_head_1/setMaterial Nylon\n\
/gate/screw_head_1/geometry/setRmax   4.2 mm\n\
/gate/screw_head_1/geometry/setRmin   0. mm\n\
/gate/screw_head_1/geometry/setHeight 2.3 mm\n\
/gate/screw_head_1/placement/setTranslation 7.5 0. 37.65 mm\n\
/gate/screw_head_1/vis/forceWireframe\n\
/gate/screw_head_1/vis/setColor blue\n\
\n\
#Screw head 2\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name screw_head_2\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/screw_head_2/setMaterial Nylon\n\
/gate/screw_head_2/geometry/setRmax   4.2 mm\n\
/gate/screw_head_2/geometry/setRmin   0. mm\n\
/gate/screw_head_2/geometry/setHeight 2.3 mm\n\
/gate/screw_head_2/placement/setTranslation -7.5 0. 37.65 mm\n\
/gate/screw_head_2/vis/forceWireframe\n\
/gate/screw_head_2/vis/setColor blue\n\
\n\
#Screw head 3\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name screw_head_3\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/screw_head_3/setMaterial Nylon\n\
/gate/screw_head_3/geometry/setRmax   4.2 mm\n\
/gate/screw_head_3/geometry/setRmin   0. mm\n\
/gate/screw_head_3/geometry/setHeight 2.3 mm\n\
/gate/screw_head_3/placement/setTranslation 0. 7.5 37.65 mm\n\
/gate/screw_head_3/vis/forceWireframe\n\
/gate/screw_head_3/vis/setColor blue\n\
\n\
#Done with the top half of the phantom.\n\
#Now do the bottom half which is solid plexiglass with holes of various sizes and a filling cap.\n\
#Do this by making a solid body of Plexiglass and cutting holes in it.\n\
\n\
#Solid lower body\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name body_solid\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/body_solid/setMaterial Plexiglass\n\
/gate/body_solid/geometry/setRmax   16.75 mm\n\
/gate/body_solid/geometry/setRmin   0. mm\n\
/gate/body_solid/geometry/setHeight 28. mm\n\
/gate/body_solid/placement/setTranslation 0. 0. -14. mm\n\
/gate/body_solid/vis/forceWireframe\n\
/gate/body_solid/vis/setColor green\n\
\n\
#Now make the 5 differently-sized holes filled with water & activity.\n\
\n\
#Hole 1-mm-diameter\n\
/gate/body_solid/daughters/name hole_1\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_1/setMaterial Water\n\
/gate/hole_1/geometry/setRmax   0.5 mm\n\
/gate/hole_1/geometry/setRmin   0. mm\n\
/gate/hole_1/geometry/setHeight 20. mm\n\
/gate/hole_1/placement/setTranslation -2.16 -6.66 4. mm\n\
/gate/hole_1/vis/forceWireframe\n\
/gate/hole_1/vis/setColor white\n\
\n\
#Hole 2-mm-diameter\n\
/gate/body_solid/daughters/name hole_2\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_2/setMaterial Water \n\
/gate/hole_2/geometry/setRmax   1. mm\n\
/gate/hole_2/geometry/setRmin   0. mm\n\
/gate/hole_2/geometry/setHeight 20. mm\n\
/gate/hole_2/placement/setTranslation 5.66 -4.11 4. mm\n\
/gate/hole_2/vis/forceWireframe\n\
/gate/hole_2/vis/setColor white\n\
\n\
#Hole 3-mm-diameter\n\
/gate/body_solid/daughters/name hole_3\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_3/setMaterial Water\n\
/gate/hole_3/geometry/setRmax   1.5 mm\n\
/gate/hole_3/geometry/setRmin   0. mm\n\
/gate/hole_3/geometry/setHeight 20. mm\n\
/gate/hole_3/placement/setTranslation 5.66 4.11 4. mm\n\
/gate/hole_3/vis/forceWireframe\n\
/gate/hole_3/vis/setColor white\n\
\n\
#Hole 4-mm-diameter\n\
/gate/body_solid/daughters/name hole_4\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_4/setMaterial Water\n\
/gate/hole_4/geometry/setRmax   2. mm\n\
/gate/hole_4/geometry/setRmin   0. mm\n\
/gate/hole_4/geometry/setHeight 20. mm\n\
/gate/hole_4/placement/setTranslation -2.16 6.66 4. mm\n\
/gate/hole_4/vis/forceWireframe\n\
/gate/hole_4/vis/setColor white\n\
\n\
#Hole 5-mm-diameter\n\
/gate/body_solid/daughters/name hole_5\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_5/setMaterial Water\n\
/gate/hole_5/geometry/setRmax   2.5 mm\n\
/gate/hole_5/geometry/setRmin   0. mm\n\
/gate/hole_5/geometry/setHeight 20. mm\n\
/gate/hole_5/placement/setTranslation -7. 0. 4. mm\n\
/gate/hole_5/vis/forceWireframe\n\
/gate/hole_5/vis/setColor white\n\
\n\
#Wide hole at the end of the bottom lid.\n\
/gate/body_solid/daughters/name wide_hole_lid\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/wide_hole_lid/setMaterial Water\n\
/gate/wide_hole_lid/geometry/setRmax   10. mm\n\
/gate/wide_hole_lid/geometry/setRmin   0. mm\n\
/gate/wide_hole_lid/geometry/setHeight 3. mm\n\
/gate/wide_hole_lid/placement/setTranslation 0. 0. -7.5 mm\n\
/gate/wide_hole_lid/vis/forceWireframe\n\
/gate/wide_hole_lid/vis/setColor white\n\
\n\
#Wide O-ring for bottom lid\n\
/gate/body_solid/daughters/name wide_o_ring\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/wide_o_ring/setMaterial Buna\n\
/gate/wide_o_ring/geometry/setRmax   12.825 mm\n\
/gate/wide_o_ring/geometry/setRmin   11.175 mm\n\
/gate/wide_o_ring/geometry/setHeight 1. mm\n\
/gate/wide_o_ring/placement/setTranslation 0. 0. -9 mm\n\
/gate/wide_o_ring/vis/forceWireframe\n\
/gate/wide_o_ring/vis/setColor red\n\
\n\
# Now make the 6 small nylon screws in the removable bottom cover.\n\
# The hole should be slightly deeper than the screw so add an air-filled region.\n\
# The shaft & screw cannot be repeated using the repeater because the Forbid\n\
# command in the source definition only removes the first volume from the source \n\
# volume as of GATE 6.1\n\
\n\
# Small shaft 1\n\
/gate/body_solid/daughters/name small_shaft_1\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/small_shaft_1/setMaterial Nylon\n\
/gate/small_shaft_1/geometry/setRmax   1.45 mm\n\
/gate/small_shaft_1/geometry/setRmin   0. mm\n\
/gate/small_shaft_1/geometry/setHeight 9. mm\n\
/gate/small_shaft_1/placement/setTranslation 14. 0. -9.5 mm\n\
/gate/small_shaft_1/vis/forceSolid\n\
/gate/small_shaft_1/vis/setColor blue\n\
\n\
# Air-filled hole for screw shaft 1\n\
/gate/body_solid/daughters/name hole_shaft_1\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_shaft_1/setMaterial Air\n\
/gate/hole_shaft_1/geometry/setRmax   1.45 mm\n\
/gate/hole_shaft_1/geometry/setRmin   0. mm\n\
/gate/hole_shaft_1/geometry/setHeight 4.5 mm\n\
/gate/hole_shaft_1/placement/setTranslation 14. 0. -2.75 mm\n\
/gate/hole_shaft_1/vis/forceWireframe\n\
/gate/hole_shaft_1/vis/setColor white\n\
\n\
# Small shaft 2\n\
/gate/body_solid/daughters/name small_shaft_2\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/small_shaft_2/setMaterial Nylon\n\
/gate/small_shaft_2/geometry/setRmax   1.45 mm\n\
/gate/small_shaft_2/geometry/setRmin   0. mm\n\
/gate/small_shaft_2/geometry/setHeight 9. mm\n\
/gate/small_shaft_2/placement/setTranslation 7. 12.12 -9.5 mm\n\
/gate/small_shaft_2/vis/forceSolid\n\
/gate/small_shaft_2/vis/setColor blue\n\
\n\
# Air-filled hole for screw shaft 2\n\
/gate/body_solid/daughters/name hole_shaft_2\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_shaft_2/setMaterial Air\n\
/gate/hole_shaft_2/geometry/setRmax   1.45 mm\n\
/gate/hole_shaft_2/geometry/setRmin   0. mm\n\
/gate/hole_shaft_2/geometry/setHeight 4.5 mm\n\
/gate/hole_shaft_2/placement/setTranslation 7. 12.12 -2.75 mm\n\
/gate/hole_shaft_2/vis/forceWireframe\n\
/gate/hole_shaft_2/vis/setColor white\n\
\n\
# Small shaft 3\n\
/gate/body_solid/daughters/name small_shaft_3\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/small_shaft_3/setMaterial Nylon\n\
/gate/small_shaft_3/geometry/setRmax   1.45 mm\n\
/gate/small_shaft_3/geometry/setRmin   0. mm\n\
/gate/small_shaft_3/geometry/setHeight 9. mm\n\
/gate/small_shaft_3/placement/setTranslation -7. 12.12 -9.5 mm\n\
/gate/small_shaft_3/vis/forceSolid\n\
/gate/small_shaft_3/vis/setColor blue\n\
\n\
# Air-filled hole for screw shaft 3\n\
/gate/body_solid/daughters/name hole_shaft_3\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_shaft_3/setMaterial Air\n\
/gate/hole_shaft_3/geometry/setRmax   1.45 mm\n\
/gate/hole_shaft_3/geometry/setRmin   0. mm\n\
/gate/hole_shaft_3/geometry/setHeight 4.5 mm\n\
/gate/hole_shaft_3/placement/setTranslation -7. 12.12 -2.75 mm\n\
/gate/hole_shaft_3/vis/forceWireframe\n\
/gate/hole_shaft_3/vis/setColor white\n\
\n\
# Small shaft 4\n\
/gate/body_solid/daughters/name small_shaft_4\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/small_shaft_4/setMaterial Nylon\n\
/gate/small_shaft_4/geometry/setRmax   1.45 mm\n\
/gate/small_shaft_4/geometry/setRmin   0. mm\n\
/gate/small_shaft_4/geometry/setHeight 9. mm\n\
/gate/small_shaft_4/placement/setTranslation -14. 0. -9.5 mm\n\
/gate/small_shaft_4/vis/forceSolid\n\
/gate/small_shaft_4/vis/setColor blue\n\
\n\
# Air-filled hole for screw shaft 4\n\
/gate/body_solid/daughters/name hole_shaft_4\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_shaft_4/setMaterial Air\n\
/gate/hole_shaft_4/geometry/setRmax   1.45 mm\n\
/gate/hole_shaft_4/geometry/setRmin   0. mm\n\
/gate/hole_shaft_4/geometry/setHeight 4.5 mm\n\
/gate/hole_shaft_4/placement/setTranslation -14. 0. -2.75 mm\n\
/gate/hole_shaft_4/vis/forceWireframe\n\
/gate/hole_shaft_4/vis/setColor white\n\
\n\
# Small shaft 5\n\
/gate/body_solid/daughters/name small_shaft_5\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/small_shaft_5/setMaterial Nylon\n\
/gate/small_shaft_5/geometry/setRmax   1.45 mm\n\
/gate/small_shaft_5/geometry/setRmin   0. mm\n\
/gate/small_shaft_5/geometry/setHeight 9. mm\n\
/gate/small_shaft_5/placement/setTranslation -7. -12.12 -9.5 mm\n\
/gate/small_shaft_5/vis/forceSolid\n\
/gate/small_shaft_5/vis/setColor blue\n\
\n\
# Air-filled hole for screw shaft 5\n\
/gate/body_solid/daughters/name hole_shaft_5\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_shaft_5/setMaterial Air\n\
/gate/hole_shaft_5/geometry/setRmax   1.45 mm\n\
/gate/hole_shaft_5/geometry/setRmin   0. mm\n\
/gate/hole_shaft_5/geometry/setHeight 4.5 mm\n\
/gate/hole_shaft_5/placement/setTranslation -7. -12.12 -2.75 mm\n\
/gate/hole_shaft_5/vis/forceWireframe\n\
/gate/hole_shaft_5/vis/setColor white\n\
\n\
# Small shaft 6\n\
/gate/body_solid/daughters/name small_shaft_6\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/small_shaft_6/setMaterial Nylon\n\
/gate/small_shaft_6/geometry/setRmax   1.45 mm\n\
/gate/small_shaft_6/geometry/setRmin   0. mm\n\
/gate/small_shaft_6/geometry/setHeight 9. mm\n\
/gate/small_shaft_6/placement/setTranslation 7. -12.12 -9.5 mm\n\
/gate/small_shaft_6/vis/forceSolid\n\
/gate/small_shaft_6/vis/setColor blue\n\
\n\
# Air-filled hole for screw shaft 6\n\
/gate/body_solid/daughters/name hole_shaft_6\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/hole_shaft_6/setMaterial Air\n\
/gate/hole_shaft_6/geometry/setRmax   1.45 mm\n\
/gate/hole_shaft_6/geometry/setRmin   0. mm\n\
/gate/hole_shaft_6/geometry/setHeight 4.5 mm\n\
/gate/hole_shaft_6/placement/setTranslation 7. -12.12 -2.75 mm\n\
/gate/hole_shaft_6/vis/forceWireframe\n\
/gate/hole_shaft_6/vis/setColor white\n\
\n\
# Now make the screw heads heads (can use repeater here because outside source\n\
# definition volume).\n\
\n\
# Small screw head\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name small_screw_head\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/small_screw_head/setMaterial Nylon\n\
/gate/small_screw_head/geometry/setRmax   2.25 mm\n\
/gate/small_screw_head/geometry/setRmin   0. mm\n\
/gate/small_screw_head/geometry/setHeight 2.3 mm\n\
/gate/small_screw_head/placement/setTranslation 14. 0. -29.15 mm\n\
/gate/small_screw_head/vis/forceSolid\n\
/gate/small_screw_head/vis/setColor blue\n\
\n\
# Now repeat this head 6 times\n\
/gate/small_screw_head/repeaters/insert ring\n\
/gate/small_screw_head/ring/setRepeatNumber 6\n\
\n\
# Now make a central large shaft, o-ring and screw head in the removable bottom cover\n\
\n\
#Shaft 4\n\
/gate/body_solid/daughters/name shaft_4\n\
/gate/body_solid/daughters/insert cylinder\n\
/gate/shaft_4/setMaterial Nylon\n\
/gate/shaft_4/geometry/setRmax   1.75 mm\n\
/gate/shaft_4/geometry/setRmin   0. mm\n\
/gate/shaft_4/geometry/setHeight 5. mm\n\
/gate/shaft_4/placement/setTranslation 0. 0. -11.5 mm\n\
/gate/shaft_4/vis/forceSolid\n\
/gate/shaft_4/vis/setColor blue\n\
\n\
#O-ring 4\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name o_ring_4\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/o_ring_4/setMaterial Buna\n\
/gate/o_ring_4/geometry/setRmax   3.65 mm\n\
/gate/o_ring_4/geometry/setRmin   2. mm\n\
/gate/o_ring_4/geometry/setHeight 1.5 mm\n\
/gate/o_ring_4/placement/setTranslation 0. 0. -28.75 mm\n\
/gate/o_ring_4/vis/forceSolid\n\
/gate/o_ring_4/vis/setColor red\n\
\n\
#Screw head 4\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name screw_head_4\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/screw_head_4/setMaterial Nylon\n\
/gate/screw_head_4/geometry/setRmax   4.2 mm\n\
/gate/screw_head_4/geometry/setRmin   0. mm\n\
/gate/screw_head_4/geometry/setHeight 2.3 mm\n\
/gate/screw_head_4/placement/setTranslation 0. 0. -30.65 mm\n\
/gate/screw_head_4/vis/forceSolid\n\
/gate/screw_head_4/vis/setColor blue\n\
\n\
#Screw head 4 protruding shaft\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/name screw_head_shaft_4\n\
/gate/NEMA_IQ_"+str(SourceID)+"/daughters/insert cylinder\n\
/gate/screw_head_shaft_4/setMaterial Nylon\n\
/gate/screw_head_shaft_4/geometry/setRmax   1.75 mm\n\
/gate/screw_head_shaft_4/geometry/setRmin   0. mm\n\
/gate/screw_head_shaft_4/geometry/setHeight 1.5 mm\n\
/gate/screw_head_shaft_4/placement/setTranslation 0. 0. -28.75 mm\n\
/gate/screw_head_shaft_4/vis/forceWireframe\n\
/gate/screw_head_shaft_4/vis/setColor blue\n\
\n\
# Refreshes the viewer\n\
/gate/geometry/rebuild\n\
\n\
#Attach all volumes as sensitive detectors\n\
/gate/body_hollow/attachPhantomSD\n\
/gate/body_hollow_water/attachPhantomSD\n\
/gate/body_solid/attachPhantomSD\n\
/gate/fixed_top_cover/attachPhantomSD\n\
/gate/hole_1/attachPhantomSD\n\
/gate/hole_2/attachPhantomSD\n\
/gate/hole_3/attachPhantomSD\n\
/gate/hole_4/attachPhantomSD\n\
/gate/hole_5/attachPhantomSD\n\
/gate/hole_shaft_1/attachPhantomSD\n\
/gate/hole_shaft_2/attachPhantomSD\n\
/gate/hole_shaft_3/attachPhantomSD\n\
/gate/hole_shaft_4/attachPhantomSD\n\
/gate/hole_shaft_5/attachPhantomSD\n\
/gate/hole_shaft_6/attachPhantomSD\n\
/gate/o_ring_1/attachPhantomSD\n\
/gate/o_ring_2/attachPhantomSD\n\
/gate/o_ring_3/attachPhantomSD\n\
/gate/o_ring_4/attachPhantomSD\n\
/gate/screw_head_1/attachPhantomSD\n\
/gate/screw_head_2/attachPhantomSD\n\
/gate/screw_head_3/attachPhantomSD\n\
/gate/screw_head_4/attachPhantomSD\n\
/gate/screw_head_shaft_1/attachPhantomSD\n\
/gate/screw_head_shaft_2/attachPhantomSD\n\
/gate/screw_head_shaft_3/attachPhantomSD\n\
/gate/screw_head_shaft_4/attachPhantomSD\n\
/gate/shaft_1/attachPhantomSD\n\
/gate/shaft_2/attachPhantomSD\n\
/gate/shaft_3/attachPhantomSD\n\
/gate/shaft_4/attachPhantomSD\n\
/gate/small_screw_head/attachPhantomSD\n\
/gate/small_shaft_1/attachPhantomSD\n\
/gate/small_shaft_2/attachPhantomSD\n\
/gate/small_shaft_3/attachPhantomSD\n\
/gate/small_shaft_4/attachPhantomSD\n\
/gate/small_shaft_5/attachPhantomSD\n\
/gate/small_shaft_6/attachPhantomSD\n\
/gate/top_cover_chamber_1/attachPhantomSD\n\
/gate/top_cover_chamber_1_contents/attachPhantomSD\n\
/gate/top_cover_chamber_2/attachPhantomSD\n\
/gate/top_cover_chamber_2_contents/attachPhantomSD\n\
/gate/wide_hole_lid/attachPhantomSD\n\
/gate/wide_o_ring/attachPhantomSD\n\
\n\
\n\
#=====================================================\n\
#   D I G I T I Z E R: DETECTOR ELECTRONIC RESPONSE\n\
#=====================================================\n\
\n\
/control/execute	 "+OutputFilesDirectory+"/digitizerScanner1.mac\n\
\n\
/control/execute	 "+OutputFilesDirectory+"/digitizerScanner2.mac\n\
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
/gate/physics/Gamma/SetCutInRegion      body_hollow_water 0.1 mm\n\
/gate/physics/Electron/SetCutInRegion   body_hollow_water 0.1 mm\n\
/gate/physics/Positron/SetCutInRegion   body_hollow_water 0.1 mm\n\
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
# INITIALISATION\n\
#=====================================================\n\
\n\
#initialization was moved to the source file\n\
/gate/run/initialize\n\
#################\n\
#               #\n\
#  S O U R C E  #\n\
#               #\n\
#################\n\
\n\
# NEMA Specification NU 4-2008: Image Quality Phantom\n\
\n\
# This is the source associated with the NEMA image quality phantom for\n\
# small animal imaging. Seven regions describe the location of activity:\n\
#\n\
# - The large upper chamber is filled with F18 solution.\n\
# - The 5 line sources in the solid part.\n\
# - The disk-shaped cap on the bottom of the phantom.\n\
# \n\
# These sources can be added, by creating large source volume encompassing\n\
# all these smaller regions and then using the Forbid command to remove\n\
# cold regions or regions composed of Plexiglass.\n\
\n\
# Set the activity\n\
/gate/source/addSource F18Main_"+str(SourceID)+"\n\
/gate/source/F18Main_"+str(SourceID)+"/setActivity 11000000. becquerel #Properly is 3700000 in units Bq\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/particle e+\n\
\n\
#add back-to-back\n\
#/gate/source/F18Main_"+str(SourceID)+"/gps/setType backtoback\n\
#/gate/source/F18Main_"+str(SourceID)+"/gps/particle gamma\n\
#/gate/source/F18Main_"+str(SourceID)+"/gps/monoenergy 511. keV\n\
\n\
/gate/source/F18Main_"+str(SourceID)+"/setForcedUnstableFlag true\n\
/gate/source/F18Main_"+str(SourceID)+"/setForcedHalfLife 6586.2 s\n\
\n\
# Set the geometry large main volume\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/type Volume\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/shape Cylinder\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/radius 15. mm\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/halfz 2. mm\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/angtype iso\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/centre 0. 0. 0. mm #this plus halffz allows to simulate only the 2D disk formed by the detectors\n\
\n\
# Now make sure there's no activity in the cold areas\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid top_cover_chamber_1\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid top_cover_chamber_1_contents\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid top_cover_chamber_2\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid top_cover_chamber_2_contents\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid body_solid\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid wide_o_ring\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid small_shaft_1\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid small_shaft_2\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid small_shaft_3\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid small_shaft_4\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid small_shaft_5\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid small_shaft_6\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid hole_shaft_1\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid hole_shaft_2\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid hole_shaft_3\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid hole_shaft_4\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid hole_shaft_5\n\
/gate/source/F18Main_"+str(SourceID)+"/gps/Forbid hole_shaft_6\n\
/gate/source/F18Main_"+str(SourceID)+"/visualize 1000 yellow 3\n\
# The particles emitted by the source are gammas\n\
\n\
/gate/source/list")
file.close()
