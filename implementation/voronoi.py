from Queue import PriorityQueue


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __cmp__(self, other):
        """The sweepline moves up the plane, so we consider points
        with lower y first, and break ties in y by lower x first"""
        if self.y != other.y:
            return self.y - other.y
        else:
            return self.x - other.x

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class LineSegment(object):
    def __init__(self, endpoints):
        assert len(endpoints) == 2
        self.endpoints = endpoints

    def __str__(self):
        return str(self.endpoints[0]) + " to " + str(self.endpoints[1])


def create_diagram(points):
    # Lexicographical ordering of the data points
    ordered_points = PriorityQueue()
    for point in points:
        ordered_points.put(point)
    return ordered_points
