import random
import logging


def iterate_pairs(a):
    for i in xrange(0, len(a) - 1):
        yield (a[i], a[i + 1])


def call_nodes(g, f):
    for n in g.nodes_iter():
        f(g, n)


def call_edges(g, f):
    for e in g.edges_iter():
        f(g, e)


def random_blocks(g, u=0, v=10, bias=7, weight=random.random()):
    def f(g, n):
        r = random.randint(u, v)
        if r > bias:
            g.node[n].radius *= 2
            g.node[n].weight = weight
            g.node[n].fill = 'red'
            for e, _ in g.edge[n].items():
                g.edge[n][e] = {'weight': weight}

    call_nodes(g, f)


def remove_node_edges_by_weight(g, weight, exclude_nodes=[]):
    def f(g, n):
        if g.node[n].weight == weight:
            edges = [(n, i) for i in g.edge[n] if n not in exclude_nodes]
            g.remove_edges_from(edges)
            logging.info('Removing edges: {}'.format(edges))
    call_nodes(g, f)


def dist_h(u, v):
    x1, y1 = u
    x2, y2 = v
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def total_path_weight(g, path):
    total = 0
    for e in path:
        total += g.edge[e].weight
    return total


class Node(object):
    def __init__(self, radius):
        self.radius = radius
        self.weight = 1000
        self.fill = 'grey'

    def style(self):
        return {
            'fill': self.fill
        }

    def __repr__(self):
        return "{} {}".format(self.radius, self.weight)


def make_node(r):
    return Node(r)


def print_node(g, n):
    print n


def random_point_path(gx, gy, path, exclude_path=True):
    i = 0
    while True and i < gx * gy:
        _a = (random.randint(0, gx-1), random.randint(0, gy-1))
        if (_a in path) and not exclude_path:
            return _a
        else:
            return _a
        i += 1
        print i, gx*gy


def random_path_node(path, bias):
    return random.choice(path)


def make_bottle_necks(G, paths):
    for path in paths:
        for p in path:
            G.node[p].weight = 999999999
        G.node[random.choice(path)].weight = 1


def set_nodes_weight(G, nodes, weight):
    for n in nodes:
        G.node[n]['weight'] = weight
