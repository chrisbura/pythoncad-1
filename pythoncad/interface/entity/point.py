#
# Copyright (c), 2010 Matteo Boscolo
# Copyright (c), 2013 Christopher Bura
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
from interface.entity.base import BaseItem


class Point(BaseItem, QtGui.QGraphicsEllipseItem):
    def __init__(self, point):
        self.point = point
        radius = 2.0
        super(Point, self).__init__(
            self.point.x - radius,
            self.point.y - radius,
            radius * 2.0,
            radius * 2.0
        )
        self.setBrush(QtCore.Qt.black)

    def hoverEnterEvent(self, event):
        super(Point, self).hoverEnterEvent(event)
        self.setBrush(QtCore.Qt.red)

    def hoverLeaveEvent(self, event):
        super(Point, self).hoverLeaveEvent(event)
        self.setBrush(QtCore.Qt.black)

    def shape(self):
        shape = super(Point, self).shape()
        path = QtGui.QPainterPath()
        width = 10.0
        path.addEllipse(self.point.x - width / 2.0, self.point.y - width / 2.0, width, width)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.cyan))
        # painter.drawPath(self.shape())
        super(Point, self).paint(painter, option, widget)
