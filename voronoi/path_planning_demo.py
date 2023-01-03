from voronoi import PolygonVoronoi, run_type
from geometry import Line, Triangle
from astar import Astar
from image import PolygonDetector


if __name__ == '__main__':
    # adjustable values
    Line.point_distance = 0.02
    Triangle.distance_trash = 0.04

    PolygonVoronoi.rdp_epsilon = 0.01
    PolygonDetector.rdp_epsilon = 0.035
    PolygonDetector.area_threshold = 400
    PolygonDetector.gray_thresh_boundary = 3

    # boundary
    b1 = Line([[0.0, 0.0], [1.0, 0.0]])
    b2 = Line([[1.0, 0.0], [1.0, 1.0]])
    b3 = Line([[1.0, 1.0], [0.0, 1.0]])
    b4 = Line([[0.0, 0.0], [0.0, 1.0]])

    #point
    start = [0.05, 0.05]
    end = [0.9, 0.9]

    # polygon detector
    pd = PolygonDetector('./testdata/testmap_3.png')
    pd.add_color_threshold(214)
    pd.run(bound=[1.0, 1.0])
    triangles = pd.convert_result()

    # voronoi
    vor = PolygonVoronoi()
    vor.add_triangles(triangles)
    vor.add_boundaries([b1, b2, b3, b4])
    vor.add_points([start, end])
    vor.run(run_type.non_lined)
    vor.run(run_type.non_deleted)
    vor.run(run_type.non_optimized)
    vor_result = vor.run(run_type.optimized)

    # astar
    astar = Astar(vor_result, start, end)
    astar.run()
    astar.generate_plot()
    
    # show result
    pd.show()
    pd.save()
    astar.show()
