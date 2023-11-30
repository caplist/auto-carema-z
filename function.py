import carema
import zz
import os
import huidu
import circle
import cv2 
import xlwt
import mcode
from process_data import DrawPicture
import pandas as pd
from matplotlib import pyplot as plt
class Auto:
    # 创建两个实例，一个是相机，一个是位移台，放到构造函数里面
    def __init__(self):
        self.c = carema.Carema()
        self.z = zz.Piezoconcept(port = "COM3")
        # 用于存储图片名字和对应的位移台的位置
        self.wide_name_position = {}
        # 细定焦下面的图片名字和对应位移台的位置
        self.narrow_name_position = {}
        # 采集数据的数量
        self.max_num = 0
        # 初始位置
        self.position = 0
        # 采集数据的间距
        self.step = 0
        # 粗定焦保存的数据位置
        self.wide_data_path = ""
        # wide_data_path下面文件的名字， 用列表存储
        self.wide_data_namelists = []
        # 细定焦保存的数据位置
        self.narrow_data_path = ""
        # narrow_data_path下面文件的名字
        self.narrow_data_namelists = []
        # 焦点位置
        self.focus_position = 0
        # 灰度最大值对应的图片名
        self.max_px_name = ""
        # 灰度最大值
        self.max_px = 0
        # 创建字典：用于保存name和光强
        self.name_px = {}
        # 细定焦下面的excel文件路径
        self.narrow_excel_path = ""

    def SetNumPosition(self, num, position,step):
        """
        实验室设置
        num: 采集数据的数量
        position: 初始位置
        step: 采集数据的间距
        """
        self.max_num = num 
        self.position = position
        self.step = step

    def CreateDataFile(self):
        """
        创建两个文件夹：wide_data 和 narrow_data
        """
        # 得到当前路径
        current_path = os.getcwd()
        # 拼接路径：存放图片数据
        data_path1 = current_path + '\\' + "wide_data"
        data_path2 = current_path + '\\' + "narrow_data"
        # 判断是否存在定焦文件夹，如果不存在，就创建
        if not os.path.exists(data_path1):
            os.mkdir(data_path1)
        if not os.path.exists(data_path2):
            os.mkdir(data_path2)
        # 将路径保存起来
        self.wide_data_path = data_path1
        self.narrow_data_path = data_path2
    
    # 得到粗定焦文件下面的所有文件名字
    def GetWideDataName(self):
        """
        得到粗定焦文件下面的所有文件名字
        """
        self.wide_data_namelists = os.listdir(self.wide_data_path)
        # print(self.wide_data_namelists)

    # 得到细定焦文件下面的所有文件名字
    def GetNarrowDataName(self):
        """
        得到细定焦文件下面的所有文件名字
        """
        self.narrow_data_namelists = os.listdir(self.narrow_data_path)
        # print(self.narrow_data_namelists)

    # 主循环：采集数据 : 用于粗定焦和细定焦
    def Circulate(self, data_posion, s) :
        """
        主循环：采集数据 : 用于粗定焦和细定焦
        data_posion: 位移台的位置 粗定焦为0 细定焦为焦点位置
        s: 控制在哪个文件夹下面保存文件
        """
        if s == "wide":
            data_path = self.wide_data_path
        elif s == "narrow":
            data_path = self.narrow_data_path
        for i in range(self.max_num):
            # 位移台移动
            self.z.move(data_posion, unit = "u")
            # 相机拍照
            self.c.CapturePicture()
            # 存储数据
            # 将i为转化为三位数的保存格式，比如001，002
            if i < 10:
                picture_path = data_path + '\\' + "Z" + "00" + str(i) + ".jpg"
            elif i < 100:
                picture_path = data_path + '\\' + "Z" + "0" + str(i) + ".jpg"
            else:
                picture_path = data_path + '\\' + "Z" + str(i) + ".jpg"
            # 去除图片名字前面的所有路径
            name = os.path.basename(picture_path)
            # 保存键值对关系
            if s == "wide":
                self.wide_name_position[name] = data_posion
            elif s == "narrow":
                self.narrow_name_position[name] = data_posion
            self.c.SavePicture(picture_path)
            # 每次加步长
            data_posion = data_posion + self.step
        
    # 得到焦点位置
    def GetFocusPosition(self):
        """
        得到焦点位置
        """            
        # self.focus_position = self.wide_name_position[self.max_px_name]
        # print(self.focus_position)
        if self.max_px_name not in self.wide_name_position:
            print(f"Error: {self.max_px_name} not found in wide_name_position")
            return
        self.focus_position = self.wide_name_position[self.max_px_name]
        print(self.focus_position)

    # 粗定焦数据处理 得到像素的最大值对应的名字
    def WideDataProcessing(self):
        """
        粗定焦数据处理 得到像素的最大值对应的名字
        """
        for name in self.wide_data_namelists:
            img_path = os.path.join(self.wide_data_path, name)
            print(img_path)
            # img = cv2.imread(img_path, 1)
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # px = huidu.huidu(img_path,3) # 这个函数直接使用的是原来图像，并没有进行其他处理
            px = mcode.Nihe(img_path)
            # px不为空 并且 px > max_px 更新最大值
            if px and px > self.max_px:
                self.max_px = px
                self.max_px_name = name
            # if px > self.max_px:
                #self.max_px = px
                #self.max_px_name = name
    
    # 细定焦的数据处理
    def NarrowDataProcessing(self):
        """
        细定焦的数据处理
        """
        # 创建excel表格类型文件.
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 在表格中创建一张sheet表单
        sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)
        # 自定义列表
        col = ('name', '光强I')
        # 将列属性元组件col写入sheet中
        for i in range(0, 2):                    # 这里的2是表格的列数
            sheet.write(0, i, col[i])            # 第一个参数是行，第二个参数是列，第三个参数是需要写的内容。
        # 去除列表中的非jpg文件
        for name in self.narrow_data_namelists:
            if not name.endswith('.jpg'):
                self.narrow_data_namelists.remove(name)

        for name in self.narrow_data_namelists:
            img_path = os.path.join(self.narrow_data_path, name)
            print(img_path)
            # img = cv2.imread(img_path, 1)
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # px = circle.huidu(img_path,3)
            px = mcode.Nihe(img_path)
            self.name_px[name] = px
        # 写入数据
            i = 1
            for name, px in self.name_px.items():
                # 将name对应的位置作为横坐标写入excel
                sheet.write(i, 0, self.narrow_name_position[name])
                sheet.write(i, 1, px)
                i = i + 1
        # 保存数据
        self.narrow_excel_path = self.narrow_data_path + '\\' + "data.xls"
        book.save(self.narrow_excel_path)
        # print(self.narrow_data_namelists)

    # 绘制图像
    def DrawPicture(self):
        """
        绘制图像
        """
        df = pd.read_excel(self.narrow_excel_path)
        plt.figure(figsize=(10, 6)) # 设置画布的尺寸
        plt.plot(df['name'], df['光强I']) # 绘制折线图
        plt.title('Axial sensing curve') # 设置图表的标题
        plt.xlabel('Axial position') # 设置x轴的标签
        plt.ylabel('Gray intensity') # 设置y轴的标签
        plt.show()  # 显示图像
        plt.savefig('test.png') # 保存图像

    # 关闭相机和位移台
    def Close(self):
        """
        关闭相机和位移台
        """
        self.c.Close()
        self.z.close()


if __name__ == "__main__":
    # 开始实验
    a = Auto()
    # 设置实验参数
    a.SetNumPosition(100, 0, 1)
    # 创建文件夹
    a.CreateDataFile()
    # 粗定焦
    a.Circulate(0, "wide")
    # 得到粗定焦文件下面的所有文件名字
    a.GetWideDataName()
    # 粗定焦数据处理 得到像素的最大值对应的名字
    a.WideDataProcessing()
    # 得到焦点位置
    a.GetFocusPosition()
    # 细定焦
    # 重新设置实验参数
    a.SetNumPosition(100, a.focus_position - 5, 0.1)  # 后面再修改函数的调用方式
    # 创建细定焦文件夹
    a.Circulate(a.focus_position, "narrow")
    # 得到细定焦文件下面的所有文件名字
    a.GetNarrowDataName()
    # 细定焦的数据处理
    a.NarrowDataProcessing()
    # 绘制图像
    a.DrawPicture()
    # 关闭相机和位移台
    a.Close()