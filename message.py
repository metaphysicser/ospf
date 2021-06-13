#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)

class Message:
    """
    消息类，定义发送消息的格式
    """
    def __init__(self, sender, recipient, m_type, m_body=None):
        self.sender = sender # 消息的发送者
        self.recipient = recipient # 消息的接受者
        self.type = m_type # 消息的类型
        self.body = m_body # 消息的内容


