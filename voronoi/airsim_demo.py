from voronoi import PolygonVoronoi, run_type
from geometry import Line, Triangle
from astar import Astar
from image import PolygonDetector

import airsim
from multiprocessing import Process


# adjustable values
def init_var():
    Line.point_distance = 0.02
    Triangle.distance_trash = 0.04
    PolygonVoronoi.rdp_epsilon = 0.01

    PolygonDetector.rdp_epsilon = 0.035
    PolygonDetector.area_threshold = 400
    PolygonDetector.gray_thresh_boundary = 3


def show_result(objs: list) -> None:
    for obj in objs:
        obj.generate_plot()
    if len(objs) > 0:
        objs[0].show()


def demo_voroni(image_path, start, end, bound, ref_size):
    # boundary
    b1 = Line([[0.0, 0.0], [1.0, 0.0]])
    b2 = Line([[1.0, 0.0], [1.0, 1.0]])
    b3 = Line([[1.0, 1.0], [0.0, 1.0]])
    b4 = Line([[0.0, 0.0], [0.0, 1.0]])

    # reference range detector
    ref = PolygonDetector(image_path)
    ref.add_color_threshold(156)
    ref_result = ref.run(bound=bound, triangulation=False)

    max = [0.0, 0.0]
    min = [bound[0], bound[1]]
    for ele in ref_result[0]:
        if ele[0] < min[0]: min[0] = ele[0]
        if ele[1] < min[1]: min[1] = ele[1]
        if ele[0] > max[0]: max[0] = ele[0]
        if ele[1] > max[1]: max[1] = ele[1]

    # get scaled size from reference range detector
    x_diff = max[0] - min[0]
    y_diff = max[1] - min[1]
    scaler = [ref_size[0]/x_diff, ref_size[1]/y_diff]

    # polygon detector
    pd = PolygonDetector(image_path)
    pd.add_color_threshold(214)
    pd.run(bound=bound)
    triangles = pd.convert_result()

    # voronoi
    vor = PolygonVoronoi()
    vor.add_triangles(triangles)
    vor.add_boundaries([b1, b2, b3, b4])
    vor.add_points([start, end])
    vor_result = vor.run_optimized()

    # astar
    astar = Astar(vor_result, start, end)
    astar_result = astar.run()

    # show result
    show_p = Process(target=show_result, args=([ref, pd, vor, astar],))
    show_p.daemon = True
    show_p.start()

    return astar_result * scaler, show_p


def init_airsim():
    drone = airsim.MultirotorClient()
    drone.reset()
    drone.confirmConnection()
    drone.enableApiControl(True)
    drone.takeoffAsync().join()
    drone.hoverAsync().join()
    return drone

def airsim_run(drone):
    velocity = 1.0
    path = voronoi_result.tolist()
    for i in range(len(path)):
        path[i] = [path[i][1], path[i][0], -0.5]
    
    for ele in path:
        drone.moveToPositionAsync(ele[0], ele[1], ele[2], velocity).join()

    print("goal reached!")


if __name__ == '__main__':
    init_var()
    drone = init_airsim()

    while True:
        coord_in = input("Enter Coordinate to start demo: ").split()
        if coord_in[0] == 'q': break
        
        start = [float(coord_in[0]), float(coord_in[1])]
        end = [float(coord_in[2]), float(coord_in[3])]
        voronoi_result, show_p = demo_voroni(image_path='./testdata/testmap_3.png',
                                             start=start, 
                                             end=end,
                                             bound=[1.0, 1.0], 
                                             ref_size=[0.9, 0.9])

        airsim_run(drone)
        show_p.join()
