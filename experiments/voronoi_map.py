import random

from scipy.spatial import Voronoi, KDTree

import networkx as nx

import svgwrite


def iterate_pairs(a):
    for i in xrange(len(a) - 1):
        yield (a[i], a[i + 1])


def sqrd_dist(a, b):
    """Squared distance
    """
    def f(i):
        return (a[i]-b[i])**2
    return f(0) + f(1)


def create_points(n, mi=1.0, ma=10.0, md=20.0, po=2):
    """Create a random set of points with no overlap
    within a random radius.
    Produces a farely uniform distribution of points.
    """
    points = []
    count = 0
    while count < n**po:
        p = (random.randint(mi, ma), random.randint(mi, ma))
        r = random.uniform(mi, md)
        if md > 0:
            if not [i for i in points if sqrd_dist(i, p) < r]:
                points.append(p)
        else:
            points.append(p)
        if count == n:
            break
        count += 1

    return points


colours = [
    'green',
    'red',
    'blue',
    'yellow'
]


mi = 0
ma = 800
n = 800
s = 30  # percentage of points to sample or include in map

# create random set of points.
points = create_points(n, mi, ma, 0)
if len(points) < n:
    print "Not Enough points"
    exit()
# filter points based on predicates. i.e. radius
# pick random point set random radius then remove all points in radius
# keep original point
tree = KDTree(points)
# select a portion of point to merge if they overlap
merge_points = random.sample(points, s)
print "keep {} points".format(len(merge_points))
remove = set()  # set of points to remove

large = 2
rr = [random.uniform(1, 100) for p in merge_points[:-large]]
rr = [random.uniform(100, 400) for p in range(large)] + rr

for p, radius in zip(points, rr):
    # can query a list of points, so could pre-select(random)
    # if 2 of the pre-selected points overlap on query.
    found = tree.query_ball_point(p, radius)
    # print "found {} points in ball query".format(len(found))
    for f in found:
        if points[f] not in merge_points:
            remove.add(points[f])

print "Count before cull", len(points)
points = [p for p in points if p not in remove]
print "Count after cull", len(points)

# Make a graph
g = nx.Graph()
g.add_nodes_from(points)

tree = KDTree(points)
_, start = tree.query([5, 5], 8)
_, end = tree.query([695, 695], 8)

print "start points: {}".format(start)
print "end points: {}".format(end)

for point in points:
    _, neighbours = tree.query(point, 8)  # 3 of the nearest neighbours
    edges = [(point, points[x], random.uniform(0, 10.0)) for x in neighbours]
    if edges:
        g.add_weighted_edges_from(edges)
    else:
        print "No neighbours"

print("Number of subgraphs:", len(list(nx.connected_component_subgraphs(g))))
path = None
i = 0
while not path:
    if i == -1:
        print "Failed to find path"
        exit()
    try:
        path = nx.dijkstra_path(g, points[start[i]], points[end[i]])
        print "path from {} to {}".format(start[0], end[0])
    except Exception:
        i = i - 1
        pass


vor = Voronoi(points)
dwg = svgwrite.Drawing(
    filename='vor.svg',
    size=('{}'.format(ma), '{}'.format(ma)),
    viewBox=('0 0 {} {}'.format(ma, ma)),
    debug=True)

for region in [i for i in vor.regions if -1 not in i]:
    p = [vor.vertices[j] for j in region]
    if p:
        cells = dwg.add(dwg.g(id='cell', fill=random.choice(colours)))
        cells.add(dwg.polyline(points=p))

# Draw the path
# import ipdb;ipdb.set_trace()
for i, p in enumerate(path[:-1]):
    _path = dwg.add(dwg.g(id="path", stroke="black", stroke_width=3))
    _path.add(dwg.line(start=path[i], end=path[i+1]))

dwg.save()
