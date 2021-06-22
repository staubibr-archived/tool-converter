from abc import abstractmethod


class Parser(object):
    def get_content(self):
        return self._content

    def set_content(self, value):
        self._content = value

    content = property(get_content, set_content)

    def __init__(self):
        self._content = None

    @abstractmethod
    def parse(self, files):
        pass

    @abstractmethod
    def get_valid_file(self, files):
        pass


class FullParser(Parser):

    def parse(self, files):
        file = self.get_valid_file(files)

        if file is None:
            return self.content

        stream = open(file)

        self.full_parse(stream)

        stream.close()

        return self.content

    @abstractmethod
    def get_valid_file(self, files):
        pass

    @abstractmethod
    def full_parse(self, line):
        pass


class LineParser(Parser):

    def parse(self, files):
        file = self.get_valid_file(files)

        if file is None:
            return self.content

        stream = open(file)

        for line in stream:
            if len(line) == 0:
                continue

            self.line_parse(line.strip())

        stream.close()

        return self.content

    @abstractmethod
    def get_valid_file(self, files):
        pass

    @abstractmethod
    def line_parse(self, line):
        pass

