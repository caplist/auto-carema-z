from math import pi
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QLabel,QVBoxLayout
from PyQt5.QtGui import QPixmap,QPalette, QColor, QPainter
from PyQt5.QtCore import Qt
from Ui_02 import Ui_MainWindow  #导入你写的界面类
 
 
class MyMainWindow(QMainWindow,Ui_MainWindow): #这里也要记得改
    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("1.png")
        painter.drawPixmap(self.rect(), pixmap)
 
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())    