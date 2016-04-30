import geometry


class EdgesList(object):
    def __init__(self):
        self.start = None
        self.end = self.start

    def insert(self, start_point, site):
        if self.start is None:
            self.start = EdgeNode(
                start_point,
                None,
                site,
                )
            self.end = self.start
            return self.start

        else:
            new_node = EdgeNode(start_point, self.end, site)
            self.end = new_node
            return new_node


class EdgeNode(object):
    def __init__(self, start_point, previous_edge, site):
        self.start_point = start_point
        self.end_point = None
        self.previous_edge = previous_edge
        self.next_edge = None
        if self.previous_edge is not None:
            self.previous_edge.next_edge = self
        self.twin = None
        """
        if self.twin is not None:
            self.twin.twin = self
            """
        self.site = site


class OpenList(object):
    """Stores the arcs on the beach line"""
    def __init__(self):
        self.start = None

    def update_moving_edges(self, new_site):
        current_node = self.start
        if current_node is None:
            pass
        else:
            sweep_y = new_site.y
            next_node = current_node.next_node
            while next_node is not None:
                new_intersection = geometry.breakpoint(
                    current_node.site,
                    next_node.site,
                    sweep_y,
                    )
                current_node.set_right_endpoint(new_intersection)
                current_node = next_node
                next_node = next_node.next_node


class SiteNode(object):
    def __init__(self, site):
        self.site = site
        self.previous_node = None
        self.next_node = None
        self.left_edge = None
        self.right_edge = None

    def right_endpoint(self):
        return self.right_edge.edge.end_point

    def set_right_endpoint(self, new_point):
        self.right_edge.edge.end_point = new_point
