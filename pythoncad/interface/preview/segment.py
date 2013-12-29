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
from interface.entity.base import BaseComposite
from interface.preview.base import Preview, BasePreview
from interface.preview.circle import Point


class Segment(BasePreview, QtGui.QGraphicsLineItem):
    pass


class SegmentPreview(Preview, BaseComposite, QtGui.QGraphicsItemGroup):
    def __init__(self, command):
        self.command = command
        super(SegmentPreview, self).__init__()

        self.start_point = Point(self.command.inputs[0].value)
        self.segment = Segment(
            self.command.inputs[0].value.x,
            self.command.inputs[0].value.y,
            self.command.inputs[0].value.x,
            self.command.inputs[0].value.y
        )

        self.addToGroup(self.start_point)
        self.addToGroup(self.segment)

    def updatePreview(self, event):
        segment_update = Segment(
            self.command.inputs[0].value.x,
            self.command.inputs[0].value.y,
            event.scenePos().x(),
            event.scenePos().y()
        )

        self.segment.setLine(segment_update.line())
