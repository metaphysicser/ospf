#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from gui_ui import UiMainWin
from routing import Router
import setting
from PyQt5 import QtWidgets
import sys
from subwin import RouterUI


class GUI(UiMainWin):
    def __init__(self):
        super().__init__()
        self.subwins = list()
        for i in range(len(setting.DEFAULT_ROUTING)):
            subwin = RouterUI(i)
            subwin.update.connect(self.router_update)
            subwin.stop.connect(self.stop_router)
            self.subwins.append(subwin)
        self.threads = list()
        # 绑定停止按钮的点击事件
        self.stopbut.clicked.connect(self.stop)
        # 绑定更新权重按钮的点击事件
        self.updatewbut.clicked.connect(self.update_weight)
        # 绑定重置按钮的点击事件
        self.resetbut.clicked.connect(self.reset)
        # 绑定开始按钮的点击事件
        self.initbut.clicked.connect(self.run)
        # 绑定路由的点击事件
        for i in range(len(self.router_labels)):
            self.router_labels[i].set_id(i)
            self.router_labels[i].clicked.connect(self.jump_to_subwin)

        # 按默认设置初始化路由线程
        for rout_conf in setting.DEFAULT_ROUTING:
            t = Router(rout_conf['id'], rout_conf['ip'], rout_conf['mask'], rout_conf['neighbors'],
                       rout_conf['vertex_set'], rout_conf['edge_set'])
            t.light_sig.connect(self.change_light)
            self.threads.append(t)

        self.weight = setting.DEFAULT_WEIGHT
        weights = list(self.weight.values())
        for i in range(len(self.edges)):
            self.edges[i].setPlaceholderText(str(weights[i]))

    def run(self):
        """
        运行函数
        :return:
        """
        # 开启线程
        for t in self.threads:
            t.start()

    def update_weight(self):
        """
        更新权重
        :return:
        """
        weight = self.weight.copy()
        keys = list(weight.keys())
        for i in range(len(self.edges)):
            if self.edges[i].text() != '':
                weight[keys[i]] = int(self.edges[i].text())
                self.edges[i].setPlaceholderText(self.edges[i].text())
        self.weight = weight
        for t in self.threads:
            t.update_weight(self.weight)

    def reset(self):
        """
        重置路由
        :return:
        """
        self.stop()
        self.threads = list()

    def router_continue(self):
        """
        继续路由
        :return:
        """
        for router in self.threads:
            router.router_continue()

    def stop(self):
        """
        停止路由
        :return:
        """
        for router in self.threads:
            router.stop()

    def stop_router(self, r_id):
        """
        停止某个路由
        :param r_id:
        :return:
        """
        self.threads[r_id].stop()

    def jump_to_subwin(self, r_id):
        """
        跳转到路由状态界面
        :param r_id:
        :return:
        """
        print(1)
        conf = self.threads[r_id].get_conf()
        table = self.threads[r_id].get_router_table()
        self.subwins[r_id].update_conf(conf)
        if len(table):
            self.subwins[r_id].update_table(table)
        self.subwins[r_id].show()

    def router_update(self, r_id, conf):
        """
        路由状态更新
        :return:
        """
        self.threads[r_id].update_conf(conf)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())
