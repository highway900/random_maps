import svgwrite


NODE_STYLE = {
    'stroke_width': 5.0,
    'stroke': 'green',
    'fill': 'grey',
}

EDGE_STYLE = {
    'stroke_width': 10.0,
    'stroke': 'green',
}

PATH_STYLE = {
    'stroke_width': 14,
    'stroke': 'purple',
}


class Scaler(object):
    def __init__(self, mx, my, gx, gy):
        """Scale point u by factor s
        """
        self.sx = mx / gx
        self.sy = my / gy

    def scale(self, u):
        x, y = u
        return (x * self.sx + self.sx / 2, y * self.sy + self.sy / 2)


def _draw_edges(dwg, edges, _sp, style=EDGE_STYLE):
    edges_layer = dwg.add(dwg.g(id="edges", **style))
    for u, v in edges:
        edges_layer.add(dwg.line(start=_sp.scale(u), end=_sp.scale(v)))


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
        mx, my,
        gx, gy,
        filename,
        draw_nodes=True,
        draw_edges=True):

    dwg = svgwrite.Drawing(
        filename='{}.svg'.format(filename),
        size=('{}'.format(mx), '{}'.format(my)),
        viewBox=('0 0 {} {}'.format(mx, my)))

    _sp = Scaler(mx, my, gx, gy)

    _draw_edges(dwg, g.edges_iter(), _sp)
    _draw_nodes(dwg, g, _sp)

    return dwg
