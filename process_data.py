import pandas as pd
import xlrd
from matplotlib import pyplot as plt

def DrawPicture(filepath):

    df = pd.read_excel(filepath)
    plt.figure(figsize=(10, 6)) # 设置画布的尺寸
    plt.plot(df['name'], df['光强I']) # 绘制折线图
    plt.title('Axial sensing curve') # 设置图表的标题
    plt.xlabel('Axial position') # 设置x轴的标签
    plt.ylabel('Gray intensity') # 设置y轴的标签
    plt.show()  # 显示图像
