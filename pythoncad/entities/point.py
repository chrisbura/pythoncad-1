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

from math import sqrt
from decimal import Decimal

from pythoncad.entities import Entity


class Point(Entity):
    def __init__(self, x, y):
        self.x = Decimal(str(x))
        self.y = Decimal(str(y))

    def __repr__(self):
        return 'Point({}, {})'.format(self.x, self.y)

    def __add__(self, point):
        if not isinstance(point, Point):
            raise TypeError('Only points can be added to other points')

        return Point(self.x + point.x, self.y + point.y)

    def __sub__(self, point):
        if not isinstance(point, Point):
            raise TypeError('Only points can be substracted from other points')

        return Point(self.x - point.x, self.y - point.y)

    def equals(self, point):
        if not isinstance(point, Point):
            raise TypeError('Incorrect type supplied for point comparison')

        if (self.x == point.x) and (self.y == point.y):
            return True

        return False

    def clone(self):
        return Point(self.x, self.y)

    def distance(self, point):
        if not isinstance(point, Point):
            raise TypeError('Incorrect type supplied for calculating distance')

        distance_x = self.x - point.x
        distance_y = self.y - point.y

        return (distance_x ** 2 + distance_y ** 2).sqrt()

    def move(self, start_point, end_point):
        # TODO: return value?

        if not (isinstance(start_point, Point) or isinstance(end_point, Point)):
            raise TypeError('Arguments must both be Points')

        self.x = self.x + (end_point.x - start_point.x)
        self.y = self.y + (end_point.y - start_point.y)

    def rotate(self, rotation_center, angle):
        if not isinstance(rotation_center, Point):
            raise TypeError('Rotation center must be a Point')

        # TODO: Use sympy instead
