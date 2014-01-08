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

# This is only needed for Python v2 but is harmless for Python v3.

#import sip
#sip.setapi('QString', 2)

import os
import datetime
from functools import partial

from PyQt4 import QtCore, QtGui

import cadwindow_rc

#Interface
from interface.subwindow            import SubWindow
from interface.cadinitsetting       import *
from interface.dialogs.preferences  import Preferences
#Kernel
from kernel.exception               import *
from kernel.initsetting             import * #SNAP_POINT_ARRAY, ACTIVE_SNAP_POINT

from interface.drawinghelper.polarguides import getPolarMenu

from kernel.command.segmentcommand import SegmentCommand
from kernel.command.circlecommand import CircleCommand
from kernel.command.pointcommand import PointCommand
from kernel.command.ellipsecommand import EllipseCommand
from kernel.command.rectanglecommand import RectangleCommand

from interface.db.settings import InterfaceDb
from interface.db.schema import RecentFile, Settings

from kernel.document import Document

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Add title text and icon to QMainWindow
        self.setWindowTitle('PythonCAD')
        qIcon = self._getIcon('pythoncad')
        if qIcon:
            self.setWindowIcon(qIcon)

        # Create and add QMdiArea (multiple document area) as central widget in QMainWindow
        self.mdiArea = QtGui.QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        # Initialize Interface settings
        # TODO: Have user configurable location (or just the homedir)
        current_folder = os.getcwd()
        db_path = os.path.join(current_folder, 'pycad_interface_settings.tmp')
        self.settings_db = InterfaceDb(db_path)
        self.db = self.settings_db.session

        # Initialize self.settings with either the row in the db or a new Settings object
        self.initialize_settings()




        # create all dock windows
        # self._createDockWindows()
        # create status bar
        self._createStatusBar()
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.lastDirectory=os.getenv('USERPROFILE') or os.getenv('HOME')

        # Menubar
        self.menubar = self.menuBar()
        self.populate_menu()

        self.updateRecentFileList()

        # Toolbar
        self.actions = [
            'point_action',
            'segment_action',
            'rectangle_action',
            'circle_action',
            'ellipse_action'
        ]
        self.command_toolbar = self.addToolBar('Commands')
        self.command_toolbar.setMovable(False)
        self.command_toolbar.setObjectName('command_toolbar')
        self.populate_toolbar()

        # Toggle button enabled/disabled
        self.updateMenus()

        # Build window menu
        self.update_window_menu()

        # Signals
        # TODO: Merge into a 'rebuild' method
        self.mdiArea.subWindowActivated.connect(self.subWindowActivatedEvent)
        self.mdiArea.subWindowActivated.connect(self.update_window_menu)
        self.mdiArea.subWindowActivated.connect(self.updateMenus)

        self.readSettings() #now works for position and size and ismaximized, and finally toolbar position

    def populate_menu(self):
        # File Menu
        self.file_menu = self.menubar.addMenu('&File')

        file_new = QtGui.QAction('&New File', self, triggered=self._onNewDrawing)

        self.file_open_recent = QtGui.QMenu('Open &Recent File', self)

        file_close = QtGui.QAction('&Close File', self, triggered=self._onCloseDrawing)

        # TODO: Close all subwindows properly (close the db connections)?
        file_quit  = QtGui.QAction('&Quit', self, triggered=QtGui.qApp.closeAllWindows)

        self.file_menu.addAction(file_new)
        self.file_menu.addMenu(self.file_open_recent)
        self.file_menu.addSeparator()
        self.file_menu.addAction(file_close)
        self.file_menu.addSeparator()
        self.file_menu.addAction(file_quit)

        self.window_menu = self.menubar.addMenu('&Windows')

    @property
    def scene(self):
        if self.mdiArea.activeSubWindow():
            return self.mdiArea.activeSubWindow().scene

    @property
    def view(self):
        if self.mdiArea.activeSubWindow():
            return self.mdiArea.activeSubWindow().view

    def _createStatusBar(self):
        '''
            Creates the statusbar object.
        '''

        self.statusBar().showMessage("Ready")

        #------------------------------------------------------------------------------------Create status buttons



        #Grid
        self.GridStatus=statusButton('SGrid.png', 'Grid Mode [not available yet]')
        self.connect(self.GridStatus, QtCore.SIGNAL('clicked()'), self.setGrid)
        self.statusBar().addPermanentWidget(self.GridStatus)

        #------------------------------------------------------------------------------------Set coordinates label on statusbar (updated by idocumet)
        self.coordLabel=QtGui.QLabel("x=0.000\ny=0.000")
        self.coordLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.coordLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        self.coordLabel.setMinimumWidth(80)
        self.coordLabel.setMaximumHeight(20)
        self.coordLabel.setFont(QtGui.QFont("Sans", 6))
        self.statusBar().addPermanentWidget(self.coordLabel)

    def setForceDirection(self):
        if self.forceDirectionStatus.isChecked():
            self.scene.forceDirectionEnabled=True
            self.forceDirectionStatus.setFocus(False)
            if self.scene.activeICommand!=None and self.scene.fromPoint!=None:
                self.scene.GuideHandler.show()
        else:
            self.scene.forceDirectionEnabled=False
            self.scene.GuideHandler.hide()

    def setSnapStatus(self):
        if self.SnapStatus.isChecked():
            self.scene.snappingPoint.activeSnap=SNAP_POINT_ARRAY['LIST']
        else:
            self.scene.snappingPoint.activeSnap=SNAP_POINT_ARRAY['NONE']

    def setGrid(self):
        pass

    def commandExecuted(self):
        self.resetCommand()

    def _createDockWindows(self):
        '''
            Creates all dockable windows for the application
        '''
        # commandline
        # command_dock = self.__cmd_intf.commandLine
        # if the commandline exists, add it
        if not command_dock is None:
            self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, command_dock)
        return

    def closeEvent(self, event):
        # Close all open document db connections
        subwindows = self.mdiArea.subWindowList()
        for subwindow in subwindows:
            subwindow.document.close()

        # Close all subwindows
        # TODO: Check if their closeEvents are called, move db close to there
        self.mdiArea.closeAllSubWindows()

        # Write settings (window position, maximized, etc)
        self.writeSettings()

        # Close the settings database
        del(self.settings_db)

        event.accept()

    def subWindowActivatedEvent(self):
        """
            Sub windows activation
        """
        self.updateMenus()

    def resetCommand(self):
        """
            Resect the active command
        """
        # self.__cmd_intf.resetCommand()
        if self.scene!=None:
            self.scene.cancelCommand()
        self.statusBar().showMessage("Ready")

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)

        # TODO: refactor
        for action in self.actions:
            getattr(self, action).setEnabled(hasMdiChild)

    def create_subwindow(self, file_name=None):

        # If the file is already open then just activate that subwindow
        subwindows = self.mdiArea.subWindowList()
        for subwindow in subwindows:
            if subwindow.document.db_path == file_name:
                return subwindow

        # If a file_name is given then open that document, else create a new document
        if file_name:
            document = Document(file_name)
        else:
            document = Document()

        # Update recent files
        # TODO: Move to a manager class
        # TODO: Make sure the file was actually opened before adding, ie. don't add an invalid file
        recent_file = self.db.query(RecentFile).filter_by(path=document.db_path).first()
        if recent_file:
            recent_file.last_access = datetime.datetime.now()
            self.db.commit()
        else:
            recent_file = RecentFile(path=document.db_path, last_access=datetime.datetime.now())
            self.db.add(recent_file)
            self.db.commit()

        child = SubWindow(document, self)
        self.mdiArea.addSubWindow(child)
        return child

    def populate_toolbar(self):

        self.point_action  = QtGui.QAction(QtGui.QIcon('icons/point.png'), 'Point', self,
            triggered=partial(self._call_command, PointCommand))

        self.segment_action  = QtGui.QAction(QtGui.QIcon('icons/segment.png'), 'Segment', self,
            triggered=partial(self._call_command, SegmentCommand))

        self.rectangle_action  = QtGui.QAction(QtGui.QIcon('icons/rectangle.png'), 'Rectangle', self,
            triggered=partial(self._call_command, RectangleCommand))

        self.circle_action  = QtGui.QAction(QtGui.QIcon('icons/circle.png'), 'Circle', self,
            triggered=partial(self._call_command, CircleCommand))

        self.ellipse_action  = QtGui.QAction(QtGui.QIcon('icons/ellipse.png'), 'Ellipse', self,
            triggered=partial(self._call_command, EllipseCommand))

        for action in self.actions:
            self.command_toolbar.addAction(getattr(self, action))

    def _call_command(self, command):
        # TODO: can be simplified?
        self.emit(QtCore.SIGNAL('command_started'), command)

    def update_window_menu(self):
        """
        Refresh currently open document list

        To display open documents outside of a submenu the entire window menu must
        be rebuilt

        """
        self.window_menu.clear()
        window_list = self.mdiArea.subWindowList()
        for window in window_list:
            action = self.window_menu.addAction('{0}'.format(window.document.db_path))
            action.setCheckable(True)
            action.setChecked(window.widget() is self.activeMdiChild())
            action.triggered.connect(partial(self.mdiArea.setActiveSubWindow, window))

    def updateRecentFileList(self):
        # Empty out the recent submenu
        self.file_open_recent.clear()
        # TODO: Move to a manager class
        # TODO: Clear old entries after some condition
        recent_files = self.db.query(RecentFile).order_by(RecentFile.last_access.desc())[:MAX_RECENT_FILE]

        if not recent_files:
            # Add a blank action if there are no recent files
            self.file_open_recent.addAction('None').setDisabled(True)

        for recent_file in recent_files:
            entry = QtGui.QAction(recent_file.path, self)
            entry.triggered.connect(partial(self.openDrawing, recent_file))
            self.file_open_recent.addAction(entry)

        self.file_open_recent.addSeparator()
        clear_now = QtGui.QAction('Clear Now', self)
        clear_now.triggered.connect(self.clear_recent)
        self.file_open_recent.addAction(clear_now)

    def clear_recent(self):
        # TODO: Check return value
        self.db.query(RecentFile).delete()
        self.updateRecentFileList()

    def strippedName(self, fullFileName):
        """
            get only the name of the filePath
        """
        return QtCore.QFileInfo(fullFileName).fileName()

    def openDrawing(self, file_path):
        if not os.path.exists(file_path):
            # TODO: Return a proper error
            return
        child = self.create_subwindow(file_path)
        child.show()
        self.mdiArea.setActiveSubWindow(child)
        self.updateRecentFileList()
        self.update_window_menu()
        self.view.fit()
        return

    def _onNewDrawing(self):
        child = self.create_subwindow()
        child.show()
        self.update_window_menu()
        self.updateRecentFileList()

    def _onOpenDrawing(self):
        '''
            Open an existing drawing PDR or DXF
        '''
        # ask the user to select an existing drawing
        drawing = str(QtGui.QFileDialog.getOpenFileName(parent=self,directory=self.lastDirectory,  caption ="Open Drawing", filter ="Drawings (*.pdr *.dxf)"))
        # open a document and load the drawing
        if len(drawing)>0:
            self.lastDirectory=os.path.split(drawing)[0]
            (name, extension)=os.path.splitext(drawing)
            if extension.upper()=='.DXF':
                child = self.create_subwindow()
                child.importExternalFormat(drawing)
            elif extension.upper()=='.PDR':
                child = self.create_subwindow(drawing)
            else:
                self.critical("Wrong command selected")
                return
            child.show()
            self.updateRecentFileList()
            self.update_window_menu()
            self.view.fit()
        return

    def _onImportDrawing(self):
        '''
            Import existing drawing in current drawing (some issues with PyQt4.7)
        '''
        drawing = QtGui.QFileDialog.getOpenFileName(parent=self, caption="Import Drawing", directory=self.lastDirectory, filter="Dxf (*.dxf)");
        # open a document and load the drawing
        if len(drawing)>0:
            self.lastDirectory=os.path.split(drawing)[0]
            self.mdiArea.activeSubWindow().importExternalFormat(drawing)
        return

    def _onSaveAsDrawing(self):
        drawing = QtGui.QFileDialog.getSaveFileName(self, "Save As...", "/home", filter ="Drawings (*.pdr *.dxf)");
        if len(drawing)>0:
            self.application.saveAs(drawing)

            # Connection has been closed already so close the child window
            self.mdiArea.closeActiveSubWindow()
            # Create new child window with the new path/filename
            child = self.create_subwindow(drawing)
            child.show()
            self.updateRecentFileList()
            self.update_window_menu()
            self.view.fit()

    def _onPrint(self):
#       printer.setPaperSize(QPrinter.A4);
        self.scene.clearSelection()
        printer=QtGui.QPrinter()
        printDialog=QtGui.QPrintDialog(printer)
        if (printDialog.exec_() == QtGui.QDialog.Accepted):
            painter=QtGui.QPainter()
            painter.begin(printer)
            painter.setRenderHint(QtGui.QPainter.Antialiasing);
            #self.mdiArea.activeSubWindow().scene.render(painter)
            self.mdiArea.activeSubWindow().view.render(painter)
            painter.end()
        self.statusBar().showMessage("Ready")
        return

    def _onCloseDrawing(self):
        # Get document path of the currently active window we want to close
        active_subwindow = self.mdiArea.activeSubWindow()
        path = active_subwindow.document.db_path

        active_subwindow.document.close()
        self.mdiArea.closeActiveSubWindow()
        # TODO: Emit open document change signal
        self.update_window_menu()

    def _onCloseAll(self):
        window_list = self.mdiArea.subWindowList()
        for window in window_list:
            window.document.close()
        self.mdiArea.closeAllSubWindows()
        self.update_window_menu()
        return

    def preferences(self):
        p=Preferences(self)
        #TODO: Fill up preferences
        if (p.exec_() == QtGui.QDialog.Accepted):
            #TODO: save Preferences
            pass

    def _onAbout(self):
        QtGui.QMessageBox.about(self, "About PythonCAD",
                """<b>PythonCAD</b> is a CAD package written, surprisingly enough, in Python using the PyQt4 interface.<p>
                   The PythonCAD project aims to produce a scriptable, open-source,
                   easy to use CAD package for any Python/PyQt supported Platforms
                   <p>
                   This is an Alfa Release For The new R38 Vesion <b>(R38.0.0.5)<b><P>
                   <p>
                   <a href="http://sourceforge.net/projects/pythoncad/">PythonCAD Web Site On Sourceforge</a>
                   <p>
                   <a href="http://pythoncad.sourceforge.net/dokuwiki/doku.php">PythonCAD Wiki Page</a>
                   """)
        return

    def updateInput(self, message):
        # self.__cmd_intf.commandLine.printMsg(str(message))
        self.statusBar().showMessage(str(message))

    @staticmethod
    def critical(text):
        '''
            Shows an critical message dialog
        '''
        dlg = QtGui.QMessageBox()
        dlg.setText(text)
        dlg.setIcon(QtGui.QMessageBox.Critical)
        dlg.exec_()
        return

    def initialize_settings(self):
        """
        Store settings inside the database instead of QSettings to allow multiple
        instances to be run at the same time.

        """

        # Read settings from database
        settings = self.db.query(Settings).first()
        if settings:
            self.settings = settings
        else:
            # Initialize default settings values
            # TODO: Get better defaults from somewhere
            self.settings = Settings(
                window_maximized = False,
                window_height = 768,
                window_width = 1024,
                window_x = 100,
                window_y = 100,
                state = self.saveState().data()
            )
            self.db.add(self.settings)
            self.db.commit()

    def readSettings(self):
        """
        Restores window geometry as well as toolbar positions

        """

        # Resize the window
        self.resize(QtCore.QSize(
            self.settings.window_width,
            self.settings.window_height
        ))

        # Move the window, top left is QPoint(0, 0)
        self.move(QtCore.QPoint(
            self.settings.window_x,
            self.settings.window_y
        ))

        # Maximize the window
        if self.settings.window_maximized:
            self.showMaximized()

        # Restore toolbar positions
        self.restoreState(
            QtCore.QByteArray(self.settings.state)
        )

    def writeSettings(self):
        """
        Saves window geometry values as well as the location of toolbars
        See http://qt-project.org/doc/qt-4.8/application-windows.html#window-geometry

        """
        # Don't save the window geometry if the window is maximized
        # When user un maximizes the window it returns to previous values
        if not self.isMaximized():
            self.settings.window_height = self.size().height()
            self.settings.window_width = self.size().width()
            self.settings.window_x = self.pos().x()
            self.settings.window_y = self.pos().y()

        self.settings.window_maximized = self.isMaximized()

        # Save toolbar locations
        self.settings.state = self.saveState().data()

        # Save to db
        self.db.commit()

    def activeMdiChild(self):
        # TODO: From PyQt examples, add license info back in
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def switchLayoutDirection(self):
        if self.layoutDirection() == QtCore.Qt.LeftToRight:
            QtGui.qApp.setLayoutDirection(QtCore.Qt.RightToLeft)
        else:
            QtGui.qApp.setLayoutDirection(QtCore.Qt.LeftToRight)

    def _getIcon(self, cmd):
        '''
        Create an QIcon object based on the command name.
        The name of the icon is ':/images/' + cmd + '.png'.
        If the cmd = 'Open', the name of the icon is ':/images/Open.png'.
        '''
        icon_name = cmd + '.png'
        icon_path = os.path.join(os.path.join(os.getcwd(), 'icons'), icon_name)
        # check if icon exist
        if os.path.exists(icon_path):
            icon = QtGui.QIcon(icon_path)
            return icon
        # icon not found, don't use an icon, return None
        return None

    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Escape:
            self.resetCommand()

        super(MainWindow, self).keyPressEvent(event)

    def plotFromSympy(self, objects):
        """
            plot the sympy Object into PythonCAD
        """
        if self.mdiArea.currentSubWindow()==None:
            self._onNewDrawing()
        for obj in objects:
            self.plotSympyEntity(obj)

    def plotSympyEntity(self, sympyEntity):
        """
            plot the sympy entity
        """
        self.mdiArea.currentSubWindow().document.saveSympyEnt(sympyEntity)

    def createSympyDocument(self):
        """
            create a new document to be used by sympy plugin
        """
        self._onNewDrawing()

    def getSympyObject(self):
        """
            get an array of sympy object
        """
        #if self.Application.ActiveDocument==None:
        if self.mdiArea.currentSubWindow()==None:
            raise StructuralError("unable to get the active document")

        ents=self.mdiArea.currentSubWindow().scene.getAllBaseEntity()
        return [ents[ent].geoItem.getSympy() for ent in ents if ent!=None]

class statusButton(QtGui.QToolButton):
    def __init__(self, icon=None,  tooltip=None):
        super(statusButton, self).__init__()
        self.setCheckable(True)
        self.setFixedSize(30, 20)
        if icon:
            self.getIcon(icon)
        self.setToolTip(tooltip)

    def getIcon(self, fileName):
        iconpath=os.path.join(os.getcwd(), 'icons', fileName)
        self.setIcon(QtGui.QIcon(iconpath))

    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            self.click()
        elif event.button()==QtCore.Qt.RightButton:
            self.showMenu()
