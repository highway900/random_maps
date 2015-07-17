import svgwrite


NODE_STYLE = {
    'stroke_width': 5.0,
    'stroke': 'green',
    'fill': 'grey',
}

EDGE_STYLE = {
    'stroke_width': 5.0,
    'stroke': 'green',
}

PATH_STYLE = {
    'stroke_width': 14,
    'stroke': 'purple',
}


class Scaler(object):
    def __init__(self, resX, resY, gx, gy):
        """Scale point u by factor s
        """
        self.sx = resX / gx
        self.sy = resY / gy

    def scale(self, u):
        x, y = u
        return (x * self.sx + self.sx / 2, y * self.sy + self.sy / 2)


def _draw_edges(dwg, g, edges, _sp, style=EDGE_STYLE):
    edges_layer = dwg.add(dwg.g(id="edges"))
    for u, v in edges:
        # print u, v, g.edge[u][v]
        edges_layer.add(
            dwg.line(
                start=_sp.scale(u),
                end=_sp.scale(v),
                **g.edge[u][v].style()))


def _draw_nodes(dwg, g, _sp, style=NODE_STYLE):
    nodes_layer = dwg.add(dwg.g(id="nodes", **style))
    for n, d in g.nodes_iter(data=True):
        x, y = n
        nodes_layer.add(dwg.circle(
            center=_sp.scale(n),
            r=d.radius,
            **d.style()))


def draw_graph(
        g,
        resX, resY,
        gx, gy,
        filename,
        draw_nodes=True,
        draw_edges=True):

    dwg = svgwrite.Drawing(
        filename='{}.svg'.format(filename),
        size=('{}'.format(resX), '{}'.format(resY)),
        viewBox=('0 0 {} {}'.format(resX, resY)))

    _sp = Scaler(resX, resY, gx, gy)

    _draw_edges(dwg, g, g.edges(), _sp)
    _draw_nodes(dwg, g, _sp)

    return dwg
