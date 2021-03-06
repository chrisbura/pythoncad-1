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
# This  module provide all the global variable to be used from the pythoncad Application
#
#
# Command List
#

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4  import QtCore, QtGui

from interface.layerintf.layertreeobject import LayerView

class LayerDock(QtGui.QDockWidget):

    def __init__(self, parent, document, model):
        """
        # TODO: Wrong docstring
        Creates an edit line in which commands or expressions are evaluated.
        Evaluation of expressions is done by the FunctionHandler object.

        """
        super(LayerDock, self).__init__('Layers', parent)
        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self._layerModel=LayerView(self, document, model)
        self.setWidget(self._layerModel)

    def RefreshStructure(self):
        """
        Refresh the tree view

        """
        # TODO:
        self._layerModel.updateView(None)
