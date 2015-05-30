import random
import networkx as nx

from nxsvg import (
    draw_graph,
    _draw_edges,
    Scaler,
    PATH_STYLE)


def iterate_pairs(a):
    for i in xrange(len(a) - 1):
        yield (a[i], a[i + 1])


def random_blocks(g, u=0, v=10, w=7, value=random.random()):
    def r(g, n):
        r = random.randint(u, v)
        if r > w:
            g.node[n].radius = r
            g.node[n].weight = value
            g.node[n].fill = 'red'

            for e, _ in g.edge[n].items():
                g.edge[n][e] = {'weight': value}
    call_nodes(g, r)


def create_nx_grid(gx=5, gy=5):
    G = nx.grid_2d_graph(gx, gy)
    print nx.info(G)
    return G


def call_nodes(g, f):
    for n in g.nodes_iter():
        f(g, n)


def dist_h(u, v):
    x1, y1 = u
    x2, y2 = v
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class Node(object):
    def __init__(self, radius):
        self.radius = radius
        self.weight = 0.1
        self.fill = 'grey'

    def style(self):
        return {
            'fill': self.fill
        }

    def __repr__(self):
        print self.radius, self.weight


def make_node(r):
    return Node(r)


def main():
    mx = 800
    my = 400
    gx = 30
    gy = 15
    G = create_nx_grid(gx, gy)

    def init_data(g, n):
        for n in g.nodes_iter():
            g.node[n] = make_node(8)

    call_nodes(G, init_data)
    random_blocks(G, w=7, value=30)
    random_blocks(G, w=9, value=300)

    def print_node(g, n):
        print n

    call_nodes(G, print_node)

    start = (0, 0)
    a = (random.randint(0, gx-1), random.randint(0, gy-1))
    end = (gx-1, gy-1)

    dwg = draw_graph(G, mx, my, gx, gy, 'graph')

    dwg.save()

    # Draw the path
    path1 = iterate_pairs(nx.astar_path(G, start, a, dist_h))
    path2 = iterate_pairs(nx.astar_path(G, a, end, dist_h))
    path3 = iterate_pairs(nx.astar_path(G, start, end, dist_h))

    _sp = Scaler(mx, my, gx, gy)
    _draw_edges(dwg, path1, _sp, style=PATH_STYLE)
    PATH_STYLE.update([('stroke', 'blue')])
    _draw_edges(
        dwg, path2, _sp, style=PATH_STYLE)

    PATH_STYLE.update([('stroke', 'red')])
    _draw_edges(
        dwg, path3, _sp, style=PATH_STYLE)

    dwg.save()


main()
