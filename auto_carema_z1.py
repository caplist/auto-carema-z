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
from process_data import DrawPicture
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
import pandas as pd
import circle

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
  
    # 使用循环控制采集数据的数量
    # 采集数据的间距
    # 采集数据的单位

    # 采集数据的数量
    max_num = 100
    # 初始位置
    step = 0
    # 保存图片名字和位置的字典
    name_position = {}
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
        # print(picture_path)
        # 去除图片名字前面的所有路径
        name_path = os.path.basename(picture_path)
        # 保存键值对关系
        name_position[name_path] = step
        c.SavePicture(picture_path)
        # 每次加步长
        step = step + 1
        # z.PrintPosition()

    # 位移台进行回退
    # 关闭相机和位移台
    # c.Close()
    # z.close()

    print("粗定焦完成，开始细定焦")
    # 数据处理部分
    name_lists = os.listdir(data_path)
    # print('name_lists:', name_lists)
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
    # dict = {}
    # 去除列表中的非jpg文件
    for name in name_lists:
        if not name.endswith('.jpg'):
            name_lists.remove(name)
    # 定义全局保存图片路径
    savepath = ''
    # 保存最大值对应的图片名
    max_px_name = ''
    max_px = 0
    for name in name_lists:
        img_path = os.path.join(data_path, name)    # 返回指定文件夹下的一张图片的路径
        img = cv.imread(img_path, 1)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        px = circle.huidu(img_path,3)
        # 更新最大值
        if px > max_px:
            max_px = px
            max_px_name = name

    # 得到焦点的位置
    focul_position = name_position[max_px_name]
    # 开始细定焦实验
    print("本次实验完成")



