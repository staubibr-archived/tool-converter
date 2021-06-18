import os

from components.parser import Parser
from formats.messages import Frame, MessageCA
from components.indexed_list import Index


class ValInitialValue(object):

    def get_coords(self):
        return self._coords

    def set_coords(self, value):
        self._coords = value

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    coords = property(get_coords, set_coords)
    value = property(get_value, set_value)

    def __init__(self, coords, value):
        super().__init__()

        self.coords = coords
        self.value = value

    @staticmethod
    def from_val(line):
        # (0,0,0)=100
        # (0,0,1)=0.567
        # ...
        lr = [s.strip() for s in line.split("=")]

        coords = [s.strip() for s in lr[0][1:-1].split(",")]
        value = [s.strip() for s in lr[1].split(" ")]

        if len(coords) == 2:
            coords.append('0')

        return ValInitialValue(coords, value)


class Val(Parser):

    def __init__(self, structure, component):
        super().__init__()

        self.content = Frame("00:00:00:000")
        self.structure = structure
        self.index = Index()

    def add_initialvalue_messages(self, dim, initialvalue):
        for x in range(dim.x):
            for y in range(dim.y):
                for z in range(dim.z):
                    self.add_message([str(x), str(y), str(z)], [initialvalue])

    def add_initialrowvalues_messages(self, initialrowvalues):
        for irv in initialrowvalues:
            for y in range(len(irv.values)):
                self.add_message([irv.row, str(y), '0'], [irv.values[y]])

    def add_message(self, coords, value):
        m = self.index.get_item(coords)

        if m is None:
            m = self.content.add_message(MessageCA(coords, value))
            self.index.add_item(m.id, m)
        else:
            m.values = value

    def get_valid_file(self, files):
        val = list(filter(lambda f: os.path.splitext(f)[1] == '.val', files))

        if len(val) > 1:
            raise ValueError("Multiple .val files were provided. Only a single .val file can be provided.")

        return val[0] if len(val) == 1 else None

    def line_parse(self, line):
        if line == "":
            return

        # First 2 are always top and its port in a Cell-DEVS model
        val_value = ValInitialValue.from_val(line)

        self.add_message(val_value.coords, val_value.value)