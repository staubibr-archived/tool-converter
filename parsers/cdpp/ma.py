import os

from components.parser import Parser
from components.indexed_list import IndexedList
from formats.structure import Link, Dim, Structure


class MaSubcomponent(object):

    def get_model(self):
        return self._model

    def set_model(self, value):
        self._model = value

    def get_type(self):
        return self._type

    def set_type(self, value):
        self._type = value

    model = property(get_model, set_model)
    type = property(get_type, set_type)

    def __init__(self, model=None, type=None):
        self.model = model
        self.type = type

    @staticmethod
    def from_ma(raw):
        subs = []

        for s in raw.split():
            split = s.split('@')
            model = split[0]
            typ = split[0] if len(split) == 1 else split[1]

            subs.append(MaSubcomponent(model, typ))

        return subs


class MaPort(object):

    def get_type(self):
        return self._type

    def set_type(self, value):
        self._type = value

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    type = property(get_type, set_type)
    name = property(get_name, set_name)

    def __init__(self, type=None, name=None):
        self.type = type
        self.name = name

    @staticmethod
    def from_ma(type, raw):
        return [MaPort(type, p) for p in raw.split()]


class MaInitialRowValue(object):

    def get_row(self):
        return self._row

    def set_row(self, value):
        self._row = value

    def get_values(self):
        return self._values

    def set_values(self, value):
        self._values = value

    row = property(get_row, set_row)
    values = property(get_values, set_values)

    def __init__(self, row=None, values=None):
        self.row = row
        self.values = [] if values is None else values

    @staticmethod
    def from_ma(raw):
        lr = raw.split()

        return MaInitialRowValue(lr[0], [c for c in lr[1]])


class MaComponent(object):

    def get_atomic_or_coupled(self):
        return "coupled" if len(self.subcomponents) > 0 else "atomic"

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_type(self):
        return self._type

    def set_type(self, value):
        self._type = value

    def get_subcomponents(self):
        return self._subcomponents

    def set_subcomponents(self, value):
        self._subcomponents = value

    def get_links(self):
        return self._links

    def set_links(self, value):
        self._links = value

    def get_ports(self):
        return self._ports

    def set_ports(self, value):
        self._ports = value

    name = property(get_name, set_name)
    type = property(get_type, set_type)
    subcomponents = property(get_subcomponents, set_subcomponents)
    links = property(get_links, set_links)
    ports = property(get_ports, set_ports)

    def __init__(self, name=None, type=None, subcomponents=None, ports=None, links=None):
        self._name = name
        self._type = type
        self._subcomponents = [] if subcomponents is None else subcomponents
        self._ports = IndexedList() if ports is None else ports
        self._links = [] if links is None else links


class MaComponentCA(MaComponent):

    def get_atomic_or_coupled(self):
        return "coupled"

    def get_dim(self):
        return self._dim

    def set_dim(self, value):
        self._dim = value

    def get_width(self):
        return self._dim[0]

    def set_width(self, value):
        self._dim[0] = value

    def get_height(self):
        return self._dim[1]

    def set_height(self, value):
        self._dim[1] = value

    def get_z(self):
        return self._dim[2]

    def set_z(self, value):
        self._dim[2] = value

    def get_initialvalue(self):
        return self._initialvalue

    def set_initialvalue(self, value):
        self._initialvalue = value

    def get_initialrowvalues(self):
        return self._initialrowvalues

    def set_initialrowvalues(self, value):
        self._initialrowvalues = value

    dim = property(get_dim, set_dim)
    width = property(get_width, set_width)
    height = property(get_height, set_height)
    z = property(get_z, set_z)
    initialvalue = property(get_initialvalue, set_initialvalue)
    initialrowvalues = property(get_initialrowvalues, set_initialrowvalues)

    def __init__(self, name=None, type=None, subcomponents=None, ports=None, links=None, dim=None, initialvalue=None, initialrowvalues=None):
        super().__init__(name, type, subcomponents, ports, links)

        self._dim = dim
        self._initialvalue = initialvalue
        self._initialrowvalues = [] if initialrowvalues is None else initialrowvalues

        self.ports.add_item("out", MaPort("output", "out"))


class Ma(Parser):

    def __init__(self, component_class):
        super().__init__()

        self.current = None
        self.content = IndexedList()
        self.component_class = component_class

        c = self.content.add_item("top", self.component_class("top", "top"))

    def get_valid_file(self, files):
        mas = list(filter(lambda f: os.path.splitext(f)[1] == '.ma', files))

        if len(mas) == 0:
            raise ValueError("No .ma file provided. An .ma file is mandatory.")

        if len(mas) > 1:
            raise ValueError("Multiple .ma files were provided. Only a single .ma file can be provided.")

        return mas[0]

    def line_parse(self, line):
        line = line.lower()

        if line.startswith('['):
            # finished processing current model, add all subcomponents as models to process in further iterations
            if self.current is not None:
                for s in self.current.subcomponents:
                    c = self.content.add_item(s.model, self.component_class(s.model, s.type))

            self.current = self.content.get_item(line[1:-1])

        elif self.current is None or line.startswith('%') or ':' not in line:
            return

        else:
            kv = [s.strip() for s in line.split(':')]

            if kv[0] == "components":
                self.current.subcomponents += MaSubcomponent.from_ma(kv[1])

            elif kv[0] == "in":
                for p in MaPort.from_ma("input", kv[1]):
                    self.current.ports.add_item(p.name, p)

            elif kv[0] == "out":
                for p in MaPort.from_ma("output", kv[1]):
                    self.current.ports.add_item(p.name, p)

            elif kv[0] == "neighborports":
                for p in MaPort.from_ma("output", kv[1]):
                    p.name = "out_" + p.name
                    self.current.ports.add_item(p.name, p)

            elif kv[0] == "link":
                self.current.links.append(Link.link_from_ma(self.current.name, kv[1]))

            elif kv[0] == "dim":
                self.current.dim = Dim.dim_from_ma(kv[1])

            elif kv[0] == "height":
                self.current.dim = Dim.dim_from_ma_height(self.current.dim, kv[1])

            elif kv[0] == "width":
                self.current.dim = Dim.dim_from_ma_width(self.current.dim, kv[1])

            elif kv[0] == "initialvalue":
                self.current.initialvalue = kv[1]

            elif kv[0] == "initialrowvalue":
                self.current.initialrowvalues.append(MaInitialRowValue.from_ma(kv[1]))


class MaUtil(object):

    @staticmethod
    def ma_ports_from_links(ma):
        for c in ma.items:
            for l in c.links:
                portsA = ma.get_item(l.modelA).ports
                portsB = ma.get_item(l.modelB).ports

                if portsA.get_item(l.portA) is None:
                    portsA.add_item(l.portA, MaPort("output", l.portA))

                if portsB.get_item(l.portB) is None:
                    portsB.add_item(l.portB, MaPort("input", l.portB))

    @staticmethod
    def ma_to_structure(ma, info):
        s = Structure(info)

        for c in ma.items:
            template = '["' + '","'.join([p.name for p in c.ports.items]) + '"]'

            # This is a bit awkward
            dim = c.dim if hasattr(c, "dim") else None

            model_type = s.add_model_type(c.type.lower(), template, c.get_atomic_or_coupled(), dim)
            model_node = s.add_model_node(c.name, model_type)

            for p in c.ports.items:
                port_type = s.add_port_type(p.name, p.type, '["out"]', model_type)
                port_node = s.add_port_node(model_node, port_type)
                model_type.port_types.append(port_type)

            s.links += c.links

        return s