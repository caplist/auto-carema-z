import gxipy as gx
from PIL import Image
import sys

class Carema:
    def __init__(self):
        self.device_manager = gx.DeviceManager()
        # 枚举设备
        self.dev_num, self.dev_info_list = self.device_manager.update_all_device_list()
        if self.dev_num == 0:
            sys.exit(1)
        self.strSN = self.dev_info_list[0].get("sn")
        # 通过序列号打开设备
        self.cam = self.device_manager.open_device_by_sn(self.strSN)
        #  开始采集
        self.cam.stream_on()

    # 相机拍照
    def CapturePicture(self):
        # 从第 0 个流通道获取一幅图像
        raw_image = self.cam.data_stream[0].get_image()
        # 从彩色原始图像获取 RGB 图像
        rgb_image = raw_image.convert("RGB")
        if rgb_image is None:
            pass
        # 从 RGB 图像数据创建 numpy 数组
        self.numpy_image = rgb_image.get_numpy_array()
        if self.numpy_image is None:
            pass
        # 显示并保存获得的 RGB 图片
    # 将保存的图像放到指定目录(修改)
    def SavePicture(self, path):
        image = Image.fromarray(self.numpy_image, 'RGB')
        #image.show()
        # 保存图像的时候，需要将图像的名字进行修改，命名依次为Z1,Z2,Z3,Z4,Z5......
        image.save(path)
        # image.save("image.jpg")

    def Close(self):
        # 停止采集，关闭设备
        self.cam.stream_off()
        self.cam.close_device()