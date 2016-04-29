import math

from enum import Enum


def breakpoint(point1, point2, sweep_y):
    """Transform coordinates so that the sweep y is at 0
    and the left point's x is at 0"""
    # http://www.kmschaal.de/Diplomarbeit_KevinSchaal.pdf

    # need something for when one of the points lies on the line?
    left_point, right_point = sort_points(point1, point2)

    x_offset = left_point.x
    y_offset = sweep_y

    left_point = Point(left_point.x - x_offset, left_point.y - y_offset)
    right_point = Point(right_point.x - x_offset, right_point.y - y_offset)

    if left_point.y != right_point.y:
        breakpoint_x = float(left_point.y * right_point.x - math.sqrt(
            left_point.y * right_point.y * ((
                left_point.y - right_point.y) ** 2 + right_point.x ** 2))) / (
                    left_point.y - right_point.y)
    else:
        breakpoint_x = float(right_point.x - left_point.x) / 2

    breakpoint_y = float(left_point.y ** 2 + left_point.x ** 2 - 2 *
                         breakpoint_x * left_point.x + breakpoint_x ** 2
                         ) / (2 * left_point.y)

    breakpoint = Point(breakpoint_x, breakpoint_y)

    """Apply inverse transformation to breakpoint"""
    breakpoint = Point(breakpoint.x + x_offset, breakpoint.y - y_offset)
    return breakpoint


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
