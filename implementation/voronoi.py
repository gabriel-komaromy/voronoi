import heapq

from data_structures import OpenList
# from data_sturctures import EdgesList
# from geometry import Point
from geometry import PointType


def create_diagram(points):
    # Lexicographical ordering of the data points
    ordered_points = list(points)
    heapq.heapify(ordered_points)

    open_list = OpenList()
    print open_list

    while ordered_points:
        current_point = next_point(ordered_points)
        if current_point.point_type is PointType.SITE:
            pass


def next_point(ordered_points):
    return heapq.heappop(ordered_points)


def print_points(point_list):
    while len(point_list) > 0:
        print heapq.heappop(point_list)
