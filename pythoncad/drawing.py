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

from pythoncad.models import Metadata, Layer

class Drawing(object):
    def __init__(self):
        self.metadata = Metadata()
        self.layers = []

    @property
    def title(self):
        return self.metadata.title

    @title.setter
    def title(self, value):
        self.metadata.title = value

    @property
    def layer_count(self):
        return len(self.layers)

    def create_layer(self):
        layer = Layer()
        # Only temporary
        layer.id = self.layer_count + 1
        layer.title = 'Layer {0}'.format(layer.id)
        self.layers.append(layer)
        return layer

    def add_layer(self, layer):
        if layer.id is not None:
            raise Exception('Layer is already bound to another drawing')

        layer.id = self.layer_count + 1
        self.layers.append(layer)
