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

from kernel.db.schema import Point, Ellipse, Entity
from kernel.command.inputs import PointInput, LengthInput
from kernel.command.command import Command

class EllipseCommand(Command):
    """
        this class represents the ellipse command
    """
    def __init__(self, document):
        super(EllipseCommand, self).__init__(document)
        self.can_preview = True
        self.preview_start = 0
        self.inputs = (
            PointInput('Enter first point'),
            LengthInput('Enter x radius'),
            LengthInput('Enter y radius'),
        )
        self.inputs[1].point = self.inputs[0]
        self.inputs[2].point = self.inputs[0]

    def apply_command(self):
        center_point = self.inputs[0].value
        self.db.add(center_point)
        ellipse = Ellipse(point=center_point, radius_x=self.inputs[1].value,
            radius_y=self.inputs[2].value)

        entity = Entity(layer=self.active_layer)
        self.db.add(entity)
        ellipse.entities = [entity]

        self.db.add(ellipse)
        self.db.commit()

        return entity
