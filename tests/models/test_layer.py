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
from pythoncad.models.layer import Layer
from pythoncad.entities import Entity, Point, LineSegment


class TestEntityCreation(unittest.TestCase):
    def setUp(self):
        self.drawing = Drawing()
        self.layer = self.drawing.create_layer()

    def test_entity_adding_point(self):
        point = Point()
        self.layer.add_entity(point)
        self.assertEquals(self.layer.entity_count, 1)
        self.assertEquals(point.layer, self.layer)

    def test_adding_multiple_entity(self):
        for i in range(5):
            self.layer.add_entity(Point())
            self.layer.add_entity(LineSegment())
        self.assertEquals(self.layer.entity_count, 10)

    def test_entity_adding_segment_and_point(self):
        point = Point()
        self.layer.add_entity(point)
        segment = LineSegment()
        self.layer.add_entity(segment)
        self.assertEquals(point.layer, self.layer)
        self.assertEquals(segment.layer, self.layer)
        self.assertEquals(self.layer.entity_count, 2)

    def test_entity_removal(self):
        point = Point()
        self.layer.add_entity(point)
        self.assertEquals(self.layer, point.layer)
        self.assertEquals(self.layer.entity_count, 1)
        self.layer.remove_entity(point)
        self.assertEquals(point.layer, None)
        self.assertEquals(self.layer.entity_count, 0)

    def test_entity_readd(self):
        point = Point()
        self.layer.add_entity(point)
        self.assertEquals(self.layer.entity_count, 1)
        self.layer.remove_entity(point)
        self.assertEquals(self.layer.entity_count, 0)
        self.layer.add_entity(point)
        self.assertEquals(self.layer.entity_count, 1)

    def test_entity_already_added(self):
        point = Point()
        self.layer.add_entity(point)
        self.assertEquals(point.layer, self.layer)
        self.assertEquals(self.layer.entity_count, 1)
        self.layer.add_entity(point)
        self.assertEquals(self.layer.entity_count, 1)

    def test_entity_already_bound(self):
        point = Point()
        self.layer.add_entity(point)

        # Add second layer to try adding point
        layer2 = self.drawing.create_layer()

        with self.assertRaises(Exception):
            layer2.add_entity(point)

        self.assertEquals(self.layer.entity_count, 1)
        self.assertEquals(self.layer2.entity_count, 0)

    def test_add_random_object_as_entity(self):
        layer = Layer()
        with self.assertRaises(Exception):
            self.layer.add_entity(layer)

    def test_entity_not_bound_remove(self):
        point = Point()
        with self.assertRaises(Exception):
            self.layer.remove_entity(point)


class TestHidingLayer(unittest.TestCase):
    def setUp(self):
        self.drawing = Drawing()
        self.layer = self.drawing.create_layer()
