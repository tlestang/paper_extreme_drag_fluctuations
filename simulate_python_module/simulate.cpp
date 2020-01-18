#include <fstream>
#include <algorithm>
#include <python3.7/Python.h>

#include "libpipeLBM.h"

static PyObject* method_simulate(PyObject *self, PyObject *args){

  char* path_to_init;
  int tmin;
  int tmax;
  int tvismin;
  int tvismax;

  bool parse_args_error = PyArg_ParseTuple(args, "siiii", &path_to_init, &tmin,
					   &tmax, &tvismin, &tvismax);
  if (!parse_args_error)
    return NULL;

  // Setup LBM
  int Dx = 257;
  int Dy = 65;
  int R = (Dy-1)/16;
  int x0 = (Dx-1)/16;
  int L = 16;
  int xsq = (Dx-1)/2;
  int ysq = (Dy-1)/2 - L/2;
  double U0 = 0.05;
  double tau = 0.5005;
  int spongeStart = (int) 3*(Dx-1)/4+1;
  double F0 = 0.0;

  pipeLBM *myLB = new pipeLBM(Dx, Dy);
  myLB->setInletBC("poiseuille");
  myLB->setOutletBC("open");
  myLB->setSpongeLayer(spongeStart, Dx);
  myLB->setParameters(tau, U0, F0);

  Obstacle* obs[2];
  obs[0] = new Grid(x0, R, Dy);
  obs[1] = new squareObstacle(xsq, ysq, L);
  myLB->setObstacles(obs, 2);

  // -------- Initialise simulation -----------
  myLB->initFromFile(std::string(path_to_init));

  // -------- Simulate -------------------
  int N = min(tmax,tvismax)-max(tmin,tvismin)+1;
  double *f = new double[N];
  for (int t=tmin;t<tvismin;t++)
    {
      myLB->advanceOneTimestep(obs, 2);
    }
  for (int t=std::max(tmin,tvismin);t<std::min(tmax,tvismax)+1;t++)
    {
      myLB->advanceOneTimestep(obs, 2);
      myLB->writeSnapshot();
      myLB->computeStress(obs[1]);
      f[t-tmin] = obs[1]->getDrag();
    }
  for (int t=tvismax+1;t<tmax;t++)
    {
      myLB->advanceOneTimestep(obs, 2);
    }

  ofstream dragFile("dragFile.dat", ios::binary | ios::app);
  dragFile.write((char*)&f[0], N*sizeof(double));
  dragFile.close();

  delete[] f;
  delete obs[0];
  delete obs[1];
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
