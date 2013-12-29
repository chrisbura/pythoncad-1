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
#
# This  module PROVIDE ALL GLOBAL VARIABLE NEEDE TO THE SCENE
#
from interface.entity.point         import Point
from interface.entity.segment import SegmentComposite
from interface.entity.arc           import Arc
from interface.entity.text          import Text
from interface.entity.ellipse import EllipseComposite
from interface.entity.polyline      import Polyline
from interface.entity.dimension     import Dimension
from interface.entity.circle import CircleComposite

from interface.dialogs.widget.widgets import PyCadQColor
from interface.dialogs.widget.widgets import PyCadQLineType
from interface.dialogs.widget.widgets import PyCadQDouble
from interface.dialogs.widget.widgets import PyCadQFont

from PyQt4 import QtCore

from interface.command.distance2point import Distance2Point

from kernel.command.segmentcommand import SegmentCommand
from kernel.command.circlecommand import CircleCommand
from kernel.command.ellipsecommand import EllipseCommand
from kernel.db import schema

ENTITY_MAP = {
   schema.Point: Point,
   schema.Segment: SegmentComposite,
   schema.Circle: CircleComposite,
   schema.Ellipse: EllipseComposite
}

SCENE_SUPPORTED_TYPE=["SEGMENT",
                      "POINT",
                        "ARC",
                        "TEXT",
                        "ELLIPSE",
                        "POLYLINE",
                        "DIMENSION"]

SCANE_OBJECT_TYPE=dict(zip(SCENE_SUPPORTED_TYPE,
                       (
                        # Segment,
                        Point,
                        Arc,
                        Text,
                        # Ellipse,
                        Polyline,
                        Dimension
                       )))

INTERFACE_COMMAND={'DISTANCE2POINT':Distance2Point}

RESTART_COMMAND_OPTION=True

BACKGROUND_COLOR=(255, 255, 255)

KEY_MAP={
         QtCore.Qt.Key_Delete:'DELETE',
         QtCore.Qt.Key_L:'SEGMENT',
         QtCore.Qt.Key_P:'POLYLINE',
         QtCore.Qt.Key_G:'MOVE',
         QtCore.Qt.Key_C:'COPY',
         QtCore.Qt.Key_D:'DELETE',
         QtCore.Qt.Key_R:'ROTATE',
         QtCore.Qt.Key_M:'MIRROR'
         }



PYTHONCAD_STYLE_WIDGET={'entity_color':PyCadQColor,
                        'entity_linetype':PyCadQLineType,
                        'entity_thickness':PyCadQDouble,
                        'text_font':PyCadQFont,
                        'text_height':PyCadQDouble,
                        }
PYTHONCAD_STYLE_DESCRIPTION={'entity_color':'Color',
                        'entity_linetype':'Line Type',
                        'entity_thickness':'Line Thickness',
                        'text_font':'Font',
                        'text_height':'Text Height',
                        }
