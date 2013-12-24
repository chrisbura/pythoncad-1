
from PyQt4 import QtGui, QtCore
from Interface.Preview.base import Preview
import numpy


class Point(QtGui.QGraphicsEllipseItem):
    def __init__(self, point):
        radius = 2
        super(Point, self).__init__(
            point.x - radius,
            point.y - radius,
            radius * 1.5,
            radius * 1.5
         )
        self.setAcceptHoverEvents(True)
        self.setBrush(QtCore.Qt.black)
        self.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))


class Circle(QtGui.QGraphicsEllipseItem):
    def __init__(self, center_point, radius):
        super(Circle, self).__init__(
            center_point.x - radius,
            center_point.y - radius,
            radius * 2.0,
            radius * 2.0
        )
        self.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
        self.setAcceptHoverEvents(True)


class CirclePreview(Preview, QtGui.QGraphicsItemGroup):
    def __init__(self, command):
        self.command = command
        super(CirclePreview, self).__init__()
        self.setHandlesChildEvents(False)

        self.center = self.command.inputs[0].value

        self.center_point = Point(self.center)
        self.ellipse = Circle(self.center, 0.0)

        self.addToGroup(self.center_point)
        self.addToGroup(self.ellipse)

    def updatePreview(self, event):
        a = abs(self.center.x - event.scenePos().x())
        b = abs(self.center.y - event.scenePos().y())
        c = numpy.sqrt(numpy.power(a, 2) + numpy.power(b, 2))
        ellipse_update = Circle(self.center, c)
        self.ellipse.setRect(ellipse_update.rect())
