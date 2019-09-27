"""RuNNer"""

from .dataset import DataSet, Sample, AtomicData, CollectiveData
from .unit import UnitConversion
from .utils import get_time_and_date
import random

# ----------------------------------------------------------------------------
# Setup class for RuNNer adaptor
# ----------------------------------------------------------------------------
class RunnerAdaptor:
    """A bas class for conversion file formats of RuNNer package."""

    def __init__(self):
        self.dataset = DataSet()  # initialize with empty RuNNer data set

    def clean(self):
        self.dataset = DataSet()

    def write_runner(self, filename, uc=UnitConversion()):
        """This method writes outputs in RuNNer structure file format."""
        with open(str(filename), "w") as out_file:
            # loop over samples
            for sample in self.dataset.samples:
                # add begin and comment
                out_file.write("begin\n")
                out_file.write("comment Generated by PyNNP at %s\n" % get_time_and_date())
                # write cell data (collective data)
                cell = [c for c in sample.collective.cell]
                for i in range(0, 9, 3):
                    out_file.write("lattice %.10f %.10f %.10f\n" % tuple([c*uc.length for c in cell[i:i+3]]))
                # loop over atoms in a sample (atomic data)
                for atom in sample.atomic:
                    out_file.write("atom ")
                    out_file.write("%15.10f %15.10f %15.10f " % tuple([pos*uc.length for pos in atom.position]))
                    out_file.write("%s %15.10f %15.10f " % (atom.symbol, atom.charge*uc.charge, atom.energy*uc.energy*0.0))
                    out_file.write("%15.10f %15.10f %15.10f\n" % tuple([frc*uc.force for frc in atom.force]))
                # write total energy and charge (collective data)
                out_file.write("energy %.10f\n" % (sample.collective.total_energy*uc.energy))
                out_file.write("charge %.10f\n" % (sample.collective.total_charge*uc.charge))
                out_file.write("end\n")
        # return object
        return self

    def read_runner(self, filename="input.data", uc=UnitConversion()):
        """This method reads the RuNNer atomic structure file format."""
        in_file = open(str(filename), "r")
        line = in_file.readline()
        # loop over lines in the input file
        while line:
            # read a frame
            if "begin" in line.rstrip("/n").split()[0]:
                # initialize sample data
                sample = Sample()
                cell = []
                atomid = 0
                total_energy = 0.0
                total_charge = 0.0
                # loop over current data frame
                while True:
                    # read next line
                    line = next(in_file).rstrip("/n").split()
                    # skip comment line
                    if "comment" in line[0]:
                        continue
                    # read cell data
                    if "lattice" in line[0]:
                        for c in line[1:4]:
                            cell.append(float(c)*uc.length)
                    # read atomic data
                    if "atom" in line[0]:
                        atomid += 1
                        position = [float(pos)*uc.length for pos in line[1:4]]
                        symbol = line[4]
                        charge = float(line[5])*uc.charge
                        energy = float(line[6])*uc.energy
                        force = [float(frc)*uc.force for frc in line[7:10]]
                        sample.atomic.append(AtomicData(atomid, position, symbol, charge, energy, force))
                    # read total energy (collective data)
                    if "energy" in line[0]:
                        total_energy = float(line[1])*uc.energy
                    # read total charge (collective data)
                    if "charge" in line[0]:
                        total_charge = float(line[1])*uc.charge
                    # end of current data frame
                    if "end" in line[0]:
                        break
                # set collective data
                assert len(cell) == 9, "Unexpected number of cell dimension (%d)" % len(cell)
                sample.collective = CollectiveData(cell, total_energy, total_charge)
                # add sample to the data set
                self.dataset.append(sample)
            # next line
            line = in_file.readline()
        # return object
        return self

    def sample(self, number_of_samples=None, seed=1234):
        """This method randomly samples and replaces the data set."""
        # set random seed
        random.seed(int(seed))
        # select samples randomly
        if number_of_samples is None:
            sel_samples = random.sample(self.dataset.samples, 1)  # default number of sample
        else:
            assert int(number_of_samples) <= self.dataset.number_of_samples, "Number of structures exceeds number of samples"
            sel_samples = random.sample(self.dataset.samples, int(number_of_samples))
        # replace the data set with new selected samples
        self.dataset.samples = sel_samples
        # return object
        return self

    def select(self, list_of_indices):
        """This method selects and replace the data set based on given indices (zero-index-based)."""
        if isinstance(list_of_indices, int):
            list_of_indices = [list_of_indices]
        self.dataset.samples = [self.dataset.samples[int(index)] for index in list(list_of_indices)]
        return self

    def delete(self, list_of_indices):
        """This method deletes some samples from data set based on given indices (zero-index-based)."""
        if isinstance(list_of_indices, int):
            list_of_indices = [list_of_indices]
        n_samples = self.dataset.number_of_samples
        self.dataset.samples = [self.dataset.samples[index] for index in range(n_samples) if index not in list(list_of_indices)]
        return self
