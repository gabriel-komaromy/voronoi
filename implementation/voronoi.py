import heapq
# import random

from data_structures import OpenList
from data_structures import SiteNode
from data_structures import Edge
from geometry import Point
from geometry import PointType
from geometry import breakpoint
from geometry import circle_center_below
from geometry import circle_event
from geometry import circle_center
from geometry import passes_through
from plots import plot_diagram


def create_diagram(sites):
    # Lexicographical ordering of the data points
    ordered_points = list(sites)
    heapq.heapify(ordered_points)
    voronoi_regions = {}

    open_list = OpenList()
    edges_list = []

    while ordered_points:
        heapq.heapify(ordered_points)
        current_point = next_point(ordered_points)
        heapq.heapify(ordered_points)

        open_list.update_moving_edges(current_point.y)
        heapq.heapify(ordered_points)

        sweep_x = current_point.x
        sweep_y = current_point.y
        if current_point.point_type is PointType.SITE:
            voronoi_regions[current_point] = []
            open_list, edges_list, new_node, voronoi_regions = insert_site(
                open_list,
                edges_list,
                current_point,
                voronoi_regions
                )

            ordered_points = update_circle_points(
                new_node,
                ordered_points,
                sweep_x,
                sweep_y,
                )
            heapq.heapify(ordered_points)

        elif current_point.point_type is PointType.CIRCLE_EVENT:
            middle_node = current_point.event_node
            middle_site = middle_node.site
            left_node = middle_node.previous_node
            left_site = left_node.site
            right_node = middle_node.next_node
            right_site = right_node.site
            center_point = circle_center(left_site, middle_site, right_site)

            middle_node.left_edge.finalized = True
            middle_node.right_edge.finalized = True
            left_node.right_edge.finalized = True
            right_node.left_edge.finalized = True

            new_edge = Edge(center_point)
            voronoi_regions[left_node.site].append(new_edge)
            voronoi_regions[right_node.site].append(new_edge)
            left_node.right_edge = new_edge
            right_node.left_edge = new_edge
            left_node.next_node = right_node
            right_node.previous_node = left_node
            edges_list.append(new_edge)
            heapq.heapify(ordered_points)
            ordered_points = update_circle_points(
                left_node,
                ordered_points,
                sweep_x,
                sweep_y,
                )

            ordered_points = update_circle_points(
                right_node,
                ordered_points,
                sweep_x,
                sweep_y,
                )

            current_node = open_list.start
            while current_node is not None:
                if current_node.circle_minimum is not None:
                    if current_point == current_node.circle_minimum:
                        current_node.circle_minimum = None
                current_node = current_node.next_node

        else:
            raise ValueError("unexpected point type")

        heapq.heapify(ordered_points)

    edges_list = post_processing(
        edges_list,
        open_list,
        sweep_y,
        )

    return edges_list, voronoi_regions


def post_processing(edges_list, open_list, sweep_y):
    # go back through and extend edges that still say None
    sweep_y = sweep_y - 10
    remaining_node = open_list.start
    while remaining_node is not None:
        if remaining_node.right_edge is not None:
            current_edge = remaining_node.right_edge
            if current_edge.end_point is None:
                breakpoints = breakpoint(
                    remaining_node.site,
                    remaining_node.next_node.site,
                    sweep_y,
                    )
                current_edge = check_intersections(
                    breakpoints,
                    current_edge,
                    edges_list,
                    )

        remaining_node = remaining_node.next_node
    return edges_list


def check_intersections(breakpoints, current_edge, edges_list):
    if len(breakpoints) > 1:
        for new_point in breakpoints:
            if new_point > current_edge.start_point:
                candidate_new_edge = Edge(
                    current_edge.start_point,
                    )
                candidate_new_edge.end_point = new_point
                intersected = False
                for edge in edges_list:
                    if passes_through(
                            edge,
                            candidate_new_edge,
                            ):
                        intersected = True
                if not intersected:
                    current_edge.end_point = new_point
    return current_edge


def update_circle_points(new_node, ordered_points, sweep_x, sweep_y):
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
                if event.y > sweep_y:
                    pass
                elif event.y == sweep_y and event.x <= sweep_x:
                    pass
                else:
                    event.event_node = b
                    if previous_event is None:
                        b.circle_minimum = event
                        ordered_points.append(event)
                    else:
                        if event != previous_event:
                            if previous_event in ordered_points:
                                ordered_points.remove(previous_event)
                            b.circle_minimum = event
                            ordered_points.append(event)
            else:
                if b.circle_minimum is not None:
                    if b.circle_minimum in ordered_points:
                        ordered_points.remove(b.circle_minimum)
                    b.circle_minimum = None
        elif relevant_nodes[middle_node] is not None:
            if relevant_nodes[middle_node].site in ordered_points:
                ordered_points.remove(relevant_nodes[middle_node].site)
            relevant_nodes[middle_node].circle_minimum = None

    heapq.heapify(ordered_points)
    return ordered_points


def next_point(ordered_points):
    return heapq.heappop(ordered_points)


def insert_site(open_list, edges_list, new_site, voronoi_regions):
    new_node = SiteNode(new_site)
    sweep_y = new_site.y
    if open_list.start is None:
        open_list.start = new_node

    else:
        first_node = open_list.start
        if first_node.right_edge is not None:
            if first_node.right_endpoint().x > new_site.x:
                new_left_node, new_right_node, edges_list, voronoi_regions = \
                    split_node(
                        open_list,
                        edges_list,
                        first_node,
                        new_site,
                        sweep_y,
                        voronoi_regions,
                        )
                open_list.start = new_left_node
                new_node = new_left_node.next_node
                first_node.next_node.previous_node = new_right_node

            else:
                current_node = first_node.next_node

                while True:
                    if current_node.next_node is None:
                        new_left_node, new_right_node, edges_list,\
                            voronoi_regions = split_node(
                                open_list,
                                edges_list,
                                current_node,
                                new_site,
                                sweep_y,
                                voronoi_regions,
                                )
                        new_node = new_left_node.next_node
                        current_node.previous_node.next_node = new_left_node
                        break

                    right_endpoint = current_node.right_endpoint()

                    if right_endpoint.x < new_site.x:
                        current_node = current_node.next_node
                        continue

                    elif right_endpoint.x > new_site.x:
                        new_left_node, new_right_node, edges_list,\
                            voronoi_regions = split_node(
                                open_list,
                                edges_list,
                                current_node,
                                new_site,
                                sweep_y,
                                voronoi_regions,
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
                        voronoi_regions[current_node.site].append(
                            current_to_new,
                            )
                        voronoi_regions[new_site].append(current_to_new)
                        voronoi_regions[new_site].append(new_to_right)
                        voronoi_regions[right_node.site].append(new_to_right)
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
            new_left_node, new_right_node, edges_list, voronoi_regions =\
                split_node(
                    open_list,
                    edges_list,
                    first_node,
                    new_site,
                    sweep_y,
                    voronoi_regions,
                    )
            new_node = new_left_node.next_node
            open_list.start = new_left_node

    return open_list, edges_list, new_node, voronoi_regions


def split_node(
        open_list,
        edges_list,
        current_node,
        new_site,
        sweep_y,
        voronoi_regions
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
        new_left_node.previous_node = current_node.previous_node

        left_to_new = Edge(breakpoints[0])
        voronoi_regions[current_site].append(left_to_new)
        voronoi_regions[new_site].append(left_to_new)
        edges_list.append(left_to_new)
        new_left_node.right_edge = left_to_new
        new_left_node.next_node = new_center_node

        new_center_node.previous_node = new_left_node
        new_center_node.left_edge = left_to_new

        new_right_node = SiteNode(current_site)
        new_to_right = Edge(breakpoints[1])
        voronoi_regions[new_site].append(new_to_right)
        voronoi_regions[current_site].append(new_to_right)
        edges_list.append(new_to_right)
        new_center_node.right_edge = new_to_right
        new_center_node.next_node = new_right_node
        new_right_node.previous_node = new_center_node
        new_right_node.left_edge = new_to_right
        new_right_node.right_edge = current_node.right_edge
        new_right_node.next_node = current_node.next_node
        return new_left_node, new_right_node, edges_list, voronoi_regions


def make_point(entry):
    return Point(
        entry[0],
        entry[1],
        PointType.SITE,
        )


def print_points(point_list):
    new_list = list(point_list)
    while len(new_list) > 0:
        print heapq.heappop(new_list)


if __name__ == '__main__':
    num_points = 10
    """
    points = []
    for _ in xrange(num_points):
        point = (random.uniform(0, 10), random.uniform(0, 10))
        print point
        points.append(point)
        """
    points = [
        (3.275661885046801, 3.0222362547546955),
        (1.3877360795680072, 7.053142850672501),
        (2.1880080423526884, 8.123687279692929),
        (9.954413013349567, 8.15572399707384),
        (1.0391367560749831, 4.549779494418429),
        (5.3856661554554455, 6.377200870511951),
        (0.2198910037649937, 9.317312159668973),
        (4.04799141544917, 0.9749349934132701),
        (0.1256612482931252, 2.7451945294930447),
        (3.488035475641953, 0.5303251310648605),
        ]

    made_points = map(make_point, points)
    edges, voronoi = create_diagram(made_points)
    plot_diagram(edges, made_points)
