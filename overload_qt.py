#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from PyQt5 import QtWidgets, QtCore
from subwin import RouterUI
import sys
from PyQt5 import Qt


class RouterLabel(QtWidgets.QLabel):
    clicked = Qt.pyqtSignal(int)

    def __init__(self, parent=None):
        super(RouterLabel, self).__init__(parent)
        self.id = 0

    def set_id(self, l_id):
        self.id = l_id

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.clicked.emit(self.id)

