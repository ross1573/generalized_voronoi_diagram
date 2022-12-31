import numpy as np
import matplotlib.pyplot as plt
from rdp import rdp
from enum import Enum
from collections import deque
from scipy.spatial import Voronoi, voronoi_plot_2d

from indexDictionary import IndexDict
from geometry import Triangle, Line
from Util import *


# optimized voronoi diagram
class OptimizedVoronoi:
    class type(Enum):
        non_lined = 0,
        non_deleted = 1,
        non_optimized = 2,
        optimized = 3
    
    class _RetT:
        points: list
        vertices: list
        ridges: list

    rdp_epsilon: int

    def __init__(self) -> None:
        self.__points = []
        self.__triangles = []
        self.__boundaries = []

        self.__triangle_points = []
        self.__boudnary_points = []
        self.__triangle_lined_points = []
        self.__boundary_lined_points = []

    def add_points(self, points: list) -> None:
        self.__points += points
    
    def add_triangle(self, triangle: Triangle) -> None:
        self.__triangles.append(triangle)
        self.__triangle_lined_points += triangle.generate_line()
        for ele in triangle.points:
            self.__triangle_points.append(ele)

    def add_boundary(self, boundary: Line) -> None:
        self.__boundaries.append(boundary)
        self.__boundary_lined_points += boundary.generate_line()
        for ele in boundary.points:
            self.__boudnary_points.append(ele)

    def __run_voronoi(self, points) -> None:
        self.__vor = Voronoi(points=points)

    def run_non_lined(self) -> _RetT:
        self.__run_voronoi(self.__boudnary_points + 
                           self.__triangle_points +
                           self.__points)
        return self.__generate_return_value()
    
    def run_non_deleted(self) -> _RetT:
        self.__run_voronoi(self.__boundary_lined_points + 
                           self.__triangle_lined_points +
                           self.__points)
        return self.__generate_return_value()
    
    def run_non_optimized(self) -> _RetT:
        # run voronoi
        self.__run_voronoi(self.__boundary_lined_points + 
                           self.__triangle_lined_points +
                           self.__points)

        # calculate vertices and ridges to delete
        vertex_to_delete = self.__vertices_in_polygon()
        ridge_to_delete = self.__ridges_to_delete(vertex_to_delete)

        # delete
        self.__delete_vertex(vertex_to_delete)
        self.__delete_ridge(ridge_to_delete)

        # reorganize ridge vertices
        self.__reorganize_ridge(vertex_to_delete)

        return self.__generate_return_value()

    def run_optimized(self) -> _RetT:
        # run voronoi
        self.run_non_optimized()

        # generate chains in voronoi diagram
        chains = self.__generate_chains()
        vertex_chains = self.__generate_vertex_chains(chains)

        # unoptimizable case
        if chains == []: return self.__vor

        # optimize line
        optimized_chains = self.__optimize_line(vertex_chains)

        # regenerate ridges
        self.__regenerate_voronoi(optimized_chains)
        
        return self.__generate_return_value()

    def run(self, type = type.optimized, plot = True) -> _RetT:
        if   type == self.type.non_lined:     result = self.run_non_lined()
        elif type == self.type.non_deleted:   result = self.run_non_deleted()
        elif type == self.type.non_optimized: result = self.run_non_optimized()
        elif type == self.type.optimized:     result = self.run_optimized()
        if plot: self.generate_plot()
        return result

    # optimize line using Ramer-Douglas-Peucker algorithm
    def __optimize_line(self, chains) -> list:
        optimized_chains = []
        for chain in chains:
            optimized_chains.append(rdp(chain, epsilon=self.rdp_epsilon))
        return optimized_chains
    
    # regenerate voronoi based on optimized valued
    def __regenerate_voronoi(self, chains) -> None:
        vertices = []
        ridge_vertices = []

        for chain in chains:
            if chain[0] not in vertices:
                vertices.append(chain[0])

            for i in range(len(chain)-1):
                idx = [vertices.index(chain[i]), -1]
                
                if chain[i+1] not in vertices:
                    vertices.append(chain[i+1])
                    idx[1] = len(vertices)-1
                else:
                    idx[1] = vertices.index(chain[i+1])
                
                ridge_vertices.append(np.array(idx))
        
        self.__vor.vertices = np.array(vertices)
        self.__vor.ridge_vertices = np.array(ridge_vertices)


    # generate vertex chain by line unit
    def __generate_chains(self):
        dic = IndexDict(self.__vor.ridge_vertices)

        # ignition value must be dead end point(which has only 1 neighbor)
        ignition_idx = -1
        for key, value in dic.items():
            if len(value) == 1:
                ignition_idx = key
                break

        # voronoi diagram with no dead end point cannot be optimized
        if (ignition_idx == -1):
            print("Unable to optimize voronoi diagram")
            return []

        # generate chains
        feature_point = []
        chains = []
        start_point = deque()
        start_point.append([-1, ignition_idx])
        while len(start_point) > 0:
            chains.append(self.__generate_chain(dic, start_point, feature_point))

        return chains

    # generate vertex chain based on index chain
    def __generate_vertex_chains(self, chains):
        vertex_chains = []
        for chain in chains:
            vertex_chain = []
            for ele in chain:
                vertex_chain.append(self.__vor.vertices[ele])
            vertex_chains.append(vertex_chain)
        return vertex_chains

    # generate chain
    def __generate_chain(self, dic, start, feature) -> None:
        chain = []

        # get new starting point
        idx = start.pop()

        # case of dead end point
        if idx[0] != -1: chain.append(idx[0])

        # ignite chain
        new_start = self.__chain_(dic, idx, chain, feature)

        # add chain start and end to feature points
        feature.append(chain[0])
        feature.append(chain[-1])

        # add new starting points to queue
        for ele in new_start:
            start.append(ele)
        
        return chain

    # generate chain by finding next vertex recursively
    def __chain_(self, dic, idx, chain, feature) -> list:
        # append current point to chain
        chain.append(idx[1])

        # search neighbor on index dictionary
        neighbor = dic.find(idx[1])
        neighbor_count = len(neighbor)

        # visited is selected base on feature point(diverging point) and previous point
        visited = feature + idx[:1]

        # case 1, dead end point
        if neighbor_count == 1:
            if neighbor[0] == idx[0]: return []
            return self.__chain_(dic, [idx[1], neighbor[0]], chain, feature)

        # case 2, middle of line
        elif neighbor_count == 2:
            has_visited = [False, False]
            if neighbor[0] in visited: has_visited[0] = True
            if neighbor[1] in visited: has_visited[1] = True

            # if both neighbor is visited, it's end of line
            if has_visited[0] and has_visited[1]:
                if   idx[0] == neighbor[0]: chain.append(neighbor[1])
                elif idx[0] == neighbor[1]: chain.append(neighbor[0])
                return []

            # prevent going back
            elif has_visited[0]: next_idx = 1
            elif has_visited[1]: next_idx = 0
            else: raise ValueError("at least one neighbor has to be visited")

            # find next vertex
            return self.__chain_(dic, [idx[1], neighbor[next_idx]], chain, feature)
        
        # case more than 2, diverging point
        # line must end on diverging point
        # new starting points must be added for full construction
        new_start_points = []
        for i in range(neighbor_count):
            if neighbor[i] in visited: continue
            new_start_points.append([idx[1], neighbor[i]])
        return new_start_points
    
    # calculate vertices which are in convex
    def __vertices_in_polygon(self) -> list:
        in_polygon = []

        for i in range(len(self.__vor.vertices)):
            for tri in self.__triangles:
                if (tri.is_in_polygon(self.__vor.vertices[i])):
                    in_polygon.append(i)
                    break

        return in_polygon

    # calculate ridges which are related to deleted vertices and outside
    def __ridges_to_delete(self, vertex_vec) -> list:
        to_delete = []

        for i in range(len(self.__vor.ridge_vertices)):
            rv = self.__vor.ridge_vertices[i]

            # if ridge heads outside, delete ridge
            if rv[0] == -1 or rv[1] == -1:
                to_delete.append(i)
                continue

            # if ridge contains deleted vertex, delete ridge
            for ver in vertex_vec:
                if rv[0] == ver or rv[1] == ver:
                    to_delete.append(i)
                    break
        
        return to_delete

    # delete vertices
    def __delete_vertex(self, to_delete) -> None:
        self.__vor.vertices = np.delete(self.__vor.vertices, to_delete, 0)
    
    # delete unused ridge
    def __delete_ridge(self, to_delete) -> None:
        self.__vor.ridge_vertices = np.delete(self.__vor.ridge_vertices, to_delete, 0)

    # reorganize ridge
    def __reorganize_ridge(self, deleted_vertices) -> None:
        for i in range(len(self.__vor.ridge_vertices)):
            _0, _1 = self.__vor.ridge_vertices[i][0], self.__vor.ridge_vertices[i][1]
            _0_i, _1_i = find_closest(deleted_vertices, _0), find_closest(deleted_vertices, _1)
            self.__vor.ridge_vertices[i] = np.array([_0 - _0_i, _1 - _1_i], int)

    def __generate_return_value(self) -> _RetT:
        ret_val = self._RetT()
        ret_val.points = np.array(self.__vor.points, dtype=float, copy=True)
        ret_val.vertices = np.array(self.__vor.vertices, dtype=float, copy=True)
        ret_val.ridges = np.array(self.__vor.ridge_vertices, dtype=int, copy=True)
        return ret_val

    def generate_plot(self) -> None:
        voronoi_plot_2d(self.__vor)
    
    def show(self) -> None:
        plt.show()