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
# You should have received a copy of the GNU General Public Licensesegmentcmd.py
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#This module provide a class for the Trim command
#
from kernel.exception               import *
from kernel.command.basecommand     import *
from kernel.geoentity               import *
from kernel.geoutil.intersection    import *
from kernel.geoutil.util            import *

class DeleteCommand(BaseCommand):
    """
        this class represents the delete command
    """
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        self.exception=[ExcMultiEntity]
        self.message=["Select Entities to be Deleted: "]

    def applyDefault(self):
        """
            aver written to  avoid apply default in this command
        """
        return

    def applyCommand(self):
        """
            apply the delete command
        """
        if len(self.value)!=1:
            raise PyCadWrongInputData("Wrong number of input parameter")
        try:
            self.document.startMassiveCreation()
            for id in str(self.value[0]).split(','):
                self.document.deleteEntity(id)
        finally:
            self.document.stopMassiveCreation()

