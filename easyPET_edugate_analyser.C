#include <cstring>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <TCanvas.h>
#include <TH3F.h>
#include <TH2F.h>
#include <TH1F.h>
#include <TTree.h>
#include <TLatex.h>
#include <TFile.h>
#include <TStyle.h>
#include "TSystem.h"
#include "TApplication.h"
#include "TROOT.h"
#include <time.h>
#include <algorithm>
#include <iterator>
#include <math.h>
#include <set>
#include <functional>
#include <array>


// to compile
//g++ -o easyPET_edugate_analyser easyPET_edugate_analyser.C `root-config --cflags --libs` -O3 -std=c++0x
// to run
//./easyPET_edugate_analyser "rootFileName" CoincidenceTimeWindow(ns) ScannerType(default = 1)
//./easyPET_edugate_analyser "rootFileName" 10 1
using namespace std;

bool UseOpenMP=false;
float CrystalSize;// = 0.2; //2.0 or 2.1mm, considering the white painting layer
float distanceCrystals;// = 5.77; //5.77 cm

vector<string> split(string str, char delimiter) {
  vector<string> internal;
  stringstream ss(str); // Turn the string into a stream.
  string tok;

  while(getline(ss, tok, delimiter)) {
    internal.push_back(tok);
  }

  return internal;
}

double constrainAngle(double x){
  x = fmod(x,360);
  if (x < 0)
  x += 360;
  return x;
}

std::vector<float> Ang2Cartesian(float AngBot, float AngTop){
  std::vector<float>output(2);

  float x1, x2, y1, y2;
  x1=(distanceCrystals/2)*cos( AngBot * M_PI / 180.0);
  y1=(distanceCrystals/2)*sin( AngBot * M_PI / 180.0);
  //cout<<"AngBot= "<<AngBot<< " AngTop= "<< AngTop<< "X 1= "<<positions[0]<< " Y1="<<positions[0]<<endl;

  float R[2][2];
  float m, b;
  float distance;
  float s, phi;
  std::vector<float> T(2);
  R[0][0]=cos( AngTop * M_PI / 180.0);
  R[0][1]=sin( AngTop * M_PI / 180.0);
  R[1][0]=-sin( AngTop * M_PI / 180.0);
  R[1][1]=cos( AngTop * M_PI / 180.0);

  //cout<<"R[0][0]=" <<R[0][0]<< " R[0][1]=" <<R[0][1]<<" R[1][0]=" <<R[1][0]<<" R[1][1]=" <<R[1][1]<<endl;

  T[0]=x1;
  T[1]=y1;

  x2=(-2*(R[0][0]*x1+R[0][1]*y1))+T[0];
  y2=(-2*(R[1][0]*x1+R[1][1]*y1))+T[1];

  m = (y1-y2)/(x1-x2);
  b = y2-(m*x2);
  output[0]=m;
  output[1]=b;
  //cout<<"m "<<m<< " b "<<b<<endl;
  return output;
}
std::vector<float> Ang2Sino(float AngBot, float AngTop){
  std::vector<float>output(2);
  std::vector<float>line(2);
  float m, b;
  float s, phi;


  line=Ang2Cartesian(AngBot, AngTop);
  m = line[0];//(y1-y2)/(x1-x2);
  b = line[1];//y2-(m*x2);

  AngTop=round(AngTop*1e5)/1e5;
  AngBot=round(AngBot*1e5)/1e5;

  s=(sin(AngTop * M_PI / 180.0 ))*(distanceCrystals/2);
  s=round(s*1e6)/1e6;
  output[0]=s;

  //if (AngTop<=0.){
  phi=90.+AngBot-AngTop;
  //}
  //  else{
  //  phi=270.+AngBot-AngTop;
  //}
  phi=constrainAngle(phi);
  phi=round(phi*1e4)/1e4;
  //phi=constrainAngle(phi);
  output[1]=phi;

  //  cout<<AngTop<<" "<<AngBot<<" "<<s<< " " <<phi<<endl;

  return output;


}


int getIndex(double valueToFind, std::vector<double> *indexesVector){

  int index = 0;
  int size = indexesVector->size();

  for(int i = 0; i < size; i++){
    if(TMath::Abs(indexesVector->at(i)-valueToFind) <= TMath::Abs(indexesVector->at(index)-valueToFind)){
      index = i;
    }
  }

  return index;

  //index=std::find(indexesVector->begin(), indexesVector->end(), valueToFind) -indexesVector->begin();

  //return index;

}

double getStep(std::vector<double> *angleVector){
  double t_prev=angleVector->at(0);
  //cout<<"t_prev = " << t_prev<<endl;
  double t;
  double step;
  double stepMin=1e3;
  int size = angleVector->size();
  //cout<<"Size is "<<size<<endl;
  for (int j = 0; j < size; j++){

    t=angleVector->at(j);
    if (j>0) t_prev=angleVector->at(j-1);
    //cout<<"t is "<<t<<endl;
    if (TMath::Abs(t-t_prev)>1e-1) {
      step=(TMath::Abs(t-t_prev));
      //  cout<<"step is "<<step<<endl;
      if (TMath::Abs(step)<=stepMin) stepMin=step;

    }
  }
  cout<<"StepMin is "<<stepMin<<endl;
  return stepMin;
}



void ReadPositionsFiles(const char *PositionFile1, std::vector<double> *Rotation, std::vector<double> *TimeVector, std::vector<double> *PositionX, std::vector<double> *PositionY, std::vector<double> *PositionZ){
  std::ifstream file(PositionFile1);

  std::string line;
  double instant=0;
  double rotationAngle=0;
  double rotationX=0;
  double rotationY=0;
  double rotationZ=0;
  double translationX=0;
  double translationY=0;
  double translationZ=0;
  while (std::getline(file,line)){
    std::istringstream iss(line);
    if(iss>> instant >> rotationAngle >> rotationX >> rotationY >> rotationZ >> translationX >> translationY >> translationZ){
      iss>> instant >> rotationAngle >> rotationX >> rotationY >> rotationZ >> translationX >> translationY >> translationZ;
      TimeVector->push_back(instant);
      PositionX->push_back(translationX);
      PositionY->push_back(translationY);
      PositionZ->push_back(translationZ);

      Rotation->push_back(rotationAngle);
    }

  }


}


void CoincidenceToLOR(std::vector<double> *LOR1Vect, std::vector<double> *LOR2Vect, std::vector<double> *LOR3Vect, std::vector<double> *TimeVector, Double_t time_instant, std::vector<double> *TopAngVector, std::vector<double> *BotAngVector, std::vector<double>*CoincBotAng, std::vector<double>*CoincTopAng){

  std::vector<double>::iterator it;
  unsigned index=0;
  Double_t topAng=0;
  Double_t botAng=0;
  for (it = TimeVector->begin(); it < TimeVector->end(); it++){
    if( time_instant > *(it)  && time_instant <= *(it+1)){
      LOR3Vect->at(index)++;
      CoincTopAng->push_back(LOR2Vect->at(index));
      CoincBotAng->push_back((-1)*LOR1Vect->at(index));


    }
    index++;
    //it++;
    //return angles;
  }

}

void easyPETScannerType( int value){
  //to choose easyPETScannerType
  //if 1, then easyPET-edu

  if (value==1){
    CrystalSize = 0.2; //in mm, considering the white painting layer
    distanceCrystals = 5.77; //5.77 cm
  }
  else {
    CrystalSize = 0.2; //in mm, considering the white painting layer
    distanceCrystals = 6.0; //5.77 cm
  }
}

int main(int argc, char** argv) {

  time_t tstart, tend;
  double dif;
  time(&tstart);
  clock_t start, end = 0;
  double cpuTime = 0;
  start = clock();

  char rootFileDir[1000]="";
  std::strcpy(rootFileDir,argv[1]);
  cout<<rootFileDir<<endl;
  Double_t coincidenceWindowValue;
  coincidenceWindowValue=std::atof(argv[2]);
  Int_t easyPETScannerTypeValue;
  easyPETScannerTypeValue=std::atoi(argv[3]);

  easyPETScannerType(easyPETScannerTypeValue);

  Double_t energy_threshold_lower;
  energy_threshold_lower=std::atof(argv[4])/1000;
  Double_t energy_threshold_upper;
  energy_threshold_upper=std::atof(argv[5])/1000;

  //  chdir(rootFileDir);
  TApplication app("ROOT Application", &argc, argv);
  //TApplication allways after the parameter argv load, like   std::strcpy(rootFileDir,argv[1]);


  std::string mycwd(getenv("PWD"));
  std::cout << "Current Directory: " << mycwd << std::endl;

  char rootFileName[1000]="";
  std::strcpy(rootFileName,rootFileDir);
  //std::strcat(rootFileName,"/easyPET.root");
  //std::cout<<"RootFileName = "<<rootFileName<<endl;

  string CoincidencesDir  = rootFileDir;
  string CoincidencesDirWithoutExtension = CoincidencesDir.substr(0, CoincidencesDir.rfind("."));
  string ResultsDirectory = CoincidencesDir.substr(0, CoincidencesDir.rfind("/"));


  char CoincidencesFileDir[1000]="";
  std::strcpy(CoincidencesFileDir, CoincidencesDirWithoutExtension.c_str());
  std::strcat(CoincidencesFileDir,".dat");

  char ParametersFileDir[1000]="";
  std::strcpy(ParametersFileDir, ResultsDirectory.c_str());
  std::strcat(ParametersFileDir,"/parameters.txt");


  char RacioFileDir[1000]="";
  std::strcpy(RacioFileDir, ResultsDirectory.c_str());
  std::strcat(RacioFileDir,"/Racio.dat");
  //std::cout<<"RacioFilesDir = "<<RacioFileDir<<endl;


  char EnergyFileDir[1000]="";
  std::strcpy(EnergyFileDir, CoincidencesDirWithoutExtension.c_str());
  std::strcat(EnergyFileDir,".energy");

  char ListModeFileDir[1000]="";
  std::strcpy(ListModeFileDir, ResultsDirectory.c_str());
  std::strcat(ListModeFileDir,"/ListMode.dat");

  char ProjectionsFileDir[1000]="";
  std::strcpy(ProjectionsFileDir, CoincidencesDirWithoutExtension.c_str());
  std::strcat(ProjectionsFileDir,".sinogram");


  char positionsDir[1000]="";

  std::strcpy(positionsDir, ResultsDirectory.c_str());
  std::strcat(positionsDir,"/positions.mac");
  //std::cout<<"PositionsDir = "<<positionsDir<<endl;

  char positionsScanner1Dir[1000]="";
  std::strcpy(positionsScanner1Dir, ResultsDirectory.c_str());
  std::strcat(positionsScanner1Dir,"/positionsScanner1.mac");

  char positionsScanner2Dir[1000]="";
  std::strcpy(positionsScanner2Dir, ResultsDirectory.c_str());
  std::strcat(positionsScanner2Dir,"/positionsScanner2.mac");


  float ndecays=1;

  std::vector<double> LOR1;
  std::vector<double> LOR2;
  std::vector<double> LOR3;
  std::vector<double> timeVect;
  std::vector<double> timeVectBot;
  std::vector<double> PositionX1;
  std::vector<double> PositionY1;
  std::vector<double> PositionZ1;
  std::vector<double> PositionX1Bot;
  std::vector<double> PositionY1Bot;
  std::vector<double> PositionZ1Bot;
  std::vector<double> PositionX2;
  std::vector<double> PositionY2;
  std::vector<double> PositionZ2;
  std::vector<double> RotationAngleTop;
  std::vector<double> RotationAngleBottom;

  std::vector<double> level3ID_1_vector;
  std::vector<double> level3ID_2_vector;


  std::vector<double> Energy1_vector;
  std::vector<double> Energy2_vector;

  std::vector<double> AnglesTop;
  std::vector<double> AnglesBot;


  TFile *f = new TFile(rootFileName);
  TTree *SinglesScanner1 = (TTree*)gDirectory->Get("SinglesScanner1");
  TTree *SinglesScanner2 = (TTree*)gDirectory->Get("SinglesScanner2");

  TH1F *gamma1 = new TH1F("gamma1","",80,0.2,.8);
  TH1F *gamma2 = new TH1F("gamma2","",100,0.2,.8);


  //creation of histo 3 Dim.
  TH3F *position = new TH3F("position","",80,-40,40,80,-40,40,80,-40,40);


  //
  //Declaration of leaves types - TTree Coincidences
  //


  Float_t         globalPosX1;
  Float_t         globalPosX2;
  Float_t         globalPosY1;
  Float_t         globalPosY2;
  Float_t         globalPosZ1;
  Float_t         globalPosZ2;
  Float_t         sourcePosX1;
  Float_t         sourcePosX2;
  Float_t         sourcePosY1;
  Float_t         sourcePosY2;
  Float_t         sourcePosZ1;
  Float_t         sourcePosZ2;
  Double_t         time1;
  Double_t         time2;

  Float_t         energy1;
  Float_t         energy2;

  Int_t           level3ID_1;
  Int_t           level3ID_2;

  //
  //Set branch addresses - TTree Coincicences
  //

  SinglesScanner1->SetBranchAddress("energy",&energy1);
  SinglesScanner2->SetBranchAddress("energy",&energy2);
  SinglesScanner1->SetBranchAddress("globalPosX",&globalPosX1);
  SinglesScanner2->SetBranchAddress("globalPosX",&globalPosX2);
  SinglesScanner1->SetBranchAddress("globalPosY",&globalPosY1);
  SinglesScanner2->SetBranchAddress("globalPosY",&globalPosY2);
  SinglesScanner1->SetBranchAddress("globalPosZ",&globalPosZ1);
  SinglesScanner2->SetBranchAddress("globalPosZ",&globalPosZ2);
  SinglesScanner1->SetBranchAddress("sourcePosX",&sourcePosX1);
  SinglesScanner2->SetBranchAddress("sourcePosX",&sourcePosX2);
  SinglesScanner1->SetBranchAddress("sourcePosY",&sourcePosY1);
  SinglesScanner2->SetBranchAddress("sourcePosY",&sourcePosY2);
  SinglesScanner1->SetBranchAddress("sourcePosZ",&sourcePosZ1);
  SinglesScanner2->SetBranchAddress("sourcePosZ",&sourcePosZ2);
  SinglesScanner1->SetBranchAddress("time",&time1);
  SinglesScanner2->SetBranchAddress("time",&time2);
  SinglesScanner1->SetBranchAddress("level3ID",&level3ID_1);
  SinglesScanner2->SetBranchAddress("level3ID",&level3ID_2);

  Int_t nentriesScanner1 = SinglesScanner1->GetEntries();
  Int_t nentriesScanner2 = SinglesScanner2->GetEntries();

  //cout<<" nentries in Scanner1:   "<<  nentriesScanner1 <<endl;
  //cout<<" nentries in Scanner2:   "<<  nentriesScanner2 <<endl;

  ReadPositionsFiles(positionsDir, &RotationAngleTop, &timeVect, &PositionX1, &PositionY1, &PositionZ1);

  for (std::vector<double>::iterator it = RotationAngleTop.begin(); it != RotationAngleTop.end(); it++){

    LOR2.push_back(*it);
    LOR3.push_back(0);

  }

  ReadPositionsFiles(positionsScanner1Dir, &RotationAngleBottom, &timeVectBot, &PositionX1Bot, &PositionY1Bot, &PositionZ1Bot);

  for (std::vector<double>::iterator it2 = RotationAngleBottom.begin(); it2 != RotationAngleBottom.end(); it2++){

    LOR1.push_back(*it2);

  }

  //
  //loop on the events in the TTree Coincidences
  //

  Float_t Nbr_Coinc_Prompt = 0. ;
  Float_t Nbr_Coinc_Random = 0. ;
  Float_t Nbr_Coinc_Scatter = 0. ;
  Float_t Nbr_Coinc_Trues = 0. ;
  Double_t CoincidenceWindow=coincidenceWindowValue*1e-9*1e11; // its *1e11 to go for picosecond resolution

  std::ofstream CoincidencesFile;
  //cout<<CoincidencesFileDir<<endl;
  CoincidencesFile.open(CoincidencesFileDir);

  std::vector<Double_t> Scanner1Vector(nentriesScanner1);
  std::vector<Double_t> Scanner2Vector(nentriesScanner2);

  Int_t nentries_max;
  nentries_max=max(nentriesScanner1,nentriesScanner2);
  std::vector<Double_t> Scanner3Vector(nentries_max);
  for (int i = 0 ; i < nentriesScanner1 ; i++){
    SinglesScanner1->GetEntry(i);
    Scanner1Vector[i]=round(time1*1e11);

  }
  for (int j = 0 ; j < nentriesScanner2 ; j++){
    SinglesScanner2->GetEntry(j);
    Scanner2Vector[j]=round(time2*1e11);

  }

  int j_last=0;
  int j=0;
  int coincidences=0;
  SinglesScanner1->GetEntry(0);
  SinglesScanner2->GetEntry(0);
  std::vector<float> angles(2);

  for (int i = 0;i<nentriesScanner1; i++){
    Double_t time_1=Scanner1Vector[i];
    if (true){//energy1>0.25 && energy1<0.85){
      j=j_last;
      Double_t time_2=Scanner2Vector[j];
      //#pragma omp parallel for
      //for (j = j_last ; j<nentriesScanner2; j++){
      //while (time_2<time_1+2000e-9 && j<nentriesScanner2){
      while (time_2<time_1+2000e-9*1e11 && j<nentriesScanner2){
        time_2=Scanner2Vector[j];
        if (time_2<time_1-2000e-9*1e11){
          j++;
          j_last=j;
          continue;
        }
        if(TMath::Abs(time_1-time_2)<CoincidenceWindow ){

          j_last=j;

          //cout<<j_last;
          //cout<<TMath::Abs(time1-time2)<<endl;
          //cout<<"Coincidence between instant "<<time_1*1e-11<<"s and "<<time_2*1e-11<<"s in positions ("<<globalPosX1<<","<<globalPosY1<<","<<globalPosZ1<<") and ("<<globalPosX2<<","<<globalPosY2<<","<<globalPosZ2<<")"<<endl;
          SinglesScanner1->GetEntry(i);
          SinglesScanner2->GetEntry(j);
          if (energy2>energy_threshold_lower && energy2<energy_threshold_upper && energy1>energy_threshold_lower && energy1<energy_threshold_upper){
            //std::cout<<"time "<<time1<<" and energy "<<energy1<< " and limit "<<energy_threshold_lower <<" "<<energy_threshold_upper<<endl;

          //time_vector.push_back(time1);
          level3ID_1_vector.push_back(level3ID_1);
          level3ID_2_vector.push_back(level3ID_2);
          Energy1_vector.push_back(energy1);
          Energy2_vector.push_back(energy2);
          position->Fill(sourcePosZ1,sourcePosX1,sourcePosY1);
          CoincidenceToLOR(&LOR1, &LOR2, &LOR3, &timeVect, time_1*1e-11,&RotationAngleTop, &RotationAngleBottom, &AnglesBot, &AnglesTop);
          //AnglesBot.push_back(angles.at(0));
          //AnglesTop.push_back(angles.at(1));

          coincidences++;
          break;
        }
        }
        j++;

      }
    }

    //i++;
  }

  cout<<"Number of coincidences "<<coincidences<<endl;


  unsigned index2=0;
  for (std::vector<double>::iterator it = LOR1.begin(); it != LOR1.end(); it++){

    CoincidencesFile<<LOR1.at(index2)<<" "<<LOR2.at(index2)<<" "<<LOR3.at(index2)<<" "<<LOR3.at(index2)<< endl;
    index2++;
  }
  CoincidencesFile.close();



  unsigned index5=0;
  float top_count=0;

  double topAng;//=getStep(&AnglesTop);
  double botAng;//=getStep(&AnglesBot);
  //cout<<"Top Step is "<<topAng<<endl;
  double topRange;

  std::ifstream infile(ParametersFileDir);
  std::string line,token;
  while (std::getline(infile, line))
  {
    std::istringstream iss(line);
    vector<string> sep = split(line, '=');
    if (sep[0]=="topStep") {
      cout<< sep[0]<< " = "<<sep[1]<<endl;
      topAng=stof(sep[1]);
    }
    if (sep[0]=="topAng") {
      cout<< sep[0]<< " = "<<sep[1]<<endl;
      topRange=stof(sep[1]);
    }
    if (sep[0]=="botStep") {
      cout<< sep[0]<< " = "<<sep[1]<<endl;
      botAng=stof(sep[1]);
    }

  }

  int nRays=float(topRange/topAng)+1;
  cout<<"Top range is "<<topRange<<endl;
  cout<<"nRays is "<<nRays<<endl;
  cout<<"distanceCrystals/2 is "<<distanceCrystals/2<<endl;


  //double minS= 2*(sin( (*topRange) * M_PI / 180.0)*distanceCrystals/2)/(nRays-1);
  //cout<<"Min S "<<minS<<endl;

  std::vector<double> raysVector;

  int nProj=float(360./botAng);


  //int nRays=AnglesTop.size();
  int dir = 1;
  cout<<"Number of projections (bottom angles) ="<<nProj<<endl;
  cout<<"Number of rays (top angles) ="<<nRays<<endl;

  /*
  for (std::vector<double>::iterator it = LOR1.begin(); it != LOR1.end(); it++){

  raysVector.push_back(LOR3.at(index5+top_count));
  if (top_count==(nRays-1)){

  if (dir != 1) std::reverse(raysVector.begin(),raysVector.end());
  //for (int k = 0; k < nRays; k++) ProjectionsFile<<raysVector.at(k)<< " ";

  //ProjectionsFile<<endl;
  raysVector.clear();
  index5+=nRays;
  top_count=0;
  dir*=-1;
}

else top_count++;
}
*/

std::ofstream RacioFile;
RacioFile.open(RacioFileDir);

std::ofstream EnergyFile;
EnergyFile.open(EnergyFileDir);

std::ofstream ListModeFile;
ListModeFile.open(ListModeFileDir);
std::vector<float> variables;
unsigned index3=0;

float s, phi;

std::vector<double> sVector;
std::vector<double> phiVector;



//auto topRange=std::max_element(AnglesTop.begin(),AnglesTop.end());
double phiStep= std::min(topAng,botAng);
const int nS=(topRange/topAng)+1;
const int nPhi=(360/phiStep);

// Create the three pads

Double_t w = 1200;
Double_t h = 600;
TCanvas * c2 = new TCanvas("c", "c", w, h);
c2->SetWindowSize(w + (w - c2->GetWw()), h + (h - c2->GetWh()));

c2->Divide(2);

c2->cd(1);


// Create, fill and project a 2D histogram.

TH1F *h4 = new TH1F("S","S",nRays,-0.5, nRays-0.5);
TH1F *h5 = new TH1F("phi","phi",nProj, -0.5 , nProj-0.5);
TH2F *h2 = new TH2F("Sinogram","Sinogram",nRays, -0.5 , nRays-0.5,nPhi,-0.5,nPhi-0.5);
h2->SetStats(0);
int sIndex, phiIndex;

double s_temp=0;
double deltaS=(sin(topAng * M_PI / 180.0)*distanceCrystals/2);
double minS=-(sin((topRange/2) * M_PI / 180.0)*distanceCrystals/2);
cout<<"TopRange = "<<topRange<<endl;
cout<<"TopAng = "<<topAng<<endl;
cout<<"MinS = "<<minS<<endl;
cout<<"nS = "<<nS<<endl;
cout<<"DeltaS = "<<deltaS<<endl;
for (int j = 0; j < nS; j++){
  s_temp=minS+deltaS*j;
  sVector.push_back(s_temp);
}
double phi_temp=0;
for (int j = 0; j < nPhi; j++){
  phi_temp=phiStep*(j);
  phiVector.push_back(phi_temp);

}

index3=0;
for (std::vector<double>::iterator it = level3ID_1_vector.begin(); it != level3ID_1_vector.end(); it++){


  level3ID_2_vector.at(index3);
  variables=Ang2Sino(AnglesBot[index3], AnglesTop[index3]);
  s=variables[0];
  phi=variables[1];
  ListModeFile << s << " " << phi  <<endl;
  RacioFile << level3ID_1_vector.at(index3) <<" "<< level3ID_2_vector.at(index3)<<endl;
  EnergyFile << Energy1_vector.at(index3) <<" "<< Energy2_vector.at(index3)<<endl;
  sIndex=getIndex(s,&sVector)+1;
  phiIndex=getIndex(phi,&phiVector)+1;
  h2->Fill(sIndex,phiIndex);
  h4->Fill(sIndex);
  h5->Fill(phiIndex);
  index3++;
}


// Drawing
c2->cd();
gStyle->SetPalette(1);
h2->Draw("CONT4Z");
c2->Update();


TCanvas * c22 = new TCanvas("c22", "c22", w, h);
c22->SetWindowSize(w + (w - c22->GetWw()), h + (h - c22->GetWh()));

c22->Divide(2);

c22->cd(1);
gStyle->SetPalette(1);
h4->Draw();
c22->cd(2);
gStyle->SetPalette(1);
h5->Draw();
c22->Update();


std::ofstream ProjectionsFile;
ProjectionsFile.open(ProjectionsFileDir);
cout<<"Number of Bins = "<<h2->GetNbinsY()<<endl;

for(Int_t j = 1; j <= h2->GetNbinsX(); j++) {
  for(Int_t i = 1; i <= h2->GetNbinsY(); i++) {
    Int_t bin = h2->GetBin(j,i);
    Float_t value = h2->GetBinContent(bin);
    ProjectionsFile<<value<< " ";
  }
  ProjectionsFile<<endl;
}
ProjectionsFile.close();


//TCanvas *c3;

// c3 = new TCanvas("Rec2D","Rec2D",900,800,500,600);

//c2->cd(2);

TH2D *TwoDRec = new TH2D("Backprojection", "Backprojection", 200, -5, 5, 200, -5,5);
TwoDRec->SetStats(0);


unsigned index4=0;

for (std::vector<double>::iterator it = level3ID_1_vector.begin(); it != level3ID_1_vector.end(); it++){

  variables=Ang2Cartesian(AnglesBot[index4], AnglesTop[index4]);


  Double_t m = variables[0], b = variables[1];
  if (TMath::Abs(m)<1){
    for(Int_t i = 1; i <= TwoDRec->GetNbinsX(); i++) {
      // Double_t x = h->GetXaxis()->GetBinLowEdge(i);
      Double_t x = TwoDRec->GetXaxis()->GetBinCenter(i);
      // Double_t x = h->GetXaxis()->GetBinCenterLog(i);
      // Double_t x = h->GetXaxis()->GetBinUpEdge(i);
      Double_t y = (m * x + b);
      TwoDRec->Fill(x, y);
    }
  }
  else{
    for(Int_t i = 1; i <= TwoDRec->GetNbinsY(); i++) {
      // Double_t x = h->GetXaxis()->GetBinLowEdge(i);
      Double_t y = TwoDRec->GetYaxis()->GetBinCenter(i);
      // Double_t x = h->GetXaxis()->GetBinCenterLog(i);
      // Double_t x = h->GetXaxis()->GetBinUpEdge(i);
      Double_t x = (y - b)/m;
      TwoDRec->Fill(x, y);

    }
  }
  index4++;
}
//TwoDRec->Draw("CONT4");
//c2->Update();

std::sort(sVector.begin(), sVector.end());
std::sort(phiVector.begin(), phiVector.end());

RacioFile.close();
ListModeFile.close();
EnergyFile.close();

TFile *f1 = new TFile("SourcePositions2.root","recreate");
position->Write();
h2->Write();
f1->Close();
 

cout<<"Number of coincidences = "<<coincidences<<endl;

time(&tend);
dif = difftime (tend,tstart);
std::cout << "It took you " << dif << " seconds to finish.\n";

end = clock();
cpuTime = (end-start)/(double)(CLOCKS_PER_SEC);
printf("CPU time = %gs\n", cpuTime);
//app.Run();


}
