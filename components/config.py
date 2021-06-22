import os
import json

from argparse import ArgumentParser


def is_simulator_valid(p, arg):
    if arg in ['CDpp', 'Lopez', 'Cadmium']:
        return arg
    else:
        p.error('Simulator provided is invalid. Valid simulators are Cdpp or Lopez.')


def is_formalism_valid(p, arg):
    if arg in ['DEVS', 'Cell-DEVS']:
        return arg
    else:
        p.error('Formalism provided is invalid. Valid formalisms are DEVS or Cell-DEVS.')


class Config(object):

    def get_name(self):
        return self.args.name

    def get_simulator(self):
        return self.args.simulator

    def get_formalism(self):
        return self.args.formalism

    def get_folder(self):
        return self.args.folder or ""

    def get_files(self):
        return self.args.files

    def get_output(self):
        return self.args.output or ""

    name = property(get_name)
    simulator = property(get_simulator)
    formalism = property(get_formalism)
    folder = property(get_folder)
    files = property(get_files)
    output = property(get_output)

    def __init__(self):

        parser = ArgumentParser(description='This script is used to convert DEVS and Cell-DEVS results from the CD++ and Lopez simulators.')

        parser.add_argument('--name', dest='name', type=str, help='Name of the simulation model', required=True)
        parser.add_argument('--simulator', dest='simulator', type=lambda v: is_simulator_valid(parser, v), help='Name of the simulator (CDpp or Lopez)', required=True)
        parser.add_argument('--formalism', dest='formalism', type=lambda v: is_formalism_valid(parser, v), help='Name of the formalism used (DEVS or Cell_DEVS)', required=True)
        parser.add_argument('--folder', dest='folder', type=str, help='The folder where the files are located. This path will prefix the files provided.')
        parser.add_argument('--files', dest='files', nargs='*', type=str, help='The list of raw simulation result files.', required=True)
        parser.add_argument('--output', dest='output', type=str, help='The output folder where the results will be saved.')

        self.args = parser.parse_args()

        for i in range(len(self.files)):
            self.files[i] = os.path.join(self.folder, self.files[i])

            if not os.path.exists(self.files[i]):
                parser.error('Path {} provided does not exist.'.format(self.files[i]))

    def get_output_path(self, file):
        return os.path.join(self.output, file)

    def make_output_folder(self):
        try:
            os.makedirs(self.output)
        except FileExistsError:
            pass
