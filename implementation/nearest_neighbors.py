from collections import Counter
import copy
import random

from voronoi import create_diagram
from voronoi import make_point
from data_structures import Edge
from geometry import Point
from geometry import intersects
from geometry import intersection
from plots import plot_diagram


class NearestNeighborsClassifier(object):
    def __init__(self, x_extent, y_extent):
        self.x_extent = x_extent
        self.y_extent = y_extent
        bottom_left = Point(0, 0)
        top_left = Point(0, y_extent)
        top_right = Point(x_extent, y_extent)
        bottom_right = Point(x_extent, 0)
        self.left_edge = Edge(bottom_left, end_point=top_left)
        self.top_edge = Edge(top_left, end_point=top_right)
        self.right_edge = Edge(top_right, end_point=bottom_right)
        self.bottom_edge = Edge(bottom_right, end_point=bottom_left)
        self.box_edges = [
            self.left_edge,
            self.top_edge,
            self.right_edge,
            self.bottom_edge,
            ]

    def train(self, points):
        sites = map(make_point, points)
        site_counts = Counter()
        for site in sites:
            site_counts[site] += 1
        weighted_sites = []
        for site, weight in zip(site_counts.keys(), site_counts.values()):
            site.weight = weight
            weighted_sites.append(site)

        edges, voronoi = create_diagram(weighted_sites)
        site_edges = make_tuples(voronoi)

        boxed_tuples = map(self.make_box, site_edges)
        sorted_tuples = sorted(boxed_tuples, key=lambda bt: lowest_y(bt))
        for st in sorted_tuples:
            print lowest_y(st)
        new_edges = []
        for t in boxed_tuples:
            new_edges += t[1]
        plot_diagram(new_edges, weighted_sites)

        return boxed_tuples

        """
        convert dictionary to list of tuples of (point, edges_list)
        make_box
        sort list of tuples by minimal y-vertex of any edge in the list

        to classify a point:
            do binary search to find the highest y with minimal vertex lower
            than the point
            from there, move up linearly by y, checking if it's in region
            when you find the region:
                if the weight is > k, done
                otherwise, decrement k by weight, remove region from sites,
                    recreate diagram

        make_box(point, edges_list):
            filter out the points that have no edges with None
            box boundaries are:
            (0, 0) to (0, 10)
            (0, 10) to (10, 10)
            (10, 10) to (10, 0)
            (10, 0) to (0, 0)
            check which of the box boundaries each edge with None intersects
            If there are two edges with the same intersected boundary, create
            an edge between the intersections and you're done.
            If there are edges intersecting two different boundaries, make
            an edge from each intersection to the common corner
        """

    def make_box(self, site_edges):
        site = site_edges[0]
        edges = map(copy.deepcopy, site_edges[1])

        def edge_intersects_box(edge):
            for box_edge in self.box_edges:
                if intersects(edge, box_edge):
                    return True
            return False

        filtered_edges = filter(edge_intersects_box, edges)

        edge_collisions = {}
        for box_edge in self.box_edges:
            edge_collisions[box_edge] = []
            for voronoi_edge in filtered_edges:
                if intersects(box_edge, voronoi_edge):
                    edge_collisions[box_edge].append(voronoi_edge)

        unmatched_edges = []
        for box_edge, collision_list in zip(
                edge_collisions.keys(),
                edge_collisions.values(),
                ):
            if len(collision_list) == 0:
                pass
            elif len(collision_list) == 1:
                unmatched_edges.append(
                    (box_edge, collision_list[0]),
                    )
            else:
                new_start = intersection(
                    collision_list[0],
                    box_edge,
                    )
                new_end = intersection(
                    collision_list[1],
                    box_edge,
                    )
                new_edge = Edge(new_start, end_point=new_end)
                edges.append(new_edge)
                break

        if len(unmatched_edges) > 0:
            first_start = unmatched_edges[0][0].start_point
            first_end = unmatched_edges[0][0].end_point
            second_start = unmatched_edges[1][0].start_point
            second_end = unmatched_edges[1][0].end_point
            if first_start == second_start or first_start == second_end:
                common_corner = first_start
            elif first_end == second_start or first_end == second_end:
                common_corner = first_end
            else:
                raise ValueError("no common corner")
            first_intersection = intersection(
                unmatched_edges[0][0],
                unmatched_edges[0][1],
                )
            first_new_edge = Edge(
                first_intersection,
                end_point=common_corner,
                )
            second_intersection = intersection(
                unmatched_edges[1][0],
                unmatched_edges[1][1],
                )
            second_new_edge = Edge(
                second_intersection,
                end_point=common_corner,
                )
            edges.append(first_new_edge)
            edges.append(second_new_edge)

        return (site, edges)

    def classify(self, test_point):
        pass


def lowest_y(site_edge_tuple):
    possible_y = []
    for edge in site_edge_tuple[1]:
        possible_y.append(edge.start_point.y)
        possible_y.append(edge.end_point.y)

    ret = min(possible_y)
    print ret
    return ret


def make_tuples(sites_edges):
    tuples = []
    for site, edges_list in zip(sites_edges.keys(), sites_edges.values()):
        tuples.append((site, edges_list))
    return tuples


if __name__ == '__main__':
    num_points = 10
    points = []
    for _ in xrange(num_points):
        point = (random.uniform(0, 10), random.uniform(0, 10))
        print point
        points.append(point)
    cls = NearestNeighborsClassifier(10, 10)
    cls.train(points)
