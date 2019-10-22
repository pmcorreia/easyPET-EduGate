from PyQt4 import QtCore, QtGui
import sys
import os
import time
import sys
import string
import subprocess
import math
import datetime
import signal
import DraggableColorbar
import re #added
#
import matplotlib
#matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage import data_dir
from skimage.transform import radon, rescale
from skimage.transform import iradon
from skimage.morphology import disk
from skimage.filters import rank, gaussian,gabor
import scipy.misc
from scipy.ndimage import median_filter
#

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlibwidget import *
from matplotlib.gridspec import GridSpec

sys.path.insert(0,os.path.dirname(os.path.realpath(__file__))+'/SimulationGUI')
print(os.path.dirname(os.path.realpath(__file__))+'/SimulationGUI')
#sys.path.insert(0, os.getcwd()+'/SimulationGUI')
import Simulations
from jobcontrol import is_running, tail, kill

import scipy
import shlex
from shutil import copyfile

class ProgressClass(QtCore.QObject):
    valueUpdated = QtCore.pyqtSignal(int, int)


class OtherClass(QtCore.QObject):
    valueUpdated = QtCore.pyqtSignal(int)

#    print("Prog ="+str(progressBarRunning))
    def method(self):
        # i want to connect variable i to progress bar value
        i=0
        dir=1
#        print("Prog ="+str(ExampleGUIApp.progressBarRunning))
        ExampleGUIApp.progressBarRunning=True
        while ExampleGUIApp.progressBarRunning:
            self.valueUpdated.emit(i)
            time.sleep(0.1)
            i+=int(1*dir)
            if (i==100):
                dir=-dir
            elif (i==0):
                dir=-dir
        self.valueUpdated.emit(0)

class ExampleGUIApp(QtGui.QMainWindow, Simulations.Ui_MainWindow):

    progressBarRunning=False

    def __init__(self, parent=None):
        super(ExampleGUIApp, self).__init__(parent)
        self.setupUi(self)

        self.SelectSource_Button.clicked.connect(self.browse_sourceFile)  # When the button is pressed
        self.SelectSimulationOutput_Button.clicked.connect(self.outputSimulationFile)
        self.RemoveSource_pushButton.clicked.connect(self.remove_SourceListFile)  # When the button is pressed
        self.StartSimulation_pushButton.clicked.connect(self.startSimulationParametersFnc)
        self.StartSimulation_pushButton.clicked.connect(self.myButtonSlot)
        self.abortSimulation_Button.clicked.connect(self.abortSimulation_Fnc)
        self.RunningSimulation_tableWidget.itemClicked.connect(self.unlockAbortButton_Fnc)
        self.StartSimulation_pushButton.clicked.connect(self.unlockAbortButton_Fnc) #added if Sim Start, then remove files and processes enabled
        self.StartAnalysis_pushButton.clicked.connect(self.analyse_openMP)
        self.SelectResults_Button.clicked.connect(self.browse_AnalysisFile)
        self.interp_comboBox.activated.connect(self.interp_comboBox_Update)
        self.filter_comboBox.activated.connect(self.filter_comboBox_Update)
        self.gaussFilter_doubleSpinBox.valueChanged.connect(self.gaussFilter_doubleSpinBox_Update)
        self.pixelSize_comboBox.activated.connect(self.pixelSize_comboBox_Update)
        self.saveFigures_pushButton.clicked.connect(self.saveFigures_pushButton_Fnc)
        self.cmapname_comboBox.activated.connect(self.cmapname_comboBox_Fnc)
        self.Recon_pushButton.clicked.connect(self.FBP_selectFile)
        self.energy_threshold_lower_doubleSpinBox.valueChanged.connect(self.energy_threshold_Fnc)
        self.energy_threshold_upper_doubleSpinBox.valueChanged.connect(self.energy_threshold_Fnc)

        self.SourcesList_listWidget.resizeColumnsToContents()
        #self.SourcesList_listWidget.resizeRowsToContents()
        #self.SourcesList_listWidget.setSectionResizeMode()

        self.interp=str(self.interp_comboBox.currentText())
        self.filter=str(self.filter_comboBox.currentText())
        self.gaussFilter=float(str(self.gaussFilter_doubleSpinBox.value()))
        self.pixelSize=float(str(self.pixelSize_comboBox.currentText()))
        self.pixelSize_per_mm=1/self.pixelSize
        self.cmapname=str(self.cmapname_comboBox.currentText())
        self.energy_threshold_lower=float(str(self.energy_threshold_lower_doubleSpinBox.value()))
        self.energy_threshold_upper=float(str(self.energy_threshold_upper_doubleSpinBox.value()))

        self.processes = {}
        self.processes_stat = {}
        self.processes_dir = {}

        self.outputSimulationSelected = False
        self.sourceSelected = False
        self.resultsSelected = False
        self.clusterBool = False


        self.otherclass = OtherClass(self)
        self.otherclass.valueUpdated.connect(self.handleValueUpdated)

        self.progressclass = ProgressClass(self)
        self.progressclass.valueUpdated.connect(self.handleProgress)


        self.fig = Figure(dpi=100)
        self.fig.patch.set_alpha(0)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.FBPWidget)
        self.toolbar = NavigationToolbar(self.canvas, self.FBPWidget)
        # place plot components in a layout
        self.plotLayout = QtGui.QVBoxLayout()
        self.plotLayout.addWidget(self.canvas)
        self.plotLayout.addWidget(self.toolbar)
        self.FBPWidget.setLayout(self.plotLayout)

        #for energy histogram plot
        self.fig_energy = Figure(dpi=100)
        self.fig_energy.patch.set_alpha(0)
        self.canvas_energy = FigureCanvas(self.fig_energy)
        self.canvas_energy.setParent(self.Energywidget_3)
        #self.toolbar_energy = NavigationToolbar(self.canvas_energy, self.Energywidget_3)
        # place plot components in a layout
        self.plotLayout_energy = QtGui.QVBoxLayout()
        self.plotLayout_energy.addWidget(self.canvas_energy)
        #self.plotLayout_energy.addWidget(self.toolbar_energy)
        self.Energywidget_3.setLayout(self.plotLayout_energy)


        self.distanceCrystals=57.7

    def energy_threshold_Fnc(self):
        a=float(str(self.energy_threshold_lower_doubleSpinBox.value()))
        b=float(str(self.energy_threshold_upper_doubleSpinBox.value()))
        #if (b>a):
        #    self.energy_threshold_lower=a
        #    self.energy_threshold_upper=b
        #else:
        #    self.energy_threshold_lower=a
        #    self.energy_threshold_upper=a+1
        #    self.energy_threshold_lower_doubleSpinBox.setValue(self.energy_threshold_lower)
        #    self.energy_threshold_upper_doubleSpinBox.setValue(self.energy_threshold_upper)

    def cmapname_comboBox_Fnc (self):
        try:
            self.cmapname=str(self.cmapname_comboBox.currentText())
            self.ReconstructionFBP()
        except Exception as e:
            print(e)
            pass

    def saveFigures_pushButton_Fnc (self):
        matplotlib.image.imsave('reconstruction.jpg', self.reconstruction_fbp, cmap=plt.get_cmap(self.cmapname))
        matplotlib.image.imsave('sinogram.jpg', self.sinogram, cmap=plt.get_cmap(self.cmapname))



    def FBP_selectFile(self):
        try:
            self.FBP_filedir=QtGui.QFileDialog.getOpenFileName(self, 'Open File')
            self.FBP_filepath = os.path.dirname(str(self.FBP_filedir))
            self.SelectResultsString=str(self.FBP_filedir[:-4])
            print("Path is "+str(self.SelectResultsString))
            self.ReconstructionFBP()
            self.saveFigures_pushButton.setEnabled(True)

        except Exception as e:
            print(e)
            pass
        try:
            self.EnergyPlot()
        except Exception as e:
            print(e)
            pass



    def pixelSize_comboBox_Update (self):
        self.pixelSize=float(str(self.pixelSize_comboBox.currentText()))
        self.pixelSize_per_mm=1/self.pixelSize
        self.ReconstructionFBP()

    def interp_comboBox_Update (self):
        self.interp=str(self.interp_comboBox.currentText())
        self.ReconstructionFBP()

    def filter_comboBox_Update (self):
        self.filter=str(self.filter_comboBox.currentText())
        self.ReconstructionFBP()


    def gaussFilter_doubleSpinBox_Update (self):
        self.gaussFilter=float(str(self.gaussFilter_doubleSpinBox.value()))
        self.ReconstructionFBP()

    def startButtonDisable (self):
            self.StartAnalysis_pushButton.setEnabled(False)

    def startButtonEnable (self):
        if (self.resultsSelected == True):
            self.StartAnalysis_pushButton.setEnabled(True)

    def browse_sourceFile(self):
        #filename=QtGui.QFileDialog.getSaveFileName(self, 'Open File')
        self.filename=QtGui.QFileDialog.getOpenFileName(self, 'Open File', "SourcesFiles")
        self.filename=self.filename.split("/")[-1]
        self.StartSimulation_pushButton.setEnabled(True)
        #print(self.filename)

        if self.filename:
            #self.SourcesList_listWidget.addItem(self.filename)
            rowPosition=self.SourcesList_listWidget.rowCount()
            self.SourcesList_listWidget.insertRow(rowPosition)
            self.SourcesList_listWidget.setItem(rowPosition,0, QtGui.QTableWidgetItem(self.filename))

            self.SourcesList_listWidget.setItem(rowPosition,1, QtGui.QTableWidgetItem(str(0)))
            self.SourcesList_listWidget.setItem(rowPosition,2, QtGui.QTableWidgetItem(str(0)))
            self.SourcesList_listWidget.setItem(rowPosition,3, QtGui.QTableWidgetItem(str(0)))

    def interpSinogram(self, sinogram):
        x = np.arange(0, sinogram.shape[1])
        y = np.arange(0, sinogram.shape[0])
        sinogramMasked = np.ma.masked_equal(sinogram,0)
        xx, yy = np.meshgrid(x, y)
        x1 = xx[~sinogramMasked.mask]
        y1 = yy[~sinogramMasked.mask]
        newarr = sinogram[~sinogramMasked.mask]
        sinogram = scipy.interpolate.griddata((x1, y1), newarr.ravel(),
                          (xx, yy),
                          method='linear',
                          fill_value=0)

        return sinogram

    def EnergyPlot(self):

        gs=GridSpec(2,1)
        self.fig_energy.clf()

        self.axes1_energy = self.fig_energy.add_subplot(gs[0,0],sharey=None,sharex=None)
        self.axes2_energy = self.fig_energy.add_subplot(gs[1:2,0],sharey=None,sharex=self.axes1_energy)
        
        self.axes1_energy.patch.set_alpha(0)
        self.axes2_energy.patch.set_alpha(0)
        self.axes1_energy.set_xlim(0, 1500)
        self.axes2_energy.set_xlim(0, 1500)



        #self.axes1_energy.imshow(np.random.random((100, 100)))
        #self.axes2_energy.imshow(np.random.random((100, 100)))
        energyFile=str(self.SelectResultsString[:-5]+'.energy')
    	
	
        print(energyFile)
        try:
            x, y = np.loadtxt(energyFile, delimiter=' ', usecols=(0, 1), unpack=True)
            x=x*1000;
            y=y*1000;
            self.axes1_energy.hist(x, 100, facecolor='g', alpha=0.75)
            self.axes2_energy.hist(y, 100, facecolor='r', alpha=0.75)

            plt.setp(self.axes1_energy.get_xticklabels(), visible=False)
            self.axes2_energy.set_xlabel(str("Gamma Energy [keV]"))
            self.axes2_energy.set_ylabel(str("Counts"))
            self.fig_energy.canvas.draw()

        except Exception as e:
            print(e)
            pass



    def ReconstructionFBP(self):

        gs=GridSpec(1,3)
        self.fig.clf()
        self.axes1 = self.fig.add_subplot(gs[0,1:3],sharey=None,sharex=None)
        self.axes2 = self.fig.add_subplot(gs[0,0],sharey=None,sharex=None)

        self.axes1.patch.set_alpha(0)
        self.axes2.patch.set_alpha(0)
        filename=str(self.FBP_filedir)
        try:
            sinogram = np.loadtxt(filename)
        except:
            sinogram = imread(filename, as_grey=True)




        sinogram=np.array(sinogram)#,dtype=np.uint8)
        #sinogram = median_filter(sinogram, size=2)
        #sinogram=self.interpSinogram(sinogram)

        try:
            with open(str(self.FBP_filepath)+"/parameters.txt", "r") as ins:
                for line in ins:
                    line=line.replace('=', ' ')
                    line=line.split()
                    if line[0]=='topStep':
                        topStep=float(line[1])
                    if line[0]=='botStep':
                        botStep=float(line[1])
                    if line[0]=='topAng':
                        topAng=float(line[1])

                sMin=math.sin(math.radians(topStep))*self.distanceCrystals/2
                rangeDistance=2*math.sin(math.radians(topAng/2))*self.distanceCrystals/2
                #print("TopAng = "+str(topAng))
                #print("Range distance = "+str(rangeDistance))
            height, width = sinogram.shape
            nRange=height
            Image_output_size=int(math.ceil(self.distanceCrystals*self.pixelSize_per_mm))
            nRangeNew=int(math.ceil(Image_output_size*rangeDistance/self.distanceCrystals));
            sNew=nRange*sMin/nRangeNew
            sinogram=scipy.misc.imresize(sinogram,[nRangeNew,360], interp='bicubic')


            height, width = sinogram.shape
        except:
            height, width = sinogram.shape
            nRange=height
            Image_output_size=int(math.ceil(self.distanceCrystals*self.pixelSize_per_mm))
            nRangeNew=int(math.ceil(Image_output_size));
            sNew=nRange*(self.distanceCrystals/nRange)/nRangeNew
            sinogram=scipy.misc.imresize(sinogram,[nRangeNew,360], interp='bicubic')
            height, width = sinogram.shape
            #Image_output_size=height
            pass





        #print("Sinogram dimensions are = "+str(height)+"x"+str(width))
        theta = np.linspace(0., 360.,width, endpoint=False)


        sinogram = gaussian(sinogram,  sigma=self.gaussFilter, mode='nearest',
                            cval=0, multichannel=None)
        if self.filter=="None":
            self.filter=None
        self.reconstruction_fbp = iradon(sinogram, theta=theta, circle=True,
                                    filter=self.filter, interpolation=self.interp,
                                    output_size=Image_output_size)
        #self.axes1 = self.fig.add_subplot(211,sharex=False, sharey=False)

        #ax1.imshow(sinogram,cmap=plt.cm.Greys_r)

        img1=self.axes1.imshow(self.reconstruction_fbp,cmap=plt.get_cmap(self.cmapname))#,vmin=0, vmax=1e-3)
        self.sinogram=scipy.ndimage.rotate(sinogram, 90.)
        img2=self.axes2.imshow(self.sinogram,cmap=plt.get_cmap(self.cmapname),aspect='auto')#,vmin=0, vmax=1)
        #self.axes1.set_xlim([0,height])
        #self.axes2.set_xlim([0,width])
        self.axes1.autoscale(enable=True, axis='both', tight=True)
        self.axes2.autoscale(enable=True, axis='both', tight=True)
        #self.axes1.axis('off')
        #self.axes2.axis('off')
        self.cbar1 = plt.colorbar(img1, ax=self.axes1)
        self.cbar1 = DraggableColorbar.DraggableColorbar(self.cbar1,img1)
        self.cbar1.connect()

        self.cbar2 = plt.colorbar(img2, ax=self.axes2)
        self.cbar2 = DraggableColorbar.DraggableColorbar(self.cbar2,img2)
        self.cbar2.connect()

        self.fig.canvas.draw()



    def remove_SourceListFile(self):
        for SelectedItem in self.SourcesList_listWidget.selectedItems():
            self.SourcesList_listWidget.removeRow(self.SourcesList_listWidget.row(SelectedItem))
        rowPosition=self.SourcesList_listWidget.rowCount()
        if rowPosition==0:
            self.startButtonDisable()
            
    def outputSimulationFile(self):
        self.OutputSimulationDirStr = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.SelectSimulationOutput_lineEdit.setText(self.OutputSimulationDirStr)
        self.outputSimulationSelected = True


    def browse_AnalysisFile(self):
        try:
            self.SelectResults_lineEdit.clear() # In case there are any existing elements in the list
            #filename=QtGui.QFileDialog.getSaveFileName(self, 'Open File')

            self.Resultsfilename=QtGui.QFileDialog.getOpenFileName(self, 'Open File','' ,'ROOT files (*.root)')
            self.SelectResultsString = self.Resultsfilename

            self.Resultsfilename=self.Resultsfilename.split("/")[-2]
            self.SelectResults_lineEdit.setText(self.Resultsfilename)
            self.resultsSelected = True
            self.startButtonEnable()
        except:
            pass

    def myButtonSlot(self):
        self.otherclass.method()
        

    def handleValueUpdated(self, value):
        self.progressBar.setValue(value)
        QtGui.qApp.processEvents()
        
    def handleProgress(self,value, row):#row
        try:
            self.RunningSimulation_tableWidget.setItem(row, 1, QtGui.QTableWidgetItem(str(value))) #added/changed - pathname to outputfilesdirect
            item = self.RunningSimulation_tableWidget.itemAt(row, 1)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
        except:
            pass
        QtGui.qApp.processEvents()

        # Execute browse_folder function


    def unlockAbortButton_Fnc(self):
        self.abortSimulation_Button.setEnabled(True)

    def abortSimulation_Fnc(self):
	#self.OutputSimulationDirStr = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")) #added
        simulationToAbort=str(self.RunningSimulation_tableWidget.currentItem().text()).split('/')[-1]
        #print(self.processes)
        #print("Pid="+self.processes[simulationToAbort])
        #self.RunningSimulation_tableWidget.takeItem(self.RunningSimulation_tableWidget.currentRow())
        print(simulationToAbort)
        print(self.processes)
        self.processes_stat[simulationToAbort]=False
	#pathJobSplitOut = str(self.OutputSimulationDirStr)+'/'+str(self.processes_dir.keys()[0])+'/easyPET_jobsplit.out'
        if self.clusterBool:
            pathJobSplitOut = str(simulationToAbort)+'/easyPET_jobsplit.out'
            print(pathJobSplitOut)
            jobSplitOut = open(pathJobSplitOut, 'r')
            for line in jobSplitOut.readlines():
                os.system('qdel '+str(line))
        else:
            processToKill=int(self.processes[simulationToAbort])
            print('Ill kill process '+str(processToKill))
            os.system('kill -9 '+str(processToKill))
            
        self.RunningSimulation_tableWidget.removeRow(self.RunningSimulation_tableWidget.currentRow())

        #os.system('rm -r '+str(self.processes_dir[simulationToAbort]))






    def startSimulationParametersFnc(self):
        self.SimulationThread = GenericThread(self.startSimulationParametersFnc_thread)
        self.SimulationThread.start()

    def startSimulationParametersFnc_thread(self):


        data=datetime.datetime.now()
        numberOfTurns=self.NumberOfTurns_spinBox.value()
        acqTime=self.TimeLor_doubleSpinBox.value()/1000
        topStep=float(str(self.TopAng_comboBox.currentText()))
        topAng=self.TopRange_comboBox.currentText()
        botStep=float(str(self.BotAng_comboBox.currentText()))
        #sourceFileDir=self.filename

        self.StartSimulation_pushButton.setEnabled(False)
#	clusterBool=self.cluster_checkBox.checkState() - add checkBox to GUI

 #       QtGui.QApplication.processEvents()
 #       self.disableInputs()

        pathName=str(data.day)+'-'+str(data.strftime("%B"))+'-'+str(data.year)+'_'+str(data.hour)+'h'+str(data.minute)+'_'+str(numberOfTurns)+'turn_'+str(int(math.modf(acqTime)[1]))+'p'+str(math.modf(acqTime)[0])[2:]+'s_'+str(int(math.modf(botStep)[1]))+'p'+str("%.2f" % math.modf(botStep)[0])[2:]+'bot_'+str(int(math.modf(topStep)[1]))+'p'+str("%.2f" % math.modf(topStep)[0])[2:]+'top_range'+str(topAng)

        #pathName=pathName[:-4]

        #OutputFilesDirectory = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', '.', QtGui.QFileDialog.ShowDirsOnly)
        #str(QtGui.QFileDialog.getExistingDirectory(self, "Select directory to save acquisition"))
        #print(OutputFilesDirectory)
        #OutputFilesDirectory=os.getcwd()+'/'+pathName[0:-4] #to remove extension i.e. .mac
        OutputFilesDirectory=self.OutputSimulationDirStr+'/'+pathName
        #OutputFilesDirectory=OutputFilesDirectory+'/'+pathName[0:-4]
        print(OutputFilesDirectory)
        time.sleep(1)
        os.mkdir(OutputFilesDirectory)
        fh=open(OutputFilesDirectory+'/parameters.txt','w')

        #itemsTextList = [str(self.SourcesList_listWidget.item(i).text()) for i in range(self.SourcesList_listWidget.count())]

        fh.write('sliceTime='+str(acqTime*1000)+'\n\
topStep='+str(topStep)+'\n\
topAng='+str(topAng)+'\n\
botStep='+str(botStep)+'\n\
numberOfTurns='+str(numberOfTurns)+'\n')
        index=0
        allRows = self.SourcesList_listWidget.rowCount()
        for row in range(0,allRows):
            item=str(self.SourcesList_listWidget.item(row,0).text())
            x=str(self.SourcesList_listWidget.item(row,1).text())
            y=str(self.SourcesList_listWidget.item(row,2).text())
            z=str(self.SourcesList_listWidget.item(row,3).text())
            #fh.write('Source '+item+' '+str(self.posX[index])+' '+str(self.posY[index])+' '+str(self.posZ[index])+'\n')
            fh.write('Source '+item+' '+str(x)+' '+str(y)+' '+str(z)+'\n')

        fh.close()

        #sourceFileString='X'+str(posX)+'_Y'+str(posY)+'_Z'+str(posZ)+'_'+sourceFileDir


        subprocess.call(["python","DependentFiles/easyPET.py",str(OutputFilesDirectory)] , stdout = open(str(OutputFilesDirectory)+"/easyPET_auxiliar.out",'w'), stderr = open(str(OutputFilesDirectory)+"/easyPET_auxiliar.err",'w'))
        print("Begin of simulation")
        
        rowPosition=self.RunningSimulation_tableWidget.rowCount()
        self.RunningSimulation_tableWidget.insertRow(rowPosition) #added/changed - pathname to outputfilesdirectory
        self.RunningSimulation_tableWidget.setItem(rowPosition, 0, QtGui.QTableWidgetItem(OutputFilesDirectory)) #added/changed - pathname to outputfilesdirectory 

        self.progressclass.valueUpdated.emit(0, rowPosition)
        self.Simulationname_lineEdit.setText(pathName)

        ExampleGUIApp.progressBarRunning=False

        self.StartSimulation_pushButton.setEnabled(True)


        #      self.enableInputs()
        ########
        #	started changing in 05/01/2018 - add clusterBool (always True??)
        #					- p=psubprocess if clusterBool =False
        #					- jobsplitter if clusterBool =True (end this part)
        #					- p.pid = -99999
        #					- add checkBox for clusterBool (added line in the beginning of this function)
        #					- no dropbox related code implemented in this version
        #					- need changes where any of the cluster-related variables are mentioned
        clusterBool = self.clusterBool

        if not clusterBool:
            p=subprocess.Popen(["Gate "+str(OutputFilesDirectory)+"/easyPET.mac"],stdout = open(str(OutputFilesDirectory)+'/easyPETSimulationGate.out','w'),stderr = open(str(OutputFilesDirectory)+'/easyPETSimulationGate.err','w'),shell=True, executable='/bin/bash')
        else:
            p=subprocess.Popen(["python","jobSplitter_easyPET.py",str(OutputFilesDirectory)+'/easyPET.mac'] ,stdout = open(str(OutputFilesDirectory)+"/easyPET_jobsplit.out",'w'), stderr = open(str(OutputFilesDirectory)+"/easyPET_jobsplit.err",'w'))
        if clusterBool:
            p.pid = -99999
        self.processes[str(pathName)] = str(p.pid)
        self.processes_stat[str(pathName)] = True
        self.processes_dir[str(pathName)] = pathName
        print(self.processes)

        isRunning=True
        #pid = p.pid
        #
        init_time = time.time()
        self.progressclass.valueUpdated.emit(0,rowPosition )

        current_slice = 0
        nSlices = 1
        simulation_finished = False
        
        while not os.path.exists(str(OutputFilesDirectory)+'/easyPETSimulationGate.out'):
            time.sleep(1)
        time.sleep(1)
        try:
            output = subprocess.check_output(['head','-400',str(OutputFilesDirectory)+'/easyPETSimulationGate.out']).decode('ascii')
        except subprocess.CalledProcessError as e:
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        
        for line in output.splitlines():
            if "[Acquisition-0] Simulation will have  = " in line:
                print(line)
                temp_string = line.split(" = ")[1]
                nSlices = temp_string.split(" ")[0]
                
        if not clusterBool:
            currentSlice = 0
            while is_running(p.pid) and not simulation_finished:
                try:
                    copyfile(str(OutputFilesDirectory)+'/easyPETSimulationGate.out',str(OutputFilesDirectory)+'/out_temp')
                    output_lines = tail(str(OutputFilesDirectory)+'/out_temp', 30)
                    for line in output_lines:
                        if "[Acquisition-0] Slice" in line:
                            #print(line)
                            currentSlice = line.split()[2]
                        elif "[Core-0] End of macro" in line:
                            print("Found -End of Macro-")
                            os.system('kill -9 '+str(p.pid))
                            simulation_finished = True
                    os.remove(str(OutputFilesDirectory)+'/out_temp')                    
                    percentage = 100 * int(currentSlice)/int(nSlices)
                    self.progressclass.valueUpdated.emit(percentage, rowPosition)
                except subprocess.CalledProcessError as e:
                    raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                    print('Ended')

                
        if (self.processes_stat[str(pathName)] is True):
            print(pathName)
            print(str(pathName))
            remove_selected_item=self.RunningSimulation_tableWidget.findItems(str(pathName),QtCore.Qt.MatchContains)    
            for item in remove_selected_item:
                self.RunningSimulation_tableWidget.removeRow(self.RunningSimulation_tableWidget.row(item))
            del self.processes[str(pathName)]
            del self.processes_stat[str(pathName)]


    def analyse_openMP(self):
        if str(self.SelectResultsString[-5:])==".root":
            pathName=self.SelectResultsString
        else:
            self.browse_AnalysisFile()
            pathName=self.SelectResultsString
        time_window=float(str(self.CoincidenceWindow_doubleSpinBox.value()))
        scannerType=1

        ##added - merge root files
        #print('###########\n###########\n###########\n'+pathName+'###########\n###########\n###########\n')
        path2file = os.path.dirname(os.path.realpath(str(pathName)))
        self.SelectResultsString = str(path2file+'/easyPET_total.root')
        rootFilesList = [f for f in os.listdir(path2file) if f.endswith('.root')]
        #next two def are meant to test if hadd needs the files to be in angular order, hence the sorting
        def atoi(text):
            return int(text) if text.isdigit() else text
        def natural_keys(text):
            return [ atoi(c) for c in re.split('(\d+)', text) ]
        if 'easyPET_total.root' not in rootFilesList:
            rootFilesList.sort(key=natural_keys)
            mergeStr = 'hadd easyPET_total.root'
            for f in rootFilesList:
                mergeStr += str(' '+path2file+'/'+f)
                print(mergeStr)
                os.system(mergeStr)
            os.system('mv easyPET_total.root '+str(path2file))
        pathName = self.SelectResultsString
        
## ended - lack .sino and .energy paths - it fetches the path created by the file originally selected
			

        os.system('./easyPET_edugate_analyser '+str(pathName)+' '+str(time_window)+' '+str(scannerType)+' '+str(self.energy_threshold_lower)+' '+str(self.energy_threshold_upper))
        self.EnergyPlot()
        try:
            self.FBP_filedir=str(self.SelectResultsString[:-5]+'.sinogram')
            self.FBP_filepath = self.FBP_filepath = os.path.dirname(str(self.FBP_filedir))
            #print("Path is "+FBP_filepath)
            self.ReconstructionFBP()
            self.saveFigures_pushButton.setEnabled(True)
        except Exception as e:
            print(e)
            pass


#        directory = QtGui.QFileDialog.getExistingDirectory(self,
#                                                           "Pick a folder")
        # execute getExistingDirectory dialog and set the directory variable to be equal
        # to the user selected directory

        #if directory: # if user didn't pick a directory don't continue
        #    for file_name in os.listdir(directory): # for all files, if any, in the directory
        #        self.listWidget.addItem(file_name)  # add file to the listWidget


class GenericThread(QtCore.QThread):
    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def run(self):
        self.function(*self.args, **self.kwargs)
        return


def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyle('cleanlooks')
#this avoids the error  Gtk-CRITICAL **: IA__gtk_widget_get_direction: assertion 'GTK_IS_WIDGET (widget)' failed".
#and the terminal looks nice
    form = ExampleGUIApp()
    form.show()
    app.exec_()




if __name__ == '__main__':
    main()
