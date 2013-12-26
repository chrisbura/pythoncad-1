
# Copyright (c) 2009,2010 Matteo Boscolo
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

from PyQt4 import QtCore, QtGui
from Interface.Entity.base import BaseItem

class Segment(BaseItem, QtGui.QGraphicsLineItem):
    def __init__(self, obj):
        super(Segment, self).__init__(obj.point1.x, obj.point1.y, obj.point2.x, obj.point2.y)
        self.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
        self.setAcceptHoverEvents(True)

    def shape(self):
        shape = super(Segment, self).shape()
        path_stroker = QtGui.QPainterPathStroker()
        # TODO: Customizable 'snap'
        path_stroker.setWidth(6.0)
        path1 = path_stroker.createStroke(shape)
        return path1

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.cyan))
        # painter.drawPath(self.shape())
        super(Segment, self).paint(painter, option, widget)
