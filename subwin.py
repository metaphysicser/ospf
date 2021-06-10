# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5 import Qt


class RouterUI(QtWidgets.QWidget):
    update = Qt.pyqtSignal(int, dict)
    stop = Qt.pyqtSignal(int)

    def __init__(self, u_id):
        super().__init__()
        self.id = u_id
        self.setObjectName("Form")
        self.resize(400, 400)
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 391, 401))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 371, 321))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_status = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_status.setObjectName("label_status")
        self.gridLayout.addWidget(self.label_status, 3, 0, 1, 1)
        self.edit_mask = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_mask.setObjectName("edit_mask")
        self.gridLayout.addWidget(self.edit_mask, 2, 1, 1, 1)
        self.label_id = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_id.setObjectName("label_id")
        self.gridLayout.addWidget(self.label_id, 0, 0, 1, 1)
        self.label_neighbors = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_neighbors.setObjectName("label_neighbors")
        self.gridLayout.addWidget(self.label_neighbors, 4, 0, 1, 1)
        self.edit_id = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_id.setObjectName("edit_id")
        self.gridLayout.addWidget(self.edit_id, 0, 1, 1, 1)
        self.edit_status = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_status.setObjectName("edit_status")
        self.gridLayout.addWidget(self.edit_status, 3, 1, 1, 1)
        self.edit_neighbors = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_neighbors.setObjectName("edit_neighbors")
        self.gridLayout.addWidget(self.edit_neighbors, 4, 1, 1, 1)
        self.label_ip = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_ip.setObjectName("label_ip")
        self.gridLayout.addWidget(self.label_ip, 1, 0, 1, 1)
        self.edit_ip = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_ip.setObjectName("edit_ip")
        self.gridLayout.addWidget(self.edit_ip, 1, 1, 1, 1)
        self.label_mask = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_mask.setObjectName("label_mask")
        self.gridLayout.addWidget(self.label_mask, 2, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 320, 371, 41))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.but_update = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.but_update.setMinimumSize(QtCore.QSize(0, 0))
        self.but_update.setObjectName("but_update")
        self.gridLayout_2.addWidget(self.but_update, 0, 0, 1, 1)
        self.but_stop = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.but_stop.setObjectName("but_stop")
        self.gridLayout_2.addWidget(self.but_stop, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        # 路由表设置
        self.tableWidget = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 391, 371))
        self.tableWidget.setMaximumSize(QtCore.QSize(391, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(5)
        self.table_headers = ['目标ID', '目标IP', '目标掩码', '下一跳', '路由开销', '路径']
        for i in range(6):
            item = QtWidgets.QTableWidgetItem()
            item.setText(self.table_headers[i])
            self.tableWidget.setHorizontalHeaderItem(i, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(80)
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.addTab(self.tab_2, "")

        self.setWindowTitle("详细信息")
        self.label_id.setText("路由id")
        self.label_ip.setText("路由ip")
        self.label_status.setText("路由状态")
        self.label_neighbors.setText("相邻路由")
        self.label_mask.setText("子网掩码")
        self.but_update.setText("更新")
        self.but_stop.setText("停止")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "路由状态")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "路由表")
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        # 绑定按钮
        self.but_update.clicked.connect(self.update_router)
        self.but_stop.clicked.connect(self.stop_router)

    def update_conf(self, conf):
        self.edit_ip.setPlaceholderText(conf['ip'])
        self.edit_mask.setPlaceholderText(conf['mask'])
        self.edit_id.setPlaceholderText(str(conf['id']))
        self.edit_status.setPlaceholderText(str(conf['status']))
        self.edit_neighbors.setPlaceholderText(str(conf['neighbors']))

    def update_table(self, router_table):
        for i in range(len(self.table_headers)):
            for j in range(len(router_table[self.table_headers[i]])):
                item = QtWidgets.QTableWidgetItem()
                text = router_table[self.table_headers[i]][j]
                if type(text) != str:
                    text = str(text)
                item.setText(text)
                self.tableWidget.setItem(j, i, item)


    def update_router(self):
        """
        输入路由状态更新
        :return:
        """
        conf = dict(ip=self.edit_ip.text(), mask=self.edit_mask.text())
        if self.edit_ip.text() != '':
            self.edit_ip.setPlaceholderText(self.edit_ip.text())
        if self.edit_mask.text() != '':
            self.edit_mask.setPlaceholderText(self.edit_mask.text())
        self.update.emit(self.id, conf)

    def stop_router(self):
        self.stop.emit(self.id)





