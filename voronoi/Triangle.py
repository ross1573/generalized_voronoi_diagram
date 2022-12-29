from Line import Line
from Util import *

import numpy as np


# triangle class
class Triangle(Line):
    # distance between point and vertex trash value
    # point which distance is lower than this will be ignored
    distance_trash: float

    def __init__(self, points) -> None:
        if len(points) != 3:
            raise TypeError('Triangle have to be 3 points.')
        self.points = np.array(points)
    
    # generate line by points
    # points size equals to line length divided by _point_distance
    def generate_line(self) -> list:
        result = []

        # loop for every line in Triangle
        for i in range(len(self.points)):
            _1 = self.points[i]
            _2 = self.points[i+1 if i < len(self.points)-1 else 0]
            result += super()._generate_line(_1, _2)
        
        return result        

    # test if point is in triangle
    def is_in_convex(self, point) -> bool:
        # if point is close enough, filter out
        if self._test_distance_trash(point):
            return True

        # loop for every vertex in Triangle
        for i in range(3):
            # vector ab
            l_1 = self.points[(i+1)%3] - self.points[i]
            # vector ac
            l_2 = self.points[(i+2)%3] - self.points[i]
            # vector ap
            l_3 = point - self.points[i]

            # ab x ap
            c_1 = np.cross(l_1, l_3)
            # ap x ac
            c_2 = np.cross(l_3, l_2)

            # if (ab x ap) * (ap x ac) < 0 than the point is in convex
            if np.dot(c_1, c_2) < 0:
                return False
        return True

    # test if a point is close enough to vertex
    # test value is self._distance_trash
    def _test_distance_trash(self, point) -> bool:
        for i in range(3):
            dis = distance(point, self.points[i])
            if dis < self.distance_trash:
                return True
        return False