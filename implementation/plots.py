import matplotlib.pyplot as plt
from matplotlib import collections as mc


def edge_to_list(edge):
    if edge.start_point is None or edge.end_point is None:
        return []

    start = (edge.start_point.x, edge.start_point.y)
    end = (edge.end_point.x, edge.end_point.y)
    return [start, end]


def point_to_site(point):
    return (point.x, point.y)


def plot_diagram(edges, points):
    lines = map(
        edge_to_list,
        edges,
        )
    lines = filter(lambda line: line, lines)
    sites = map(point_to_site, points)
    x, y = zip(*sites)
    plt.scatter(x, y)
    lc = mc.LineCollection(lines, linewidths=2)
    ax = plt.axes()
    ax.set_xlim((-1, 11))
    ax.set_ylim((-1, 11))
    ax.add_collection(lc)
    ax.margins(0.1)
    plt.show()
