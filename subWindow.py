# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 400)
        self.tabWidget = QtWidgets.QTabWidget(Form)
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
        self.tableWidget = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 391, 371))
        self.tableWidget.setMaximumSize(QtCore.QSize(391, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 5, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(80)
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_status.setText(_translate("Form", "路由状态"))
        self.edit_mask.setPlaceholderText(_translate("Form", "255.255.255.0"))
        self.label_id.setText(_translate("Form", "路由id"))
        self.label_neighbors.setText(_translate("Form", "相邻路由"))
        self.edit_id.setPlaceholderText(_translate("Form", "0"))
        self.edit_status.setPlaceholderText(_translate("Form", "正常"))
        self.edit_neighbors.setPlaceholderText(_translate("Form", "[1, 2, 3]"))
        self.label_ip.setText(_translate("Form", "路由ip"))
        self.edit_ip.setPlaceholderText(_translate("Form", "192.168.0.0"))
        self.label_mask.setText(_translate("Form", "子网掩码"))
        self.but_update.setText(_translate("Form", "更新"))
        self.but_stop.setText(_translate("Form", "停止"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "路由状态"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Form", "3"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("Form", "4"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "目标ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "目标IP"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "目标掩码"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "下一跳"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "开销"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "具体路径"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Form", "192.168.0.0"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("Form", "mask"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("Form", "11"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("Form", "14"))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("Form", "[1, 2, 3]"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "路由表"))
