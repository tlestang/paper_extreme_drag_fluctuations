#include <iostream>
#include <fstream>
#include <algorithm>
#include <python3.7/Python.h>

#include "libpipeLBM.h"

static PyObject* method_simulate(PyObject *self, PyObject *args){

  char* path_to_init = NULL;
  int tmin;
  int tmax;
  int tvismin;
  int tvismax;
  char* path_to_perturb;

  bool parse_args_error = PyArg_ParseTuple(args, "siiii|s", &path_to_init, &tmin,
					   &tmax, &tvismin, &tvismax, &path_to_perturb);
  if (!parse_args_error)
    return NULL;

  // Setup LBM
  int Dx = 513;
  int Dy = 129;
  int R = (Dy-1)/16;
  int x0 = (Dx-1)/16;
  int L = 16;
  int xsq = (Dx-1)/2;
  int ysq = (Dy-1)/2 - L/2;
  double U0 = 0.05;
  double tau = 0.501;
  int spongeStart = (int) 3*(Dx-1)/4+1;
  double F0 = 0.0;

  pipeLBM *myLB = new pipeLBM(Dx, Dy);
  myLB->setInletBC("poiseuille");
  myLB->setOutletBC("open");
  myLB->setSpongeLayer(spongeStart, Dx);
  myLB->setParameters(tau, U0, F0);

  Obstacle* obs[2];
  squareObstacle mySquare(xsq, ysq, L);
  obs[0] = new Grid(x0, R, Dy);
  obs[1] = &mySquare;
  myLB->setObstacles(obs, 2);

  // Parameters of perturbation
  std::string root = "pops";
  int NN = 20;
  int NbFiles = 10;
  double eps = 0.002;
  // -------- Initialise simulation -----------
  myLB->initFromFile(std::string(path_to_init));
  if(path_to_perturb){
    myLB->makePerturbation(std::string(path_to_perturb), root, NN, NbFiles, eps);
  }

  // -------- Simulate -------------------
  int N = std::min(tmax,tvismax)-std::max(tmin,tvismin)+1;
  int writingPeriod = (tvismax-tvismin)/100;
  double *f = new double[N];
  double *viscousRear = new double[N];
  double *viscousTop = new double[N];
  double *viscousFront = new double[N];
  double *viscousBot = new double[N];
  double *pRear = new double[N];
  double *pFront = new double[N];

  for (int t=tmin;t<tvismin;t++)
    {
      myLB->advanceOneTimestep(obs, 2);
    }
  int tt;
  for (int t=std::max(tmin,tvismin);t<std::min(tmax,tvismax)+1;t++)
    {
      tt = t-std::max(tmin,tvismin);
      myLB->advanceOneTimestep(obs, 2);
      if((t-tvismin)%writingPeriod == 0){
	myLB->writeSnapshot();
      }
      myLB->computeStress(obs[1]);
      f[tt] = obs[1]->getDrag();
      viscousTop[tt] = mySquare.getViscousTop();
      viscousBot[tt] = mySquare.getViscousBot();
      viscousFront[tt] = mySquare.getViscousFront();
      viscousRear[tt] = mySquare.getViscousRear();
      pFront[tt] = mySquare.getpFront();
      pRear[tt] = mySquare.getpRear();
    }

  std::ofstream outputFile;
  outputFile.open("dragFile.dat", std::ios::binary | std::ios::app);
  outputFile.write((char*)&f[0], N*sizeof(double));
  outputFile.close();
  outputFile.open("viscousTop.dat", std::ios::binary | std::ios::app);
  outputFile.write((char*)&viscousTop[0], N*sizeof(double));
  outputFile.close();
  outputFile.open("viscousBot.dat", std::ios::binary | std::ios::app);
  outputFile.write((char*)&viscousBot[0], N*sizeof(double));
  outputFile.close();
  outputFile.open("viscousRear.dat", std::ios::binary | std::ios::app);
  outputFile.write((char*)&viscousRear[0], N*sizeof(double));
  outputFile.close();
  outputFile.open("viscousFront.dat", std::ios::binary | std::ios::app);
  outputFile.write((char*)&viscousFront[0], N*sizeof(double));
  outputFile.close();
  outputFile.open("pFront.dat", std::ios::binary | std::ios::app);
  outputFile.write((char*)&pFront[0], N*sizeof(double));
  outputFile.close();
  outputFile.open("pRear.dat", std::ios::binary | std::ios::app);
  outputFile.write((char*)&pRear[0], N*sizeof(double));
  outputFile.close();

  delete[] f;
  delete obs[0];
  delete myLB;

  return PyLong_FromLong(N);
}

static PyMethodDef SimulateMethod[] = {
    {"simulate",  method_simulate, METH_VARARGS,
     "Simulates the flow."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef simulatemodule = {
    PyModuleDef_HEAD_INIT,
    "simulate",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    SimulateMethod
};

PyMODINIT_FUNC PyInit_simulate(void) {
    return PyModule_Create(&simulatemodule);
}
