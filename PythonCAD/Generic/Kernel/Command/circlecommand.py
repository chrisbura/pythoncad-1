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

from Kernel.Db.schema import Point, Circle, Entity
from Kernel.Command.inputs import PointInput, LengthInput
from Kernel.Command.command import Command

class CircleCommand(Command):
    def __init__(self, document):
        super(CircleCommand, self).__init__(document)
        self.can_preview = True
        self.preview_start = 0
        self.inputs = (
            PointInput('Enter first point'),
            LengthInput('Enter radius'),
        )
        # TODO: Add input relation mechanism
        # Want LengthInput to be from PointInput to mouse click
        self.inputs[1].point = self.inputs[0]

    def apply_command(self):
        center_point = self.inputs[0].value
        self.db.add(center_point)
        circle = Circle(point=center_point, radius=self.inputs[1].value)

        entity = Entity()
        entity.layer = self.document.get_layer_table().getActiveLayer()
        self.db.add(entity)
        circle.entities = [entity]

        self.db.add(circle)
        self.db.commit()

        return entity
