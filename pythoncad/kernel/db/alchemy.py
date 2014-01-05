from common.db.connection import Connection

class DocumentDb(Connection):
    def __init__(self, db_path):
        super(DocumentDb, self).__init__(db_path)
        # TODO: Check if it will add new tables when a file is opened, warn about changes if so
        from kernel.db.schema import Base
        Base.metadata.create_all(bind=self.engine, checkfirst=True)
