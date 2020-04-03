#include <iostream>
#include <fstream>
#include <string>
#include "libpipeLBM.h"

#define _PATH_TO_INIT_ "/home/thibault/transition_hdd/thibault/These/lbm_code/seq/draft/run_for_pops/populations/pops_1.datout"

using namespace std;

int main(int argc, char* argv[])
{
  int Dx = 513; int Dy = 129;
  int N = 2000;
  pipeLBM *myLB = new pipeLBM(Dx, Dy);
  myLB->setInletBC("poiseuille");
  myLB->setOutletBC("open");
  
  int spongeStart = (int) 3*(Dx-1)/4+1;
  int R = (Dy-1)/16; int x0 = (Dx-1)/16;
  int L = 16; int xsq = (Dx-1)/2; int ysq = (Dy-1)/2 - L/2;
  double U0 = 0.05; double tau = 0.501; double F0 = 0.0;
				    
  myLB->setSpongeLayer(spongeStart, Dx);
  myLB->setParameters(tau, U0, F0);

  Obstacle* obs[2];
  squareObstacle mySquare(xsq, ysq, L);
  obs[0] = new Grid(x0, R, Dy);
  //  obs[1] = new squareObstacle(xsq, ysq, L);
  obs[1] = &mySquare;
  myLB->setObstacles(obs, 2);
  string path_to_file=_PATH_TO_INIT_;
  bool errFlag;
  errFlag = myLB->initFromFile(path_to_file);
  if(errFlag){cout << "PB with init" << endl;}

  double *fd = new double[N];
  // double *viscousRear = new double[N];
  // double *viscousTop = new double[N];
  // double *viscousFront = new double[N];
  // double *viscousBot = new double[N];
  // double *pRear = new double[N];
  // double *pFront = new double[N];
  // double *shearBotVec = new double[N];
  // double *shearTopVec = new double[N];
  double *meanTransVelocityVec = new double[N];
  double shearTop = 0, shearBot=0, meanTransVelocity=0;
  int k = 0;
  int kk=0;
  for (int t=0;t<N;t++)
    {
      myLB->displayPercentage(t,N);
      myLB->computeStress(obs[1]);
      fd[t] = obs[1]->getDrag();
      if(t%400==0)
      	{
      	  myLB->writeSnapshot();
	  //myLB->writeVTK(k);
      	  k++;
      	}
      // shearTop = 0.0;
      // shearBot = 0.0;
      // for(int x=xsq;x<xsq+L+1;x++)
      // 	{
      // 	  shearTop += myLB->getLongVelocityAtPoint(x,ysq+L+1);
      // 	  shearBot += myLB->getLongVelocityAtPoint(x,ysq-1);
      // 	}
      // shearTop /= (L+1);
      // shearBot /= (L+1);
      // shearTopVec[t] = shearTop;
      // shearBotVec[t] = shearBot;
      // myLB->computeStress(obs[1]);
      // fd[t] = obs[1]->getDrag();
      // viscousTop[t] = mySquare.getViscousTop();
      // viscousBot[t] = mySquare.getViscousBot();
      // viscousFront[t] = mySquare.getViscousFront();
      // viscousRear[t] = mySquare.getViscousRear();
      // pFront[t] = mySquare.getpFront();
      // pRear[t] = mySquare.getpRear();
      // meanTransVelocity = 0.0;
      // kk = 0;
      // for(int x=xsq+3+L;x<xsq+7+L;x++)
      // 	{
      // 	  for(int y=ysq;y<ysq+L+1;y++)
      // 	    {
      // 	      meanTransVelocity += myLB->getTransVelocityAtPoint(x,y);
      // 	      kk++;
      // 	    }
      // 	}
      // meanTransVelocityVec[t] = meanTransVelocity/kk;;
      myLB->advanceOneTimestep(obs, 2);
    }
  ofstream outputFile;
  outputFile.open("data_force.datout", ios::binary);
  outputFile.write((char*)&fd[0], N*sizeof(double));
  outputFile.close();
  // outputFile.open("viscousTop.dat", ios::binary);
  // outputFile.write((char*)&viscousTop[0], N*sizeof(double));
  // outputFile.close();
  // outputFile.open("viscousBot.dat", ios::binary);
  // outputFile.write((char*)&viscousBot[0], N*sizeof(double));
  // outputFile.close();
  // outputFile.open("viscousRear.dat", ios::binary);
  // outputFile.write((char*)&viscousRear[0], N*sizeof(double));
  // outputFile.close();
  // outputFile.open("viscousFront.dat", ios::binary);
  // outputFile.write((char*)&viscousFront[0], N*sizeof(double));
  // outputFile.close();
  // outputFile.open("pFront.dat", ios::binary);
  // outputFile.write((char*)&pFront[0], N*sizeof(double));
  // outputFile.close();
  // outputFile.open("pRear.dat", ios::binary);
  // outputFile.write((char*)&pRear[0], N*sizeof(double));
  // outputFile.close();
  // outputFile.open("shearTop.dat", ios::binary);
  // outputFile.write((char*)&shearTopVec[0], N*sizeof(double));
  // outputFile.close();
  // outputFile.open("shearBot.dat", ios::binary);
  // outputFile.write((char*)&shearBotVec[0], N*sizeof(double));
  // outputFile.close();
  // outputFile.open("meanTransVelocity.dat", ios::binary);
  // outputFile.write((char*)&meanTransVelocityVec[0], N*sizeof(double));
  // outputFile.close();

  // delete[] shearBotVec;
  // delete[] shearTopVec;
  // delete[] viscousTop;
  // delete[] viscousBot;
  // delete[] viscousRear;
  // delete[] viscousFront;
  // delete[] pFront;
  // delete[] pRear;
  delete[] fd;
  delete[] meanTransVelocityVec;
  delete myLB;
}
