import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

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

        return self.__vor

    def __generate_ridge_dictionary(self) -> list:
        sorted = []
        for i in range(len(self.__vor.ridge_vertices)):
            vertex = self.__vor.ridge_vertices[i]
            indexed = [i]
            for ele in vertex:
                indexed.append(ele)
            sorted.append(indexed)
        sorted.sort(key=lambda x: x[1])

        pairs, key, value = [], [], []
        current = sorted[0][1]
        for ele in sorted:
            if ele[1] != current:
                value.append(pairs)
                key.append(current)
                pairs = []
                current = ele[1]
            pairs.append([ele[2], ele[0]])
        value.append(pairs)
        key.append(current)
        
        return {key[i]: value[i] for i in range(len(key))}
    
    def __swap_ridge_vertex(self, vertex_idx, vertex) -> None:
        self.__vor.ridge_vertices[vertex_idx] = vertex
    
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
        self.__vor.ridge_points = np.delete(self.__vor.ridge_points, to_delete, 0)

    # reorganize indexes
    def __reorganize_ridge(self, deleted_vertices) -> None:
        for i in range(len(self.__vor.ridge_vertices)):
            _0, _1 = self.__vor.ridge_vertices[i][0], self.__vor.ridge_vertices[i][1]
            _0_i, _1_i = find_closest(deleted_vertices, _0), find_closest(deleted_vertices, _1)
            self.__vor.ridge_vertices[i] = np.array([_0 - _0_i, _1 - _1_i], int)

    def generate_plot(self) -> None:
        voronoi_plot_2d(self.__vor)
    
    def show(self) -> None:
        plt.show()