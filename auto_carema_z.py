# Z位移台移动一次，carema拍一次照片进行存储，然后统一命名，

# 存储： 获取当前目录的相对路径，在当前工作目录下面创建data文件夹，后期用于图像的灰度值提取


# 界面：
#
# 日志区域：eg：创建文件夹成功后，打印一下绝对路径
# 采集进度条： 表示本次实验采集数据的进度（可选）
# 测量设置
# 单位的选定，n和u
# 上下按钮：Z轴的位移
# 选定模式按钮：以间距为多少进行数据采集
# 数据数量按钮： 本次实验采集需要的数据
# 显示Z轴的位移框框
#
#
#
# 开始采集按钮：   开始实验数据采集
# 数据分析按钮：   对data文件夹下面的图片进行灰度值分析，将结果存到表格里面
#
# 将数据进行拟合，画出图像（用什么画，这一步自动还是手动）
# 结果分析：需要看论文
# 验证
# 先用程序采集一张图片，跑一下灰度值，然后程序自己采集一张，对比一下灰度值，或者连续采集一张，灰度值有没有变化

from zz import Piezoconcept
from carema import Carema
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


if __name__ == "__main__":

    # 得到当前路径
    current_path = os.getcwd()
    print("当前工作路径：", current_path)
    # 创建data文件夹
    # os.mkdir(current_path + '\\' + "data")
    # 拼接路径：存放图片数据
    data_path = current_path + '\\' + "data"
    # picture_path = data_path + '\\' + "Z" + "00" + str(0) + ".jpg"
    print("存放图片数据路径：", data_path)
    # print("图片名称", picture_path)
    # 创建两个实例，一个是相机，一个是位移台
    # 没有连接设备的时候，直接异常退出了
    c = Carema()
    z = Piezoconcept(port = "COM3")
   # print(z.INFO())
  
    # 使用循环控制采集数据的数量
    # 采集数据的间距
    # 采集数据的单位

    # 采集数据的数量
    max_num = 10
    # 初始位置
    step = 0
    for i in range(max_num):
        # 位移台移动
        z.move(step, unit = "u")
        # 相机拍照
        c.CapturePicture()
        # 存储数据
        # 将i为转化为三位数的保存格式，比如001，002
        if i < 10:
            picture_path = data_path + '\\' + "Z" + "00" + str(i) + ".jpg"
        elif i < 100:
            picture_path = data_path + '\\' + "Z" + "0" + str(i) + ".jpg"
        else:
            picture_path = data_path + '\\' + "Z" + str(i) + ".jpg"
        print(picture_path)
        c.SavePicture(picture_path)
        step = step + 9
        z.PrintPosition()


    # 位移台进行回退
    z.move(-max_num * step, unit = "u")
    # 关闭相机和位移台
    c.Close()
    z.close()

    print("采集数据完成，开始数据处理")
    # 数据处理部分
    name_lists = os.listdir(data_path)
    print('name_lists:', name_lists)
    time_start = time.time()

    # 创建excel表格类型文件.
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 在表格中创建一张sheet表单
    sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)
    # 自定义列表
    col = ('name', '光强I')
    # 将列属性元组件col写入sheet中
    for i in range(0, 2):                    # 这里的2是表格的列数
        sheet.write(0, i, col[i])            # 第一个参数是行，第二个参数是列，第三个参数是需要写的内容。
    # 创建字典，用于保存name和光强
    dict = {}
    for name in name_lists:
        img_path = os.path.join(data_path, name)    # 返回指定文件夹下的一张图片的路径
        img = cv.imread(img_path, 1)
        print('name:', name)
        # 转换为灰度图像
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # 2.灰度化、中值滤波、边缘检测
        # img = cv.blur(img, (5, 5))  # 均值模糊，滤波作用
        # double__otsu_threshold, src = cv.threshold(img, 100, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # 阈值化处理
        # edges = cv.Canny(src, 0, 255)
        # 找到最亮像素点的坐标
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(gray)
        brightest_pixel = max_loc
        # 5.输入中心点坐标，并显示中心点的像素值
        xx = brightest_pixel[0] # x,y转换中心坐标对了
        yy = brightest_pixel[1]
        # xx = yc_2
        # yy = xc_2
        # px = edges[yy, xx]
        # print('px:', px)
        # edges[yy, xx] = 255  # 改变中心点的灰度值，看中心点定位是否准确
        # 显示处理后图像
        # plt.imshow(edges)
        # plt.show()
        # 6.3*3的中心区域的像素值
        # roi = img[yy - 1:yy + 2, xx - 1:xx + 3]  # 3*3区域。    取原图的像素值
        cy, cx, r = yy, xx, 15
        # Create a grid of indices
        y, x = np.ogrid[:img.shape[0], :img.shape[1]]
        # Create a mask where the condition is True
        mask = ((y - cy)**2 + (x - cx)**2) <= r**2
        # Apply the mask to the image
        roi = img[mask]
        px = np.mean(roi)
        print('I:', px)
        # 输出数据为表格
        # 将数据写入sheet中
        # 用哈希表存数据
        dict[name] = px                
        i = 1
        # print(dict)
        for key in dict:
            sheet.write(i, 0, key)
            sheet.write(i, 1, dict[key])
            i = i + 1
        savepath = data_path + '\\' + "result.xls"
        book.save(savepath)
        # 本次实验完成
    print("本次实验完成")



