import abc
import networkx as nx
import random


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

    def __getitem__(self, k):
        return self.__dict__['_{}'.format(k)]

    def __repr__(self):
        return '{}'.format(self.__class__.__name__)


class Block(Edge):
    def __init__(self):
        self.weight = 9999999


class Clear(Edge):
    def __init__(self):
        self.weight = 1


def get_col(g, c, y):
    return [((c,i), (c,i+1)) for i in xrange(0, y-2)]


if __name__ == '__main__':
    g = nx.grid_2d_graph(4, 4)

    b = Block()
    c = Clear()

    mx = 5
    my = 5

    for u, v in g.edges():
        g.edge[u][v] = b


    for col in xrange(0, mx-1):
        c_edges = get_col(g, col, my)
        count = 0
        while count != 2:
            u, v = random.choice(c_edges)
            if g.edge[u][v] != c:
                g.edge[u][v] = c
                count += 1

    for _, _, d in g.edges(data=True):
        print d
