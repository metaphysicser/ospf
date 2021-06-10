#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)


class Message:
    def __init__(self, sender, recipient, m_type, m_body=None):
        self.sender = sender
        self.recipient = recipient
        self.type = m_type
        self.body = m_body


