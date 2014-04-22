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
import math
from decimal import Decimal

from pythoncad.entities import Point, LineSegment


class TestPoint(unittest.TestCase):
    def setUp(self):
        self.first_point = Point(1.1, 2.2)
        self.second_point = Point(3.3, 4.4)

    def test_point_creation(self):
        self.assertTrue(isinstance(self.first_point, Point))
        self.assertEquals(self.first_point.x, Decimal('1.1'))
        self.assertEquals(self.first_point.y, Decimal('2.2'))

    def test_point_repr(self):
        self.assertEquals(repr(self.first_point), 'Point(1.1, 2.2)')

    def test_point_equality(self):
        point = Point(1.1, 2.2)
        self.assertTrue(self.first_point.equals(point))

    def test_point_equality_wrong_type(self):
        with self.assertRaises(TypeError):
            self.first_point.equals(LineSegment())

    def test_point_addition(self):
        result = self.first_point + self.second_point
        self.assertTrue(result.equals(Point(4.4, 6.6)))

    def test_point_addition_wrong_type(self):
        with self.assertRaises(TypeError):
            self.first_point + LineSegment()

    def test_point_subtraction(self):
        result = self.first_point - self.second_point
        self.assertTrue(result.equals(Point(-2.2, -2.2)))

    def test_point_subtraction_wrong_type(self):
        with self.assertRaises(TypeError):
            self.first_point - LineSegment()

    def test_point_clone(self):
        point = self.first_point.clone()
        self.assertTrue(self.first_point.equals(point))

    def test_point_distance(self):
        distance = self.first_point.distance(self.second_point)
        self.assertEquals(distance, Decimal('9.68').sqrt())

    def test_point_distance_incorrect_type(self):
        with self.assertRaises(TypeError):
            self.first_point.distance(1)

    def test_point_move(self):
        start_point = Point(1.5, 1.5)
        end_point = Point(3.5, 3.5)
        self.first_point.move(start_point, end_point)
        self.assertTrue(self.first_point.equals(Point(3.1, 4.2)))

    def test_point_move_incorrect_type(self):
        with self.assertRaises(TypeError):
            self.first_point.move(1, 1)

    def test_point_rotate_90_degrees(self):
        point = Point(1, 1)
        point.rotate(Point(0, 0), Decimal(str(math.pi / 2.0)))
        self.assertEquals(point, Point(-1, 1))

    def test_point_rotate_360_degrees(self):
        point = Point(1, 1)
        point.rotate(Point(0, 0), Decimal(str(math.pi * 2.0)))
        self.assertEquals(point, Point(1, 1))

    def test_point_rotate_incorrect_type(self):
        with self.assertRaises(TypeError):
            self.first_point.rotate(1, 1)

    def test_point_mirror_across_x_axis(self):
        line_segment = LineSegment(Point(0, 0), Point(1, 0))
        self.first_point.mirror(line_segment)
        self.assertEquals(self.first_point, Point(1.1, -2.2))

    def test_point_mirror_by_point(self):
        with self.assertRaises(TypeError):
            self.first_point.mirror(Point(0, 0))
