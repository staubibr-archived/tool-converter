import os
import re

from components.parser import Parser
from components.util import Util
from formats.style import Style, Bucket


class Pal(Parser):

    def __init__(self):
        super().__init__()

        self.line_parse_fn = self.line_parse_a
        self.content = Style()
        self.i = 0

    def get_valid_file(self, files):
        pal = list(filter(lambda f: os.path.splitext(f)[1] == '.pal', files))

        if len(pal) > 1:
            raise ValueError("Multiple .pal files were provided. Only a single .pal file can be provided.")

        return pal[0] if len(pal) == 1 else None

    def line_parse(self, line):
        if line == "VALIDSAVEDFILE":
            self.line_parse_fn = self.line_parse_b

        elif line == '':
            return None

        else:
            self.line_parse_fn(line)

    def line_parse_a(self, line):
        # [-0.1;0.9] 255 255 51
        # [-1.1;-0.9] 153 255 255
        # ...
        self.content.buckets.append(Bucket.bucket_from_pal_a(line))

    def line_parse_b(self, line):
        # VALIDSAVEDFILE
        # 169,169,169
        # ...
        # 4.0,4.9
        split = [s.strip() for s in line.split(',')]
        # split = [Util.number_format(c) for c in split]

        if len(split) == 3:
            self.content.buckets.append(Bucket(None, None, split))

        else:
            self.content.buckets[self.i].start = split[0]
            self.content.buckets[self.i].end = split[1]
            self.i += 1
