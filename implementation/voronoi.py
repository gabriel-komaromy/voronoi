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
            open_list.update_moving_edges(current_point.y)
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
        first_node = open_list.start
        if first_node.right_endpoint().x > new_site.x:
            new_left_node, new_right_node = update_list_pointers(
                open_list,
                edges_list,
                first_node,
                new_site,
                sweep_y,
                )
            open_list.start = new_left_node
            first_node.next_node.previous_node = new_right_node

        else:
            current_node = first_node.next_node

            while current_node is not None:
                right_endpoint = current_node.right_endpoint()
                if right_endpoint is None:
                    # need to handle if it goes after end
                    pass

                elif right_endpoint.x < new_site.x:
                    current_node = current_node.next_node

                elif right_endpoint.x > new_site.x:
                    # TODO handle the edge list crap
                    """idea: the site that an edge holds is
                    the edge that its PointNode points to.
                    Would have to update edges in both directions
                    in update_moving_edges"""

                    new_left_node, new_right_node = update_list_pointers(
                        open_list,
                        edges_list,
                        current_node,
                        new_site,
                        sweep_y,
                        )
                    current_node.previous_node.next_node = new_left_node
                    current_node.next_node.previous_node = new_right_node
                    # TODO: new site directly below existing site

                else:
                    # new site lies directly beneath a current breakpoint
                    new_center_node = SiteNode(new_site)
                    new_center_node.previous_node = current_node
                    right_node = current_node.next_node
                    new_center_node.next_node = right_node
                    right_node.previous_node = new_center_node
                    current_node.next_node = new_center_node
                    current_to_new = EdgeNode(right_endpoint)
                    new_to_right = EdgeNode(right_endpoint)
                    # TODO finalize the old edge between current and right
                    current_node.right_edge = current_to_new
                    new_center_node.left_edge = current_to_new
                    new_center_node.right_edge = new_to_right
                    right_node.left_edge = new_to_right

    """
    if self.start.point.x > new_point.x:
        old_start = self.start
        new_node.next_node = old_start
        old_start.previous_node = new_node
        """

    return open_list, edges_list


def update_list_pointers(
        open_list,
        edge_list,
        current_node,
        new_site,
        sweep_y,
        ):

        current_site = current_node.site
        breakpoints = breakpoint(
            new_site,
            current_site,
            sweep_y,
            )

        new_center_node = SiteNode(new_site)

        new_left_node = SiteNode(current_site)
        new_left_node.left_edge = current_node.left_edge

        left_to_new = EdgeNode(breakpoints[0])
        new_left_node.right_edge = left_to_new
        new_left_node.next_node = new_center_node

        new_center_node.previous_node = new_left_node
        new_center_node.left_edge = left_to_new

        new_right_node = SiteNode(current_site)
        new_to_right = EdgeNode(breakpoints[1])
        new_center_node.right_edge = new_to_right
        new_center_node.next_node = new_right_node
        new_right_node.previous_node = new_center_node
        new_right_node.left_edge = new_to_right
        new_right_node.right_edge = current_node.right_edge
        return new_left_node, new_right_node


def print_points(point_list):
    while len(point_list) > 0:
        print heapq.heappop(point_list)
