from components.indexed_list import IndexedList, Index
from abc import abstractmethod


class Message(object):

    @abstractmethod
    def get_id(self):
        pass

    def get_values(self):
        return self._values

    def set_values(self, values):
        self._values = values

    values = property(get_values, set_values)
    id = property(get_id)

    def __init__(self, values=None):
        self._values = {} if values is None else values

    @abstractmethod
    def to_log(self, structure):
        pass


class MessageState(Message):

    def get_id(self):
        return [self.model.id]

    def get_model(self):
        return self._model

    id = property(get_id)
    model = property(get_model)

    def __init__(self, model=None, values=None):
        super().__init__(values)

        self._model = model

    def to_log(self, structure):
        model_node = structure.components_index.get_item(self.id[0])

        return "{};{}".format(model_node.index, ','.join(self.values))


class MessageOutput(MessageState):

    def get_id(self):
        return [self.model.id, self.port_type.name]

    def get_port_type(self):
        return self._port_type

    id = property(get_id)
    port_type = property(get_port_type)

    def __init__(self, model=None, port_type=None, values=None):
        super().__init__(model, values)

        self._port_type = port_type

    def to_log(self, structure):
        model_node = structure.components_index.get_item(self.id[0])
        port_type = model_node.model_type.port_types.get_item(self.id[1])

        return "{},{};{}".format(model_node.index, port_type.index, ','.join(self.values))


class MessageCA(Message):

    def get_id(self):
        return self.coord

    def get_coord(self):
        return self._coord

    id = property(get_id)
    coord = property(get_coord)

    def __init__(self, coord=None, values=None):
        super().__init__(values)

        self._coord = coord

    def to_log(self, structure):

        return "{};{}".format(','.join(self.coord), ','.join(self.values))


class Frame(object):

    def get_messages(self):
        return self._messages

    def get_time(self):
        return self._time

    time = property(get_time)
    messages = property(get_messages)

    def __init__(self, time=None, messages=None):
        self._time = time
        self._messages = [] if messages is None else messages

    def add_message(self, message):
        self.messages.append(message)

        return message

    def to_log(self, structure):
        return [self.time] + [m.to_log(structure) for m in self]

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)


class Messages(object):

    def get_frames(self):
        return self._frames

    frames = property(get_frames)

    def __init__(self, frames=None):
        self._frames = IndexedList() if frames is None else frames

    def get_frame(self, time):
        return self.frames.get_item([time])

    def add_frame(self, frame):
        f = self.get_frame(frame.time)

        if f is not None:
            return f

        return self.frames.add_item([frame.time], frame)

    def to_log(self, structure):
        content = []

        for f in self:
            content += f.to_log(structure)

        return content

    def __iter__(self):
        return iter(self.frames.items)

    def __len__(self):
        return len(self.frames.items)
