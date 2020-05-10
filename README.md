# Python-NNP
Python-NNP (`pynnp`) is a set of basic python modules for easier neural network potential construction and validation using 
[RuNNer](http://www.uni-goettingen.de/de/560580.html) and
[N2P2](https://github.com/CompPhysVienna/n2p2) codes.

Please see `examples/pynnp_demo` for more details.

## Current status:
- [x] read and write RuNNer structure file format
- [x] structure selection and basic modification
- [x] providing methods to explore structures such as range of energies, forces, atom types, etc
- [x] [LAMMPS](https://lammps.sandia.gov/) dump files conversion to RuNNer file format and vice versa
- [x] [VASP](https://www.vasp.at/) output files conversion to RuNNer file format and vice versa
- [x] flexible unit conversion 
- [x] methods for applying multi-NNP reconstruction


## Dependencies:
- python>=3.7
- numpy


## Install:
```
export PYTHONPATH=${PYTHONPATH}:"/path/to/pynnp/root/directory"
```
