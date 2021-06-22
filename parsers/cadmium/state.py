import os

from components.util import Util
from components.parser import LineParser
from formats.messages import Messages, Frame, MessageCA


class CadmiumState(LineParser):

    def __init__(self, structure):
        super().__init__()

        self.structure = structure
        self.content = Messages()
        self.frame = None

    def get_valid_file(self, files):
        log = list(filter(lambda f: "state.txt" in f, files))

        if len(log) == 0:
            raise ValueError("No .ma file provided. An .ma file is mandatory.")

        if len(log) > 1:
            raise ValueError("Multiple .ma files were provided. Only a single .ma file can be provided.")

        return log[0]

    def line_parse(self, line):
        i = line.find('(')
        j = line.find(')')
        k = line.find('<')
        l = line.find('>')

        if i == -1 and j == -1 and k == -1 and l == -1:
            self.frame = self.content.add_frame(Frame(line))

        else:
            coords = [s.strip() for s in line[i+1:j].split(',')]
            values = [s.strip() for s in line[k+1:l].split(',')]

            if len(coords) == 2:
                coords.append("0")

            self.frame.add_message(MessageCA(coords, values))
