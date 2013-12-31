#
#
# Copyright (c) 2010 Matteo Boscolo, Gertwin Groen
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
# This module the graphics scene class
#
#

import math, time

import numpy
from PyQt4 import QtCore, QtGui

from interface.pycadapp             import PyCadApp
from interface.entity.base          import BaseEntity
from interface.entity.segment       import Segment
from interface.entity.arc           import Arc
from interface.entity.text          import Text
from interface.entity.ellipse       import Ellipse
from interface.entity.arrowitem     import ArrowItem
from interface.entity.actionhandler import PositionHandler
from interface.entity.dinamicentryobject   import DinamicEntryLine
from interface.cadinitsetting       import *
from interface.preview.base         import PreviewBase, Preview

from interface.drawinghelper.snap import *
from interface.drawinghelper.polarguides import GuideHandler

from kernel.pycadevent              import PyCadEvent
from kernel.geoentity.point         import Point
from kernel.exception               import *
from kernel.entity                  import Entity

from kernel.command.inputs import PointInput, LengthInput
from kernel.db.schema import Point as Point2
from kernel.db import schema
from interface.preview.factory import getPreviewObject


class CadScene(QtGui.QGraphicsScene):
    def __init__(self, document, parent=None):
        super(CadScene, self).__init__(parent)

        self.active_command = None
        self.active_entity = None
        self.preview_item = None
        self.connect(parent._mainwindow, QtCore.SIGNAL('command_started'), self._start_command)
        self.connect(self, QtCore.SIGNAL('left_mouse_release'), self._process_click)
        self.connect(self, QtCore.SIGNAL('mouse_move'), self._process_move)

        # drawing limits
        self.setSceneRect(-10000, -10000, 20000, 20000)
        # scene custom event
        self.zoomWindows=PyCadEvent()
        self.fireCommandlineFocus=PyCadEvent()
        self.fireKeyShortcut=PyCadEvent()
        self.fireKeyEvent=PyCadEvent()
        self.fireWarning=PyCadEvent()
        self.fireCoords=PyCadEvent()
        #fire Pan and Zoom events to the view
        self.firePan=PyCadEvent()
        self.fireZoomFit=PyCadEvent()
        self.document = document
        self.needPreview=False
        self.forceDirectionEnabled=False
        self.forceDirection=None
        self.__lastPickedEntity=None
        self.isInPan=False
        self.forceSnap=None
        self._cmdZoomWindow=None
        self.showHandler=False
        self.posHandler=None
        #
        # new command implementation
        #
        self.__activeKernelCommand=None
        self.activeICommand=None
        #
        self.__grapWithd=20.0
        #
        # Input implemetation by carlo
        #
        self.fromPoint=None #frompoint is assigned in icommand.getClickedPoint() and deleted by applycommand and cancelcommand, is needed for statusbar coordinates dx,dy
        self.selectionAddMode=False

        # Init loading of snap marks
        self.initSnap()

        # Init loading of guides
        self.isGuided=None
        self.isGuideLocked=None
        self.initGuides()

        # scene aspect
        r, g, b=BACKGROUND_COLOR #defined in cadinitsetting
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(r, g, b), QtCore.Qt.SolidPattern))

    def _start_command(self, command):
        if self.active_command or self.active_entity:
            # TODO: Cancel current command (cancel and then start the new one)
            pass

        self.active_command = command(self.document)

    def _process_click(self, event):
        if not self.active_command:
            return False

        command = self.active_command
        current_input = command.inputs[command.active_input]

        if isinstance(current_input, PointInput):
            point = Point2(x=event.scenePos().x(), y=event.scenePos().y())
            current_input.value = point

        if isinstance(current_input, LengthInput):
            # TODO: Want to pass point and let preview item deal with it
            a = abs(current_input.point.value.x - event.scenePos().x())
            b = abs(current_input.point.value.y - event.scenePos().y())
            c = numpy.sqrt(numpy.power(a, 2) + numpy.power(b, 2))
            current_input.value = c

        if command.can_preview and (command.active_input == command.preview_start):
            self.preview_item = getPreviewObject(command)
            self.addItem(self.preview_item)

        command.active_input = command.active_input + 1

        if command.active_input == len(command.inputs):
            entity = command.apply_command()
            # TODO: Better way to check if single or multiple entities
            if not isinstance(entity, schema.Entity):
                self.add_entities(entity)
            else:
                self.addGraficalObject(entity)
            # TODO: Rebuild scene
            self.end_command()

    def _process_move(self, event):
        if not self.active_command:
            return False

        if self.preview_item:
            self.preview_item.updatePreview(event)

    def end_command(self):
        self.clearSelection()
        self.active_command = None
        self.active_entity = None
        self.preview_item = None
        self.clearPreview()

    def initSnap(self):
        # Init loading of snap marks
        self.snappingPoint=SnapPoint(self)
        self.endMark=SnapEndMark(0.0, 0.0)
        self.addItem(self.endMark)

    def initGuides(self):
        self.GuideHandler=GuideHandler(self, 0.0, 0.0,0.0 )
        self.addItem(self.GuideHandler)
        self.GuideHandler.reset()

    @property
    def activeKernelCommand(self):
        """
            return the active command
        """
        return self.__activeKernelCommand
    @activeKernelCommand.setter
    def activeKernelCommand(self, value):
        self.__activeKernelCommand=value

    def setActiveSnap(self, value):
        if self.activeICommand!=None:
            self.activeICommand.activeSnap=value
            self.snappingPoint.activeSnap=value

    def _qtInputPopUpReturnPressed(self):
        self.forceDirection="F"+self.qtInputPopUp.text

# ###############################################MOUSE EVENTS
# ##########################################################

    def mouseMoveEvent(self, event):
        self.emit(QtCore.SIGNAL('mouse_move'), event)
        scenePos=event.scenePos()
        mouseOnSceneX=scenePos.x()
        mouseOnSceneY=scenePos.y()*-1.0
        self.geoMousePointOnScene=Point(mouseOnSceneX,mouseOnSceneY)
        #
        # This event manages middle mouse button PAN
        #
        if self.isInPan:
            self.firePan(None, event.scenePos())
        #
        #This event manages the status bar coordinates display (relative or absolute depending on self.fromPoint)
        #
        else:
            if self.fromPoint==None:
                self.fireCoords(mouseOnSceneX, mouseOnSceneY, "abs")
            else:
                x=mouseOnSceneX-self.fromPoint.getx()
                y=mouseOnSceneY-self.fromPoint.gety()
                self.fireCoords(x, y, "rel")
        #
        #This seems needed to preview commands
        #
        ps=self.geoMousePointOnScene

        # if self.activeICommand:
        #     #SNAP PREVIEW
        #     if self.activeKernelCommand.activeException()==ExcPoint or self.activeKernelCommand.activeException()==ExcLenght:
        #         item=self.activeICommand.getEntity(ps)
        #         if item:
        #             ps=self.snappingPoint.getSnapPoint(self.geoMousePointOnScene, item)
        #             if ps!=self.geoMousePointOnScene:
        #                 self.endMark.move(ps.getx(), ps.gety()*-1.0)
        #         else:
        #             self.hideSnapMarks()
        #     qtItem=[self.itemAt(scenePos)]
        #     self.activeICommand.updateMauseEvent(ps, qtItem)
        super(CadScene, self).mouseMoveEvent(event)
        return



    def mousePressEvent(self, event):
        self.emit(QtCore.SIGNAL('mouse_press'), event)
        # TODO: Ignore groupitems?
        # print self.items(event.scenePos())

        if event.button()==QtCore.Qt.MidButton:
            self.isInPan=True
            self.firePan(True, event.scenePos())
        if not self.isInPan:
            qtItem=self.itemAt(event.scenePos())
            if qtItem:
                qtItem.setSelected(True)
                self.updateSelected()
                if event.button()==QtCore.Qt.RightButton:
                    self.showContextMenu(qtItem, event)
        super(CadScene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.emit(QtCore.SIGNAL('left_mouse_release'), event)

        if event.button()==QtCore.Qt.MidButton:
            self.isInPan=False
            self.firePan(False, None)
        if not self.isInPan:
            self.updateSelected()
            if self.activeICommand:
                if event.button()==QtCore.Qt.RightButton:
                    try:
                        self.activeICommand.applyDefault()
                    except PyCadWrongInputData:
                        self.fireWarning("Wrong input value")
                if event.button()==QtCore.Qt.LeftButton:
                    point=Point(event.scenePos().x(), event.scenePos().y()*-1.0)
                    qtItems=[item for item in self.selectedItems() if isinstance(item, BaseEntity)]
                    if self.showHandler:
                        if self.posHandler==None:
                            self.posHandler=PositionHandler(event.scenePos())
                            self.addItem(self.posHandler)
                        else:
                            self.posHandler.show()

                    # fire the mouse to the ICommand class
                    point_2 = Point2(x=event.scenePos().x(), y=event.scenePos().y() * (-1.0))
                    self.activeICommand.addMouseEvent(point=point_2,
                        entity=qtItems, force=self.forceDirection)
            else:
                self.hideHandler()

        if self._cmdZoomWindow:
            self.zoomWindows(self.selectionArea().boundingRect())
            self._cmdZoomWindow=None
            self.clearSelection() #clear the selection after the window zoom, why? because zoom windows select entities_>that's bad

        super(CadScene, self).mouseReleaseEvent(event)
        return

    def showContextMenu(self, selectedQtItems, event):
        """
            show a context menu
        """
        def delete():
            self.fireKeyShortcut('DELETE')

        def property():
            self.fireKeyShortcut('PROPERTY')

        contexMenu=QtGui.QMenu()
        # Create Actions
        removeAction=contexMenu.addAction("Delete")
        QtCore.QObject.connect(removeAction, QtCore.SIGNAL('triggered()'), delete)

        propertyAction=contexMenu.addAction("Property")
        QtCore.QObject.connect(propertyAction, QtCore.SIGNAL('triggered()'), property)
        contexMenu.exec_(event.screenPos())
        del(contexMenu)

    def hanhlerDoubleClick(self):
        """
            event add from the handler
        """
        point=Point(self.posHandler.scenePos.x(), self.posHandler.scenePos.y()*-1.0)
        self.activeICommand.addMouseEvent(point=point,
                                            distance=self.posHandler.distance,
                                            angle=self.posHandler.angle)
        self.hideHandler()

    def hideHandler(self):
        """
            this function is used to hide the handler
        """
        if self.posHandler!=None:
            self.posHandler.hide()

    def hideSnapMarks(self):
        """
            this function is used to hide the handler
        """
        self.endMark.hide()

    def mouseDoubleClickEvent(self, event):
        if event.button()==QtCore.Qt.MidButton:
            self.fireZoomFit()
        else:
            return QtGui.QGraphicsScene.mouseDoubleClickEvent(self, event)

    # TODO: signal?
    def command_finished(self):
        self.cancelCommand()

    def cancelCommand(self):
        """
            cancel the active command
        """
        self.clearSelection()
        self.updateSelected()
        #self.forceDirection=None
        self.__activeKernelCommand=None
        self.activeICommand=None
        self.showHandler=False
        self.clearPreview()
        self.hideSnapMarks()
        self.fromPoint=None
        self.GuideHandler.reset()

# ################################################# KEY EVENTS
# ##########################################################

    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Return:
            if self.activeICommand!=None:
                self.activeICommand.applyCommand()
        elif event.key()==QtCore.Qt.Key_Escape:
            self.cancelCommand()
        elif event.key()==QtCore.Qt.Key_Space:
            self.fireCommandlineFocus(self, event)
        elif event.key()==QtCore.Qt.Key_Shift:
            if self.isGuided==True:
                self.isGuideLocked=True
                print "GUIDE LOCKED"
            else:
                self.selectionAddMode=True

#        elif event.key()==QtCore.Qt.Key_F8:  <<<<this must maybe be implemented in mainwindow
#            if self.forceDirection is None:
#                self.forceDirection=True
#            else:
#                self.forceDirection=None
#            print self.forceDirection
#            self.forceDirection='H'        <<<<<<<H and V are substituted by ortho mode, for future implementations it could be nice if shift pressed locks the direction of the mouse pointer
#        elif event.key()==QtCore.Qt.Key_V:  <<<Ortho mode should be rewritten allowing to enter step angles and snap direction
#            self.forceDirection='V'
        elif event.key()==QtCore.Qt.Key_Q: #Maybe we could use TAB
            self.showHandler=True
        else:
            if self.activeICommand!=None:
                self.fireCommandlineFocus(self, event)
                self.fireKeyEvent(event)
            elif event.key() in KEY_MAP:
                    #exec(KEY_MAP[event.key()])
                    self.fireKeyShortcut(KEY_MAP[event.key()])
        super(CadScene, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key()==QtCore.Qt.Key_Shift:
#            if self.activeICommand!=None:
#                if self.activeKernelCommand.activeException()==ExcMultiEntity:
            if self.isGuided==True:
                self.isGuideLocked=None
                self.isGuided=None
                self.GuideHandler.hideGuides()
            else:
                self.selectionAddMode=False
        else:
            pass

    def textInput(self, value):
        """
            someone give some test imput at the scene
        """
        if self.activeICommand!=None:
            #self.forceDirection=None # reset force direction for the imput value
            self.updateSelected()
            self.activeICommand.addTextEvent(value)
        return

    def updateSelected(self):
        """
            update all the selected items
        """
        for item in self.selectedItems():
            item.updateSelected()

    def clearPreview(self):
        """
            remove the preview items from the scene
        """
        entitys=[item for item in self.items() if isinstance(item, Preview)]
        for ent in entitys:
            self.removeItem(ent)

    def initDocumentEvents(self):
        """
            Initialize the document events.
        """
        if not self.document is None:
            self.document.showEntEvent        += self.eventShow
            self.document.updateShowEntEvent  += self.eventUpdate
            self.document.deleteEntityEvent   += self.eventDelete
            self.document.massiveDeleteEvent  += self.eventMassiveDelete
            self.document.undoRedoEvent       += self.eventUndoRedo
            self.document.hideEntEvent        += self.eventDelete

    def populateScene(self, document):
        """
        Traverse all entities in the document and add these to the scene.

        """
        all_entities = self.document.db.query(schema.Entity)
        for entity in all_entities:
            self.addGraficalObject(entity)

    def add_entities(self, entities):
        for entity in entities:
            self.addGraficalObject(entity)

    def addGraficalObject(self, entity):
        """
        Add the single object

        """

        obj = entity.content_object
        graphical_entity = ENTITY_MAP[obj.__class__](obj)
        self.addGraficalItem(graphical_entity)

        # newQtEnt=None
        # entityType=entity.getEntityType()
        # if entityType in SCENE_SUPPORTED_TYPE:
        #     newQtEnt=SCANE_OBJECT_TYPE[entityType](entity)
        #     self.addGraficalItem(newQtEnt)

    def addGraficalItem(self, qtItem):
        """
        Add item to the scene

        """
        if qtItem != None:
            self.addItem(qtItem)

    def eventUndoRedo(self, document, entity):
        """
            Manage the undo redo event
        """
        self.clear()
        self.populateScene(document)
        self.initSnap()
        self.initGuides()


    def eventShow(self, document, entity):
        """
            Manage the show entity event
        """
        self.addGraficalObject(entity)


    def eventUpdate(self, document, entity):
        """
            Manage the Update entity event
        """
        self.updateItemsFromID([entity])


    def eventDelete(self, document, entity):
        """
            Manage the Delete entity event
        """
        #import time
        #startTime=time.clock()
        self.deleteEntity([entity])
        #endTime=time.clock()-startTime
        #print "eventDelete in %s"%str(endTime)

    def eventMassiveDelete(self, document,  entitys):
        """
            Massive delete of all entity event
        """
        #import time
        #startTime=time.clock()
        self.deleteEntity(entitys)
        #endTime=time.clock()-startTime
        #print "eventDelete in %s"%str(endTime)

    def deleteEntity(self, entitys):
        """
            delete the entity from the scene
        """
        dicItems=dict([( item.ID, item)for item in self.items() if isinstance(item, BaseEntity)])
        for ent in entitys:
            if ent.eType!="LAYER":
                itemId=ent.getId()
                if dicItems.has_key(itemId):
                    self.removeItem(dicItems[itemId])

    def getEntFromId(self, id):
        """
            get the grafical entity from an id
        """
        dicItems=dict([( item.ID, item)for item in self.items() if isinstance(item, BaseEntity) and item.ID==id])
        if len(dicItems)>0:
            return dicItems[0][1]
        return None

    def updateItemsFromID(self,entitys):
        """
            Update the scene from the Entity []
        """
        dicItems=self.getAllBaseEntity()
        for ent in entitys:
            if ent.getId() in dicItems:
                self.removeItem(dicItems[ent.getId()])
                self.addGraficalObject(ent)

    def getAllBaseEntity(self):
        """
            get all the base entity from the scene
        """
        return dict([( item.ID, item)for item in self.items() if isinstance(item, BaseEntity)])

    def updateItemsFromID_2(self,entities):
        """
            update the scene from the Entity []
        """
        ids=[ent.getId() for ent in entities]
        items=[item for item in self.items() if item.ID in ids]
        for item in items:
                self.removeItem(item)
        for ent in entities:
                self.addGraficalObject(ent)
