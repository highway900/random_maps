import networkx as nx

from nxsvg import (
    draw_graph,
    _draw_edges,
    Scaler,
    PATH_STYLE)


def main():
    mx = 800
    my = 400
    gx = 10
    gy = 5
    G = nx.grid_2d_graph(gx, gy)

    def init_data(g, n):
        g.node[n] = make_node(8)
    call_nodes(G, init_data)

    random_blocks(G, bias=3, weight=random.randint(300, 500))
    random_blocks(G, bias=9, weight=300)

    start = (0, 0)
    end = (gx-1, gy-1)

    dwg = draw_graph(G, mx, my, gx, gy, 'graph')

    dwg.save()

    cols = []
    for c in xrange(gx-1):
        cols.append([(c, r) for r in xrange(gy-1)])
    make_bottle_necks(G, cols)

    main_path = list(iterate_pairs(nx.astar_path(G, start, end, dist_h)))

    avoid_G = G.copy()
    set_nodes_weight(avoid_G, main_path, 9999999)

    _sp = Scaler(mx, my, gx, gy)
    a = random_point_path(gx, gy, main_path, False)
    b = random_point_path(gx, gy, main_path, True)
    try:
        path1 = iterate_pairs(nx.astar_path(avoid_G, a, b, dist_h))
        _draw_edges(dwg, path1, _sp, style=PATH_STYLE)
        path2 = iterate_pairs(nx.astar_path(avoid_G, b, end, dist_h))
        PATH_STYLE.update([('stroke', 'blue')])
        _draw_edges(dwg, path2, _sp, style=PATH_STYLE)
    except nx.exception.NetworkXNoPath:
        logging.error('unable to find path {}'.format([start, a, end]))

    PATH_STYLE.update([('stroke', 'red')])
    _draw_edges(dwg, main_path, _sp, style=PATH_STYLE)
    dwg.save()


main()
