import os

from components.parser import LineParser
from formats.messages import Messages, MessageCA, Frame
from components.indexed_list import Index


class Log(LineParser):

    def __init__(self, structure):
        super().__init__()

        self.structure = structure
        self.content = Messages()
        self.index = Index()

    def get_valid_file(self, files):
        log = list(filter(lambda f: os.path.splitext(f)[1].startswith('.log'), files))

        if len(log) == 0:
            raise ValueError("No .log file provided. An .log file is mandatory.")

        if len(log) > 1:
            raise ValueError("Multiple .log files were provided. Only a single .log file can be provided.")

        return log[0]

    def line_parse(self, line):
        if not line.startswith("0 / L / Y"):
            return None

        # Mensaje Y / 00:00:47:405 / sandpile(5,5)(58) / out /      3.00000 para sandpile(02)
        split = [s.strip() for s in line.split('/')]
        model = split[4].replace('(', ' ').replace(')', ' ').split()
        coord = [c for c in model[1].split(',')] if len(model) == 3 else None

        if coord is None:
            return None

        if len(coord) == 2:
            coord.append("0")

        time = split[3]
        port = split[5]
        value = split[6]

        f = self.content.add_frame(Frame(time))
        m = self.index.get_item([time] + coord)

        model_type = self.structure.model_types.get_item(model[0])
        port_type = model_type.port_types.get_item([port])
        i = int(port_type.index)

        if m is None:
            m = f.add_message(MessageCA(coord, [""] * len(model_type.port_types)))
            self.index.add_item([time] + coord, m)

        m.values[i] = value
