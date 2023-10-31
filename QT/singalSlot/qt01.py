# 内置信号和自定义槽函数
# from PyQt5.QtWidgets import *
# import sys

# class Winform(QWidget):
# 	def __init__(self,parent=None):
# 		super().__init__(parent)
# 		self.setWindowTitle('内置的信号和自定义槽函数示例')
# 		self.resize(330,  50 ) 
# 		btn = QPushButton('关闭', self)		
# 		btn.clicked.connect(self.btn_close) 

# 	def btn_close(self):
# 		# 自定义槽函数
# 		# self.close()
#             print('自定义槽函数被调用了')
		
# if __name__ == '__main__':
# 	app = QApplication(sys.argv)
# 	win = Winform()
# 	win.show()
# 	sys.exit(app.exec_())

# 自定义信号和内置槽函数
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import pyqtSignal
# import sys

# class Winform(QWidget):
# 	# 自定义信号，不带参数
# 	button_clicked_signal = pyqtSignal()

# 	def __init__(self,parent=None):
# 		super().__init__(parent)
# 		self.setWindowTitle('自定义信号和内置槽函数示例')
# 		self.resize(330,  50 ) 
# 		btn = QPushButton('关闭', self)
# 		# 连接 信号和槽
# 		btn.clicked.connect(self.btn_clicked)
# 		# 接收信号，连接到槽
# 		self.button_clicked_signal.connect(self.close) 

# 	def btn_clicked(self):
# 		# 发送自定义信号，无参数
# 		self.button_clicked_signal.emit()
		                    		
# if __name__ == '__main__':
# 	app = QApplication(sys.argv)
# 	win = Winform()
# 	win.show()
# 	sys.exit(app.exec_())
	

# 使用自定义参数
from PyQt5.QtWidgets import QMainWindow, QPushButton , QWidget , QMessageBox, QApplication, QHBoxLayout
import sys 

class WinForm(QMainWindow):  
	def __init__(self, parent=None):  
		super(WinForm, self).__init__(parent)  
		self.setWindowTitle("信号和槽传递额外参数例子")
		button1 = QPushButton('Button 1')  
		button2 = QPushButton('Button 2')  
        # lambda 表达式传递额外的参数
		button1.clicked.connect(lambda: self.onButtonClick(1)) 
		button2.clicked.connect(lambda: self.onButtonClick(2)) 		

		layout = QHBoxLayout()  
		layout.addWidget(button1)  
		layout.addWidget(button2)  
  
		main_frame = QWidget()  
		main_frame.setLayout(layout)       
		self.setCentralWidget(main_frame)  
  
	def onButtonClick(self, n):  
		print('Button {0} 被按下了'.format(n))  
		QMessageBox.information(self, "信息提示框", 'Button {0} clicked'.format(n))            
  
if __name__ == "__main__":  
	app = QApplication(sys.argv)  
	form = WinForm()  
	form.show()  
	sys.exit(app.exec_())