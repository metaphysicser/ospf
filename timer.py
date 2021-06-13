#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from threading import Thread, Event
import time


class RepeatingTimer(Thread):
    """   在特定时间后使用特定的函数
            t = Timer(30.0, f, args=[], kwargs={})
            t.start()
            t.cancel() # stop the timer's action if it's still waiting
    """

    def __init__(self, interval, function, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()
        self.active = True

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def stop(self):
        self.active = False

    def t_continue(self):
        self.active = True

    def run(self):
        while not self.finished.is_set():
            if self.active:
                self.finished.wait(self.interval)
                self.function(*self.args, **self.kwargs)
