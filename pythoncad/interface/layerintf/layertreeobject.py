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
# This Class define a QTreeWidget implementation for showing the layer structure
#
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

from kernel.db.schema import Layer

NAME, VISIBLE = range(2)


class LayerModel(QtCore.QAbstractTableModel):
    """
    The model of the Qt Model/View pattern

    Represents the data in a table as a two dimensional array

    """
    def __init__(self, parent):
        super(LayerModel, self).__init__(parent)
        self._document = parent.document
        self.layers = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.layers)

    def columnCount(self, parent):
        return 2

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        if index.column() == VISIBLE:
            return QtCore.QAbstractTableModel.flags(self, index) | QtCore.Qt.ItemIsUserCheckable
        return QtCore.QAbstractTableModel.flags(self, index)

    def data(self, index, role):
        if not index.isValid():
            return None
        layer = self.layers[index.row()]
        column = index.column()

        if role == QtCore.Qt.CheckStateRole:
            if column == VISIBLE:
                if layer.visible:
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked

        if role == QtCore.Qt.DisplayRole:
            if column == NAME:
                return layer.name

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if index.isValid() and role == QtCore.Qt.CheckStateRole:
            column = index.column()
            if column == VISIBLE:
                layer = self.layers[index.row()]
                if layer.visible:
                    # TODO: Replace with a 'toggle' signal
                    self.emit(QtCore.SIGNAL('hide_layer'), layer)
                else:
                    self.emit(QtCore.SIGNAL('show_layer'), layer)
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.Qt.AlignLeft
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            if section == NAME:
                return "Layer Name"
            elif section == VISIBLE:
                return "Visible"
        return None

    def removeRows(self, row, count, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        self.layers = self.layers[:row] + self.layers[row + count:]
        self.endRemoveRows()
        return True

    def clear(self):
        self.removeRows(0, self.rowCount())
        self.reset()


class LayerDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, document, parent=None):
        super(LayerDelegate, self).__init__(parent)
        self._document = document

    def paint(self, painter, option, index):
        if index.column() == NAME:
            layer = index.model().layers[index.row()]
            active_layer = self._document.getTreeTable.getActiveLayer()
            if layer == active_layer:
                painter.fillRect(option.rect, QtCore.Qt.lightGray)
        QtGui.QStyledItemDelegate.paint(self, painter, option, index)


class LayerView(QtGui.QTableView):
    """
    The view of the Qt Model/View pattern

    Displays the layers in a simple table instead of a tree. This allows for
    easier management of layers.
    """

    layers_changed = QtCore.pyqtSignal()

    def __init__(self, parent, document, model):
        super(LayerView, self).__init__(parent)
        self._document = document
        self.model = model
        self.setModel(self.model)
        self.setItemDelegate(LayerDelegate(self._document, self))
        # Configuration Options
        self.setShowGrid(False)
        self.verticalHeader().hide()
        self.horizontalHeader().setClickable(False)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.populateStructure()

        # Bug in Qt that doesn't resize rows to content on initialization
        # http://www.qtforum.org/article/13421/qtableview-how-to-make-rows-size-smaller.html
        # TODO: Find actual fix
        for row in range(self.model.rowCount()):
            self.resizeRowToContents(row)

        # Events
        self._document.getTreeTable.insertEvent = self.updateView
        self._document.getTreeTable.updateEvent = self.updateView
        self._document.getTreeTable.deleteEvent = self.updateView
        self._document.getTreeTable.setCurrentEvent = self.updateView

        # Signals
        self.connect(self.model, QtCore.SIGNAL('hide_layer'), self._hide)
        self.connect(self.model, QtCore.SIGNAL('show_layer'), self._show)
        self.layers_changed.connect(self.updateView)

    def updateView(self):
        self.model.clear()
        self.populateStructure()
        self.reset()

    def populateStructure(self):
        layers = self._document.getTreeTable.getLayers()
        active_layer = self._document.getTreeTable.getActiveLayer()
        for layer in layers:
            self.model.layers.append(layer)
        self.resizeRowsToContents()

    def contextMenuEvent(self, event):
        contextMenu = QtGui.QMenu(self)

        addLayerAction = QtGui.QAction('Add Layer', self, triggered=self._addLayer)
        renameLayerAction = QtGui.QAction('Rename Layer', self, triggered=self._rename)
        removeAction = QtGui.QAction('Remove Layer', self, triggered=self._remove)
        hideAction = QtGui.QAction('Hide', self, triggered=self._hide)
        showAction = QtGui.QAction('Show', self, triggered=self._show)
        setCurrentAction = QtGui.QAction('Set Current', self, triggered=self._setCurrent)

        contextMenu.addAction(addLayerAction)
        contextMenu.addAction(renameLayerAction)
        contextMenu.addAction(removeAction)
        contextMenu.addAction(hideAction)
        contextMenu.addAction(showAction)
        contextMenu.addAction(setCurrentAction)

        contextMenu.exec_(event.globalPos())
        del(contextMenu)

    def _addLayer(self):
        layer_name, ok = QtGui.QInputDialog.getText(self, 'Add Layer', 'Enter a name for the layer')

        # Layer name cannot be empty
        if not ok or not layer_name:
            # TODO: Give user a warning message
            return False

        # TODO: Move to manager
        new_layer = Layer(name=layer_name)
        self._document.db.add(new_layer)
        self._document.db.commit()

        self._document.getTreeTable.insert(new_layer)

        self.layers_changed.emit()

    def _remove(self):
        # TODO: Add warning
        layer = self.current_selection
        self._document.getTreeTable.delete(layer)
        self.layers_changed.emit()

    def _rename(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Rename Layer', 'Enter New Layer Name')
        if ok:
            layer = self.current_selection
            self._document.getTreeTable.rename(layer, text)
            self.layers_changed.emit()

    def _hide(self, layer=None):
        # TODO: Move to object property
        tree_table = self._document.getTreeTable
        if tree_table.getLayerCount() <= 1:
            QtGui.QMessageBox.warning(self, 'Error', 'You cannot hide the only layer')
            return False

        if not layer:
            layer = self.current_selection

        active_layer = tree_table.getActiveLayer()

        if layer == active_layer:
            visible_layer = tree_table.getVisibleLayer(ignore = [layer.id, ])
            if not visible_layer:
                QtGui.QMessageBox.warning(self, 'Error', 'Unable to hide the last visible layer')
                return False

        self._document.getTreeTable.hide(layer)
        self.layers_changed.emit()

    def _show(self, layer=None):
        if not layer:
            layer = self.current_selection
        self._document.getTreeTable.show(layer)
        self.layers_changed.emit()

    def _setCurrent(self):
        # TODO: Can you even click on this without having a selection
        cito = self.current_selection
        if cito != None:
            self._document.getTreeTable.setActiveLayer(cito)
            self.layers_changed.emit()

    @property
    def current_selection(self):
        layer_indexes = self.selectionModel().selectedRows()
        for index in layer_indexes:
            layer = self.model.layers[index.row()]
            if layer.id != None:
                return layer
