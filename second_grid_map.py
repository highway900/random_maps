import random
import networkx as nx

from grids import (
    edges,
    grid_map)

from draw.nxsvg import (
    draw_graph,
    _draw_edges,
    Scaler,
    PATH_STYLE)


def get_col(c, y):
    return [((c, i), (c, i+1)) for i in xrange(0, y-1)]

def get_row(r, x):
    return [((r, i), (r, i+1)) for i in xrange(0, x-1)]

if __name__ == '__main__':
    # Image Res XY
    resx = 800
    resy = 400
    # Grid XY Res
    gx = 9
    gy = 6
    g = nx.grid_2d_graph(gx, gy)

    def init_data(g, n):
        g.node[n] = grid_map.Node(resx / gx * 0.1)
        if n == (0, 0) or n == (gx-1, gy-1):
            g.node[n].fill = 'red'
    grid_map.call_nodes(g, init_data)

    b = edges.Block()
    c = edges.Clear()

    for u, v in g.edges():
        g.edge[u][v] = b

    def assign_random_edge(start, end, n_edges, edges):
        for x in xrange(start, end):
            c_edges = get_col(x, gy)
            count = 0
            while count != n_edges:
                u, v = random.choice(edges)
                if g.edge[u][v] != c:
                    g.edge[u][v] = c
                    g.edge[v][u] = c
                    count += 1

    print "after random edge assignement"
    for e in g.edges(data=True):
        print e
    dwg = draw_graph(g, resx, resy, gx, gy, 'second_gmap')
    dwg.save()
