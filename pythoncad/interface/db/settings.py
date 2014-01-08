from common.db.connection import Connection

class InterfaceDb(Connection):
    """
    Stores gui related information such as window geometry and recent file lists.

    """
    def __init__(self, db_path):
        super(InterfaceDb, self).__init__(db_path)
        from interface.db.schema import Base
        Base.metadata.create_all(bind=self.engine, checkfirst=True)
