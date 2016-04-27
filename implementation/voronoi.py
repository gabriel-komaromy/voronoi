class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class LineSegment(object):
    def __init__(self, endpoints):
        self.endpoints = endpoints


def create_diagram(points):
    pass
