
class Util(object):
    @staticmethod
    def number_format(s):
        try:
            return int(s)
        except ValueError:
            return float(s)
