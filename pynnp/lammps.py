"""LAMMPS"""

from .runner import RunnerAdaptor
from .dataset import AtomicData, CollectiveData
from .unit import UnitConversion

# ----------------------------------------------------------------------------
# Setup class for RuNNer adaptor to LAMMPS
# ----------------------------------------------------------------------------
class RuNNerAdaptorForLAMMPS(RunnerAdaptor):
    """An inherited class for conversion file formats between RuNNer and LAMMPS packages."""

    def __init__(self):
        RunnerAdaptor.__init__(self)

    def read_lammps(self, filename, symbol_dict=None, uc=UnitConversion()):

        with open(filename, 'r') as in_file:
            # loop over lines in file
            for line in in_file:

                # create a instance of sample data
                sample = Sample()

                # number of steps
                line = next(in_file)
                steps = int(line.split()[0])
                # number of atoms
                next(in_file)
                line = next(in_file)
                number_of_atoms = int(line.split()[0])
                # read cell sizes
                # TODO: read non-orthogonal cell in lammps
                cell = []
                line = next(in_file)
                for n in range(9):
                    if n in [0, 4, 8]:
                        line = next(in_file)
                        line = line.rstrip("/n").split()
                        cell.append((float(line[1]) - float(line[0]))*uc.length)
                    else:
                        cell.append(0.0)

                # read atomic positions, symbol, charge, forces, energy, etc.
                line = next(in_file)
                for n in range(number_of_atoms):
                    line = next(in_file).rstrip("/n").split()
                    atomid = int(line[0])
                    position = [float(pos)*uc.length for pos in line[1:4]]
                    symbol = line[4]
                    charge = float(line[5])*uc.charge
                    energy = float(line[6])*uc.energy
                    force = [float(frc)*uc.force for frc in line[7:10]]
                    # convert number to an atomic symbol
                    if symbol_dict is not None:
                        symbol = symbol_dict[symbol]

                    # create atomic data and append it to sample
                    sample.atomic.append(AtomicData(atomid, position, symbol, charge, energy, force))

                # set collective data
                sample.collective = CollectiveData(cell, sample.total_energy, sample.total_charge)

                # add sample to DataSet (list of samples)
                self.dataset.append(sample)

        return self

    def write_lammps(self, filename, uc=UnitConversion()):
        """A method that writes lammps input data."""
        pass
