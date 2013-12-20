from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from Kernel import models

Base = declarative_base()

class Layer(Base):
    __tablename__ = 'layers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    visible = Column(Boolean, default=True)


class Point(Base):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)


class Segment(Base):
    __tablename__ = 'segments'
    id = Column(Integer, primary_key=True)
    point1_id = Column(Integer, ForeignKey('points.id'))
    point2_id = Column(Integer, ForeignKey('points.id'))

    point1 = relationship('Point', foreign_keys=point1_id)
    point2 = relationship('Point', foreign_keys=point2_id)
