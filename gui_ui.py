# -*- coding: utf-8 -*-


from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QPen, QPixmap, QImage
import sys
from overload_qt import RouterLabel
import itertools
ROUTER_NUM = 4
SCREEN_H = 800
SCREEN_W = 600


class UiMainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super(UiMainWin, self).__init__()
        self.setObjectName("mainWin")
        self.resize(SCREEN_H, SCREEN_W)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.router_labels = list()
        self.router_id_labels = list()

        # 设置路由图标
        router_x = [SCREEN_W * 0.25, SCREEN_W * 0.90]
        router_y = [SCREEN_H * 0.1, SCREEN_H * 0.3]
        router_x += router_x
        router_y += router_y[::-1]
        seq = [0, 2, 3, 1]
        for i in range(ROUTER_NUM):
            label = RouterLabel(self.centralwidget)
            label.setGeometry(QtCore.QRect(router_x[i], router_y[i], 72, 15))
            label.setObjectName("label" + str(i))
            qi = QImage('figures/router_s.png')
            label.resize(qi.width(), qi.height())
            label.setPixmap(QPixmap(qi))
            self.router_labels.append(label)
            self.label = RouterLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(router_x[i], router_y[i] + 70, 72, 15))
            self.label.setText(str(seq[i]))

        # 设置状态灯图标
        status_lights_x = [SCREEN_W * 0.15, SCREEN_W * 1.1]
        status_lights_y = [SCREEN_H * 0.12, SCREEN_H * 0.32]
        status_lights_x += status_lights_x
        status_lights_y += status_lights_y[::-1]
        self.status_lights = list()
        for i in range(ROUTER_NUM):
            status_light = QtWidgets.QLabel(self.centralwidget)
            status_light.setGeometry(QtCore.QRect(status_lights_x[i], status_lights_y[i], 72, 15))
            status_light.setObjectName("status_light" + str(i))
            qi = QImage('figures/red_s.png')
            status_light.resize(qi.width(), qi.height())
            status_light.setPixmap(QPixmap(qi))
            self.status_lights.append(status_light)

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 360, 801, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.layout_but = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.layout_but.setContentsMargins(0, 0, 0, 0)
        self.layout_but.setObjectName("layout_but")

        # 重置按钮
        self.resetbut = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.resetbut.setMaximumSize(QtCore.QSize(100, 30))
        self.resetbut.setObjectName("stopbut")
        self.layout_but.addWidget(self.resetbut, 0, 1, 1, 1)

        # 初始化按钮
        self.initbut = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.initbut.setMaximumSize(QtCore.QSize(100, 30))
        self.initbut.setObjectName("initbut")
        self.layout_but.addWidget(self.initbut, 0, 0, 1, 1)

        # 停止按钮
        self.stopbut = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.stopbut.setMaximumSize(QtCore.QSize(100, 30))
        self.stopbut.setObjectName("unknowbut")
        self.layout_but.addWidget(self.stopbut, 1, 0, 1, 1)

        # 继续按钮
        self.updatewbut = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.updatewbut.setMaximumSize(QtCore.QSize(100, 30))
        self.updatewbut.setObjectName("exitbut")
        self.layout_but.addWidget(self.updatewbut, 1, 1, 1, 1)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # 设置按钮文字
        self.add_name()
        QtCore.QMetaObject.connectSlotsByName(self)

        # 设置画笔
        self.qp = QPainter()

        self.edges = list()
        edge = QtWidgets.QLineEdit(self.centralwidget)
        edge.setGeometry(QtCore.QRect(SCREEN_W * 0.62, SCREEN_H * 0.12, 30, 20))
        self.edges.append(edge)
        edge = QtWidgets.QLineEdit(self.centralwidget)
        edge.setGeometry(QtCore.QRect(SCREEN_W * 0.62, SCREEN_H * 0.23, 30, 20))
        self.edges.append(edge)
        edge = QtWidgets.QLineEdit(self.centralwidget)
        edge.setGeometry(QtCore.QRect(SCREEN_W * 0.25, SCREEN_H * 0.23, 30, 20))
        self.edges.append(edge)
        edge = QtWidgets.QLineEdit(self.centralwidget)
        edge.setGeometry(QtCore.QRect(SCREEN_W * 1.02, SCREEN_H * 0.23, 30, 20))
        self.edges.append(edge)
        edge = QtWidgets.QLineEdit(self.centralwidget)
        edge.setGeometry(QtCore.QRect(SCREEN_W * 0.62, SCREEN_H * 0.32, 30, 20))
        self.edges.append(edge)

    def paintEvent(self, event):
        """
        设置绘画事件
        :param event:
        :return:
        """
        # 开始在窗口绘制
        self.qp.begin(self)
        # 画线方法
        self.draw_lines()
        # 结束在窗口的绘制
        self.qp.end()

    def draw_lines(self, color='b'):
        """
        绘制拓扑网络连线
        :param color:
        :return:
        """
        if color == 'b':
            self.qp.setPen(Qt.black)
        else:
            self.qp.setPen(Qt.red)
        self.qp.drawLine(SCREEN_W * 0.25, SCREEN_H * 0.15, SCREEN_W * 0.90, SCREEN_H * 0.3)
        self.qp.drawLine(SCREEN_W * 0.25, SCREEN_H * 0.15, SCREEN_W * 0.90, SCREEN_H * 0.15)
        self.qp.drawLine(SCREEN_W * 0.25, SCREEN_H * 0.35, SCREEN_W * 0.90, SCREEN_H * 0.35)
        self.qp.drawLine(SCREEN_W * 0.34, SCREEN_H * 0.15, SCREEN_W * 0.34, SCREEN_H * 0.35)
        self.qp.drawLine(SCREEN_W * 0.99, SCREEN_H * 0.15, SCREEN_W * 0.99, SCREEN_H * 0.35)

    def add_name(self):
        """
        设置按钮文字说明
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainWin", "OSPF模拟"))
        self.resetbut.setText(_translate("mainWin", "重置路由"))
        self.initbut.setText(_translate("mainWin", "初始化路由"))
        self.stopbut.setText(_translate("mainWin", "停止"))
        self.updatewbut.setText(_translate("mainWin", "更新权重"))

    def change_light(self, p, l_type='r'):
        if l_type == 'y':
            qi = QImage('figures/yellow_s.png')
        elif l_type == 'g':
            qi = QImage('figures/green_s.png')
        else:
            qi = QImage('figures/red_s.png')
        mapping = {0: 0, 1: 3, 2: 1, 3: 2}
        self.status_lights[mapping[p]].resize(qi.width(), qi.height())
        self.status_lights[mapping[p]].setPixmap(QPixmap(qi))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = UiMainWin()
    ui.show()
    sys.exit(app.exec_())
