from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


class RecentFile(Base):
    path = Column(String)
    last_access = Column(DateTime)


class Settings(Base):
    window_maximized = Column(Boolean)
    window_height = Column(Integer)
    window_width = Column(Integer)
    window_x = Column(Integer)
    window_y = Column(Integer)
    state = Column(LargeBinary)
