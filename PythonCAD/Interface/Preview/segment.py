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
#
# SegmentPreview object
#

from PyQt4 import QtGui, QtCore
from Interface.Preview.base         import PreviewBase, Preview
from Interface.Entity.segment       import Segment


class SegmentPreview(Preview, QtGui.QGraphicsLineItem):
    def __init__(self, command):
        self.command = command

        super(SegmentPreview, self).__init__(
            self.command.inputs[0].value.x, self.command.inputs[0].value.y,
            self.command.inputs[0].value.x, self.command.inputs[0].value.y)

        self.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))

    def updatePreview(self, event):
        line_update = QtCore.QLineF(
            self.command.inputs[0].value.x, self.command.inputs[0].value.y,
            event.scenePos().x(), event.scenePos().y())

        self.setLine(line_update)
