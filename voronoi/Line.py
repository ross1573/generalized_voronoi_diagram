import numpy as np
from Util import *


# line class
class Line:
    # distance bewteen two points in line
    point_distance: float

    def __init__(self, points) -> None:
        if len(points) != 2:
            raise TypeError('Line have to be 2 points.')
        self.points = np.array(points)
    
    # generate line by points
    # points size equals to line length divided by _point_distance
    def generate_line(self) -> list:
        return self._generate_line(self.points[0], self.points[1])

    def _generate_line(self, _1, _2) -> list:
        result = []

        if _1[0] != _2[0]:
            result += self.__generate_line_x(_1, _2)
        elif _1[1] != _2[1]:
            result += self.__generate_line_y(_1, _2)
        else:
            print("Identical point has been detected: ")
            print(self.points)
        
        return result
        
    def __generate_line_x(self, _1, _2) -> list:
        return self.__generate_line_base(_1, _2, 0)
    
    def __generate_line_y(self, _1, _2) -> list:
        return self.__generate_line_base(_1, _2, 1)
    
    def __generate_line_base(self, _1, _2, axis):
        result = []

        # if vec_1[axis] > vec_2[axis] then swap
        if (_1[axis] > _2[axis]):
                _1, _2 = _2, _1

        # get step vector
        # one step equals to distance between two points
        dis = distance(_1, _2)
        step_vec = (_2 - _1) / dis
        step_vec *= self.point_distance

        # initialize to first point
        current = np.array(_1)
            
        # loop until current point reaches second point
        # add current point to result
        while current[axis] <= _2[axis]:
            result.append(np.array(current))
            current += step_vec
        
        return result