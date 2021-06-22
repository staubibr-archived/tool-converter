import os
import json

from components.parser import FullParser
from formats.structure import Info, Structure, Dim


class CadmiumStructure(FullParser):

    def __init__(self):
        super().__init__()

        self.content = Structure()

    def get_valid_file(self, files):
        data = list(filter(lambda f: os.path.splitext(f)[1] == '.json', files))

        if len(data) == 0:
            raise ValueError("No .json file provided. A .json file is mandatory.")

        if len(data) > 1:
            raise ValueError("Multiple .json files were provided. Only a single .json file can be provided.")

        return data[0]

    def full_parse(self, stream):
        data = json.load(stream)

        self.content.info = Info(data["info"]["simulator"], data["info"]["name"], data["info"]["type"])

        for t in data["model_types"]:
            dim = Dim(t["dim"][0], t["dim"][1], t["dim"][2]) if "dim" in t else None

            self.content.add_model_type(t["name"], t["template"], t["type"], dim)

        for t in data["port_types"]:
            model_type = self.content.model_types.items[t["model_type"]]
            port_type = self.content.add_port_type(t["name"], t["type"], t["template"], model_type)

            model_type.port_types.append(port_type)

        for n in data["nodes"]:
            if "id" in n and "model_type" in n:
                model_type = self.content.model_types.items[n["model_type"]]
                self.content.add_model_node(n["id"], model_type)

            if "model_id" in n and "port_type" in n:
                port_type = self.content.port_types.items[n["port_type"]]
                model_node = self.content.get_model(n["model_id"])
                self.content.add_port_node(model_node, port_type)