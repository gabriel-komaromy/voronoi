import heapq
from enum import Enum


class Point(object):
    def __init__(self, x, y, point_type):
        self.x = x
        self.y = y
        self.point_type = point_type

    def __cmp__(self, other):
        """The sweepline moves up the plane, so we consider points
        with lower y first, and break ties in y by lower x first"""
        if self.y != other.y:
            return self.y - other.y
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


def create_diagram(points):
    # Lexicographical ordering of the data points
    ordered_points = list(points)
    heapq.heapify(ordered_points)
    new_point = Point(1, 2, PointType.INTERSECTION)
    heapq.heappush(ordered_points, new_point)
    print_points(ordered_points)


def next_point(ordered_points):
    return heapq.heappop(ordered_points)


def print_points(point_list):
    while len(point_list) > 0:
        print heapq.heappop(point_list)
