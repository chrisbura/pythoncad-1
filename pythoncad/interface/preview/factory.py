#!/usr/bin/env python
#
# Copyright (c) 2010 Matteo Boscolo
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
# This module provide a factory for the preview objects
#
from kernel.command.pointcommand        import PointCommand
from kernel.command.segmentcommand      import SegmentCommand
from kernel.command.arccommand          import ArcCommand
from kernel.command.circlecommand       import CircleCommand
from kernel.command.rectanglecommand    import RectangleCommand
from kernel.command.ellipsecommand      import EllipseCommand
from kernel.command.polylinecommand     import PolylineCommand
from kernel.command.polygoncommand      import PolygonCommand

from interface.preview.point        import PreviewPoint
from interface.preview.arc          import PreviewArc

from interface.preview import *

#from Interface.preview.rectangle    import QtRectangleItem
#from Interface.preview.ellipse      import QtEllipseItem
#from Interface.preview.polyline     import QtPolylineItem
#from Interface.preview.polygon      import QtPolygonItem

def getPreviewObject(command):
    if isinstance(command, PointCommand):
        return PreviewPoint(command)
    if isinstance(command, SegmentCommand):
        return SegmentPreview(command)
    elif isinstance(command, ArcCommand):
        return PreviewArc(command)
    elif isinstance(command, CircleCommand):
        return CirclePreview(command)
    elif isinstance(command , RectangleCommand):
        return RectanglePreview(command)
    elif isinstance(command , EllipseCommand):
        return EllipsePreview(command)
#    elif isinstance(command , PolylineCommand):
#        return QtPolylineItem(command)
#    elif isinstance(command ,  PolygonCommand):
#        return QtPolygonItem(command)
    else:
        return None
