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

|-----------------------------------------------|
| testmap_3.png - [0.6, 0.05] > [0.4, 0.95]     |
|-----------------------------------------------|
| Fig | epsilon | seconds | vertices | distance |
|-----|---------|---------|----------|----------|
|   1 |  0.0000 |  15.379 |      449 | 1.387036 | 
|   2 |  0.0002 |   7.079 |      281 | 1.386946 | 
|   3 |  0.0004 |   4.174 |      203 | 1.386847 | 
|   4 |  0.0008 |   2.663 |      143 | 1.386651 | 
|   5 |  0.0016 |   1.796 |       98 | 1.386312 | 
|   6 |  0.0032 |   1.424 |       74 | 1.385955 | 
|   7 |  0.0064 |   1.083 |       52 | 1.384770 | 
|   8 |  0.0128 |   1.017 |       41 | 1.383525 | 
|   9 |  0.0256 |   0.897 |       28 | 1.377260 | 
|  10 |  0.0512 |   0.910 |       24 | 1.377260 | 
|-----------------------------------------------|

|-----------------------------------------------|
| testmap_3.png - [0.05, 0.6] > [0.95, 0.3]     |
|-----------------------------------------------|
| Fig | epsilon | seconds | vertices | distance |
|-----|---------|---------|----------|----------|
|   1 |  0.0000 |  13.804 |      449 | 1.161987 | 
|   2 |  0.0002 |   5.562 |      259 | 1.161941 | 
|   3 |  0.0004 |   3.694 |      191 | 1.161881 | 
|   4 |  0.0008 |   2.319 |      130 | 1.161640 | 
|   5 |  0.0016 |   1.606 |       95 | 1.161399 | 
|   6 |  0.0032 |   1.254 |       66 | 1.160908 | 
|   7 |  0.0064 |   1.098 |       49 | 1.159958 | 
|   8 |  0.0128 |   0.997 |       37 | 1.159180 | 
|   9 |  0.0256 |   0.907 |       27 | 1.156477 | 
|  10 |  0.0512 |   0.891 |       24 | 1.144292 | 
|-----------------------------------------------|
"""


from voronoi.voronoi import PolygonVoronoi, run_type
from voronoi.geometry import *
from voronoi.astar import Astar
from voronoi.image import PolygonDetector

import matplotlib.pyplot as plt
from datetime import datetime


def print_result(file, start, end, result):
    print('|-----------------------------------------------|')
    print('| ' + str(file + ' - ' + str(start) + ' > ' + str(end)).ljust(45) + ' |')
    print('|-----------------------------------------------|')
    print('| Fig | epsilon | seconds | vertices | distance |')
    print('|-----|---------|---------|----------|----------|')
    for i in range(len(result)):
        ele = result[i]
        print('| ' + str(i+1).rjust(3) + ' |  '
                    + '{:1.4f}'.format(ele[0]) + ' | ' 
                    + str(ele[1].seconds).rjust(3) + "." 
                    + str(int(ele[1].microseconds / 1000)).zfill(3) + ' | '
                    + str(ele[2]).rjust(8) + ' | '
                    + '{:1.6f}'.format(ele[3]) + ' | ')
    print('|-----------------------------------------------|')


def image_detect(path, start, end):
    # adjustable values
    Line.point_distance = 0.015
    Triangle.distance_trash = 0.005

    PolygonDetector.rdp_epsilon = 0.035
    PolygonDetector.area_threshold = 400
    PolygonDetector.gray_thresh_boundary = 3

    # boundary
    b1 = Line([[0.0, 0.0], [1.0, 0.0]])
    b2 = Line([[1.0, 0.0], [1.0, 1.0]])
    b3 = Line([[1.0, 1.0], [0.0, 1.0]])
    b4 = Line([[0.0, 0.0], [0.0, 1.0]])

    # polygon detector
    pd = PolygonDetector(path)
    pd.add_color_threshold(214)
    pd.run(bound=[1.0, 1.0])
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
    astar.generate_plot()
    
    end_t = datetime.now()
    vertices_count = len(vor_result.vertices)

    # total distance
    dist = 0.0
    for i in range(len(astar_result)-1):
        dist += distance(astar_result[i], astar_result[i+1])

    result.append((epsilon, end_t - start_t, vertices_count, dist))
    print('epsilon ' + str(epsilon) + ' done.')


if __name__ == '__main__':
    path = './testdata/'
    file = 'testmap_1.png'
    start = [0.05, 0.95]
    end = [0.95, 0.05]
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
    plt.show()
