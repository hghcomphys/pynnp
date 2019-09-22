"""RuNNer"""

from .dataset import DataSet, Sample, AtomicData, CollectiveData
from .util import read_and_tokenize_line
import random

# ----------------------------------------------------------------------------
# Setup class for RuNNer adaptor
# ----------------------------------------------------------------------------
class RunnerAdaptor:
    """A bas class for conversion file formats of RuNNer package."""

    def __init__(self):
        self.dataset = DataSet()

    def clean(self):
        self.dataset = DataSet()

    def write_runner(self, filename):
        """Write RuNNer input data."""

        with open(filename, "w") as out_file:
            # loop over samples
            for sample in self.dataset.samples:
                out_file.write("begin\n")
                cell = [c for c in sample.collective.cell]
                out_file.write("lattice %.10f %.10f %.10f\n" % (cell[0], cell[1], cell[2]))
                out_file.write("lattice %.10f %.10f %.10f\n" % (cell[3], cell[4], cell[5]))
                out_file.write("lattice %.10f %.10f %.10f\n" % (cell[6], cell[7], cell[8]))
                # loop over atoms in a sample
                for atom in sample.atomic:
                    out_file.write("atom ")
                    out_file.write("%15.10f %15.10f %15.10f " % tuple([pos for pos in atom.position]))
                    out_file.write("%s %15.10f %15.10f " % (atom.symbol, atom.charge, atom.energy*0.0))
                    out_file.write("%15.10f %15.10f %15.10f\n" % tuple([frc for frc in atom.force]))
                out_file.write("energy %.10f\n" % (sample.collective.total_energy))
                out_file.write("charge %.10f\n" % (sample.collective.total_charge))
                out_file.write("end\n")
        return self

    def read_runner(self, filename):
        """read RuNNer atomic structure file."""

        read_file = True
        in_file = open(filename, "r")

        line = in_file.readline()
        while line:

            # read a frame
            if "begin" in line.rstrip("/n").split()[0]:

                # prepare sample
                sample = Sample()
                cell = []
                atomid = 0
                total_energy = 0.0
                total_charge = 0.0

                while True:

                    line = read_and_tokenize_line(in_file)

                    if "comment" in line[0]:
                        continue

                    if "lattice" in line[0]:
                        for c in line[1:4]:
                            cell.append(float(c))

                    if "atom" in line[0]:
                        atomid += 1
                        position = [float(pos) for pos in line[1:4]]
                        symbol = line[4]
                        charge = float(line[5])
                        energy = float(line[6])
                        force = [float(frc) for frc in line[7:10]]
                        sample.atomic.append(AtomicData(atomid, position, symbol, charge, energy, force))

                    if "energy" in line[0]:
                        total_energy = float(line[1])

                    if "charge" in line[0]:
                        total_charge = float(line[1])

                    if "end" in line[0]:
                        break

                # set collective data
                assert len(cell) == 9, "Unexpected number of cell dimension (%d)" % len(cell)
                sample.collective = CollectiveData(cell, total_energy, total_charge)
                # add sample to DataSet (list of samples)
                self.dataset.append(sample)

            # next line
            line = in_file.readline()

        return self

    def sample(self, number_of_samples=None, seed=1234):
        """This method randomly samples and replaces the data set."""
        random.seed(int(seed))
        if (number_of_samples is None):
            sel_samples = random.sample(self.dataset.samples, 1)
        else:
            assert int(number_of_samples) <= self.dataset.number_of_samples, "Number of structures exceeds number of samples"
            sel_samples = random.sample(self.dataset.samples, int(number_of_samples))

        self.dataset.samples = sel_samples
        return self

    def select(self, list_of_indices):
        """This method selects and replace the data set based on given indices."""
        self.dataset.samples = [self.dataset.samples[int(index)] for index in list(list_of_indices)]
        return self

    # def read_nnforces(self, filename, uc=UnitConversion()):
    #     """A method that reads predicted force for a given structure"""
    #     nnforces = []
    #     with open(filename, 'r') as infile:
    #         for line in infile:
    #             if "NNforces" in line:
    #                 line = line.rstrip("/n").split()
    #                 nnforces.append([float(_)*uc.force for _ in line[2:5]])
    #     return nnforces

    # def read_nnenergy(self, filename, uc=UnitConversion()):
    #     """A method that reads predicted force for a given structure"""
    #     nnenergy = None
    #     with open(filename, 'r') as infile:
    #         for line in infile:
    #             if "NNenergy" in line:
    #                 line = line.rstrip("/n").split()
    #                 nnenergy = float(line[1])*uc.energy
    #                 break
    #     return nnenergy

# if __name__ == "__main__":
    # data = RunnerAdaptor().read_runner(filename="input.data").write_runner(filename="input.2.data")
    # uc = UnitConversion(energy_conversion=EV_TO_HARTREE, length_conversion=ANGSTROM_TO_BOHR)
    # RuNNerAdaptorForVASP().read_vasp(symbol_list=['H', 'O'], uc=uc).write_runner(filename='input.vasp.data')
    # vasp.read_POSCAR(symbol_list=['O', 'H'], uc=uc)
    # vasp.read_OUTCAR(uc=uc)
    # uc = UnitConversion(energy_conversion=EV_TO_HARTREE, length_conversion=ANGSTROM_TO_BOHR)
    # RuNNerAdaptorForVASP().read_runner("input.data").write_poscar(symbol_list=['H', 'O'], uc=uc.inverse, number_of_strucure=1)
    # ra = RunnerAdaptor();
    # ra.read_runner("input.data");
    # ra.select(10, seed=1)
    # ra.write_runner("input.data.sel")