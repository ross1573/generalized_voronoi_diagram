from voronoi.image import PolygonDetector
from voronoi.geometry import *

import pyvisgraph as vg


def image_detect(path, show):
    # polygon detector
    pd = PolygonDetector(path, [214, 255])
    pd_result = pd.run(bound=[1.0, 1.0], triangulation=False)
    if show:
        pd.generate_plot()
        pd.show()

    poly = []
    for ele in pd_result:
        p = []
        for vertex in ele:
            p.append(vg.Point(vertex[0], vertex[1]))                
    poly.append(p)

    return poly


if __name__ == '__main__':
    map = 0

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
        PolygonDetector.gray_thresh_boundary = 3
    elif map == 4:
        PolygonDetector.rdp_epsilon = 0.001
        PolygonDetector.area_threshold = 400
        PolygonDetector.gray_thresh_boundary = 15
    elif map == 5:
        PolygonDetector.rdp_epsilon = 0.005
        PolygonDetector.area_threshold = 400
        PolygonDetector.gray_thresh_boundary = 5
    elif map == 6:
        PolygonDetector.rdp_epsilon = 0.0005
        PolygonDetector.area_threshold = 400
        PolygonDetector.gray_thresh_boundary = 15

    path_str = './testdata/'
    file_str = 'map' + str(map) + '.png'
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

        poly = image_detect(path_str+file_str, False)
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