from Kernel.Db.alchemy import Connection
from Kernel.Db.schema import DocumentSchema

from Kernel.models import Layer

class AlchemyDocument(object):
    def __init__(self, schema):
        self.connection = Connection(schema)
        self.db = self.connection.session
        self.db_path = self.connection.db_path

        new_layer = Layer('Sample Layer')
        self.db.add(new_layer)
        self.db.commit()
