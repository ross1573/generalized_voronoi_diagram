"""
Tested environment
------------------------
macbook pro 16inch, 2019
CPU: i9-9880HK
RAM: 32GB
OS: macOS 13.1(22C65)
PYTHON: 3.10.9
    - numpy: 1.24.1
    - scipy: 1.9.3
    - rdp: 0.8
------------------------

|-----------------------------------------------|
| testmap_1.png - [0.05, 0.05] > [0.9, 0.9]     |
|-----------------------------------------------|
| Fig | epsilon | seconds | vertices | distance |
|-----|---------|---------|----------|----------|
|   1 |  0.0000 |  14.158 |      456 | 1.472487 | 
|   2 |  0.0002 |   9.246 |      342 | 1.472450 | 
|   3 |  0.0004 |   5.245 |      242 | 1.472374 | 
|   4 |  0.0008 |   2.783 |      144 | 1.471773 | 
|   5 |  0.0016 |   2.027 |      107 | 1.471745 | 
|   6 |  0.0032 |   1.551 |       70 | 1.471251 | 
|   7 |  0.0064 |   1.305 |       52 | 1.471153 | 
|   8 |  0.0128 |   1.159 |       37 | 1.469695 | 
|   9 |  0.0256 |   1.207 |       33 | 1.469695 | 
|  10 |  0.0512 |   1.187 |       25 | 1.469695 | 
|-----------------------------------------------|

|-----------------------------------------------|
| testmap_3.png - [0.05, 0.05] > [0.9, 0.9]     |
|-----------------------------------------------|
| Fig | epsilon | seconds | vertices | distance |
|-----|---------|---------|----------|----------|
|   1 |  0.0000 |  16.324 |      464 | 1.449920 | 
|   2 |  0.0002 |   7.113 |      284 | 1.449840 | 
|   3 |  0.0004 |   4.110 |      200 | 1.449757 | 
|   4 |  0.0008 |   2.555 |      141 | 1.449545 | 
|   5 |  0.0016 |   1.779 |      101 | 1.449023 | 
|   6 |  0.0032 |   1.294 |       68 | 1.448546 | 
|   7 |  0.0064 |   1.158 |       55 | 1.447291 | 
|   8 |  0.0128 |   0.981 |       38 | 1.445277 | 
|   9 |  0.0256 |   0.929 |       29 | 1.440250 | 
|  10 |  0.0512 |   0.901 |       23 | 1.432812 | 
|-----------------------------------------------|


Tested environment
------------------------
CPU: i9-10900K
RAM: 64GB
OS: Windows 10 Education(21H2)
PYTHON: 3.10.7
    - numpy: 1.24.1
    - scipy: 1.9.3
    - rdp: 0.8
------------------------

|-----------------------------------------------|
| testmap_1.png - [0.05, 0.05] > [0.9, 0.9]     |
|-----------------------------------------------|
| Fig | epsilon | seconds | vertices | distance |
|-----|---------|---------|----------|----------|
|   1 |  0.0000 |   5.065 |      413 | 1.472487 |
|   2 |  0.0002 |   3.286 |      310 | 1.472450 |
|   3 |  0.0004 |   1.941 |      223 | 1.472374 |
|   4 |  0.0008 |   1.087 |      135 | 1.471773 |
|   5 |  0.0016 |   0.828 |      103 | 1.471745 |
|   6 |  0.0032 |   0.648 |       70 | 1.471251 |
|   7 |  0.0064 |   0.560 |       52 | 1.471153 |
|   8 |  0.0128 |   0.510 |       37 | 1.469695 |
|   9 |  0.0256 |   0.506 |       33 | 1.469695 |
|  10 |  0.0512 |   0.471 |       25 | 1.469695 |
|-----------------------------------------------|

|-----------------------------------------------|
| testmap_3.png - [0.05, 0.05] > [0.9, 0.9]     |
|-----------------------------------------------|
| Fig | epsilon | seconds | vertices | distance |
|-----|---------|---------|----------|----------|
|   1 |  0.0000 |   6.004 |      425 | 1.449920 |
|   2 |  0.0002 |   2.778 |      252 | 1.449840 |
|   3 |  0.0004 |   1.633 |      179 | 1.449757 |
|   4 |  0.0008 |   1.115 |      132 | 1.449545 |
|   5 |  0.0016 |   0.790 |       96 | 1.449023 |
|   6 |  0.0032 |   0.576 |       68 | 1.448546 |
|   7 |  0.0064 |   0.520 |       55 | 1.447291 |
|   8 |  0.0128 |   0.452 |       38 | 1.445277 |
|   9 |  0.0256 |   0.436 |       29 | 1.440250 |
|  10 |  0.0512 |   0.413 |       23 | 1.432812 |
|-----------------------------------------------|
"""


from voronoi.voronoi import PolygonVoronoi
from voronoi.geometry import *
from voronoi.astar import Astar
from voronoi.image import PolygonDetector

import matplotlib.pyplot as plt
from datetime import datetime


def print_result(file, start, end, result):
    print('|----------------------------------------------------------|')
    print('| ' + str(file + ' - ' + str(start) + ' > ' + str(end)).ljust(56) + ' |')
    print('|----------------------------------------------------------|')
    print('| Fig | epsilon | seconds | vertices | distance | obstacle |')
    print('|-----|---------|---------|----------|----------|----------|')
    for i in range(len(result)):
        ele = result[i]
        print('| ' + str(i+1).rjust(3) + ' |  '
                    + '{:1.4f}'.format(ele[0]) + ' | ' 
                    + str(ele[1].seconds).rjust(3) + "." 
                    + str(int(ele[1].microseconds / 1000)).zfill(3) + ' | '
                    + str(ele[2]).rjust(8) + ' | '
                    + '{:1.6f}'.format(ele[3]) + ' | '
                    + '{:1.6f}'.format(ele[4]) + ' | ')
    print('|----------------------------------------------------------|')


def image_detect(path, start, end):
    # boundary
    b1 = Line([[0.0, 0.0], [1.0, 0.0]])
    b2 = Line([[1.0, 0.0], [1.0, 1.0]])
    b3 = Line([[1.0, 1.0], [0.0, 1.0]])
    b4 = Line([[0.0, 0.0], [0.0, 1.0]])

    # polygon detector
    pd = PolygonDetector(path)
    pd.add_color_threshold(214)
    pd.run(bound=[1.0, 1.0])
    pd.generate_plot()
    pd.show()
    triangles = pd.convert_result()

    # voronoi
    vor = PolygonVoronoi()
    vor.add_triangles(triangles)
    vor.add_boundaries([b1, b2, b3, b4])
    vor.add_points([start, end])

    return vor


def voronoi(epsilon, vor, start, end, result):
    PolygonVoronoi.rdp_epsilon = epsilon
    start_t = datetime.now()

    # voronoi
    vor_result = vor.run_optimized()

    # astar
    astar = Astar(vor_result, start, end)
    astar_result = astar.run()
    
    end_t = datetime.now()
    astar.generate_plot()
    vertices_count = len(vor_result.vertices)

    # distance
    dist = total_distance(astar_result)
    dist_obt = min_distance_from_obstacle(astar_result, vor_result.points_polygon)

    result.append((epsilon, end_t - start_t, vertices_count, dist, dist_obt))
    print('epsilon ' + str(epsilon) + ' done.')


if __name__ == '__main__':
    Line.point_distance = 0.015
    Triangle.distance_trash = 0.01
    PolygonDetector.rdp_epsilon = 0.025
    PolygonDetector.area_threshold = 400
    PolygonDetector.gray_thresh_boundary = 5

    path = './testdata/'
    file = 'testmap_2.png'
    start_points = [[0.05, 0.05], [0.05, 0.95], [0.55, 0.05], [0.05, 0.6]]
    end_points = [[0.9, 0.9], [0.95, 0.05], [0.4, 0.95], [0.95, 0.45]]

    for i in range(len(start_points)):
    #for i in range(1):
        start = start_points[i]
        end = end_points[i]
        #start = [0.05, 0.05]
        #end = [0.05, 0.95]

        vor = image_detect(path+file, start, end)
        result = []

        voronoi(0.0000, vor, start, end, result)
        voronoi(0.0002, vor, start, end, result)
        voronoi(0.0004, vor, start, end, result)
        voronoi(0.0008, vor, start, end, result)
        voronoi(0.0016, vor, start, end, result)
        voronoi(0.0032, vor, start, end, result)
        voronoi(0.0064, vor, start, end, result)
        voronoi(0.0128, vor, start, end, result)
        voronoi(0.0256, vor, start, end, result)
        voronoi(0.0512, vor, start, end, result)

        print_result(file, start, end, result)
        vor.generate_plot_only_points()
        plt.show()
