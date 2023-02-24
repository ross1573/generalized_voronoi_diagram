import numpy as np
from numba import jit, njit
import numba.np.extensions as nbnp
import tripy


# get length of 2d vector
@njit(cache=True, fastmath=True)
def length(vec2) -> float:
    return np.sqrt(pow(vec2[0], 2) + pow(vec2[1], 2))

# get distance between two 2d vectors
@njit(cache=True)
def distance(_1, _2) -> float:
    return length(_1 - _2)

@njit(cache=True, fastmath=True)
def total_distance(path):
    dist = 0.0
    for i in range(len(path)-1):
        dist += distance(path[i], path[i+1])
    return dist

@njit(cache=True, fastmath=True)
def distance_between_line_point(line, point):
    _1 = line[1] - line[0]
    _2 = point - line[0]
    _1_l = length(_1)
    _2_l = length(_2)
    
    _d = np.dot(_1, _2)
    if _d > _1_l * _1_l or _d < 0.0:
        return min(_2_l, length(point - line[1]))
    
    _c = np.arccos(_d / (_1_l * _2_l))
    return np.sin(_c) * _2_l

def min_distance_from_obstacle(vor):
    min_dist = np.finfo(np.float64).max
    vertices = vor.vertices
    ridges = vor.ridge_vertices
    points = vor.points_polygon

    for ridge in ridges:
        _l = np.array([vertices[ridge[0]], vertices[ridge[1]]])
        for point in points:
            _p = np.array(point)
            _d = distance_between_line_point(_l, _p)
            if _d < min_dist:
                min_dist = _d

    return min_dist

# get angle between two 2d vectors
@njit(cache=True, fastmath=True)
def radian(_1, _2) -> float:
    _1_n = _1 / length(_1)
    _2_n = _2 / length(_2)
    dot = np.dot(_1_n, _2_n)
    if dot > 1.0: dot = 1.0
    return np.arccos(dot)

# get closest(but smaller) value index on vector
@njit(cache=True)
def find_closest(vec, ele) -> int:
    for i in range(len(vec)):
        if vec[i] > ele:
            return i
    return len(vec)

@njit(cache=True, fastmath=True)
def counter_clockwise(_1, _2, _3) -> int:
        # vector ab
        v_1 = _2 - _1
        # vector ac
        v_2 = _3 - _1

        # vector ab x ac
        cross = nbnp.cross2d(v_1, v_2)

        # if cross > 0 than it's ccw
        if cross > 0: return 1
        # if cress == 0 than it's parallel
        elif cross == 0: return 0
        # if cross < 0 than it's cw
        return -1

@njit(cache=True, fastmath=True)
def is_intersecting(_1, _2) -> bool:
    # ccw(p1, p2, p3) * ccw(p1, p2, p4)
    if counter_clockwise(_1[0], _1[1], _2[0]) * counter_clockwise(_1[0], _1[1], _2[1]) < 0:
        # ccw(p3, p4, p1) * ccw(p3, p4, p2)
        if counter_clockwise(_2[0], _2[1], _1[0]) * counter_clockwise(_2[0], _2[1], _1[1]) < 0:
            return True
    return False


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
        return self.__generate_line_base(_1, _2, 0, self.point_distance)
    
    def __generate_line_y(self, _1, _2) -> list:
        return self.__generate_line_base(_1, _2, 1, self.point_distance)
    
    @staticmethod
    @jit(nopython=False, forceobj=True)
    def __generate_line_base(_1, _2, axis, point_distance):
        result = []

        # if vec_1[axis] > vec_2[axis] then swap
        if (_1[axis] > _2[axis]):
                _1, _2 = _2, _1

        # get step vector
        # one step equals to distance between two points
        dis = distance(_1, _2)
        step_vec = (_2 - _1) / dis
        step_vec *= point_distance

        # initialize to first point
        current = np.array(_1)
            
        # loop until current point reaches second point
        # add current point to result
        while current[axis] <= _2[axis]:
            result.append(np.array(current))
            current += step_vec
        
        return result

    def is_intersecting(self, line) -> bool:
        return is_intersecting(self.points, line)



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
    def is_in_polygon(self, point) -> bool:
        # if point is close enough, filter out
        if self.__test_distance_trash(self.points, point, self.distance_trash):
            return True

        return self.__test_point_convex(self.points, point)

    # test if a point is close enough to vertex
    # test value is self._distance_trash
    @staticmethod
    @njit(cache=True)
    def __test_distance_trash(points, test_point, distance_trash) -> bool:
        for i in range(3):
            dis = distance(test_point, points[i])
            if dis < distance_trash:
                return True
        return False

    @staticmethod
    @njit(cache=True, fastmath=True)
    def __test_point_convex(points, test_point) -> bool:
        for i in range(3):
            # if CCW(p1, p2, test_point) * CCW(p1, test_point, p3) < 0 than the point is in convex
            if counter_clockwise(points[i], points[(i+1)%3], test_point) * counter_clockwise(points[i], test_point, points[(i+2)%3]) <= 0.0:
                return False
        return True


def triangulation(polygon) -> list[Triangle]:
    triangles = []
    triangulation = tripy.earclip(polygon)
    for triangle in triangulation:
        vertices = []
        for vertex in triangle:
            vertices.append(list(vertex))
        triangles.append(vertices)
    return triangles