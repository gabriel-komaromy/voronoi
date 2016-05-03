import geometry


class Edge(object):
    def __init__(self, start_point):
        self.start_point = start_point
        self.end_point = None
        self.finalized = False

    def __str__(self):
        return str(self.start_point) + " to " + str(self.end_point)


class OpenList(object):
    """Stores the arcs on the beach line"""
    def __init__(self):
        self.start = None

    def update_moving_edges(self, sweep_y):
        current_node = self.start
        if current_node is None:
            pass
        else:
            next_node = current_node.next_node
            while next_node is not None:
                intersections = geometry.breakpoint(
                    current_node.site,
                    next_node.site,
                    sweep_y,
                    )
                new_intersection = self.current_intersection(
                    current_node,
                    next_node,
                    intersections,
                    )
                current_node.set_right_endpoint(new_intersection)
                current_node = next_node
                next_node = next_node.next_node

    def current_intersection(
            self,
            current_node,
            next_node,
            intersections,
            ):
        if len(intersections) == 1:
            # if there's only one intersection
            # then current and next are at same y
            new_intersection = intersections[0]
        elif len(intersections) > 1:
            if intersections[0].x == intersections[1].x:
                # vertical from one of the sites, don't
                # do anything about it for now
                assert intersections[0].x ==\
                    current_node.site.x or\
                    intersections[0].x == next_node.site.x,\
                    "equal x intersections and neither above\
                    one of the sites"
                new_intersection = intersections[0]
            else:
                current_y = current_node.site.y
                """The higher site handles the left
                intersection, the lower site handles
                the right intersection"""
                if current_y > next_node.site.y:
                    new_intersection = intersections[0]
                else:
                    new_intersection = intersections[1]

        else:
            raise ValueError("too many or too few intersections")

        return new_intersection


class SiteNode(object):
    def __init__(self, site):
        self.site = site
        self.previous_node = None
        self.next_node = None
        self.left_edge = None
        self.right_edge = None
        self.circle_minimum = None

    def left_endpoint(self):
        return self.left_edge.start_point

    def set_left_endpoint(self, new_point):
        self.left_edge.start_point = new_point

    def right_endpoint(self):
        return self.right_edge.end_point

    def set_right_endpoint(self, new_point):
        self.right_edge.end_point = new_point

    def has_right_endpoint(self):
        return self.right_edge is not None
