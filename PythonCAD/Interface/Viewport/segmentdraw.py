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


#----------------------------------------------------------------------------------------------------
def _draw_segment(self, viewport, col=None):
    color = col
    # is color defined
    if color is not None and not isinstance(color, color.Color):
        raise TypeError, "Invalid Color: " + `type(color)`
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
    self.draw(viewport, viewport.Image.getOption('BACKGROUND_COLOR'))
