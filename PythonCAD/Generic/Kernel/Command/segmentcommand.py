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

from Kernel.Db.schema import Point, Segment, Entity
from Kernel.Command.inputs import PointInput
from Kernel.Command.command import Command

class SegmentCommand(Command):
    def __init__(self, document):
        self.preview_start = 0
        # TODO: Add default values
        self.inputs = (
            PointInput('Enter first point'),
            PointInput('Enter second point'),
        )
        super(SegmentCommand, self).__init__(document)


    def apply_command(self):
        # TODO: Cleanup
        segment = Segment()
        point1 = self.inputs[0].value
        point2 = self.inputs[1].value
        self.db.add(point1)
        self.db.add(point2)
        segment.point1, segment.point2 = point1, point2

        entity = Entity()
        entity.layer = self.document.get_layer_table().getActiveLayer()
        self.db.add(entity)
        segment.entities = [entity]

        self.db.add(segment)
        self.db.commit()

        # Return the entity that was saved
        return entity
