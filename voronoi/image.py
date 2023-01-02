import cv2
import sys
import numpy as np
from scipy.spatial import Delaunay

from geometry import Triangle


class PolygonDetector:
    rdp_epsilon: float
    area_threshold: int
    thresh_boundary: int

    def __init__(self, path, color_threshold = []):
        self.__path = path
        self.__img_gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.__threshold = []
        for thresh in color_threshold:
            self.add_color_threshold(thresh)

    # generate binary image(threshold)
    def add_color_threshold(self, thresh):
        _t = [thresh - self.thresh_boundary, thresh + self.thresh_boundary]
        _,threshold = cv2.threshold(self.__img_gray, _t[0], _t[1], cv2.THRESH_BINARY)
        self.__threshold.append(threshold)

    def run(self, bound = [0.0, 0.0], triangulation = True):
        self.__contours, self.__contours_original = self.find_contours()

        if bound[0] > 0.0 or bound[1] > 0.0:
            self.normalize(bound)

        if triangulation:
            self.__result = self.triangulation()
        
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
            tri_obj = Delaunay(contour)
            for tri in tri_obj.vertices:
                points = []
                for vertex in tri:
                    points.append(contour[vertex])
                triangles.append(points)

        return triangles

    # normailize values between 0 and bound parameter
    def normalize(self, bound) -> None:
        min = [sys.maxsize, sys.maxsize]
        max = [0, 0]
        for contour in self.__contours:
            for point in contour:
                if point[0] > max[0]: max[0] = point[0]
                if point[1] > max[1]: max[1] = point[1]
                if point[0] < min[0]: min[0] = point[0]
                if point[1] < min[1]: min[1] = point[1]

        dis = [max[0] + min[0], max[1] + min[1]]
        if dis[0] == 0.0 or dis[1] == 0.0:
            raise ValueError("points have only 1d")

        multiplier = [bound[0] / (dis[0]), bound[1] / (dis[1])]
        
        contours = []
        for contour in self.__contours:
            points = []
            for point in contour:
                x = point[0] * multiplier[0]
                y = bound[1] - (point[1] * multiplier[1])
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
        for contour in self.__contours_original:
            cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)
        return img
        
    def show(self):
        img = self.__generate_result_image()
        cv2.imshow('PolygonDetectResult', img)
        cv2.waitKey(1)
    
    def save(self):
        img = self.__generate_result_image()
        cv2.imwrite('polygon_detect_result.png', img)
