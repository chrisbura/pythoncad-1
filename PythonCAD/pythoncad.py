#!/usr/bin/env python

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

import os
import sys

from PyQt4 import QtCore, QtGui

from interface.mainwindow import MainWindow

def getPythonCAD():

    app = QtGui.QApplication(sys.argv)
    # splashscreen
    splashPath = os.path.join(os.getcwd(), 'icons', 'splashScreen1.png')
    splash_pix = QtGui.QPixmap(splashPath)
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    w = MainWindow()
    w.show()

    # end splashscreen
    splash.finish(w)
    return w, app
#
if __name__ == '__main__':
    w,app = getPythonCAD()
    sys.exit(app.exec_())
