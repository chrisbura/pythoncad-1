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
        self.assertEqual(self.drawing.metadata.title, 'New Drawing')

if __name__ == '__main__':
    unittest.main()
