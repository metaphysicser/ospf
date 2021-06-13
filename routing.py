#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
    路由类设置
"""
from __future__ import (absolute_import, unicode_literals)
import time
import queue
from message import Message
from timer import RepeatingTimer
import setting
import numpy as np
from PyQt5.Qt import QThread, pyqtSignal
import networkx as nx
# 消息队列
q = queue.Queue()
# 消息队列设置
que_set = {
    0: queue.Queue(10), # 每个邻居的消息同时最多存在10个
    1: queue.Queue(10),
    2: queue.Queue(10),
    3: queue.Queue(10),
}
# 拓扑网络开销矩阵
COST_MAT = setting.DEFAULT_COST.copy()
# 路由死亡间隔
DEATH_INTERVAL = setting.DEFAULT_DEATH_INTERVAL
# 路由hello间隔
HELLO_INTERVAL = setting.DEFAULT_HELLO_INTERVAL
# 路由DD间隔
NOMAL_INTERVAL = setting.DEFAULT_NOMAL_INTERVAL


class Router(QThread):
    """
    继承父类QThread
    """
    light_sig = pyqtSignal(int, str)

    def __init__(self, routing_id:int, ip:str, mask:str, neighbors:list, vertex_set:list, edge_set:list):
        """
        初始化路由
        :param routing_id: 路由id
        :param ip: 路由ip
        :param mask: 子网掩码
        :param neighbors: 路由的邻接路由id列表
        :param vertex_set: 路由器的顶点集
        :param edge_set: 路由器边集
        """
        super().__init__()
        # 路由器id
        self.id = routing_id
        # 路由器ip
        self.ip = ip
        # 路由掩码
        self.mask = mask
        # 邻接路由器
        self.neighbors = neighbors
        # 路由表顶点集
        self.vertex_set = vertex_set
        # 顶点对应的ip集合
        self.ip_set = {k: None if k != self.id else self.ip for k in self.vertex_set}
        # 顶点对应的掩码集合
        self.mask_set = {k: None if k != self.id else self.mask for k in self.vertex_set}
        # 路由表边集, 形似(v1, v2, c)
        self.edge_set = edge_set
        # 拓扑网络
        self.net = nx.Graph()
        # 初始化路由表
        self.router_table = dict()
        # 邻接路由器不可达判断间隔
        self.death_interval = DEATH_INTERVAL
        # 邻接路由器不可达判断时间
        self.death_time = dict()
        # 数据库同步信号
        self.synchronization = {k: False for k in neighbors}
        # hello线程
        self.hello_rp = RepeatingTimer(HELLO_INTERVAL, self.hello)
        # dd线程
        self.dd_rp = RepeatingTimer(NOMAL_INTERVAL, self.database_description)
        # 信号灯控制
        self.light_rp = RepeatingTimer(NOMAL_INTERVAL, self.status_light_emit)
        # lsr线程
        self.lsr_rp = RepeatingTimer(NOMAL_INTERVAL, self.link_state_request)
        # 生成路由表线程
        self.rt_rp = RepeatingTimer(NOMAL_INTERVAL * 2, self.update_net)
        # 线程状态mm7d
        self.status = setting.ROUTER_STATUS['init']
        # 线程启动控制
        self.thread_start = {'lsr': False}
        # 线程停止时保存状态
        self.old_status = setting.ROUTER_STATUS['init']
        # 死亡时间控制变量
        self.set_death_time = False
        # 洪泛请求目标确认
        self.flooding = {k: False if k != self.id else self.ip for k in self.neighbors}
        # 防止变量冲突
        self.sender = self.id

    def get_conf(self):
        """
        获取路由器配置
        :return:
        """
        rep = dict(
            id=self.id,
            ip=self.ip,
            mask=self.mask,
            status=self.status,
            neighbors=self.neighbors
        )
        return rep

    def get_router_table(self):
        """
        获得路由表
        :return:
        """
        return self.router_table

    def update_weight(self, weight):
        """
        更新权重
        :param weight:
        :return:
        """
        for edge in self.edge_set:
            if str([edge[0], edge[1]]) in weight.keys():
                edge[2] = weight[str([edge[0], edge[1]])]
        self.update_net()

    def update_net(self):
        """
        更新网络拓扑结构
        :return:
        """
        # 初始化网络
        self.net.add_nodes_from(self.vertex_set)
        self.net.add_weighted_edges_from(self.edge_set)
        self.generate_router_table()

    def generate_router_table(self):
        try:
            targets = [x for x in self.vertex_set if x != self.id]
            targets = list(set(targets))
            target_ips = [self.ip_set[x] for x in targets]
            target_masks = [self.mask_set[x] for x in targets]
            target_gateway = list()
            target_costs = list()
            target_path = list()
            for tg in targets:
                try:
                    length, path = nx.bidirectional_dijkstra(self.net, self.id, tg)
                    target_gateway.append(self.ip_set[path[1]])
                except nx.exception.NetworkXNoPath:
                    length, path = 0, list()
                target_costs.append(length)
                target_path.append(path)
            self.router_table['目标ID'] = targets
            self.router_table['目标IP'] = target_ips
            self.router_table['目标掩码'] = target_masks
            self.router_table['下一跳'] = target_gateway
            self.router_table['路由开销'] = target_costs
            self.router_table['路径'] = target_path
        except KeyError:
            self.router_table['目标ID'] = list()
            self.router_table['目标IP'] = list()
            self.router_table['目标掩码'] = list()
            self.router_table['下一跳'] = list()
            self.router_table['路由开销'] = list()
            self.router_table['路径'] = list()
        self.log('%s' % self.router_table)
        self.log('%s' % self.net.edges)

    def run(self):
        """
        执行函数，线程开启时会执行此函数
        :return:
        """
        # 定时任务，发送hello分组
        if not self.hello_rp.is_alive():
            self.hello_rp.start()
        # 定时任务，发送DD分组
        if not self.dd_rp.is_alive():
            self.dd_rp.start()
        # 定时任务，信号灯控制
        if not self.light_rp.is_alive():
            self.light_rp.start()
        # 定时任务，更新路由表
        if not self.rt_rp.is_alive():
            self.rt_rp.start()

        while True:
            if self.status != setting.ROUTER_STATUS['stop']:
                if not self.set_death_time:
                    self.death_time = {k: v for (k, v) in zip(self.neighbors,
                                                              [time.time() + self.death_interval for _ in
                                                               range(len(self.neighbors))])}
                    self.set_death_time = True
                if que_set[self.id].qsize():
                    if que_set[self.id].qsize() == 10:
                        for i in range(10):
                            que_set[self.id].get()
                    else:
                        msg = que_set[self.id].get()
                        self.handle_msg(msg)
                self.event_check()

    def update_conf(self, conf):
        # 路由器ip
        self.ip = conf['ip'] if conf['ip'] != '' else self.ip
        # 路由掩码
        self.mask = conf['mask'] if conf['mask'] != '' else self.mask
        self.link_state_update()

    def link_state_update(self, dn=0, tg=None):
        if dn == 0:
            m_body = dict(dn=0, ip=self.ip, mask=self.mask)
            for neighbor in self.neighbors:
                if not self.flooding[neighbor]:
                    msg = Message(self.id, neighbor, setting.MSG_TYPE['LSU'], m_body=m_body)
                    que_set[neighbor].put(msg)
        elif dn == 1:
            m_body = dict(dn=1, tg=tg)
            for neighbor in self.neighbors:
                if not self.flooding[neighbor]:
                    msg = Message(self.id, neighbor, setting.MSG_TYPE['LSU'], m_body=m_body)
                    que_set[neighbor].put(msg)
        elif dn == -1:
            m_body = dict(dn=-1, tg=tg)
            for neighbor in self.neighbors:
                if not self.flooding[neighbor]:
                    msg = Message(self.id, neighbor, setting.MSG_TYPE['LSU'], m_body=m_body)
                    que_set[neighbor].put(msg)
        self.status = setting.ROUTER_STATUS['synsing']
        self.log('发送LSU')

    def stop(self):
        """
        线程停止
        :return:
        """
        self.hello_rp.stop()
        self.dd_rp.stop()
        self.light_rp.stop()
        self.rt_rp.stop()
        self.old_status = self.status
        self.status = setting.ROUTER_STATUS['stop']
        self.set_death_time = False
        self.log('被用户停止')

    def router_continue(self):
        """
        线程继续
        :return:
        """
        self.hello_rp.t_continue()
        self.dd_rp.t_continue()
        self.light_rp.t_continue()
        self.rt_rp.t_continue()
        self.status = self.old_status
        self.log('被用户启动')

    def hello(self):
        """
        发送hello分组
        :return:
        """
        for neighbor in self.neighbors:
            msg = Message(self.id, neighbor, setting.MSG_TYPE['Hello'])
            que_set[neighbor].put(msg)
            self.log('向%d号路由发送hello分组' % neighbor)

    def event_check(self):
        """

        :return:
        """
        # 心跳检测，判断邻接路由是否已死亡
        for neighbor in self.neighbors:
            if time.time() >= self.death_time[neighbor]:
                self.log('路由%d无响应, 判断其不可达' % neighbor)
                self.link_state_update(dn=1, tg=neighbor)
                while que_set[self.id].qsize():
                    que_set[self.id].get()
                # 删除该点及其路由信息
                try:
                    if neighbor in self.neighbors:
                        self.neighbors.remove(neighbor)
                    if neighbor in self.vertex_set:
                        self.vertex_set.remove(neighbor)
                    if neighbor in self.net.nodes:
                        self.net.remove_node(neighbor)
                    self.net.remove_node(neighbor)
                    self.log('邻接: %s  边集: %s' % (self.neighbors, self.net.edges))
                except KeyError or ValueError or nx.exception.NetworkXErro:
                    self.log('L251发生错误' % neighbor)
        # 网络拓扑同步检测
        if np.sum(list(self.synchronization.values())) == len(self.neighbors):
            # print('路由%d同步完毕' % self.id)
            # self.dd_rp.cancel()
            if not self.thread_start['lsr']:
                self.lsr_rp.start()
                self.thread_start['lsr'] = True
        # 链路状态信息同步检测
        if None not in self.ip_set.values():
            if self.status != setting.ROUTER_STATUS['stop']:
                self.status = setting.ROUTER_STATUS['synsed']
            # self.lsr_rp.cancel()

    def database_description(self):
        """
        向邻接路由发送数据库描述信息
        :return:
        """
        for neighbor in self.neighbors:
            m_body = {
                'vertex_set': self.vertex_set,
                'edge_set': self.edge_set
            }
            msg = Message(self.id, neighbor, setting.MSG_TYPE['DD'], m_body=m_body)
            que_set[neighbor].put(msg)
            self.log('向%d号路由发送DD分组' % neighbor)

    def link_state_request(self):
        """
        请求某些链路状态信息(IP)
        :return:
        """
        # 请求无值的ip
        for k, v in self.ip_set.items():
            if not v:
                m_body = {
                    'id': k
                }
                msg = Message(self.id, k, setting.MSG_TYPE['LSR'], m_body=m_body)
                que_set[k].put(msg)
                self.log('向%d号路由发送LSR分组' % k)
        # 请求无键值的ip
        for r_id in [x for x in self.vertex_set if x not in self.ip_set.keys()]:
            for neighbor in self.neighbors:
                m_body = {
                    'id': r_id
                }
                msg = Message(self.id, neighbor, setting.MSG_TYPE['LSR'], m_body=m_body)
                que_set[neighbor].put(msg)
                self.log('向%d号路由发送LSR分组' % neighbor)

    def status_light_emit(self):
        """
        发送更新状态灯信号
        :return:
        """
        if self.status == setting.ROUTER_STATUS['init'] or self.status == setting.ROUTER_STATUS['stop']:
            self.light_sig.emit(self.id, 'r')
        elif self.status == setting.ROUTER_STATUS['synsing']:
            self.light_sig.emit(self.id, 'y')
        elif self.status == setting.ROUTER_STATUS['synsed']:
            self.light_sig.emit(self.id, 'g')

    def handle_msg(self, msg):
        """
        处理消息
        :param msg:
        :return:
        """
        if msg.type == setting.MSG_TYPE['Hello']:
            # 收到hello分组时，对发送者的死亡时间更新
            if msg.sender not in self.neighbors:
                self.neighbors.append(msg.sender)
            if msg.sender not in self.vertex_set:
                self.vertex_set.append(msg.sender)
                self.link_state_update(dn=-1, tg=msg.sender)
                # 若发送者不存在于当前的邻居列表，则添加到列表中
            self.death_time[msg.sender] = time.time() + self.death_interval
            self.log('接收到%d号路由的hello分组' % msg.sender)
        elif msg.type == setting.MSG_TYPE['DD']:
            # 收到DD分组时, 查看是否有不同的数据库描述, 有则更新
            self.log('接收到%d号路由的DD分组' % msg.sender)
            if self.status != setting.ROUTER_STATUS['stop']:
                self.status = setting.ROUTER_STATUS['synsing']
            changed = False
            for vertex in msg.body['vertex_set']:
                if vertex not in self.vertex_set:
                    self.vertex_set.append(vertex)
                    changed = True
            for edge in msg.body['edge_set']:
                if edge not in self.edge_set:
                    self.edge_set.append(edge)
                    changed = True
            if not changed:
                # 若接受的数据库描述无需更新, 则与发送者同步
                self.synchronization[msg.sender] = True
        elif msg.type == setting.MSG_TYPE['LSR']:
            # 发送LSR响应
            self.sender = msg.sender
            self.log('接收到%d号路由的LSR分组' % msg.sender)
            r_id = msg.body['id']
            if r_id in self.ip_set.keys() and r_id in self.mask_set.keys():
                if self.ip_set[r_id] and self.mask_set[r_id]:
                    m_body = {
                        'id': r_id,
                        'ip': self.ip_set[r_id],
                        'mask': self.mask_set[r_id]
                    }
                    msg = Message(self.id, msg.sender, setting.MSG_TYPE['LSRR'], m_body=m_body)
                    if self.sender == self.id:
                        self.log('!!!!!!!!!!!!!!!!!!!!')
                    que_set[self.sender].put(msg)
                    self.log('向%d号路由发送LSRR分组' % self.sender)
        elif msg.type == setting.MSG_TYPE['LSRR']:
            # 接受LSR响应
            self.log('接收到%d号路由的LSRR分组' % msg.sender)
            self.ip_set[msg.body['id']] = msg.body['ip']
            self.mask_set[msg.body['id']] = msg.body['mask']
        elif msg.type == setting.MSG_TYPE['LSU']:
            # 接收LSU请求
            self.sender = msg.sender
            self.log('接收到%d号路由的LSU分组' % msg.sender)
            if msg.body['dn'] == 1:
                if msg.body['tg'] in self.vertex_set:
                    self.vertex_set.remove(msg.body['tg'])
                    self.link_state_update(dn=1, tg=msg.body['tg'])
                    while que_set[self.id].qsize():
                        que_set[self.id].get()
            elif msg.body['dn'] == 0:
                self.ip_set[msg.sender] = msg.body['ip']
                self.mask_set[msg.sender] = msg.body['mask']
                self.link_state_update()
            elif msg.body['dn'] == -1:
                if msg.body['tg'] not in self.vertex_set:
                    self.vertex_set.append(msg.body['tg'])
                    self.link_state_update(dn=-1, tg=msg.body['tg'])
            self.flooding[msg.sender] = True
            # 更新确认
            msg = Message(self.id, self.sender, setting.MSG_TYPE['LSUA'])
            que_set[self.sender].put(msg)
            self.log('向%d号路由发送LSUA分组' % self.sender)
        elif msg.type == setting.MSG_TYPE['LSUA']:
            # 接收LSUA请求
            self.log('接收到%d号路由的LSUA分组' % msg.sender)
            self.flooding[msg.sender] = True
            if self.status != setting.ROUTER_STATUS['stop']:
                self.status = setting.ROUTER_STATUS['synsed']

    def log(self, text):
        """
        日志函数，记录程序日志
        """
        print('[%s][%d号路由(状态: %2d)][消息队列: %2d] ' %
              (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self.id,
               self.status, que_set[self.id].qsize()) + text)


