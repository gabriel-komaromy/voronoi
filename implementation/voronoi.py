import heapq

from data_structures import OpenList
# from data_structures import EdgesList
from data_structures import SiteNode
from data_structures import Edge
from geometry import Point
from geometry import PointType
from geometry import breakpoint
from geometry import circle_center_below
from geometry import circle_event
from geometry import circle_center


def create_diagram(sites):
    # Lexicographical ordering of the data points
    ordered_points = list(sites)
    heapq.heapify(ordered_points)

    open_list = OpenList()
    # edges_list = EdgesList()
    edges_list = []

    while ordered_points:
        # print 'looping'
        current_point = next_point(ordered_points)
        # print current_point
        if current_point.point_type is PointType.SITE:
            open_list.update_moving_edges(current_point.y)
            open_list, edges_list, new_node = insert_site(
                open_list,
                edges_list,
                current_point,
                )
            ordered_points = update_circle_points(
                new_node,
                ordered_points,
                )
            heapq.heapify(ordered_points)
        elif current_point.point_type is PointType.CIRCLE_EVENT:
            open_list.update_moving_edges(current_point.y)
            middle_node = current_point.event_node
            middle_site = middle_node.site
            left_node = middle_node.previous_site
            left_site = left_node.site
            right_node = middle_node.next_site
            right_site = right_node.site
            center_point = circle_center(left_site, middle_site, right_site)

            """Next two lines maybe unnecessary"""
            middle_node.set_left_endpoint(center_point)
            middle_node.set_right_endpoint(center_point)
            middle_node.left_edge.finalized = True
            print middle_node.left_edge
            middle_node.right_edge.finalized = True
            print middle_node.right_edge
            left_node.right_edge.finalized = True
            print left_node.right_edge
            right_node.left_edge.finalized = True
            print right_node.left_edge

            new_edge = Edge(circle_center)
            left_node.right_edge = new_edge
            right_node.left_edge = new_edge
            left_node.next_node = right_node
            right_node.previous_node = left_node
            edges_list.append(new_edge)
            ordered_points = update_circle_points(
                left_node,
                ordered_points,
                )
            ordered_points = update_circle_points(
                right_node,
                ordered_points,
                )

        else:
            raise ValueError("unexpected point type")

    return edges_list


def update_circle_points(new_node, ordered_points):
    relevant_nodes = [None] * 5
    relevant_nodes[2] = new_node
    relevant_nodes[1] = new_node.previous_node
    relevant_nodes[3] = new_node.next_node
    if relevant_nodes[1] is not None:
        relevant_nodes[0] = relevant_nodes[1].previous_node
    if relevant_nodes[3] is not None:
        relevant_nodes[4] = relevant_nodes[3].next_node

    for middle_node in xrange(1, 4):
        if relevant_nodes[middle_node - 1] is not None and\
                relevant_nodes[middle_node + 1] is not None:

            a = relevant_nodes[middle_node - 1]
            b = relevant_nodes[middle_node]
            c = relevant_nodes[middle_node + 1]
            previous_event = b.circle_minimum

            if circle_center_below(a.site, b.site, c.site):
                event, center = circle_event(a.site, b.site, c.site)
                event.event_node = b
                if event != previous_event:
                    if previous_event is not None:
                        ordered_points.remove(previous_event)
                    b.circle_minimum = event
                    ordered_points.append(event)
            else:
                if b.circle_minimum is not None:
                    ordered_points.remove(b.circle_minimum)
                    b.circle_minimum = None

    return ordered_points


def next_point(ordered_points):
    return heapq.heappop(ordered_points)


def insert_site(open_list, edges_list, new_site):
    print new_site
    new_node = SiteNode(new_site)
    sweep_y = new_site.y
    if open_list.start is None:
        open_list.start = new_node

    else:
        first_node = open_list.start
        if first_node.right_edge is not None:
            if first_node.right_endpoint().x > new_site.x:
                new_left_node, new_right_node = split_node(
                    open_list,
                    edges_list,
                    first_node,
                    new_site,
                    sweep_y,
                    )
                open_list.start = new_left_node
                new_node = new_left_node.next_node
                first_node.next_node.previous_node = new_right_node

            else:
                current_node = first_node.next_node

                while True:
                    if current_node.next_node is None:
                        new_left_node, new_right_node, edges_list = split_node(
                            open_list,
                            edges_list,
                            current_node,
                            new_site,
                            sweep_y,
                            )
                        new_node = new_left_node.next_node
                        current_node.previous_node.next_node = new_left_node
                        break

                    right_endpoint = current_node.right_endpoint()

                    if right_endpoint.x < new_site.x:
                        current_node = current_node.next_node
                        print 'continuing'
                        continue

                    elif right_endpoint.x > new_site.x:
                        new_left_node, new_right_node, edges_list = split_node(
                            open_list,
                            edges_list,
                            current_node,
                            new_site,
                            sweep_y,
                            )
                        current_node.previous_node.next_node = new_left_node
                        new_node = new_left_node.next_node
                        current_node.next_node.previous_node = new_right_node
                        break

                    else:
                        """new site lies directly beneath a current breakpoint,
                        can't really use the function unfortunately"""
                        new_center_node = SiteNode(new_site)
                        new_center_node.previous_node = current_node
                        right_node = current_node.next_node
                        new_center_node.next_node = right_node
                        right_node.previous_node = new_center_node
                        current_node.next_node = new_center_node
                        current_to_new = Edge(right_endpoint)
                        new_to_right = Edge(right_endpoint)
                        edges_list.append(current_to_new)
                        edges_list.append(new_to_right)
                        current_node.right_edge.finalized = True
                        right_node.left_edge.finalized = True
                        current_node.right_edge = current_to_new
                        new_center_node.left_edge = current_to_new
                        new_center_node.right_edge = new_to_right
                        right_node.left_edge = new_to_right
                        new_node = new_center_node
                        break

        else:
            new_left_node, new_right_node, edges_list = split_node(
                open_list,
                edges_list,
                first_node,
                new_site,
                sweep_y,
                )
            new_node = new_left_node.next_node
            open_list.start = new_left_node

    return open_list, edges_list, new_node


def split_node(
        open_list,
        edges_list,
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

        left_to_new = Edge(breakpoints[0])
        edges_list.append(left_to_new)
        new_left_node.right_edge = left_to_new
        new_left_node.next_node = new_center_node

        new_center_node.previous_node = new_left_node
        new_center_node.left_edge = left_to_new

        new_right_node = SiteNode(current_site)
        new_to_right = Edge(breakpoints[1])
        edges_list.append(new_to_right)
        new_center_node.right_edge = new_to_right
        new_center_node.next_node = new_right_node
        new_right_node.previous_node = new_center_node
        new_right_node.left_edge = new_to_right
        new_right_node.right_edge = current_node.right_edge
        return new_left_node, new_right_node, edges_list


def print_points(point_list):
    while len(point_list) > 0:
        print heapq.heappop(point_list)


if __name__ == '__main__':
    points = [(3, 3), (0, 10), (9, 0), (4, 7), (4, 5)]

    def make_point(entry):
        return Point(
            entry[0],
            entry[1],
            PointType.SITE,
            )
    output = create_diagram(map(make_point, points))
    for edge in output:
        print edge
