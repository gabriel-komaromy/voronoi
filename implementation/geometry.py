def breakpoint(point1, point2, sweep_y):
    """Transform coordinates so that the sweep y is at 0
    and the left point's x is at 0"""
    if point1.x < point2.x:
        left_point = point1
        right_point = point2
    elif point1.x > point2.x:
        right_point = point1
        left_point = point2
    else:
        raise ValueError("shouldn't be finding breakpoint for lines at same x")

    x_offset = left_point.x
    y_offset = sweep_y
    left_point = Point(left_point.x - x_offset, left_point.y - y_offset)
    right_point = Point(right_point.x - x_offset, right_point.y - y_offset)

    breakpoint = None
    """Apply inverse transformation to breakpoint"""
    breakpoint = Point(breakpoint.x + x_offset, breakpoint.y - y_offset)
    return breakpoint


class Point(object):
    def __init__(self, x, y, point_type):
        self.x = x
        self.y = y
        self.point_type = point_type

    def __cmp__(self, other):
        """The sweepline moves up the plane, so we consider points
        with lower y first, and break ties in y by lower x first"""
        if self.y != other.y:
            return other.y - self.y
        else:
            return self.x - other.x

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x and\
            self.point_type == other.point_type

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + "), type: " +\
            str(self.point_type)


class PointType(Enum):
    SITE = 1
    INTERSECTION = 2


class LineSegment(object):
    def __init__(self, endpoints):
        assert len(endpoints) == 2
        self.endpoints = endpoints

    def __str__(self):
        return str(self.endpoints[0]) + " to " + str(self.endpoints[1])
