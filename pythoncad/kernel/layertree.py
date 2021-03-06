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
# This  module all the interface to store the layer
#
#TODO : REPAIR THE LOGGER FOR THIS CLASS

from kernel.exception import *
from kernel.pycadevent import PyCadEvent
from kernel.db.schema import Layer, Setting


class LayerTable(object):
    """
    Class used to interface with the database/save file

    """

    def __init__(self, kernel):
        self.kernel = kernel
        self.settings = {}

        self.db = self.kernel.db

        # Add a default layer if none exists
        layer_count = self.getLayerCount()
        if not layer_count:

            # Create 'Default' layer on new document creation
            layer = Layer(name='Default')
            self.db.add(layer)
            self.db.flush()

            self.settings['active_layer'] = Setting(name='active_layer', value=layer.id)
            self.db.add(self.settings['active_layer'])
            self.db.commit()

            self.__activeLayer = layer
        else:
            # TODO: Clean up
            self.settings['active_layer'] = self.db.query(Setting).filter_by(name='active_layer').first()
            if self.settings['active_layer']:
                layer = self.db.query(Layer).get(int(self.settings['active_layer'].value))
            else:
                self.settings['active_layer'] = Setting(name='active_layer')
                self.db.add(self.settings['active_layer']) # commited in setActiveLayer
                layer = self.getVisibleLayer()
            self.setActiveLayer(layer)

    def setActiveLayer(self, layer):
        self.__activeLayer=layer
        self.settings['active_layer'].value = layer.id
        self.db.commit()

    def getActiveLayer(self):
        return self.__activeLayer

    def insert(self, layer):
        self.setActiveLayer(layer)

    def _getLayerConstructionElement(self, pyCadEnt):
        """
            Retrive the ConstructionElement in the pyCadEnt
        """
        # TODO:
        unpickleLayers=pyCadEnt.getConstructionElements()
        for key in unpickleLayers:
            return unpickleLayers[key]
        return None

    def getLayerChildren(self,layer,entityType=None):
        """
        Delete all entities with layer as a foreign key

        """
        # TODO
        _children=self.kernel.getAllChildrenType(layer, entityType)
        return _children

    def getEntLayerDb(self,layerName):
        """
            get the pycadent  layer by giving a name
        """
        #TODO: manage logger self.__logger.debug('getEntLayerDb')
        _layersEnts=self.kernel.getEntityFromType('LAYER')
        #TODO: Optimaze this loop with the build in type [...] if possible
        for layersEnt in _layersEnts:
            unpickleLayers=layersEnt.getConstructionElements()
            for key in unpickleLayers:
                if unpickleLayers[key].name==layerName:
                    return layersEnt
        else:
            raise EntityMissing,"Layer name %s missing"%str(layerName)

    def getVisibleLayer(self, ignore = []):
        layers = self.db.query(Layer).filter(Layer.visible==True)
        if len(ignore) > 0:
            layers = layers.filter(~Layer.id.in_(ignore))

        result = layers.first()

        if result:
            return result
        return False

    def getLayerCount(self):
        layer_count = self.db.query(Layer).count()
        return layer_count

    def getLayers(self):
        layers = self.db.query(Layer).all()
        return layers

    def getLayerdbTree(self):
        # TODO: Update DXF export/import
        """
            create a dictionary with all the layer nested as db entity
        """
        # TODO
        rootDbEnt=self.getEntLayerDb(MAIN_LAYER)
        def createNode(layer):
            childs={}
            layers=self.getLayerChildrenLayer(layer)
            for l in layers:
                childs[l.getId()]=(l, createNode(l))
            return childs
        exitDb={}
        exitDb[rootDbEnt.getId()]=(rootDbEnt,createNode(rootDbEnt) )
        return exitDb

    def getParentLayer(self,layer):
        """
            get the parent layer
            ToDo: to be tested
        """
        # TODO:
        return self.kernel.getRelatioObject().getParentEnt(layer)

    def delete(self, layerId):
        """
            delete the current layer and all the entity related to it
        """
        # TODO:
        deleteLayer = self.kernel.getEntity(layerId)

        # If layer is currently active, find the first visible layer and set it active
        if layerId is self.__activeLayer.getId():
            visible_layer = self.getVisibleLayer(ignore = [layerId, ])
            if not visible_layer:
                raise PythonCadWarning("Unable to delete the last visible layer")
                return False
            self.setActiveLayer(visible_layer.getId())

        # Delete all entities (SEGMENTS, TEXT, etc.)
        self.deleteLayerEntity(deleteLayer)

        # Delete the layer
        self.kernel.deleteEntity(layerId)

    def deleteLayerEntity(self, layer):
        """
            delete all layer entity
        """
        # TODO:
        for ent in self.getLayerChildren(layer):
                self.kernel.deleteEntity(ent.getId())

    def rename(self, layer, new_name):
        self._rename(layer, new_name)

    def _rename(self, layer, new_name):
        layer.name = new_name
        self.db.commit()

    def _show(self, layer):
        layer.visible = True
        self.db.commit()

    def show(self, layer):
        self._show(layer)

    def _hide(self, layer):
        layer.visible = False
        self.db.commit()

    def hide(self, layer):
        # Prevent trying to hide the only layer
        if self.getLayerCount() <= 1:
            raise PythonCadWarning("Unable to hide the only Layer")
            return False

        # If layer is currently active, find the first visible layer and set it active
        if layer is self.__activeLayer:
            visible_layer = self.getVisibleLayer(ignore = [layer.id, ])
            if not visible_layer:
                raise PythonCadWarning("Unable to hide the last visible layer")
                return False
            self.setActiveLayer(visible_layer)

        self._hide(layer)
