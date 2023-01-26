from voronoi.voronoi import PolygonVoronoi, run_type
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
    pd = PolygonDetector(path, [214, 255])
    pd.run(bound=[1.0, 1.0])
    #pd.generate_plot()
    #pd.show()
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

    map = 6

    if map == 0:
        PolygonDetector.rdp_epsilon = 0.01
        PolygonDetector.area_threshold = 400
        PolygonDetector.gray_thresh_boundary = 3
    elif map == 1:
        PolygonDetector.rdp_epsilon = 0.025
        PolygonDetector.area_threshold = 400
        PolygonDetector.gray_thresh_boundary = 5
    elif map == 2:
        PolygonDetector.rdp_epsilon = 0.025
        PolygonDetector.area_threshold = 400
        PolygonDetector.gray_thresh_boundary = 5
    elif map == 3:
        PolygonDetector.rdp_epsilon = 0.01
        PolygonDetector.area_threshold = 400
        PolygonDetector.gray_thresh_boundary = 5
    elif map == 4:
        PolygonDetector.rdp_epsilon = 0.01
        PolygonDetector.area_threshold = 400
        PolygonDetector.gray_thresh_boundary = 15        
    elif map == 5:
        PolygonDetector.rdp_epsilon = 0.005
        PolygonDetector.area_threshold = 400
        PolygonDetector.gray_thresh_boundary = 5
    elif map == 6:
        PolygonDetector.rdp_epsilon = 0.005
        PolygonDetector.area_threshold = 400
        PolygonDetector.gray_thresh_boundary = 5

    path = './testdata/'
    file = 'map' + str(map) + '.png'
    start_points = [[0.05, 0.05], [0.05, 0.95], [0.55, 0.05], [0.05, 0.6]]
    end_points = [[0.9, 0.9], [0.95, 0.05], [0.4, 0.95], [0.95, 0.45]]

    for i in range(len(start_points)):
        if map == 4:
            start = [0.05, 0.05]
            end = [0.05, 0.95]
        elif map == 5:
            start = [0.05, 0.05]
            end = [0.5, 0.5]
        elif map == 6:
            start = [0.05, 0.95]
            end = [0.95, 0.05]
        else:
            start = start_points[i]
            end = end_points[i]

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

        if map > 3: break