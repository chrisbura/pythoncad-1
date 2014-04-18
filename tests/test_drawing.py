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

import unittest

from pythoncad.drawing import Drawing
from pythoncad.models import Layer


class TestDrawing(unittest.TestCase):

    def setUp(self):
        self.drawing = Drawing()

    def test_drawing_creation(self):
        self.assertTrue(isinstance(self.drawing, Drawing))

    def test_drawing_default_title(self):
        self.assertEqual(self.drawing.title, 'Untitled')

    def test_drawing_set_title(self):
        self.drawing.title = 'New Drawing'
        self.assertEqual(self.drawing.title, 'New Drawing')

class TestLayerCreation(unittest.TestCase):

    def setUp(self):
        self.drawing = Drawing()

    def test_layer_add(self):
        test_layer = Layer()
        self.drawing.add_layer(test_layer)
        self.assertEqual(self.drawing, test_layer.drawing)

    def test_layer_creation(self):
        test_layer = self.drawing.create_layer()
        self.assertEqual(self.drawing, test_layer.drawing)

    def test_layer_already_bound(self):
        layer = self.drawing.create_layer()
        new_drawing = Drawing()
        with self.assertRaises(Exception):
            new_drawing.add_layer(layer)

    def test_layer_count(self):
        for i in range(5):
            self.drawing.create_layer()
        self.assertEqual(self.drawing.layer_count, 5)

    def test_layer_title(self):
        self.drawing.create_layer()
        layer = self.drawing.layers[0]
        self.assertEqual(layer.title, 'Untitled')
        layer.title = 'New Title'
        self.assertEqual(layer.title, 'New Title')

    def test_layer_already_added(self):
        layer = self.drawing.create_layer()
        with self.assertRaises(Exception):
            self.drawing.add_layer(layer)
        self.assertEqual(self.drawing.layer_count, 1)

    def test_layer_removal(self):
        layer = self.drawing.create_layer()
        self.drawing.remove_layer(layer)
        self.assertEqual(layer.drawing, None)
        self.assertEqual(self.drawing.layer_count, 0)

    def test_layer_remove_and_readd(self):
        layer = self.drawing.create_layer()
        self.assertEquals(self.drawing.layer_count, 1)
        self.drawing.remove_layer(layer)
        self.assertEquals(self.drawing.layer_count, 0)
        self.drawing.add_layer(layer)
        self.assertEquals(self.drawing.layer_count, 1)

    def test_layer_not_added_removal(self):
        layer = Layer()
        with self.assertRaises(Exception):
            self.drawing.remove_layer(layer)

if __name__ == '__main__':
    unittest.main()
