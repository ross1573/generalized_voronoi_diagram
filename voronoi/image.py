import cv2
import matplotlib.pyplot as plt
import tripy

from voronoi.geometry import Triangle


class PolygonDetector:
    rdp_epsilon: float
    area_threshold: int
    gray_thresh_boundary: int

    def __init__(self, path, color_threshold = []):
        self.__path = path
        self.__img_gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.__img_gray = cv2.flip(self.__img_gray, 0)
        self.__threshold = []
        for thresh in color_threshold:
            self.add_color_threshold(thresh)

    # generate binary image(threshold)
    def add_color_threshold(self, thresh):
        _t = [thresh - self.gray_thresh_boundary, thresh + self.gray_thresh_boundary]
        _,threshold_lower = cv2.threshold(self.__img_gray, _t[0], 255, cv2.THRESH_BINARY)
        _,threshold_upper = cv2.threshold(self.__img_gray, _t[1], 255, cv2.THRESH_BINARY)
        threshold = threshold_lower - threshold_upper
        self.__threshold.append(threshold)

    def run(self, bound = [0.0, 0.0], triangulation = True):
        self.__contours, self.__contours_original = self.find_contours()

        if bound[0] > 0.0 and bound[1] > 0.0:
            self.normalize(bound)

        if triangulation:
            self.__result = self.triangulation()
        else:
            self.__result = self.__contours
        
        return self.__result

    # find contours
    def find_contours(self) -> list:
        find_result = []
        for threshold in self.__threshold:
            contours,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            find_result += contours
        
        result = []
        original = []
        for cnt in find_result:
            area = cv2.contourArea(cnt)

            if area > self.area_threshold:
                epsilon = self.rdp_epsilon * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                original.append(approx)
                approx_tf = []
                for ele in approx:
                    approx_tf.append(ele[0])
                result.append(approx_tf)

        return result, original

    # delaunay triangulation
    def triangulation(self) -> list:
        triangles = []

        for contour in self.__contours:
            triangulation = tripy.earclip(contour)
            for triangle in triangulation:
                vertices = []
                for vertex in triangle:
                    vertices.append(list(vertex))
                triangles.append(vertices)

        return triangles

    # normalize values between 0 and bound parameter
    # normalized based on image size
    def normalize(self, bound) -> None:
        size = self.__img_gray.shape
        multiplier = [bound[0] / size[1],
                      bound[1] / size[0]]
        
        contours = []
        for contour in self.__contours:
            points = []
            for point in contour:
                x = point[0] * multiplier[0]
                y = point[1] * multiplier[1]
                points.append([x,y])
            contours.append(points)
        self.__contours = contours

    # convert result to Triangle class which are acceptable in polygon voronoi
    def convert_result(self) -> list[Triangle]:
        triangles = []
        for vertices in self.__result:
            triangles.append(Triangle(vertices))
        return triangles

    def __generate_result_image(self) -> cv2.Mat:
        img = cv2.imread(self.__path, cv2.IMREAD_COLOR)
        img = cv2.flip(img, 0)
        for contour in self.__contours_original:
            cv2.drawContours(img, [contour], 0, (255, 0, 0), 5)
        return cv2.flip(img, 0)

    def generate_plot(self):
        img = self.__generate_result_image()
        _, ax = plt.subplots()
        ax.imshow(img)

    def generate_plot_gray(self):
        img = cv2.flip(self.__img_gray, 0)
        _, ax = plt.subplots()
        ax.imshow(img, cmap='gray')

    def show(self):
        plt.show()
    
    def save(self):
        img = self.__generate_result_image()
        cv2.imwrite('polygon_detect_result.png', img)
