#include <iostream>
#include <fstream>
#include <python3.7/Python.h>

#include "libpipeLBM.h"

static PyObject* method_simulate(PyObject *self, PyObject *args){

  char* path_to_init;
  int nb_timesteps;
  int write_fields;
  int write_final_state;
  
  bool parse_args_error = PyArg_ParseTuple(args, "siii", &path_to_init, &nb_timesteps,
					   &write_fields, &write_final_state);
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
  for (int t=0;t<nb_timesteps;t++)
    {
      myLB->advanceOneTimestep(obs, 2);
      if(write_fields && t%write_fields == 0){
	myLB->writeSnapshot();
      }
      std::cout << "wrote snapshot" << std::endl;
    }
  
  if (write_final_state){
    std::ofstream final_state("final_state.bin", std::ios::binary);
    final_state.write((char*)(myLB->getState()), 9*Dx*Dy);
    final_state.close();
  }   

  delete obs[0];
  delete obs[1];
  delete myLB;
  
  return PyLong_FromLong(nb_timesteps);
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
    std::cout << "PyInit_simulate" << std::endl;
    return PyModule_Create(&simulatemodule);
}
