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
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from PyQt4 import QtGui, QtCore
from kernel.db import schema
from interface.preview.base import Preview, BasePreview
from interface.preview.circle import Point

class RectanglePreview(Preview, QtGui.QGraphicsItemGroup):
    def __init__(self, command):
        self.command = command
        super(RectanglePreview, self).__init__()
        self.setHandlesChildEvents(False)

        self.point1 = self.command.inputs[0].value

        for i in range(1, 5):
            # Initialize the four lines
            name = 'segment{0}'.format(i)
            setattr(self, name, QtGui.QGraphicsLineItem())
            self.addToGroup(getattr(self, name))

            # Initialize the four points
            name = 'point{0}_item'.format(i)
            setattr(self, name, Point(self.point1))
            self.addToGroup(getattr(self, name))

    def updatePreview(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()

        # TODO: Probably should use QRectF
        self.segment1.setLine(self.point1.x, self.point1.y, x, self.point1.y)
        self.segment2.setLine(x, self.point1.y, x, y)
        self.segment3.setLine(x, y, self.point1.x, y)
        self.segment4.setLine(self.point1.x, y, self.point1.x, self.point1.y)

        # TODO: Clean up
        point_update = Point(schema.Point(x=x, y=self.point1.y))
        self.point2_item.setRect(point_update.rect())

        point_update = Point(schema.Point(x=x, y=y))
        self.point3_item.setRect(point_update.rect())

        point_update = Point(schema.Point(x=self.point1.x, y=y))
        self.point4_item.setRect(point_update.rect())
