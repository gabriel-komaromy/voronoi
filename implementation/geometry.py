import math

from enum import Enum


def shift_coordinates(func):
    def inner(point1, point2, sweep_y):
        """Transform coordinates so that the sweep y is at 0
        and the left point's x is at 0"""
        left_point, right_point = sort_points(point1, point2)

        x_offset = left_point.x
        y_offset = sweep_y

        left_point = Point(
            left_point.x - x_offset,
            left_point.y - y_offset,
            )
        right_point = Point(
            right_point.x - x_offset,
            right_point.y - y_offset,
            )

        output_list = func(left_point, right_point, sweep_y)

        """Apply inverse transformation to breakpoint"""
        for pos in xrange(len(output_list)):
            output_point = output_list[pos]
            output_list[pos] = Point(
                output_point.x + x_offset,
                output_point.y + y_offset,
                PointType.INTERSECTION,
                )
        return output_list
    return inner


@shift_coordinates
def breakpoint(a, b, sweep_y):
    # print 'finding breakpoint: ' + str(a) + ', ' + str(b)
    # http://www.kmschaal.de/Diplomarbeit_KevinSchaal.pdf

    for point in [a, b]:
        assert point.y >= 0,\
            "Points must be at or above sweepline: " + str(point)

    assert a.y != 0 or b.y != 0,\
        "Need to handle both on sweepline I guess"

    """If the points are horizontally collinear, this returns a list of length 1.
    If they are not, it returns a list of length 2. This would appear to
    oversimplify the problem, but the geometry actually works out favorably for
    us now: any two points with the same y will have equal derivative at any
    time point."""
    if a.y != b.y:
        numerator_beginning = float(a.y * b.x)
        numerator_end = math.sqrt(a.y * b.y * ((a.y - b.y) ** 2 + b.x ** 2))
        denom = a.y - b.y
        intersections_x = [
            (numerator_beginning - numerator_end) / denom,
            (numerator_beginning + numerator_end) / denom,
            ]
        """
        print 'a: ' + str(a)
        print 'b: ' + str(b)
        print 'sweep: ' + str(sweep_y)
        """

        if intersections_x[0] != intersections_x[1]:
            intersections_y = [
                parabola_y(a, intersections_x[0]),
                parabola_y(a, intersections_x[1]),
                ]

        else:
            # vertical line to other parabola
            pol = point_off_line(a, b)
            intersections_y = [parabola_y(pol, intersections_x[0])] * 2
            """
            print intersections_x[0]
            print parabola_y(pol, intersections_x[0])
            """

        output_list = list(sort_points(
            Point(intersections_x[0], intersections_y[0]),
            Point(intersections_x[1], intersections_y[1]),
            ))
        """
        assert output_list[0].x <= output_list[1].x,\
            "break points not sorted: " + str(output_list[0]) + ', ' +\
            str(output_list[1])
            """

    else:
        breakpoint_x = float(b.x - a.x) / 2

        pol = point_off_line(a, b)

        breakpoint_y = parabola_y(pol, breakpoint_x)

        output_list = [Point(
            breakpoint_x,
            breakpoint_y,
            )]

    return output_list


def point_off_line(a, b):
    pol = a
    for position in [0, 1]:
        if [a, b][position].y == 0:
            other_point = [a, b][1 - position]
            pol = other_point
    return pol


def sort_points(point1, point2):
    if point1.x < point2.x:
        left_point = point1
        right_point = point2
    elif point1.x > point2.x:
        right_point = point1
        left_point = point2
    else:
        if point1.y > point2.y:
            left_point = point1
            right_point = point2
        elif point2.y > point1.y:
            left_point = point2
            right_point = point1
        else:
            left_point = point1
            right_point = point2

    return left_point, right_point


def parabola_y(point, x):
    assert point.y != 0,\
        "Can't take parabola y with division by 0" + str(point)
    return float(point.y ** 2 + point.x ** 2 - 2 * x * point.x + x ** 2
                 ) / (2 * point.y)


def collinear(a, b, c):
    # https://math.stackexchange.com/questions/405966/if-i-have-three-points-is-there-an-easy-way-to-tell-if-they-are-collinear
    return (b.y - a.y) * (c.x - b.x) == (c.y - b.y) * (b.x - a.x)


def circle_center_below(a, b, c):
    """Checks that the circle center is below the middle point, still could
    be above the other two or the sweepline"""
    """
    print 'a: ' + str(a)
    print 'b: ' + str(b)
    print 'c: ' + str(c)
    """
    if a == c:
        return False
    # assert a.x < b.x < c.x, "points must have increasing x"
    signed_area = 0.5 * (a.x * b.y + c.x * a.y + b.x * c.y - c.x * b.y -
                         a.y * b.x - a.x * c.y)
    return signed_area < 0


def circle_center(a, b, c):
    assert circle_center_below(a, b, c), "doesn't have a center below"
    y_numerator = float(c.x ** 2 + c.y ** 2 - b.x ** 2 - b.y ** 2) *\
        (a.x - b.x) - (b.x ** 2 + b.y ** 2 - a.x ** 2 - a.y ** 2) *\
        (b.x - c.x)
    y_denominator = 2 * ((a.y - b.y) * (b.x - c.x) - (b.y - c.y) * (
        a.x - b.x))
    y = y_numerator / y_denominator
    x_numerator = float((c.x ** 2 + c.y ** 2 - b.x ** 2 - b.y ** 2) *
                        (a.y - b.y) - (b.x ** 2 + b.y ** 2 - a.x ** 2 - a.y **
                        2) * (b.y - c.y))
    x_denominator = -1 * y_denominator
    x = x_numerator / x_denominator
    return Point(x, y, PointType.INTERSECTION)


def distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def circle_event(a, b, c):
    center = circle_center(a, b, c)
    event = Point(
        center.x,
        center.y - distance(a, center),
        PointType.CIRCLE_EVENT,
        )
    return event, center


class PointType(Enum):
    SITE = 1
    INTERSECTION = 2
    CIRCLE_EVENT = 3
    OTHER = 4


class Point(object):
    def __init__(self, x, y, point_type=PointType.OTHER):
        self.x = x
        self.y = y
        self.point_type = point_type
        self.event_node = None

    def __lt__(self, other):
        if self.y != other.y:
            return self.y > other.y
        else:
            return self.x < other.x

    def __eq__(self, other):
        tolerance = 0.000001
        y_equal = self.y - tolerance < other.y < self.y + tolerance
        x_equal = self.x - tolerance < other.x < self.x + tolerance
        return y_equal and x_equal and self.point_type == other.point_type

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + "), type: " +\
            str(self.point_type)

    def __hash__(self):
        return hash(str(self))


def intersects(edge1, edge2):
    A = edge1.start_point
    B = edge1.end_point
    C = edge2.start_point
    D = edge2.end_point
    for point in [A, B, C, D]:
        if point is None:
            return False

    def ccw(A, B, C):
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def passes_through(edge1, edge2):
    if intersects(edge1, edge2):
        print 'edge 1 start: ' + str(edge1.start_point)
        print 'edge 1 end: ' + str(edge1.end_point)
        print 'edge 2 start: ' + str(edge2.start_point)
        print 'edge 2 end: ' + str(edge2.end_point)
        start_start = edge1.start_point == edge2.start_point
        print 'start_start: ' + str(start_start)
        start_end = edge1.start_point == edge2.end_point
        print 'start_end: ' + str(start_end)
        end_start = edge1.end_point == edge2.start_point
        print 'end_start: ' + str(end_start)
        end_end = edge1.end_point == edge2.end_point
        print 'end_end: ' + str(end_end)
        has_equal_points = start_start or start_end or\
            end_start or end_end
        print 'returning: ' + str(not has_equal_points)
        return not has_equal_points
    else:
        return False
