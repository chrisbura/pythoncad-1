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

from pythoncad.models import Layer


class Drawing(object):
    def __init__(self, title='Untitled'):
        self.title = title
        self.layers = []

    @property
    def layer_count(self):
        return len(self.layers)

    def create_layer(self):
        layer = Layer()
        self.add_layer(layer)
        return layer

    def add_layer(self, layer):
        if layer.drawing is not None and layer.drawing is not self:
            # TODO: Pick better exception type
            raise Exception('Layer is already bound to another drawing')

        if layer in self.layers:
            raise Exception('Layer is already part of this drawing')

        layer.drawing = self
        self.layers.append(layer)

    def remove_layer(self, layer):
        if not layer in self.layers:
            raise Exception('Layer is not part of this drawing')

        # Perform 'soft' delete so that layer can be added to
        # another drawing or to the same drawing later
        # TODO: move_layer method
        layer.drawing = None

        self.layers.remove(layer)
