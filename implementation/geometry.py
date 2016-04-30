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

        output_point = func(left_point, right_point, sweep_y)

        """Apply inverse transformation to breakpoint"""
        output_point = Point(
            output_point.x + x_offset,
            output_point.y - y_offset,
            PointType.INTERSECTION,
            )
        return output_point
    return inner


@shift_coordinates
def breakpoint(left_point, right_point, sweep_y):
    # http://www.kmschaal.de/Diplomarbeit_KevinSchaal.pdf

    for point in [left_point, right_point]:
        assert point.y >= 0,\
            "Points must be at or above sweepline: " + str(point)

    assert left_point.y != 0 or right_point.y != 0,\
        "Need to handle both on sweepline I guess"

    if left_point.y != right_point.y:
        breakpoint_x = float(left_point.y * right_point.x - math.sqrt(
            left_point.y * right_point.y * ((
                left_point.y - right_point.y) ** 2 + right_point.x ** 2))) / (
                    left_point.y - right_point.y)
    else:
        breakpoint_x = float(right_point.x - left_point.x) / 2

    point_off_line = left_point
    for position in [0, 1]:
        if [left_point, right_point][position].y == 0:
            other_point = [left_point, right_point][1 - position]
            point_off_line = other_point

    breakpoint_y = parabola_y(point_off_line, breakpoint_x)

    return Point(
        breakpoint_x,
        breakpoint_y,
        )


def sort_points(point1, point2):
    if point1.x < point2.x:
        left_point = point1
        right_point = point2
    elif point1.x > point2.x:
        right_point = point1
        left_point = point2
    else:
        raise ValueError("shouldn't be finding breakpoint for lines at same x")

    return left_point, right_point


def parabola_y(point, x):
    assert point.y != 0,\
        "Can't take parabola y with division by 0" + str(point)
    return float(point.y ** 2 + point.x ** 2 - 2 * x * point.x + x ** 2
                 ) / (2 * point.y)


def circle_center_below(point1, point2, point3):
    assert point1.x < point2.x < point3.x, "points must have increasing x"
    assert point1.y != point2.y or point2.y != point3.y,\
        "can't be colinear points"
    return point1.y <= point2.y and point3.y <= point2.y


def circle_center(a, b, c):
    assert circle_center_below(a, b, c),\
        "doesn't have a center below"
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
    return Point(x, y)


class PointType(Enum):
    SITE = 1
    INTERSECTION = 2
    OTHER = 3


class Point(object):
    def __init__(self, x, y, point_type=PointType.OTHER):
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


class LineSegment(object):
    def __init__(self, endpoints):
        assert len(endpoints) == 2
        self.endpoints = endpoints

    def __str__(self):
        return str(self.endpoints[0]) + " to " + str(self.endpoints[1])
