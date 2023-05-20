# PyNNP
Python-NNP (`pynnp`) comprises very basic Python modules designed to simplify the development and validation of neural network potentials (NNP). These modules are specifically tailored for utilization with the [RuNNer](http://www.uni-goettingen.de/de/560580.html) and [N2P2](https://github.com/CompPhysVienna/n2p2) packages.

Please see [examples/pynnp_demo](https://github.com/hghcomphys/pynnp/blob/master/examples/pynnp_demo.ipynb) for more details.

## Features:
- Parsing and writing RuNNer structure file format.
- Selecting and making basic modifications to the structures.
- Providing methods for exploring structural properties like energy range, force range, atom types, etc.
- Conversion of [LAMMPS](https://lammps.sandia.gov/) dump files to RuNNer file format, and vice versa.
- Conversion of [VASP](https://www.vasp.at/) output files to RuNNer file format, and vice versa.
- Flexible unit conversion functionality.
- Methods for applying multi-NNP reconstruction.

## Dependencies:
- python>=3.7
- numpy

