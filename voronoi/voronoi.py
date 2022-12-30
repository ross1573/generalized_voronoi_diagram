import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from scipy.spatial import Voronoi, voronoi_plot_2d

from Dictionary import IndexDict
from Triangle import Triangle
from Line import Line
from Util import *


# optimized voronoi diagram
class OptimizedVoronoi:
    division_angle: float

    def __init__(self) -> None:
        self.__triangles = []
        self.__boundaries = []

        self.__triangle_points = []
        self.__boudnary_points = []
        self.__triangle_lined_points = []
        self.__boundary_lined_points = []
    
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

    def run_non_lined(self) -> None:
        self.__run_voronoi(self.__boudnary_points + self.__triangle_points)
        return self.__vor
    
    def run_non_deleted(self) -> None:
        self.__run_voronoi(self.__boundary_lined_points + self.__triangle_lined_points)
        return self.__vor
    
    def run_non_optimized(self) -> Voronoi:
        # run voronoi
        self.__run_voronoi(self.__boundary_lined_points + self.__triangle_lined_points)

        # calculate vertices and ridges to delete
        vertex_to_delete = self.__get_vertices_to_delete()
        ridge_to_delete = self.__get_ridges_to_delete(vertex_to_delete)

        # delete
        self.__delete_vertex(vertex_to_delete)
        self.__delete_ridge(ridge_to_delete)

        # reorganize ridge vertices
        self.__reorganize_ridge(vertex_to_delete)

        return self.__vor

    def run(self) -> Voronoi:
        # run voronoi
        self.run_non_optimized()

        # get optimizable vertices
        vertex_to_delete = self.__get_optimizable_values()

        # regenerate ridge vertices
        self.__regenerate_ridges()

        # delete
        self.__delete_vertex(vertex_to_delete)

        # reorganize ridge vertices
        self.__reorganize_ridge(vertex_to_delete)

        return self.__vor

    # optimize unnecsary values in vertex
    def __get_optimizable_values(self):
        candidate = deque()
        dic = IndexDict(self.__vor.ridge_vertices)

        ignition_idx = -1
        for key, value in dic.items():
            if len(value) == 1:
                ignition_idx = key
                break

        if (ignition_idx == -1):
            print("Unable to optimize voronoi diagram")
            return []

        self.__feature = []
        candidate.append([-1, ignition_idx])
        while len(candidate) > 0:
            self.__get_chain(dic, candidate)

        vertex_to_delete = np.arange(len(self.__vor.vertices))
        vertex_to_delete = np.delete(vertex_to_delete, self.__feature)        
        return vertex_to_delete

    def __get_chain(self, dic, candidate) -> None:
        chain = []
        idx = candidate.pop()

        if idx[0] != -1: chain.append(idx[0])
        new_candidate = self.__chain_(dic, idx, chain)

        self.__feature.append(chain[0])
        self.__feature.append(chain[-1])
        for ele in new_candidate:
            candidate.append(ele)

    def __chain_(self, dic, idx, chain) -> list:
        chain.append(idx[1])
        neighbor = dic.find(idx[1])
        neighbor_count = len(neighbor)
        visited = self.__feature + idx[:1]

        if neighbor_count == 1:
            if neighbor[0] == idx[0]: return []
            return self.__chain_(dic, [idx[1], neighbor[0]], chain)

        elif neighbor_count == 2:
            has_visited = [False, False]
            if neighbor[0] in visited: has_visited[0] = True
            if neighbor[1] in visited: has_visited[1] = True

            if has_visited[0] and has_visited[1]:
                if   idx[0] == neighbor[0]: chain.append(neighbor[1])
                elif idx[0] == neighbor[1]: chain.append(neighbor[0])
                return []

            elif has_visited[0]: next_idx = 1
            elif has_visited[1]: next_idx = 0
            else: raise ValueError("at least one neighbor has to be visited")

            if not self.__test_angle(idx + [neighbor[next_idx]]):
                return self.__chain_(dic, [idx[1], neighbor[next_idx]], chain)
        
        new_candidate = []
        for i in range(neighbor_count):
            if neighbor[i] in visited: continue
            new_candidate.append([idx[1], neighbor[i]])
        return new_candidate

    def __test_angle(self, idx) -> bool:
        vertex = []
        for i in idx:
            vertex.append(self.__vor.vertices[i])
        
        _0, _1 = vertex[1] - vertex[0], vertex[2] - vertex[1]
        if radian(_0, _1) > self.division_angle: return True
        return False
    
    # calculate vertices which are in convex
    def __get_vertices_to_delete(self) -> list:
        to_delete = []

        for i in range(len(self.__vor.vertices)):
            for tri in self.__triangles:
                if (tri.is_in_convex(self.__vor.vertices[i])):
                    to_delete.append(i)
                    break

        return to_delete

    # calculate ridges which are related to deleted vertices and outside
    def __get_ridges_to_delete(self, vertex_vec) -> list:
        to_delete = []

        for i in range(len(self.__vor.ridge_vertices)):
            rv = self.__vor.ridge_vertices[i]

            # if vertex heads outside, delete ridge
            if rv[0] == -1 or rv[1] == -1:
                to_delete.append(i)
                continue

            # ridge contains deleted vertex, delete ridge
            for ver in vertex_vec:
                if rv[0] == ver or rv[1] == ver:
                    to_delete.append(i)
                    break
        
        return to_delete

    # delete vertices which are in convex
    def __delete_vertex(self, to_delete) -> None:
        self.__vor.vertices = np.delete(self.__vor.vertices, to_delete, 0)
    
    # delete unused ridge
    def __delete_ridge(self, to_delete) -> None:
        self.__vor.ridge_vertices = np.delete(self.__vor.ridge_vertices, to_delete, 0)

    # reorganize indexes
    def __reorganize_ridge(self, deleted_vertices) -> None:
        for i in range(len(self.__vor.ridge_vertices)):
            _0, _1 = self.__vor.ridge_vertices[i][0], self.__vor.ridge_vertices[i][1]
            _0_i, _1_i = find_closest(deleted_vertices, _0), find_closest(deleted_vertices, _1)
            self.__vor.ridge_vertices[i] = np.array([_0 - _0_i, _1 - _1_i], int)

    def __regenerate_ridges(self) -> None:
        new_ridges = []
        new_length = (int)(len(self.__feature) / 2)
        for i in range(new_length):
            new_ridges.append([self.__feature[2 * i], self.__feature[(2 * i) + 1]])
        self.__vor.ridge_vertices = new_ridges

    def generate_plot(self) -> None:
        voronoi_plot_2d(self.__vor)
    
    def show(self) -> None:
        plt.show()