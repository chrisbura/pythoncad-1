from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, and_
from sqlalchemy.orm import relationship, foreign, remote, backref
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import event

from Kernel import models

@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


class Entity(Base):
    layer_id = Column(Integer, ForeignKey('layer.id'))

    layer = relationship('Layer', foreign_keys=layer_id)

    # Generic fk related columns
    content_type = Column(String)
    object_id = Column(Integer)

    @property
    def content_object(self):
        return getattr(self, 'parent_{0}'.format(self.content_type))


class EntityType(object):
    pass


# From sqlalchemy example files examples/generic_associations/generic_fk.py
@event.listens_for(EntityType, 'mapper_configured', propagate=True)
def setup_listener(mapper, class_):
    name = class_.__name__
    content_type = name.lower()
    # Reverse relationship (ie. Segment.entities)
    class_.entities = relationship(Entity,
        primaryjoin = and_(
            class_.id == foreign(remote(Entity.object_id)),
            Entity.content_type == content_type
        ),
        backref = backref(
            'parent_{0}'.format(content_type),
            primaryjoin=remote(class_.id) == foreign(Entity.object_id)
        )
    )
    @event.listens_for(class_.entities, 'append')
    def append_entity(target, value, initiator):
        value.content_type = content_type


class Point(EntityType, Base):
    x = Column(Float)
    y = Column(Float)

    def __repr__(self):
        return '<Point ({self.x}, {self.y})>'.format(self=self)


class Segment(EntityType, Base):
    point1_id = Column(Integer, ForeignKey('point.id'))
    point2_id = Column(Integer, ForeignKey('point.id'))

    point1 = relationship('Point', foreign_keys=point1_id)
    point2 = relationship('Point', foreign_keys=point2_id)


class Circle(EntityType, Base):
    # TODO: Convert to two points
    point_id = Column(Integer, ForeignKey('point.id'))
    radius = Column(Float)

    point = relationship('Point')


class Ellipse(EntityType, Base):
    # TODO: Convert to three points
    point_id = Column(Integer, ForeignKey('point.id'))
    radius_x = Column(Float)
    radius_y = Column(Float)

    point = relationship('Point')


class Layer(Base):
    name = Column(String(50))
    visible = Column(Boolean, default=True)


class Setting(Base):
    """
    Setting represents individual document settings such as active_layer

    """
    name = Column(String(50), unique=True)
    value = Column(String(50))
