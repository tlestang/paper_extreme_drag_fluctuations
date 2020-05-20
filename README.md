# About 
This repository contains the software supporting the paper


Lestang, T., Bouchet, F., & Lévêque, E. (2020). Numerical study of extreme mechanical force exerted by a turbulent flow on a bluff body by direct and rare-event sampling techniques. Journal of Fluid Mechanics, 895, A19. doi:10.1017/jfm.2020.293 [arxiv:2005.09323](https://arxiv.org/abs/2005.09323)


The repository is organised as follow
```
figures/
	# Contains scripts for derived data and figures
	fig1/
		fig1.py
	fig2/
		fig2.py
	...
jfm_paper/
	# python package for generating derived data and figures
texfiles/
	# LaTeX sources
```

Many scripts currently rely on raw data for which the generating code is not yet made available, but will added to this repository soon.
If you have any issues or queries, please create a new issue on the [this repository's issue tracker](https://github.com/tlestang/paper_extreme_drag_fluctuations/issues).

# Installing the python package
## Requirements
- Python 3.6 and above
- A C++ compiler (ex: `g++`)
- The Python header files

On Debian-based GNU/Linux distribution (e.g. Ubuntu, Linux Mint), the above can be installed with
```bash
$ apt install python3 python3-dev gcc
```
On MacOS, using homebrew,
```bash
$ brew install python3 gcc
```

## Installation
To install the python package, first clone this repository
```bash
$ git clone https://github.com/tlestang/paper_extreme_drag_fluctuations.git
```

We highly recommend installing the package inside a python virtual environment, so as to keeps it and its
dependencies separate from your system's python.
```bash
# In directory paper_extreme_drag_fluctuations
$ python3 -m virtualenv venv
$ source venv/bin/activate
```
the move into the directory and install with pip
```bash
# In directory paper_extreme_drag_fluctuations
(venv) $ pip install .
```

Depending on you platform, the python installation may or may not come with the `virtualenv` and `pip`.
In most cases, these can be installed _via_
```bash
apt install python3-pip python3-venv
```

# Fluid flow data generation
All flow simulation rely on a in-house C++ library implementing the Lattice Boltzmann Method.
It is available [here](https://framagit.org/tlestang/pipeLBM).

# GKTL algorithm implementation

# AMS algorithm implementation
