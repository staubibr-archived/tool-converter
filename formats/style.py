import re

from components.util import Util


class Bucket(object):

    def get_start(self):
        return self._start

    def set_start(self, value):
        self._start = value

    def get_end(self):
        return self._end

    def set_end(self, value):
        self._end = value

    def get_color(self):
        return self._color

    def set_color(self, value):
        self._color = value

    start = property(get_start, set_start)
    end = property(get_end, set_end)
    color = property(get_color, set_color)

    def __init__(self, start=None, end=None, color=None):
        super().__init__()

        self._start = start
        self._end = end
        self._color = color

    def to_json(self):
        return {
            "start": self.start,
            "end": self.end,
            "color": [int(c) for c in self.color]
        }

    @staticmethod
    def bucket_from_pal_a(line):
        split = re.split(r'[,;\[\] ]+', line[1:])
        split = [Util.number_format(c) for c in split]

        return Bucket(split[0], split[1], [split[2], split[3], split[4]])


class Style(object):

    def get_buckets(self):
        return self._buckets

    def set_buckets(self, value):
        self._buckets = value

    buckets = property(get_buckets, set_buckets)

    def __init__(self, buckets=None):
        super().__init__()

        self._buckets = [] if buckets is None else buckets

    def to_json(self):
        return [{
            "buckets": [b.to_json() for b in self.buckets]
        }]
