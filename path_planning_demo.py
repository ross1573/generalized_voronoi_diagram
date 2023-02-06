from voronoi.voronoi import GeneralizedVoronoi, run_type
from voronoi.geometry import Line, Triangle
from voronoi.astar import Astar
from voronoi.image import PolygonDetector


if __name__ == '__main__':
    # adjustable values
    Line.point_distance = 0.015
    Triangle.distance_trash = 0.02

    GeneralizedVoronoi.rdp_epsilon = 0.0064
    PolygonDetector.rdp_epsilon = 0.01
    PolygonDetector.area_threshold = 400
    PolygonDetector.gray_thresh_boundary = 3

    # boundary
    b1 = Line([[0.0, 0.0], [1.0, 0.0]])
    b2 = Line([[1.0, 0.0], [1.0, 1.0]])
    b3 = Line([[1.0, 1.0], [0.0, 1.0]])
    b4 = Line([[0.0, 0.0], [0.0, 1.0]])
    line = Line([[0.1, 0.2], [0.2, 0.1]])

    #point
    start = [0.05, 0.05]
    end = [0.9, 0.9]

    # polygon detector
    pd = PolygonDetector('./testdata/voronoi/map0.png', [214, 255])
    polygons = pd.run(bound=[1.0, 1.0])

    # voronoi
    vor = GeneralizedVoronoi()
    vor.add_polygons(polygons)
    vor.add_boundaries([b1, b2, b3, b4])
    vor.add_line(line)
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
