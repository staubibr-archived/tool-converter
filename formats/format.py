import json
import os


class Format(object):

    def __init__(self, structure, messages, style):
        self.structure = structure
        self.messages = messages
        self.style = style

    def output_json(self, file, content):
        out = open(file, "w")
        json.dump(content, out)
        out.close()

    def output_txt(self, file, content):
        out = open(file, "w")

        for line in content:
            out.write(line + "\n")

        out.close()

    def output(self, path):
        # There should be a way to auto serialize classes but I don't have time
        self.output_json(os.path.join(path, "structure.json"), self.structure.to_json())

        if self.style is not None:
            self.output_json(os.path.join(path, "style.json"), self.style.to_json())

        self.output_txt(os.path.join(path, "messages.log"), self.messages.to_log(self.structure))
