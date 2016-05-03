from collections import Counter

from voronoi import create_diagram
from voronoi import make_point


class nearest_neighbors_classifier(object):
    def __init__(self):
        pass

    def train(self, points):
        sites = map(make_point, points)
        site_counts = Counter()
        for site in sites:
            site_counts[site] += 1
        weighted_sites = []
        for site, weight in zip(site_counts.keys(), site_counts.values()):
            site.weight = weight
            weighted_sites.append(site)

        self.diagram = create_diagram(weighted_sites)
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
