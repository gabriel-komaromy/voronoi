import heapq


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

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

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
    ordered_points = list(points)
    heapq.heapify(ordered_points)
    deleted_points = set()
    deleted_points = delete_point(Point(1, 0), deleted_points)
    print_undeleted_points(ordered_points, deleted_points)


def next_point(ordered_points, deleted_points):
    while True:
        popped_point = heapq.heappop(ordered_points)
        if not is_deleted(popped_point, deleted_points):
            break
    return popped_point


def is_deleted(point, deleted_points):
    return str(point) in deleted_points


def delete_point(point, deleted_points):
    deleted_points.add(str(point))
    return deleted_points


def print_undeleted_points(point_list, deleted_points):
    while len(point_list) > 0:
        next_point = heapq.heappop(point_list)
        if not is_deleted(next_point, deleted_points):
            print next_point
