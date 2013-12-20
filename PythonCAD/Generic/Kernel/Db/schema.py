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

