#
# Copyright (c) 2014 Christopher Bura
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
#

from pythoncad.entities.base import BaseEntity


class Layer(object):
    def __init__(self, title='Untitled', drawing=None):
        self.title = title
        self.drawing = drawing

        self.entities = []

    @property
    def entity_count(self):
        return len(self.entities)

    def add_entity(self, entity):
        if not isinstance(entity, BaseEntity):
            raise TypeError('Only entities derived from BaseEntity can be added')

        if entity.layer is not self and entity.layer is not None:
            raise Exception('Entity has already been added to another layer')

        if entity.layer == self:
            raise Exception('Entity has already been added to this layer ')

        entity.layer = self
        self.entities.append(entity)

    def remove_entity(self, entity):
        if entity not in self.entities:
            raise Exception('Entity is not bound to layer')

        entity.layer = None
        self.entities.remove(entity)
