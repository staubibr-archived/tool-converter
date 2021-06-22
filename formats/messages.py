from components.indexed_list import IndexedList, Index


class Message(object):

    def get_id(self):
        return self._id

    def get_values(self):
        return self._values

    def set_values(self, values):
        self._values = values

    id = property(get_id)
    values = property(get_values, set_values)

    def __init__(self, id=None, values=None):
        self._id = id
        self._values = {} if values is None else values

    def merge_values(self, values):
        self.values.update(values)

    def to_log(self, structure):
        port = structure.port_index.get_item(self.id)

        return ','.join([port.index] + self.values)


class MessageCA(Message):

    def to_log(self, structure):
        return ','.join(self.id + self.values)


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
        return [self.time] + [m.to_log(structure) for m in self.messages]

    def __iter__(self):
        return iter(self.messages)


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

        for f in self.frames.items:
            content += f.to_log(structure)

        return content

    def __iter__(self):
        return iter(self.frames.items)
