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
from interface.entity.point import Point
from interface.entity.base import BaseItem


class Ellipse(BaseItem, QtGui.QGraphicsEllipseItem):
    def __init__(self, obj):
        self.center = obj.point
        self.radius_x = obj.radius_x
        self.radius_y = obj.radius_y

        super(Ellipse, self).__init__(
            self.center.x - self.radius_x,
            self.center.y - self.radius_y,
            self.radius_x * 2.0,
            self.radius_y * 2.0
        )

    def shape(self):
        shape = super(Ellipse, self).shape()
        path_stroker = QtGui.QPainterPathStroker()
        # TODO: Customizable 'snap'
        path_stroker.setWidth(6.0)
        path1 = path_stroker.createStroke(shape)
        return path1

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.cyan))
        # painter.drawPath(self.shape())
        super(Ellipse, self).paint(painter, option, widget)


class EllipseComposite(QtGui.QGraphicsItemGroup):
    def __init__(self, obj):
        super(EllipseComposite, self).__init__()
        # Prevent group events from overriding child events
        self.setHandlesChildEvents(False)

        # Create child entities
        self.center_point = Point(obj.point)
        self.ellipse = Ellipse(obj)

        # Add child entities to group
        self.addToGroup(self.center_point)
        self.addToGroup(self.ellipse)
