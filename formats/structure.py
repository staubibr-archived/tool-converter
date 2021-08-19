from components.indexed_list import IndexedList, Index
from components.util import Util


class Info(object):

    def get_simulator(self):
        return self._simulator

    def set_simulator(self, value):
        self._simulator = value

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_type(self):
        return self._type

    def set_type(self, value):
        self._type = value

    simulator = property(get_simulator, set_simulator)
    name = property(get_name, set_name)
    type = property(get_type, set_type)

    def __init__(self, simulator=None, name=None, type=None):
        self._simulator = simulator
        self._name = name
        self._type = type

    def to_json(self):
        return {
            "simulator": self.simulator,
            "name": self.name,
            "type": self.type
        }


class MessageType(object):

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_description(self):
        return self._description

    def set_description(self, value):
        self._description = value

    def get_template(self):
        return self._template

    def set_template(self, value):
        self._template = value

    id = property(get_id, set_id)
    name = property(get_name, set_name)
    description = property(get_description, set_description)
    template = property(get_template, set_template)

    def __init__(self, name=None, template=None, description=None):
        self._id = -1
        self._name = name
        self._description = description
        self._template = template

    def to_json(self):
        return {
            "description": self.description,
            "id": self.id,
            "name": self.name,
            "template": self.template
        }


class ModelType(object):

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_message_type(self):
        return self._message_type

    def set_message_type(self, value):
        self._message_type = value

    def get_type(self):
        return self._type

    def set_type(self, value):
        self._type = value

    def get_port_types(self):
        return self._port_types

    def set_port_types(self, value):
        self._port_types = value

    def get_components(self):
        return self._components

    def set_components(self, value):
        self._components = value

    def get_links(self):
        return self._links

    def set_links(self, value):
        self._links = value

    def get_dim(self):
        return self._dim

    def set_dim(self, value):
        self._dim = value

    def get_index(self):
        return self._index

    id = property(get_id, set_id)
    name = property(get_name, set_name)
    message_type = property(get_message_type, set_message_type)
    type = property(get_type, set_type)
    port_types = property(get_port_types, set_port_types)
    components = property(get_components, set_components)
    links = property(get_links, set_links)
    dim = property(get_dim, set_dim)
    index = property(get_index)

    def __init__(self, name=None, message_type=None, type=None, port_types=None, dim=None, index=None):
        self._id = -1
        self._name = name
        self._message_type = message_type
        self._type = type
        self._port_types = IndexedList() if port_types is None else port_types
        self._components = []
        self._links = []
        self._dim = dim
        self._index = index

    def add_component(self, component):
        self.components.append(component)

    def add_link(self, link):
        self.links.append(link)

    def add_port_type(self, name, type, template):
        exist = self.port_types.get_item([name])

        if exist is not None:
            return exist

        port_type = PortType(name, type, template, self, len(self.port_types))

        return self.port_types.add_item([name], port_type)

    def template_message(self, message):
        templated = {}

        for i in range(len(self.message_type.template)):
            templated[self.message_type.template[i]] = message.values[i]

        return templated

    def to_json(self):
        json = {
            "id": self.id,
            "metadata": {
                "author": -1,
                "created": "",
                "description": "",
                "tags": []
            },
            "name": self.name,
            "ports": [p.to_json() for p in self.port_types],
            "type": self.type
        }

        if self.message_type is not None:
            json["message_type"] = self.message_type.id

        if len(self.links) > 0:
            json["couplings"] = [[l.modelA.index, l.portA.index, l.modelB.index, l.portB.index] for l in self.links]

        if len(self.components) > 0:
            json["components"] = [c.index for c in self.components]

        if self.dim is not None:
            json["dim"] = self.dim.to_json()

        return json


class PortType(object):

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_type(self):
        return self._type

    def set_type(self, value):
        self._type = value

    def get_message_type(self):
        return self._message_type

    def set_message_type(self, value):
        self._message_type = value

    def get_model_type(self):
        return self._model_type

    def set_model_type(self, value):
        self._model_type = value

    def get_index(self):
        return self._index

    name = property(get_name, set_name)
    type = property(get_type, set_type)
    message_type = property(get_message_type, set_message_type)
    model_type = property(get_model_type, set_model_type)
    index = property(get_index)

    def __init__(self, name=None, type=None, message_type=None, model_type=None, index=None):
        self._name = name
        self._type = type
        self._message_type = message_type
        self._model_type = model_type
        self._index = index

    def to_json(self):
        json = {
            "name": self.name,
            "type": self.type
        }

        if self.message_type is not None:
            json["message_type"] = self.message_type.id

        return json


class Link(object):

    def get_model_a(self):
        return self._model_a

    def set_model_a(self, value):
        self._model_a = value

    def get_port_a(self):
        return self._port_a

    def set_port_a(self, value):
        self._port_a = value

    def get_model_b(self):
        return self._model_b

    def set_model_b(self, value):
        self._model_b = value

    def get_port_b(self):
        return self._port_b

    def set_port_b(self, value):
        self._port_b = value

    modelA = property(get_model_a, set_model_a)
    portA = property(get_port_a, set_port_a)
    modelB = property(get_model_b, set_model_b)
    portB = property(get_port_b, set_port_b)

    def __init__(self, modelA=None, portA=None, modelB=None, portB=None):
        self.modelA = modelA
        self.portA = portA
        self.modelB = modelB
        self.portB = portB

    def to_json(self):
        return [self.modelA.index, self.portA.index, self.modelB.index, self.portB.index]


class Component(object):

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    def get_model_type(self):
        return self._model_type

    def set_model_type(self, value):
        self._model_type = value

    def get_index(self):
        return self._index

    def set_index(self, value):
        self._index = value

    id = property(get_id, set_id)
    model_type = property(get_model_type, set_model_type)
    index = property(get_index, set_index)

    def __init__(self, id=None, model_type=None):
        self.id = id
        self.model_type = model_type
        self._index = -1

    def to_json(self):
        return {
            "id": self.id,
            "model_type": self.model_type.index
        }


class Dim(object):
    def get_x(self):
        return self.dim[0]

    def set_x(self, value):
        self.dim[0] = value

    def get_y(self):
        return self.dim[1]

    def set_y(self, value):
        self.dim[1] = value

    def get_z(self):
        return self.dim[2]

    def set_z(self, value):
        self.dim[2] = value

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)

    def __init__(self, x=0, y=0, z=1):
        self.dim = [x, y, z]

    def to_json(self):
        return [self.x, self.y, self.z]

    @staticmethod
    def dim_from_ma(raw):
        dim = raw[1:-1].replace(' ', '').split(',')

        if len(dim) == 2:
            dim.append(1)

        dim = [Util.number_format(d) for d in dim]

        return Dim(dim[0], dim[1], dim[2])

    @staticmethod
    def dim_from_ma_height(dim, raw):
        if dim is None:
            dim = Dim(0, raw, 1)

        else:
            dim.y = Util.number_format(raw)

        return dim

    @staticmethod
    def dim_from_ma_width(dim, raw):
        if dim is None:
            dim = Dim(Util.number_format(raw), 0, 1)

        else:
            dim.x = Util.number_format(raw)

        return dim


class Structure(object):

    def get_simulator(self):
        return self._simulator

    def set_simulator(self, value):
        self._simulator = value

    def get_formalism(self):
        return self._formalism

    def set_formalism(self, value):
        self._formalism = value

    def get_model_types(self):
        return self._model_types

    def set_model_types(self, value):
        self._model_types = value

    def get_components(self):
        return self._components

    def set_components(self, value):
        self._components = value

    simulator = property(get_simulator, set_simulator)
    formalism = property(get_formalism, set_formalism)
    model_types = property(get_model_types, set_model_types)
    components = property(get_components, set_components)

    def __init__(self, simulator=None, formalism=None, model_types=None, message_types=None, components=None):
        self.simulator = simulator or ""
        self.formalism = formalism or ""
        self.model_types = IndexedList() if model_types is None else model_types
        self.message_types = IndexedList() if message_types is None else message_types
        self.components = [] if components is None else components
        self.components_index = Index()

    def add_message_type(self, name, template, description):
        exist = self.message_types.get_item([name])

        if exist is not None:
            return exist

        message_type = MessageType(name, template, description)
        message_type.id = len(self.message_types)

        return self.message_types.add_item([name], message_type)

    def add_model_type(self, name, message_type, type, dim):
        exist = self.model_types.get_item([name])

        if exist is not None:
            return exist

        model_type = ModelType(name, message_type, type, None, dim, len(self.model_types))
        model_type.id = len(self.model_types)

        return self.model_types.add_item([name], model_type)

    def add_component(self, name, model_type):
        node = Component(name, model_type)
        node.index = len(self.components)

        self.components_index.add_item([name], node)
        self.components.append(node)

        return node

    def get_model(self, model_name):
        return self.components_index.get_item([model_name])

    def to_json(self):
        return {
            "top": 1,
            "simulator": self.simulator,
            "formalism": self.formalism,
            "model_types": [i.to_json() for i in self.model_types],
            "message_types": [i.to_json() for i in self.message_types],
            "components": [n.to_json() for n in self.components],
        }
