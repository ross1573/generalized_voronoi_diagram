import matplotlib.pyplot as plt
from queue import PriorityQueue
from matplotlib.collections import LineCollection

from voronoi import Result
from dictionary import IndexDict
from geometry import *


# astar algorithm for polygon diagram
class Astar:
    # node used in astar
    class __Node:
        def __init__(self, idx, parent, g, h) -> None:
            self.idx = idx
            self.parent = parent
            self.g = g
            self.h = h
            self.f = g + h
        
        def __lt__(self, other) -> bool:
            return self.f < other.f

    def __init__(self, vor: Result, start, end) -> None:
        self.__vor = vor
        self.__dict = IndexDict(vor.ridge_vertices)
        self.__start = self.__add_ridge(start)
        self.__end = self.__add_ridge(end)

    def run(self) -> list:
        node = self.__astar_()

        result = []
        while node != None:
            result.insert(0, node.idx)
            node = node.parent
            
        self.__result = result
        return result

    def __astar_(self) -> __Node:
        open = PriorityQueue()
        start_node = self.__generate_node(self.__start, None)
        open.put(start_node)
        closed = []

        while not open.empty():
            current = open.get()
            if current.idx not in closed:
                if self.__test_goal(current.idx):
                    return current
                else:
                    closed.append(current.idx)
                    neighbors = self.__dict.find(current.idx)
                    for neighbor in neighbors:
                        if neighbor in closed: continue
                        open.put(self.__generate_node(neighbor, current))

        return None

    # manhattan distance is used for heruistic
    def __heruistic_(self, idx):
        cur_ver = self.__vor.vertices[idx]
        goal_point = self.__vor.vertices[self.__end]
        return distance(cur_ver, goal_point)

    def __generate_node(self, idx, current) -> __Node:
        vertices = self.__vor.vertices
        
        if current == None: g = 0
        else:
            dist = distance(vertices[current.idx], vertices[idx])
            g = current.g + dist

        return self.__Node(idx, current, g, self.__heruistic_(idx))
    
    def __test_goal(self, idx) -> bool:
        if idx == self.__end: return True
        return False

    # add new ridges between point and adjacent vertices
    def __add_ridge(self, point) -> None:
        # find adjacent vertices
        neighbors = self.__find_adjacent(point)
        
        # append point to vertices
        self.__vor.vertices = np.append(self.__vor.vertices, [point], axis=0)
        ver_idx = len(self.__vor.vertices)-1

        # append ridges
        for neighbor in neighbors:
            ridge = [[neighbor, ver_idx]]
            self.__vor.ridge_vertices = np.append(self.__vor.ridge_vertices, ridge, axis=0)
        
        # insert new ridges to dictionary
        self.__dict.insert(ver_idx, neighbors)
        return ver_idx
    
    # find adjacent vertices
    def __find_adjacent(self, point) -> list:
        vertices = self.__vor.vertices

        # order by distance
        distance_order = []
        for i in range(len(vertices)):
            dist = distance(point, vertices[i])
            distance_order.append([i, dist])
        distance_order.sort(key=lambda x: x[1])
        
        for i in range(len(distance_order)):
            distance_order[i] = distance_order[i][0]

        # append vertex until vertices is closed
        neighbors = distance_order[:3]
        for ele in distance_order[3:]:
            if self.__is_closed(neighbors): break
            neighbors.append(ele)

        # delete unchained vertex
        unchained = self.__unchained_vertex(neighbors)
        chained = np.delete(neighbors, unchained)
        return chained

    # if neighbor count < 2 than vertices are not closed
    # TODO: fix closure detecting algorithm
    def __is_closed(self, vec) -> bool:
        for ele in vec:
            neighbors = self.__dict.find(ele)
            exist_count = 0
            ###
            if len(neighbors) == 1: continue
            ###
            for neighbor in neighbors:
                if neighbor in vec:
                    exist_count += 1
            if exist_count < 2:
                return False
        return True
    
    # chain vertices to check if non-adjacent value is added
    # TODO: fix finding unchained vertices
    def __unchained_vertex(self, vec) -> bool:
        chain = [vec[0]]
        while True:
            neighbors = self.__dict.find(chain[-1])
            appended = False
            for neighbor in neighbors:
                if neighbor in vec and neighbor not in chain:
                    chain.append(neighbor)
                    appended = True
                    break
            if not appended: break

        unchained_index = []
        for i in range(len(vec)):
            if vec[i] not in chain:
                unchained_index.append(i)
        return unchained_index

    def generate_plot(self) -> None:
        fig, ax = plt.subplots()
        result = self.__result
        vertices = self.__vor.vertices
        points= self.__vor.points

        ax.plot(points[:,0], points[:,1], '.')
        ax.plot(vertices[:,0], vertices[:,1], 'o')

        segments = []
        for vertex in self.__vor.ridge_vertices:
            vertex = np.asarray(vertex)
            segments.append(vertices[vertex])
        ax.add_collection(LineCollection(segments))
        
        segments = []
        for i in range(len(result)-1):
            seg = [vertices[result[i]], vertices[result[i+1]]]
            segments.append(seg)
        ax.add_collection(LineCollection(segments, colors='r', lw=2.0))

    def show(self) -> None:
        plt.show()