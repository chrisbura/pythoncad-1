
from PyQt4 import QtGui, QtCore
from interface.entity.point import Point
from interface.entity.base import BaseItem


class Circle(BaseItem, QtGui.QGraphicsEllipseItem):
    def __init__(self, obj):
        self.center = obj.point
        self.radius = obj.radius

        super(Circle, self).__init__(
            self.center.x - self.radius,
            self.center.y - self.radius,
            self.radius * 2.0,
            self.radius * 2.0
        )

    def shape(self):
        shape = super(Circle, self).shape()
        path_stroker = QtGui.QPainterPathStroker()
        # TODO: Customizable 'snap'
        path_stroker.setWidth(6.0)
        path1 = path_stroker.createStroke(shape)
        return path1

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.cyan))
        # painter.drawPath(self.shape())
        super(Circle, self).paint(painter, option, widget)


class CircleComposite(QtGui.QGraphicsItemGroup):
    def __init__(self, obj):
        super(CircleComposite, self).__init__()
        # Prevent group events from overriding child events
        self.setHandlesChildEvents(False)

        # Create child entities
        self.center_point = Point(obj.point)
        self.ellipse = Circle(obj)

        # Add child entities to group
        self.addToGroup(self.center_point)
        self.addToGroup(self.ellipse)
