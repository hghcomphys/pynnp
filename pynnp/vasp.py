"""Vasp"""

from .runner import RunnerAdaptor
from .unit import UnitConversion
from .dataset import Sample, AtomicData
from .util import read_and_tokenize_line

# ----------------------------------------------------------------------------
# Setup class for RuNNer adaptor to VASP
# ----------------------------------------------------------------------------
class RuNNerAdaptorForVASP(RunnerAdaptor):
    """An inherited class for conversion file formats between RuNNer and VASP packages."""

    def __init__(self):
        RunnerAdaptor.__init__(self)

    def write_poscar(self, filename='POSCAR', symbol_list=None, uc=UnitConversion(), scaling_factor=1.0,
                     number_of_strucure=None, seed=1234):

        if (number_of_strucure is None):
            samples = self.dataset.samples
        else:
            assert number_of_strucure <= self.dataset.number_of_samples, "Number of structures exceeds number of samples"
            import random
            random.seed(seed)
            samples = random.sample(self.dataset.samples, int(number_of_strucure))

        index = 0
        for sample in samples:

            index += 1
            with open(filename+"_%d" % index, 'w') as out_file:

                # comment
                out_file.write(", ATOM=")
                for symbol in symbol_list:
                    out_file.write("%s " % symbol)
                out_file.write("\n")

                # write scaling factor
                out_file.write("%15.10f\n" % scaling_factor)

                # cell
                for i in range(3):
                    out_file.write("%15.10f %15.10f %15.10f\n" % tuple([c*uc.length for c in sample.collective.cell[3*i:3*(i+1)]]))

                # number of atoms for each symbol
                for symbol in symbol_list:
                    out_file.write("%d " % sample.get_number_of_atoms_for_symbol(symbol))
                out_file.write("\n")

                # atom positions
                out_file.write("Cartesian \n")
                for symbol in symbol_list:
                    for atom in sample.get_atoms_for_symbol(symbol):
                        out_file.write("%15.10f %15.10f %15.10f\n" % tuple([f*uc.length for f in atom.position]))


    def read_poscar(self, filename='POSCAR', symbol_list=None, uc=UnitConversion()):

        # create a instance of sample data
        sample = Sample()

        with open(filename, 'r') as in_file:

            # loop over lines in file
            for line in in_file:

                # create a instance of sample data
                sample = Sample()

                # read scaling factor
                line = read_and_tokenize_line(in_file)
                scaling_factor = float(line[0])
                # print ("Scaling factor (POSCAR): ", scaling_factor)

                # read cell info
                cell = []
                for n in range(3):
                    line = read_and_tokenize_line(in_file)
                    for m in range(3):
                        cell.append(float(line[m])*scaling_factor*uc.length)
                # print(cell)

                line = read_and_tokenize_line(in_file)
                natoms_each_type = [int(l) for l in line]
                # print (natoms_each_type)

                # skip the line
                line = next(in_file)
                if "select" in line.lower():
                    line = next(in_file)

                # check cartesian coordinates
                if "car" not in line.lower():
                    # print (line)
                    raise AssertionError("Expected cartesian coordinates!")

                # read atomic positions
                atomid = 0
                for natoms, n in zip(natoms_each_type, range(len(natoms_each_type))):

                    for i in range(natoms):

                        atomid += 1
                        line = read_and_tokenize_line(in_file)

                        position = [float(pos)*scaling_factor*uc.length for pos in line[0:3]]
                        symbol = symbol_list[n]

                        # create atomic data and append it to sample
                        sample.atomic.append(AtomicData(atomid, position, symbol, 0.0, 0.0, (0.0, 0.0, 0.0)))
                        # (charge, energy, and force) * uc = 0
                        # print (symbol, position)
                # Assuming it is the end of the POSCAR
                break

            # set collective data
            sample.collective = CollectiveData(cell, sample.total_energy, sample.total_charge)

            # add sample to DataSet (list of samples)
            self.dataset.append(sample)

        return self


    def read_outcar(self, filename='OUTCAR', uc=UnitConversion()):

        with open(filename, 'r') as in_file:
            # loop over lines in file

            for line in in_file:

                # read line
                # line = next(in_file)
                # print(line)

                # read the force section
                if "POSITION" in line:
                    next(in_file)
                    for atom in self.dataset.samples[0].atomic:
                        line = read_and_tokenize_line(in_file)
                        force = [float(frc)*uc.force for frc in line[3:6]]
                        atom.force = tuple(force)
                        # print(line, atom.force)

                if "TOTEN" in line:
                    total_energy = float(line.rstrip("/n").split()[-2])
                    # print (total_energy)
                    self.dataset.samples[0].collective.total_energy = total_energy*uc.energy

        return self

    def read_vasp(self, symbol_list=None, uc=UnitConversion()):
        self.read_poscar(symbol_list=symbol_list, uc=uc)
        self.read_outcar(uc=uc)
        return self