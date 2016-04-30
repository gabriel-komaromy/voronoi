import heapq

from data_structures import OpenList
from data_structures import EdgesList
from data_structures import SiteNode
from data_structures import EdgeNode
from geometry import PointType
from geometry import breakpoint


def create_diagram(sites):
    # Lexicographical ordering of the data points
    ordered_points = list(sites)
    heapq.heapify(ordered_points)

    open_list = OpenList()
    edges_list = EdgesList()

    while ordered_points:
        current_point = next_point(ordered_points)
        if current_point.point_type is PointType.SITE:
            open_list.update_moving_edges(current_point)
            open_list, edges_list = insert_site(
                open_list,
                edges_list,
                current_point,
                )

    return open_list


def next_point(ordered_points):
    return heapq.heappop(ordered_points)


def insert_site(open_list, edges_list, new_site):
    new_node = SiteNode(new_site)
    sweep_y = new_site.y
    if open_list.start is None:
        open_list.start = new_node

    else:
        # need to handle if it goes before start

        current_node = open_list.start.next_node
        while current_node is not None:
            right_endpoint = current_node.right_endpoint()
            if right_endpoint is None:
                # need to handle if it goes after end
                pass

            elif right_endpoint.x < new_site.x:
                current_node = current_node.next_node

            elif right_endpoint.x > new_site.x:
                """
                So now we need:
                Left copy of current node
                Edge
                New node
                Edge
                Right copy of current node

                Left copy of current node should have left_edge
                of current left_edge
                Right copy of current node should have right_edge
                of current right_edge
                """
                current_site = current_node.site
                new_left_node = SiteNode(current_site)
                # TODO handle the edge list crap
                """ idea: the site that an edge holds is
                the edge that its PointNode points to.
                Would have to update edges in both directions
                in update_moving_edges"""
                left_to_new = EdgeNode(breakpoint(
                    current_site,
                    new_site,
                    sweep_y,
                    ))
                new_left_node.right_edge = left_to_new
                new_node.left_edge = left_to_new

                new_right_node = SiteNode(current_site)
                new_to_right = EdgeNode(breakpoint(
                    new_site,
                    current_site,
                    "something",
                    ))
                print new_right_node, new_to_right

                # need to handle if new point is directly below
                # site

            else:
                # handle if new point is directly below endpoint,
                # probably need to just put in new point and
                # not split either adjacent one
                pass

    """
    if self.start.point.x > new_point.x:
        old_start = self.start
        new_node.next_node = old_start
        old_start.previous_node = new_node
        """

    return open_list, edges_list


def print_points(point_list):
    while len(point_list) > 0:
        print heapq.heappop(point_list)
