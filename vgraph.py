from voronoi.image import PolygonDetector
from voronoi.geometry import *

import pyvisgraph as vg


def image_detect(path):
    # polygon detector
    pd = PolygonDetector(path, [214, 255])
    result = pd.run(bound=[1.0, 1.0], triangulation=False)

    return result


if __name__ == '__main__':
    map = 4

    if map == 1:
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
        PolygonDetector.gray_thresh_boundary = 3

    path_str = './testdata/'
    file_str = 'map' + str(map) + '.png'
    start_points = [[0.05, 0.05], [0.05, 0.95], [0.55, 0.05], [0.05, 0.6]]
    end_points = [[0.9, 0.9], [0.95, 0.05], [0.4, 0.95], [0.95, 0.45]]

    for i in range(len(start_points)):
        if map == 4:
            start = [0.05, 0.05]
            end = [0.05, 0.95]
            poly = [[vg.Point(0.832, 0.792),
                 vg.Point(0.217, 0.776),
                 vg.Point(0.224, 0.190),
                 vg.Point(0.810, 0.185),
                 vg.Point(0.810, 0.622),
                 vg.Point(0.381, 0.622),
                 vg.Point(0.370, 0.417),
                 vg.Point(0.680, 0.420),
                 vg.Point(0.680, 0.370),
                 vg.Point(0.337, 0.370),
                 vg.Point(0.337, 0.670),
                 vg.Point(0.840, 0.670),
                 vg.Point(0.842, 0.140),
                 vg.Point(0.165, 0.140),
                 vg.Point(0.165, 0.835),
                 vg.Point(0.785, 0.834)]]
        elif map == 5:
            start = [0.05, 0.05]
            end = [0.5, 0.5]
            # TODO
            poly = [[]]
        elif map == 6:
            start = [0.05, 0.95]
            end = [0.95, 0.05]
            # TODO
            poly = [[]]
        else:
            start = start_points[i]
            end = end_points[i]

            image_poly = image_detect(path_str+file_str)
            poly = []
            for ele in image_poly:
                p = []
                for vertex in ele:
                    p.append(vg.Point(vertex[0], vertex[1]))                
            poly.append(p)

        g = vg.VisGraph()
        g.build(poly)
        start_point = vg.Point(start[0], start[1])
        end_point = vg.Point(end[0], end[1])
        path = g.shortest_path(start_point, end_point)
        print(path)

        points = []
        for point in path:
            points.append(np.array([point.x, point.y]))
        dist = total_distance(points)
        print(dist)

        if map > 3: break