import abc


class Edge(object):
    __meta__ = abc.ABCMeta

    def __init__(self):
        self._weight = 1

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, x):
        self._weight = x

    def style(self):
        return {
            'stroke': 'blue'
        }

    def __getitem__(self, k):
        return self.__dict__['_{}'.format(k)]

    def __repr__(self):
        return '{}'.format(self.__class__.__name__)


class Block(Edge):
    def __init__(self):
        self.weight = 9999999

    def style(self):
        return {
            'fill': 'black',
            'stroke': 'black',
        }


class Clear(Edge):
    def __init__(self):
        self.weight = 1

    def style(self):
        return {
            'fill': 'grey',
            'stroke': 'green',
            'stroke_width': 8.0,
        }
