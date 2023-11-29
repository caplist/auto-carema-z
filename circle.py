# 导入所需的库
import cv2
import numpy as np
import matplotlib.pyplot as plt

def huidu(name, radius):
    # 读取图片并转换为灰度图
    img = cv2.imread(name, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # plt.imshow(gray, cmap='gray')
    # plt.show()
    # 检测圆形光斑并找到圆心和半径
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 30, param1=200, param2=30, minRadius=10, maxRadius=50)
    if detected_circles is not None:
        # 将圆形参数转换为整数
        detected_circles = np.uint16(np.around(detected_circles))

        # 找到半径最大的一个圆形光斑
        max_r = np.max(detected_circles[0, :, 2]) # 最大半径
        max_idx = np.argmax(detected_circles[0, :, 2]) # 最大半径对应的索引
        pt = detected_circles[0, max_idx] # 最大半径对应的圆形参数
        a, b, r = pt[0], pt[1], pt[2] # 圆心和半径

        # 计算灰度质心坐标
        x0 = np.sum(np.arange(a-r, a+r+1) * gray[b-r:b+r+1, a-r:a+r+1].sum(axis=0)) / gray[b-r:b+r+1, a-r:a+r+1].sum()
        y0 = np.sum(np.arange(b-r, b+r+1) * gray[b-r:b+r+1, a-r:a+r+1].sum(axis=1)) / gray[b-r:b+r+1, a-r:a+r+1].sum()

        # 创建一个空白的掩膜，大小和图片相同
        mask = np.zeros_like(gray)
        # 在掩膜上画出圆形区域，颜色为白色（255） 强制转换
        # cv2.circle(mask, (int(x0), int(y0)), radius, (255, 255, 255), -1)
        cv2.circle(mask, (a,b), radius, (255, 255, 255), -1)
        # 使用掩膜提取圆形区域的灰度值
        gray_circle = cv2.bitwise_and(gray, gray, mask=mask)
        # 计算圆形区域的平均灰度值
        mean_gray = np.mean(gray_circle[mask == 255])
        return mean_gray
        # 提取质心位置的灰度值
        # g0 = gray[int(y0), int(x0)]

        # 打印圆形区域的圆心，半径，质心和灰度值
        # print(f'Circle at ({a}, {b}), radius {radius}, centroid at ({x0:.2f}, {y0:.2f}), gray value {mean_gray}')

        # 可视化圆形区域的灰度图像
        # plt.imshow(gray_circle, cmap='gray')
        # plt.show()
