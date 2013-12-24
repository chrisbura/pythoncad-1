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

class RectangleCommand(Command):
    def __init__(self, document):
        super(RectangleCommand, self).__init__(document)
        self.can_preview = True
        self.preview_start = 0
        self.inputs = (
            PointInput('Enter first corner'),
            PointInput('Enter second corner'),
        )

    def apply_command(self):
        # TODO: Clean this mess up
        # Create the four points
        point1 = self.inputs[0].value
        point2 = self.inputs[1].value
        point3 = Point(x=point1.x, y=point2.y)
        point4 = Point(x=point2.x, y=point1.y)
        # Add points to db
        self.db.add(point1)
        self.db.add(point2)
        self.db.add(point3)
        self.db.add(point4)

        # Create joining segments
        segment1 = Segment(point1=point1, point2=point4)
        segment2 = Segment(point1=point4, point2=point2)
        segment3 = Segment(point1=point2, point2=point3)
        segment4 = Segment(point1=point3, point2=point1)

        layer = self.document.get_layer_table().getActiveLayer()

        entity1 = Entity(layer=layer)
        entity2 = Entity(layer=layer)
        entity3 = Entity(layer=layer)
        entity4 = Entity(layer=layer)
        entities = [entity1, entity2, entity3, entity4]
        self.db.add_all(entities)

        segment1.entities = [entity1]
        segment2.entities = [entity2]
        segment3.entities = [entity3]
        segment4.entities = [entity4]

        # Add segments to db
        self.db.add(segment1)
        self.db.add(segment2)
        self.db.add(segment3)
        self.db.add(segment4)

        self.document.db.commit()

        return entities
