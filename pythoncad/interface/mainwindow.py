#
# Copyright (c) 2010 Matteo Boscolo
# Copyright (c) 2013-2014 Christopher Bura
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

import os
from datetime import datetime
from functools import partial

from PyQt4 import QtCore, QtGui

from kernel.command import *
from kernel.initsetting import MAX_RECENT_FILE

from interface.subwindow import SubWindow
from interface.db.settings import InterfaceDb
from interface.db.schema import RecentFile, Settings

from kernel.document import Document

class MainWindow(QtGui.QMainWindow):

    document_opened = QtCore.pyqtSignal()
    document_closed = QtCore.pyqtSignal()

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

        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        self.create_statusbar()
        self.update_menus()

        # Initialize Interface settings
        # TODO: Have user configurable location (or just the homedir)
        current_folder = os.getcwd()
        db_path = os.path.join(current_folder, 'pycad_interface_settings.tmp')
        self.settings_db = InterfaceDb(db_path)
        self.db = self.settings_db.session

        # Initialize self.settings with either the row in the db or a new Settings object
        self.initialize_settings()
        self.restore_geometry()

        # Update Menu > File > Recent list
        self.update_recent()

        # Build window menu
        self.update_window_menu()

        # Signals
        # TODO: Merge into a 'rebuild' method
        self.mdiArea.subWindowActivated.connect(self.update_window_menu)
        self.mdiArea.subWindowActivated.connect(self.update_menus)

        self.document_opened.connect(self.update_window_menu)
        self.document_opened.connect(self.update_recent)
        self.document_opened.connect(self.update_menus)

        self.document_closed.connect(self.update_window_menu)
        self.document_closed.connect(self.update_menus)


    def create_actions(self):
        # Menu > File Actions
        self.new_action = QtGui.QAction('&New File', self,
            triggered=self.new_document)
        self.close_action = QtGui.QAction('&Close File', self,
            triggered=self.close_document)
        self.quit_action  = QtGui.QAction('&Quit', self,
            triggered=QtGui.qApp.closeAllWindows)

        self.open_recent_menu = QtGui.QMenu('Open &Recent File', self)

        # Toolbar > Command Actions
        self.point_action  = QtGui.QAction(
            QtGui.QIcon('icons/point.png'), 'Point', self,
            triggered=partial(self._call_command, PointCommand))

        self.segment_action  = QtGui.QAction(
            QtGui.QIcon('icons/segment.png'), 'Segment', self,
            triggered=partial(self._call_command, SegmentCommand))

        self.rectangle_action  = QtGui.QAction(
            QtGui.QIcon('icons/rectangle.png'), 'Rectangle', self,
            triggered=partial(self._call_command, RectangleCommand))

        self.circle_action  = QtGui.QAction(
            QtGui.QIcon('icons/circle.png'), 'Circle', self,
            triggered=partial(self._call_command, CircleCommand))

        self.ellipse_action  = QtGui.QAction(
            QtGui.QIcon('icons/ellipse.png'), 'Ellipse', self,
            triggered=partial(self._call_command, EllipseCommand))

    def create_menus(self):
        # File Menu
        self.file_menu = self.menuBar().addMenu('&File')
        self.file_menu.addAction(self.new_action)
        self.file_menu.addMenu(self.open_recent_menu)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.quit_action)

        # Window Menu
        self.window_menu = self.menuBar().addMenu('&Windows')

    def create_toolbars(self):
        # Command Toolbar
        self.command_toolbar = self.addToolBar('Commands')
        self.command_toolbar.setObjectName('command_toolbar')
        self.command_toolbar.addAction(self.point_action)
        self.command_toolbar.addAction(self.segment_action)
        self.command_toolbar.addAction(self.rectangle_action)
        self.command_toolbar.addAction(self.circle_action)
        self.command_toolbar.addAction(self.ellipse_action)

    def create_statusbar(self):
        self.coordinate_label = QtGui.QLabel("X=0.000 Y=0.000")
        self.coordinate_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.coordinate_label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        # self.coordinate_label.setMinimumWidth(80)
        # self.coordinate_label.setMaximumHeight(20)
        self.coordinate_label.setFont(QtGui.QFont("Sans", 10))
        self.statusBar().addPermanentWidget(self.coordinate_label)

    def update_menus(self):
        hasMdiChild = (self.activeMdiChild() is not None)

        # Menu > File
        self.close_action.setEnabled(hasMdiChild)

        # Toolbar > Command
        self.point_action.setEnabled(hasMdiChild)
        self.segment_action.setEnabled(hasMdiChild)
        self.rectangle_action.setEnabled(hasMdiChild)
        self.circle_action.setEnabled(hasMdiChild)
        self.ellipse_action.setEnabled(hasMdiChild)

    def closeEvent(self, event):
        # Close all open document db connections
        subwindows = self.mdiArea.subWindowList()
        for subwindow in subwindows:
            subwindow.document.close()

        # TODO: Check if their closeEvents are called, move db close to there
        self.mdiArea.closeAllSubWindows()

        # Write settings (window position, maximized, etc)
        self.writeSettings()

        # Close the settings database
        del self.settings_db

        event.accept()

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
        # TODO: Move to signal (document opened)
        recent_file = self.db.query(RecentFile).filter_by(path=document.db_path).first()
        if recent_file:
            recent_file.last_access = datetime.now()
            self.db.commit()
        else:
            recent_file = RecentFile(path=document.db_path, last_access=datetime.now())
            self.db.add(recent_file)
            self.db.commit()

        child = SubWindow(document, self)
        self.mdiArea.addSubWindow(child)

        self.update_window_menu()
        self.update_menus()

        return child

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

    def update_recent(self):
        # Empty out the recent submenu
        self.open_recent_menu.clear()
        # TODO: Move to a manager class
        # TODO: Clear old entries after some condition
        recent_files = self.db.query(RecentFile).order_by(RecentFile.last_access.desc())[:MAX_RECENT_FILE]

        if not recent_files:
            # Add a blank action if there are no recent files
            self.open_recent_menu.addAction('None').setDisabled(True)

        for recent_file in recent_files:
            entry = QtGui.QAction(recent_file.path, self)
            entry.triggered.connect(partial(self.openDrawing, recent_file))
            self.open_recent_menu.addAction(entry)

        self.open_recent_menu.addSeparator()
        clear_now = QtGui.QAction('Clear Now', self)
        clear_now.triggered.connect(self.clear_recent)
        self.open_recent_menu.addAction(clear_now)

    def clear_recent(self):
        # TODO: Check return value
        self.db.query(RecentFile).delete()
        self.update_recent()

    def openDrawing(self, file_path):
        if not os.path.exists(file_path):
            # TODO: Return a proper error
            return
        child = self.create_subwindow(file_path)
        child.show()
        self.mdiArea.setActiveSubWindow(child)
        # self.view.fit()
        self.document_opened.emit()

    def new_document(self):
        child = self.create_subwindow()
        child.show()
        self.document_opened.emit()

    def _onOpenDrawing(self):
        '''
            Open an existing drawing PDR or DXF
        '''
        # ask the user to select an existing drawing
        directory = os.getenv('USERPROFILE') or os.getenv('HOME')
        drawing = str(QtGui.QFileDialog.getOpenFileName(parent=self,directory=directory,  caption ="Open Drawing", filter ="Drawings (*.pdr *.dxf)"))
        # open a document and load the drawing
        if len(drawing)>0:
            directory=os.path.split(drawing)[0]
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
            self.document_opened.emit()
            # self.view.fit()
        return

    def _onImportDrawing(self):
        '''
            Import existing drawing in current drawing (some issues with PyQt4.7)
        '''
        directory = os.getenv('USERPROFILE') or os.getenv('HOME')
        drawing = QtGui.QFileDialog.getOpenFileName(parent=self, caption="Import Drawing", directory=directory, filter="Dxf (*.dxf)");
        # open a document and load the drawing
        if len(drawing)>0:
            directory=os.path.split(drawing)[0]
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
            self.document_opened.emit()
            # self.view.fit()

    def _onPrint(self):
#       printer.setPaperSize(QPrinter.A4);
        # self.scene.clearSelection()
        printer=QtGui.QPrinter()
        printDialog=QtGui.QPrintDialog(printer)
        if (printDialog.exec_() == QtGui.QDialog.Accepted):
            painter=QtGui.QPainter()
            painter.begin(printer)
            painter.setRenderHint(QtGui.QPainter.Antialiasing);
            #self.mdiArea.activeSubWindow().scene.render(painter)
            # self.mdiArea.activeSubWindow().view.render(painter)
            painter.end()
        self.statusBar().showMessage("Ready")
        return

    def close_document(self):
        # Get document path of the currently active window we want to close
        active_subwindow = self.mdiArea.activeSubWindow()
        path = active_subwindow.document.db_path

        active_subwindow.document.close()
        self.mdiArea.closeActiveSubWindow()

        self.document_closed.emit()

    def _onCloseAll(self):
        # TODO: Move db close to subwindow closeEvent
        window_list = self.mdiArea.subWindowList()
        for window in window_list:
            window.document.close()
        self.mdiArea.closeAllSubWindows()

        self.document_closed.emit()

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

    def restore_geometry(self):
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
