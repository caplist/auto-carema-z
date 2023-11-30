import cv2 as cv
import functools
from matplotlib import pyplot as p, cm, colors
import time
import numpy as np
from numpy import *
from PIL import Image
from matplotlib import pyplot as plt
import os
from scipy import optimize
import xlwt


# 第2次程序
# ----上面中心坐标不对，hough单独的程序坐标是对的，所以中心坐标程序用hough的，后面光强值用原图取。-------

def Nihe(name):
    # 2.灰度化、中值滤波、边缘检测
    img = cv.imread(name)  # 读取图片，灰度化
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.blur(img, (5, 5))  # 均值模糊，滤波作用
    double__otsu_threshold, src = cv.threshold(gray, 100, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # 阈值化处理
    edges = cv.Canny(src, 0, 255)

    # 3.获取中心坐标
    x = []
    y = []
    for i in range(len(edges)):
        for j in range(len(edges[0])):
            if edges[i][j] != 0:
                x.append(i)
                y.append(j)
    basename = 'arc'

    # 质心坐标
    x_m = mean(x)
    y_m = mean(y)
    def countcalls(fn):
        "decorator function count function calls "

        @functools.wraps(fn)
        def wrapped(*args):
            wrapped.ncalls += 1
            return fn(*args)

        wrapped.ncalls = 0
        return wrapped

    def calc_R(xc, yc):

        return sqrt((x - xc) ** 2 + (y - yc) ** 2)

    @countcalls
    def f_2(c):
        Ri = calc_R(*c)
        return Ri - Ri.mean()
    # 圆心估计
    center_estimate = x_m, y_m
    center_2, _ = optimize.leastsq(f_2, center_estimate)
    xc_2, yc_2 = center_2
    Ri_2 = calc_R(xc_2, yc_2)
    # 拟合圆的半径
    R_2 = Ri_2.mean()
    residu_2 = sum((Ri_2 - R_2) ** 2)
    residu2_2 = sum((Ri_2 ** 2 - R_2 ** 2) ** 2)
    ncalls_2 = f_2.ncalls

    # 4.输出中心坐标
    # print(xc_2, yc_2)  # 中心坐标，输出的顺序是y,x

    # 5.输入中心点坐标，并显示中心点的像素值
    # xx = int(yc_2)  # x,y转换中心坐标对了
    # yy = int(xc_2)
    xx = yc_2      # x,y转换中心坐标对了
    yy = xc_2
    # px = edges[yy, xx]
    # print('px:', px)

    # edges[yy, xx] = 255  # 改变中心点的灰度值，看中心点定位是否准确

    # 显示处理后图像
    # plt.imshow(edges)
    # plt.show()

    # 6.1 方形 15*15的中心区域的像素值
    # roi = img[yy - 15:yy + 14, xx - 15:xx + 14]  # 30*30区域。    取原图的像素值

    # 6.2 圆形提取：不能直接使用切片（半径为15）
    # Assuming the center of the circle is (cy, cx) and the radius is r
    cy, cx, r = yy, xx, 5
    # Create a grid of indices
    y, x = np.ogrid[:img.shape[0], :img.shape[1]]
    # Create a mask where the condition is True
    mask = ((y - cy) ** 2 + (x - cx) ** 2) <= r ** 2
    # Apply the mask to the image
    roi = img[mask]
    return np.mean(roi)

