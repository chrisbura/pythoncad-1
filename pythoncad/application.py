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
# This  module provide the main api interface of pythoncad
#
#
import sys
import os
import shutil
#
if __name__=="__main__":
    sys.path.append(os.path.join(os.getcwd(), 'Kernel'))
#
from kernel.exception           import *
from kernel.document            import *
from kernel.command             import *


class Application(object):
    """
        this class provide the real pythoncad api interface ..
    """
    def __init__(self, **args):
        userDirectory=os.getenv('USERPROFILE') or os.getenv('HOME')
        pyUserDir=os.path.join(userDirectory, "PythonCAD")
        if not os.path.exists(pyUserDir):
            os.makedirs(pyUserDir)
        baseDbName=os.path.join(pyUserDir, 'PythonCAD_Local.pdr')
        # TODO: Dev use only, remove at will
        if os.path.exists(baseDbName):
            os.remove(baseDbName)
        #--
        # Kernel document is used for application settings
        # TODO: Convert to 'application document'
        self.kernel = Document(baseDbName)
        self.__applicationCommand=APPLICATION_COMMAND
        # manage Document inizialization
        self.open_documents={}
        if args.has_key('open'):
            self.openDocument(args['open'])
        else:
            self.__ActiveDocument=None
        # Fire the Application inizialization



    @property
    def getRecentFiles(self):
        """
            read from application settings the recent files
        """
        objSettings=self.getApplicationSetting()
        nFiles=objSettings.getVariable("MAX_RECENT_FILE")
        if nFiles:
            files=objSettings.getVariable("RECENT_FILE_ARRAY")
            if files:
                return files
            else:
                objSettings.setVariable("RECENT_FILE_ARRAY",[] )
                self.updateApplicationSetting(objSettings)
        else:
            objSettings.setVariable("MAX_RECENT_FILE",MAX_RECENT_FILE )
            objSettings.setVariable("RECENT_FILE_ARRAY",[] )
            self.updateApplicationSetting(objSettings)
        return []


    def addRecentFiles(self,fPath):
#-- - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=
#                                                                   S-PM 110427
#Method to add the given full file name on top of the "Open history list",
#provided it is different from the one already present on top of the list.
#
#--Req-global
#MAX_RECENT_FILE    local default max. history list length
#
#--Req
#fPath   full file name to add to the list
#-- - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=
        #--standard "Documentation String"
        """Add a new file name on top of the history list"""

        #--Register
        rgO=None    #Object
        rgN=None    #Integer
        rgL=None    #List

        #--Action
        rgO=self.getApplicationSetting()    #get current settings

        #--get and consider history list lenght parameter
        rgN=rgO.getVariable("MAX_RECENT_FILE")
        if (not rgN): rgN=0 #assure it's numeric
        if (rgN<1):   #<-force a local default value, if not given
            rgN=MAX_RECENT_FILE
            if (rgN<1): rgN=1   #force anyhow at least a length=1
            rgO.setVariable("MAX_RECENT_FILE",rgN)
        #>

        #--get and consider current history list
        rgL=rgO.getVariable("RECENT_FILE_ARRAY")
        if (not rgL):   #<-assign an empty list, if not given
            rgL=[]
        #>

        #--conditioned addition of the given full file name
        if (len(rgL)==0):       #<-empty list:
            rgL.insert(0,fPath)      #add given file path
        elif (rgL[0]!=fPath):   #=-last recorded path is not the same:
            rgL.insert(0,fPath)      #add given file path
        #>

        while(len(rgL)>(rgN)):    #--chop the list to the desired length
            rgL.pop(-1)
        #>

        rgO.setVariable("RECENT_FILE_ARRAY", rgL)   #--update current settings
        self.updateApplicationSetting(rgO)
    #addRecentFiles>


    def getCommand(self,commandType):
        """
            Get a command of commandType
        """
        if not self.__ActiveDocument:
            raise EntityMissing("Miss Active document in the application")

        # Check if valid command (from initsettings)
        if self.__applicationCommand.has_key(commandType):
            cmd=self.__applicationCommand[commandType]
            cmdIstance=cmd(self.__ActiveDocument)
            return cmdIstance
        else:
            raise PyCadWrongCommand("")

    def getCommandList(self):
        """
            get the list of all the command
        """
        return self.__applicationCommand.keys()

    def newDocument(self, file_name=None):
        document = Document(file_name)
        file_name = document.db_path
        self.open_documents[file_name] = document
        self.ActiveDocument = self.open_documents[file_name]              #   Set Active the document
        self.addRecentFiles(file_name)
        return self.open_documents[file_name]

    def openDocument(self, file_name):
        """
            open a saved document
        """
        if not self.open_documents.has_key(file_name):
            self.open_documents[file_name]=Document(file_name)
            self.addRecentFiles(file_name)
        self.ActiveDocument=self.open_documents[file_name]                  #   Set Active the document
        return self.open_documents[file_name]

    def saveAs(self, newFileName):
        """
            seve the current document to the new position
        """
        if self.__ActiveDocument:
            (name, extension)=os.path.splitext(str(newFileName))
            if extension.upper()=='.DXF':
                self.__ActiveDocument.exportExternalFormat(newFileName)
                return self.__ActiveDocument
            else:
                oldFileName=self.__ActiveDocument.getName()
                self.closeDocument(oldFileName)
                shutil.copy2(oldFileName,newFileName)
                return self.openDocument(newFileName)
        raise EntityMissing, "No document open in the application unable to perform the saveAs comand"


    def closeDocument(self, file_name):
        if self.open_documents.has_key(file_name):
            # Close document database connection
            self.open_documents[file_name].close()
            del(self.open_documents[file_name])
        else:
            raise IOError("Unable to close the file:  %s" % str(file_name))

    @property
    def ActiveDocument(self):
        """
            get The active Document
        """
        return self.__ActiveDocument

    @ActiveDocument.setter
    def ActiveDocument(self, document):
        """
            Set the document to active
        """
        if document:
            if self.open_documents.has_key(document.dbPath):
                self.__ActiveDocument=self.open_documents[document.dbPath]
            else:
                raise EntityMissing("Unable to set active the document %s"%str(document.dbPath))
        else:
            self.__ActiveDocument=document

    def getDocuments(self):
        """
            get the Docuemnts Collection
        """
        return self.open_documents

    #
    # manage application style
    #
    def getApplicationStyleList(self):
        """
            Get the application styles
        """
        return self.kernel.getDBStyles()

    def getApplicationStyle(self, id=None, name=None):
        """
            retrive a style from the application
        """
        return self.kernel.getStyle(id, name)

    def setApplicationStyle(self, style):
        """
            add style to the application
        """
        self.kernel.saveEntity(style)

    def deleteApplicationStyle(self, styleID):
        """
            delete the application style
        """
        self.kernel.deleteEntity(styleID)

    #
    # Manage the application settings
    #
    def getApplicationSetting(self):
        """
            return the setting object from the application
        """
        return self.kernel.getDbSettingsObject()

    def updateApplicationSetting(self, settingObj):
        """
            update the application settingObj
        """
        #apObj=self.kernel.getDbSettingsObject()
        #apObj.setConstructionElement(settingObj)
        self.kernel.saveEntity(settingObj)
