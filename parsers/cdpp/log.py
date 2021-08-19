import os

from components.parser import LineParser
from formats.messages import MessageOutput, MessageCA, Messages, Frame


class Log(LineParser):

    def __init__(self, structure, frame_0):
        super().__init__()

        self.structure = structure
        self.content = Messages()

        if frame_0 is not None:
            self.content.add_frame(frame_0)

    def get_valid_file(self, files):
        log = list(filter(lambda f: os.path.splitext(f)[1].startswith('.log'), files))

        if len(log) == 0:
            raise ValueError("No .log file provided. A .log file is mandatory.")

        if len(log) > 1:
            raise ValueError("Multiple .log files were provided. Only a single .log file can be provided.")

        return log[0]

    def line_parse(self, line):
        # Mensaje Y / 00:00:00:100 / flu(18,12)(645) / out /      2.00000 para flu(02)
        # Mensaje Y / 00:00:20:000 / sender(02) / dataout /     11.00000 para top(01)
        if not line.startswith("Mensaje Y"):
            return None

        split = [s.strip() for s in line.split('/')]
        model = split[2].replace('(', ' ').replace(')', ' ').split()
        coord = [c for c in model[1].split(',')] if len(model) == 3 else None

        time = split[1]
        port = split[3]
        value = split[4].split()[0]

        f = self.content.add_frame(Frame(time))

        if coord is not None:
            if len(coord) == 2:
                coord.append("0")

            f.add_message(MessageCA(coord, [value]))

        else:
            model_type = self.structure.components_index.get_item(model[0]).model_type
            model_type = self.structure.model_types[model_type.index]

            # this is to avoid highlighting coupled models as message origins. In CDpp, atomic models connected to coupled
            # models immediately emit the message received by the inner atomic. It's clearer if that message is not shown.
            if model_type.type == "coupled":
                return None

            model = self.structure.get_model(model[0])
            port = model.model_type.port_types.get_item(port)

            f.add_message(MessageOutput(model, port, [value]))
