
class Index(object):

    def __init__(self):
        self.index = {}

    def add_item(self, keys, item):
        keys = [keys] if type(keys) is str else keys
        index = self.index
        i = 0
        k = keys[i]

        while i < len(keys) - 1:
            if k not in index:
                index[k] = {}

            index = index[k]
            i += 1
            k = keys[i]

        index[k] = item

    def get_item(self, keys):
        keys = [keys] if type(keys) is str else keys
        index = self.index

        for i in range(len(keys)):
            k = keys[i]

            if k not in index:
                return None

            index = index[k]

        return index

    def has_item(self, keys):
        keys = [keys] if type(keys) is str else keys
        index = self.index

        for i in range(len(keys)):
            k = keys[i]

            if k not in index:
                return False

        return True


class IndexedList(Index):

    def get_items(self):
        return self._items

    def set_items(self, value):
        self._items = value

    items = property(get_items, set_items)

    def __init__(self):
        super().__init__()

        self._items = []

    def add_item(self, keys, item):
        super().add_item(keys, item)

        self.items.append(item)

        return item
