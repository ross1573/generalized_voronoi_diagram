from voronoi import PolygonVoronoi, run_type
from geometry import Line, Triangle
from astar import Astar


if __name__ == '__main__':
    # adjustable values
    Line.point_distance = 0.2
    Triangle.distance_trash = 0.5
    PolygonVoronoi.rdp_epsilon = 0.15

    # boundary
    b1 = Line([[0.0, 0.0], [10.0, 0.0]])
    b2 = Line([[10.0, 0.0], [10.0, 10.0]])
    b3 = Line([[10.0, 10.0], [0.0, 10.0]])
    b4 = Line([[0.0, 0.0], [0.0, 10.0]])

    # triangles
    t1 = Triangle([[2.0, 1.0], [3.0, 3.0], [1.0, 2.0]])
    t2 = Triangle([[7.0, 6.0], [9.0, 9.0], [5.0, 7.0]])
    t3 = Triangle([[5.0, 3.0], [7.0, 4.0], [6.0, 5.0]])

    #point
    start = [2.0, 8.0]
    end = [8.3, 2.0]

    # voronoi
    vor = PolygonVoronoi()

    # add triangles
    vor.add_triangle(t1)
    vor.add_triangle(t2)
    vor.add_triangle(t3)

    # add boundaries
    vor.add_boundary(b1)
    vor.add_boundary(b2)
    vor.add_boundary(b3)
    vor.add_boundary(b4)

    # add points
    vor.add_point(start)
    vor.add_point(end)

    # run
    vor.run(run_type.non_lined)
    vor.run(run_type.non_deleted)
    vor.run(run_type.non_optimized)
    vor.run(run_type.optimized)
    result = vor.get_result()

    astar = Astar(result, start, end)
    astar.run()
    astar.generate_plot()
    
    astar.show()
