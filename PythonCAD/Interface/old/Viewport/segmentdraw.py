#
# Copyright (c) 2005, 2006 Art Haas
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
# code for adding graphical methods to drawing entities
#


import pygtk
pygtk.require('2.0')
import gtk
import pango

from PythonCAD.Generic import color
from PythonCAD.Generic.point import Point


#----------------------------------------------------------------------------------------------------
def _draw_segment(self, viewport, col=None):
    color = col
    # if color is not defined, take color of entity
    if color is None:
        color = self.getColor()
    # display properties
    lineweight = self.getThickness()
    linestyle = self.getLinetype().getList()
    # get begin and endpoint
    p1, p2 = self.getEndpoints()
    # add points to list
    points = []
    points.append(p1)
    points.append(p2)
    # do the actual draw of the linestring
    viewport.draw_linestring(color, lineweight, linestyle, points)

#----------------------------------------------------------------------------------------------------
def _erase_segment(self, viewport):
    # draw the element in the background color
    self.draw(viewport, viewport.gimage.getOption('BACKGROUND_COLOR'))

#----------------------------------------------------------------------------------------------------
def _sample_segment(self, viewport, color):
    # display properties
    lineweight = None
    linestyle = None
    # get begin and endpoint
    p1 = self.getFirstPoint().point
    p2 = self.getCurrentPoint()
    # add points to list
    points = []
    points.append(p1)
    points.append(p2)
    # do the actual draw of the linestring
    viewport.draw_linestring(color, lineweight, linestyle, points)
