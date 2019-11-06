"""data set"""

from math import sqrt

# ----------------------------------------------------------------------------
# Setup class for AtomicData
# ----------------------------------------------------------------------------
class AtomicData:
    """A class that holds atomic data such as positions, forces, total_energy, charges, etc."""

    def __init__(self, atomid=0, position=(0.0, 0.0, 0.0), symbol='X', charge=0.0, energy=0.0, force=(0.0, 0.0, 0.0)):
        self.atomid = atomid
        self.position= position
        self.symbol = symbol # element type
        self.charge = charge
        self.energy = energy
        self.force = force

# ----------------------------------------------------------------------------
# Setup classes for CollectiveData
# ----------------------------------------------------------------------------
class CollectiveData:
    """A class that holds collective quantities of simulated system such as total energy or charge."""

    def __init__(self, cell=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), total_energy=0.0, total_charge=0.0):
            self.cell = cell
            self.total_energy = total_energy
            self.total_charge = total_charge

# ----------------------------------------------------------------------------
# Setup classes for Sample
# ----------------------------------------------------------------------------
class Sample:
    """ A class that holds a list of atomic data and also collective data for a single sample."""

    def __init__(self):
        self.atomic = []  # list of atomic data
        self.collective = None

    def get_number_of_atoms(self):
        return len(self.atomic)

    @property
    def number_of_atoms(self):
        return self.get_number_of_atoms()

    def get_total_energy(self):
        """This method returns total energy from the collective part of data set."""
        assert self.collective is None, "No total energy as collective data was found"
        return self.collective.total_energy

    @property
    def total_energy(self):
        """This method returns total energy from the collective part of data set."""
        return self.get_total_energy()

    def sum_atomic_energy(self):
        """This method calculates total energy by summing up the atomic energy."""
        tot = 0.0
        for atom in self.atomic:
            tot += atom.energy
        return tot

    def get_total_charge(self):
        """This method returns total charge from the collective part of data set."""
        assert self.collective is None, "No total charge as collective data was found"
        return self.collective.total_charge

    @property
    def total_charge(self):
        """This method returns total charge from the collective part of data set."""
        return self.get_total_energy()

    def sum_atomic_charge(self):
        """This method calculates total charge by summing up atomic charge."""
        tot = 0.0
        for atom in self.atomic:
            tot += atom.charge
        return tot

    def get_atoms_for_symbol(self, symbol):
        """This methods return a list of atoms with a specified symbol (element type)."""
        sel_atoms = []
        for atom in self.atomic:
            if atom.symbol == symbol:
                sel_atoms.append(atom)
        return sel_atoms

    def get_number_of_atoms_for_symbol(self, symbol):
        """This methods return number of atoms with a specified symbol (element type)."""
        return len(self.get_atoms_for_symbol(symbol))

    def distance2(self, atom_i, atom_j):
        """This method returns square of the distance between two given atoms."""
        # set distances in each direction
        # TODO: optimize performance
        dx = atom_i.position[0] - atom_j.position[0]
        dy = atom_i.position[1] - atom_j.position[1]
        dz = atom_i.position[2] - atom_j.position[2]
        # get cell sizes
        # TODO: extend to non-orthogonal cell
        cell = self.collective.cell
        lx, ly, lz = cell[0], cell[4], cell[8]
        # apply-PBC
        # x-direction
        if dx > lx*0.5:
            dx -= lx
        elif dx < -lx*0.5:
            dx += lx
        # y-direction
        if dy > ly*0.5:
            dy -= ly
        elif dy < -ly*0.5:
            dy += ly
        # z-direction
        if dz > lz*0.5:
            dz -= lz
        elif dz < -lz*0.5:
            dz += lz
        # return square of distance
        return dx*dx + dy*dy + dz*dz

    def distance(self, atom_i, atom_j):
        """This method returns the distance between two given atoms."""
        return sqrt(self.distance2(atom_i, atom_j))

# ----------------------------------------------------------------------------
# Setup classes for DataSet
# ----------------------------------------------------------------------------
class DataSet:
    """This class holds a collection of samples."""

    def __init__(self):
        self.samples = []  # list of samples

    def append(self, new_sample):
        """Append a sample to the list of samples."""
        assert isinstance(new_sample, Sample), "Unexpected sample type"
        self.samples.append(new_sample)
        return self

    def get_number_of_samples(self):
        return len(self.samples)

    @property
    def number_of_samples(self):
        return self.get_number_of_samples()

