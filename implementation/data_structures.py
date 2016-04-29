class EdgesList(object):
    def __init__(self, start_endpoints, start_cell):
        start = EdgeNode(start_endpoints, None, None, start_cell)
        self.start = start
        self.end = start

    def insert(self, endpoints, twin, cell):
        new_node = EdgeNode(endpoints, self.end, twin, cell)
        self.end = new_node


class EdgeNode(object):
    def __init__(self, endpoints, previous_edge, twin, cell):
        self.endpoints = endpoints
        self.previous_edge = previous_edge
        self.next_edge = None
        if self.previous_edge is not None:
            self.previous_edge.next_edge = self
        self.twin = twin
        if self.twin is not None:
            self.twin.twin = self
        self.cell = cell


class OpenList(object):
    def __init__(self):
        self.start = None

    def insert(self, new_point):
        new_node = PointNode(new_point)
        if self.start is None:
            self.start = new_node
            return
        else:
            self.update_breakpoints(new_point)
            pass
        """
        if self.start.point.x > new_point.x:
            old_start = self.start
            new_node.next_node = old_start
            old_start.previous_node = new_node
            """
        print new_node

    def update_breakpoints(self, new_point):
        pass


class PointNode(object):
    def __init__(self, point):
        self.point = point
        self.previous_node = None
        self.next_node = None
        self.left_region = None
        self.right_region = None


class Region(object):
    def __init__(self, edge):
        self.edge = edge
