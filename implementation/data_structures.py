class DoublyLinkedList(object):
    def __init__(self, root_endpoints, root_cell):
        root = ListNode(root_endpoints, None, None, root_cell)
        self.root = root
        self.end = root

    def insert(self, endpoints, twin, cell):
        new_node = ListNode(endpoints, self.end, twin, cell)
        self.end = new_node


class ListNode(object):
    def __init__(self, endpoints, previous_edge, twin, cell):
        self.endpoints = endpoints
        self.previous_edge = previous_edge
        self.next_edge = None
        if self.previous_edge is not None:
            self.previous_edge.next_edge = self
        self.twin = twin
        if self.twin is not None:
            self.twin.twin = self
        self.cell = cell


class BinarySearchTree(object):
    def __init__(self, root_point):
        self.root = LeafNode(root_point)

    def insert(self, point):
        current_node = self.root
        while isinstance(current_node, InternalNode):
            if current_node.lower_endpoint() 


class LeafNode(object):
    def __init__(self, point):
        self.point = point


class InternalNode(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def lower_endpoint(self):
        current_node = self.left
        while isinstance(current_node, InternalNode):
            current_node = current_node.right
        return current_node.point

    def higher_endpoint(self):
        current_node = self.right
        while isinstance(current_node, InternalNode):
            current_node = current_node.left
        return current_node.point
