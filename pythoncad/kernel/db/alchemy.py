from common.db.connection import Connection

class DocumentDb(Connection):
    """
    DocumentDb stores all drawing entities as well as any custom styles.
    It also stores a list of layers and the currently active layer.

    """
    def __init__(self, db_path):
        super(DocumentDb, self).__init__(db_path)
        # TODO: Check if it will add new tables when a file is opened, warn about changes if so
        from kernel.db.schema import Base
        Base.metadata.create_all(bind=self.engine, checkfirst=True)
