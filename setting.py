#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)

DEFAULT_ROUTING = [
    {
        'id': 0,
        'ip': '192.168.0.0',
        'mask': '255.255.255.0',
        'neighbors': [1, 2, 3],
        'vertex_set': [0, 1, 2, 3],
        'edge_set':[[0, 1, 1],
                    [0, 2, 3],
                    [0, 3, 7]]
    },
    {
        'id': 2,
        'ip': '192.168.0.2',
        'mask': '255.255.255.0',
        'neighbors': [0, 1, 3],
        'vertex_set': [0, 1, 2, 3],
        'edge_set': [[1, 2, 1],
                     [0, 2, 3],
                     [2, 3, 2]]
    },
    {
        'id': 3,
        'ip': '192.168.0.3',
        'mask': '255.255.255.0',
        'neighbors': [0, 2],
        'vertex_set': [0, 2, 3],
        'edge_set': [[0, 3, 7],
                     [2, 3, 2]]
    },
    {
        'id': 1,
        'ip': '192.168.0.1',
        'mask': '255.255.255.0',
        'neighbors': [0, 2],
        'vertex_set': [0, 1, 2],
        'edge_set': [[0, 1, 1],
                     [1, 2, 1]]
    },
]

DEFAULT_WEIGHT = {
            '[0, 1]': 1,
            '[0, 2]': 3,
            '[0, 3]': 7,
            '[1, 2]': 1,
            '[2, 3]': 2
        }

MSG_TYPE = {
    'Hello': 0,  # hello分组
    'DD': 1,     # 数据库描述分组
    'LSR': 2,    # 链路状态请求
    'LSRR': 3,   # 链路状态请求响应
    'LSU': 4,    # 链路状态更新
    'LSUA': 5,   # 链路状态更新确认
}

ROUTER_STATUS = {
    'init': 0,
    'synsing': 1,
    'synsed': 2,
    'stop': -1
}

DEFAULT_DEATH_INTERVAL = 2  # 路由3s内没有接受到邻居的hello则判断其死亡
DEFAULT_HELLO_INTERVAL = 1  # 路由每1s发送一次hello分组
DEFAULT_NOMAL_INTERVAL = 1  # 默认分组发送间隔

# 默认的拓扑网络开销
DEFAULT_COST = [
    [0, 1, 3, 7],
    [1, 0, 1, -1],
    [3, 1, 0, 2],
    [7, -1, 2, 0]
]