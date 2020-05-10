from .runner import RunnerAdaptor
from .unit import UnitConversion
from .dataset import SampleData, AtomicData, CollectiveData


# ----------------------------------------------------------------------------
# Setup class for RuNNer adaptor to VASP
# ----------------------------------------------------------------------------
class RuNNerAdaptorForVASP(RunnerAdaptor):
    """An inherited class for conversion file formats between RuNNer and VASP packages."""

    def __init__(self):
        RunnerAdaptor.__init__(self)

    def write_poscar(self, symbol_list=None, filename='POSCAR', uc=UnitConversion(), scaling_factor=1.0):
        """This method writes data set into POSCAR file format (VASP package)."""
        index = 0
        for sample in self.dataset.samples:
            # write each data frame into separate files
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
                for i in range(0, 9, 3):
                    out_file.write("%15.10f %15.10f %15.10f\n" % tuple([c*uc.length for c in sample.collective.cell[i:i+3]]))
                # number of atoms for each symbol
                for symbol in symbol_list:
                    out_file.write("%d " % sample.get_number_of_atoms_for_symbol(symbol))
                out_file.write("\n")
                # atom positions
                out_file.write("Cartesian \n")
                for symbol in symbol_list:
                    for atom in sample.get_atoms_for_symbol(symbol):
                        out_file.write("%15.10f %15.10f %15.10f\n" % tuple([f*uc.length for f in atom.position]))
        # return object
        return self

    def read_poscar(self, symbol_list=None, filename='POSCAR', uc=UnitConversion()):
        """This method reads POSCAR file format (VASP package)."""
        # create a instance of sample data
        sample = SampleData()
        with open(str(filename), 'r') as in_file:
            # loop over lines in file
            for line in in_file:
                # create a instance of sample data
                sample = SampleData()
                # read scaling factor
                line = next(in_file).rstrip("/n").split()
                scaling_factor = float(line[0])
                # print ("Scaling factor (POSCAR): ", scaling_factor)
                # read cell info
                cell = []
                for n in range(3):
                    line = next(in_file).rstrip("/n").split()
                    for m in range(3):
                        cell.append(float(line[m])*scaling_factor*uc.length)
                # number of atom for each element type
                line = next(in_file).rstrip("/n").split()
                natoms_each_type = [int(l) for l in line]
                # print (natoms_each_type)
                # skip the line
                line = next(in_file)
                if "select" in line.lower():
                    line = next(in_file)
                # check cartesian coordinates
                if "car" not in line.lower():
                    raise AssertionError("Expected cartesian coordinates!")

                # read atomic positions
                atomid = 0
                for natoms, n in zip(natoms_each_type, range(len(natoms_each_type))):
                    # loop over all atoms
                    for i in range(natoms):
                        atomid += 1
                        line = next(in_file).rstrip("/n").split()
                        position = [float(pos)*scaling_factor*uc.length for pos in line[0:3]]
                        symbol = symbol_list[n]
                        # create atomic data and append it to sample
                        sample.atomic.append(AtomicData(atomid, position, symbol, 0.0, 0.0, (0.0, 0.0, 0.0)))
                        # (charge, energy, and force) * uc = 0
                        # print (symbol, position)
                # Assuming it is the end of the POSCAR
                break
            # set collective data
            sample.collective = CollectiveData(cell, 0, 0)
            # add sample to DataSet (list of samples)
            self.dataset.append(sample)
        # return object
        return self

    def read_outcar(self, filename='OUTCAR', uc=UnitConversion()):
        """This method reads OUTCAT file (VASP package)."""
        with open(filename, 'r') as in_file:
            # loop over lines in file
            for line in in_file:
                # read the force section
                if "POSITION" in line:
                    next(in_file)
                    # write data into first sample in the data set (assuming having only one sample)
                    for atom in self.dataset.samples[0].atomic:
                        line = next(in_file).rstrip("/n").split()
                        force = [float(frc)*uc.force for frc in line[3:6]]
                        atom.force = tuple(force)
                        # print(line, atom.force)
                # read total energy
                if "TOTEN" in line:
                    total_energy = float(line.rstrip("/n").split()[-2])
                    self.dataset.samples[0].collective.total_energy = total_energy*uc.energy
        # return object
        return self

    def read_vasp(self, symbol_list=None, uc=UnitConversion()):
        """This method read all required data from VASP including structure (POSCAR) and forces (OUTCAR)."""
        self.read_poscar(symbol_list=symbol_list, uc=uc)
        self.read_outcar(uc=uc)
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