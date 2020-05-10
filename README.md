# Python-NNP
Python-NNP (`pynnp`) is a set of basic python modules for easier neural network potential construction and validation using [RuNNer](http://www.uni-goettingen.de/de/560580.html) code.

See `examples/pynnp_demo` for more examples.

## Current status:
- [x] read and write RuNNer structure file format
- [x] structure selection and basic modification
- [x] provides methods to explore structures such as range of energies, forces, atom types, etc.
- [x] [LAMMPS](https://lammps.sandia.gov/) dump files conversion to Runner file format and vice versa
- [x] [VASP](https://www.vasp.at/) output files conversion to Runner file format and vice versa
- [x] flexible unit conversion when read/write data files
- [x] tools for applying multi-NNP method


## Dependencies:
- python>=3.7
- numpy


## Install:
```
export PYTHONPATH=${PYTHONPATH}:"/path/to/pynnp/root/directory"
```
