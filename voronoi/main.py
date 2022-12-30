from voronoi import Line, Triangle, OptimizedVoronoi


if __name__ == '__main__':
    # adjustable values
    Line.point_distance = 0.2
    Triangle.distance_trash = 0.5
    OptimizedVoronoi.division_angle = 0.1

    # boundary
    b1 = Line([[0.0, 0.0], [10.0, 0.0]])
    b2 = Line([[10.0, 0.0], [10.0, 10.0]])
    b3 = Line([[10.0, 10.0], [0.0, 10.0]])
    b4 = Line([[0.0, 0.0], [0.0, 10.0]])

    # triangles
    t1 = Triangle([[2.0, 1.0], [3.0, 3.0], [1.0, 2.0]])
    t2 = Triangle([[7.0, 6.0], [9.0, 9.0], [5.0, 7.0]])
    t3 = Triangle([[5.0, 3.0], [7.0, 4.0], [6.0, 5.0]])

    # voronoi
    vor = OptimizedVoronoi()

    # add triangles
    vor.add_triangle(t1)
    vor.add_triangle(t2)
    vor.add_triangle(t3)

    # add boundaries
    vor.add_boundary(b1)
    vor.add_boundary(b2)
    vor.add_boundary(b3)
    vor.add_boundary(b4)

    # run
    vor.run_non_lined()
    vor.generate_plot()
    vor.run_non_deleted()
    vor.generate_plot()
    vor.run_non_optimized()
    vor.generate_plot()
    vor.run()
    vor.generate_plot()
    vor.show()
