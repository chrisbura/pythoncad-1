from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper

from Kernel import models

class DocumentSchema(object):
    def __init__(self):
        self.metadata = MetaData()
        self.tables = {}

        self.tables['layer'] = Table('layers', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
        )
        mapper(models.Layer, self.tables['layer'])
