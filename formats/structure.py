import json

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


class ModelType(object):

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_template(self):
        return self._template

    def set_template(self, value):
        self._template = value

    def get_type(self):
        return self._type

    def set_type(self, value):
        self._type = value

    def get_port_types(self):
        return self._port_types

    def set_port_types(self, value):
        self._port_types = value

    def get_dim(self):
        return self._dim

    def set_dim(self, value):
        self._dim = value

    def get_index(self):
        return self._index

    name = property(get_name, set_name)
    template = property(get_template, set_template)
    type = property(get_type, set_type)
    port_types = property(get_port_types, set_port_types)
    dim = property(get_dim, set_dim)
    index = property(get_index)

    def __init__(self, name=None, template=None, type=None, port_types=None, dim=None, index=0):
        self._name = name
        self._template = template
        self._type = type
        self._port_types = [] if port_types is None else port_types
        self._dim = dim
        self._index = index

    def template_message(self, message):
        template = json.loads(self.template)
        templated = {}

        for i in range(len(template)):
            templated[template[i]] = message.values[i]

        return templated

    def to_json(self):
        json = {
            "name": self.name,
            "template": self.template,
            "type": self.type
        }

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

    def get_template(self):
        return self._template

    def set_template(self, value):
        self._template = value

    def get_model_type(self):
        return self._model_type

    def set_model_type(self, value):
        self._model_type = value

    def get_index(self):
        return self._index

    name = property(get_name, set_name)
    type = property(get_type, set_type)
    template = property(get_template, set_template)
    model_type = property(get_model_type, set_model_type)
    index = property(get_index)

    def __init__(self, name=None, type=None, template=None, model_type=None, index=0):
        self._name = name
        self._type = type
        self._template = template
        self._model_type = model_type
        self._index = index

    def to_json(self):
        return {
            "name": self.name,
            "type": self.type,
            "template": self.template,
            "model_type": self.model_type.index
        }


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
        return {
            "modelA": self.modelA,
            "portA": self.portA,
            "modelB": self.modelB,
            "portB": self.portB
        }

    @staticmethod
    def link_from_ma(component, raw):
        lr = raw.split(' ')
        l_split = lr[0].split('@')
        r_split = lr[1].split('@')

        if len(l_split) == 1:
            l_split.append(component)

        if len(r_split) == 1:
            r_split.append(component)

        return Link(l_split[1], l_split[0], r_split[1], r_split[0])


class ModelNode(object):

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

    def __init__(self, id=None, model_type=None, index=None):
        self.id = id
        self.model_type = model_type
        self._index = index

    def to_json(self):
        return {
            "id": self.id,
            "model_type": self.model_type
        }


class PortNode(object):

    def get_model(self):
        return self._model

    def set_model(self, value):
        self._model = value

    def get_port_type(self):
        return self._port_type

    def set_port_type(self, value):
        self._port_type = value

    def get_index(self):
        return self._index

    def set_index(self, value):
        self._index = value

    model = property(get_model, set_model)
    port_type = property(get_port_type, set_port_type)
    index = property(get_index, set_index)

    def __init__(self, model=None, port_type=None, index=None):
        self.model = model
        self.port_type = port_type
        self._index = index

    def to_json(self):
        return {
            "model_id": self.model,
            "port_type": self.port_type
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
            dim = Dim("0", raw, "1")

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

    def get_info(self):
        return self._info

    def set_info(self, value):
        self._info = value

    def get_model_types(self):
        return self._model_types

    def set_model_types(self, value):
        self._model_types = value

    def get_port_types(self):
        return self._port_types

    def set_port_types(self, value):
        self._port_types = value

    def get_nodes(self):
        return self._nodes

    def set_nodes(self, value):
        self._nodes = value

    def get_links(self):
        return self._links

    def set_links(self, value):
        self._links = value

    info = property(get_info, set_info)
    model_types = property(get_model_types, set_model_types)
    port_types = property(get_port_types, set_port_types)
    nodes = property(get_nodes, set_nodes)
    links = property(get_links, set_links)

    def __init__(self, info=None, model_types=None, port_types=None, nodes=None, links=None):
        self.info = Info() if info is None else info
        self.model_types = IndexedList() if model_types is None else model_types
        self.port_types = IndexedList() if port_types is None else port_types
        self.nodes = [] if nodes is None else nodes
        self.links = [] if links is None else links
        self.model_index = Index()
        self.port_index = Index()

    def add_model_type(self, name, template, type, dim):
        exist = self.model_types.get_item([name])

        if exist is not None:
            return exist

        model_type = ModelType(name, template, type, None, dim, len(self.model_types.items))

        return self.model_types.add_item([name], model_type)

    def add_model_node(self, name, model_type):
        node = ModelNode(name, model_type.index, str(len(self.nodes)))

        self.model_index.add_item([name], node)
        self.nodes.append(node)

        return node

    def get_model(self, model_name):
        return self.model_index.get_item([model_name])

    def add_port_type(self, name, type, template, model_type):
        exist = self.port_types.get_item([model_type.name, name])

        if exist is not None:
            return exist

        port_type = PortType(name, type, template, model_type, len(self.port_types.items))

        return self.port_types.add_item([model_type.name, name], port_type)

    def add_port_node(self, model_node, port_type):
        node = PortNode(model_node.id, port_type.index, str(len(self.nodes)))

        self.port_index.add_item([model_node.id, port_type.name], node)
        self.nodes.append(node)

        return node

    def get_port(self, model_name, port_name):
        return self.port_index.get_item([model_name, port_name])

    def to_json(self):
        return {
            "info": self.info.to_json(),
            "model_types": [i.to_json() for i in self.model_types.items],
            "port_types": [p.to_json() for p in self.port_types.items],
            "nodes": [n.to_json() for n in self.nodes],
            "links": [l.to_json() for l in self.links],
        }
