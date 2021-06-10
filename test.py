import sys,math
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Drawing(QWidget):
    def __init__(self,parent=None):
        super(Drawing,self).__init__(parent)
        self.resize(300,200)
        self.setWindowTitle('在窗口画点')

    def paintEvent(self,event):
        #初始化绘图工具
        qp=QPainter()
        #开始在窗口绘制
        qp.begin(self)
        #自定义画点方法
        self.drawPoints(qp)
        #结束在窗口的绘制
        qp.end()

    def drawPoints(self,qp):
        qp.setPen(Qt.red)
        size=self.size()

        qp.drawLine(150, 70, 570, 260)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=Drawing()
    demo.show()
    sys.exit(app.exec_())
