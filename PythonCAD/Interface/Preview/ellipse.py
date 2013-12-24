#!/usr/bin/env python
#
# Copyright (c) 2010 Matteo Boscolo
# Copyright (c) 2013 Christopher Bura
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public Licensesegmentcmd.py
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from PyQt4 import QtGui, QtCore
from Interface.Preview.base import Preview
import numpy

import math
from Interface.Preview.base import *

class Point(QtGui.QGraphicsEllipseItem):
    def __init__(self, point):
        radius = 2
        super(Point, self).__init__(
            point.x - radius,
            point.y - radius,
            radius * 1.5,
            radius * 1.5
         )
        self.setAcceptHoverEvents(True)
        self.setBrush(QtCore.Qt.lightGray)
        self.setPen(QtGui.QPen(QtCore.Qt.lightGray, 2, QtCore.Qt.SolidLine))


class Ellipse(QtGui.QGraphicsEllipseItem):
    def __init__(self, center_point, radius_x=1.0, radius_y=1.0):
        super(Ellipse, self).__init__(
            center_point.x - radius_x,
            center_point.y - radius_y,
            radius_x * 2.0,
            radius_y * 2.0
        )
        self.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
        self.setAcceptHoverEvents(True)


class EllipsePreview(Preview, QtGui.QGraphicsItemGroup):
    def __init__(self, command):
        self.command = command
        super(EllipsePreview, self).__init__()
        self.setHandlesChildEvents(False)

        self.center = self.command.inputs[0].value

        self.center_point = Point(self.center)
        self.ellipse = Ellipse(self.center)

        self.addToGroup(self.center_point)
        self.addToGroup(self.ellipse)

    def updatePreview(self, event):
        if self.command.active_input == 1:
            distance = abs(self.center.x - event.scenePos().x())
            ellipse_update = Ellipse(self.center, distance)
            self.ellipse.setRect(ellipse_update.rect())

        if self.command.active_input == 2:
            distance = abs(self.center.y - event.scenePos().y())
            ellipse_update = Ellipse(self.center, self.command.inputs[1].value, distance)
            self.ellipse.setRect(ellipse_update.rect())
