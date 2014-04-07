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

from pythoncad.db.schema import Point, Entity
from pythoncad.command.inputs import PointInput
from pythoncad.command.command import Command

class PointCommand(Command):
    def __init__(self, document):
        super(PointCommand, self).__init__(document)
        self.inputs = (
            PointInput('Enter point'),
        )

    def apply_command(self):
        point = self.inputs[0].value

        entity = Entity(layer=self.active_layer)
        self.db.add(entity)
        point.entities = [entity]

        self.db.add(point)
        self.db.commit()

        return entity
